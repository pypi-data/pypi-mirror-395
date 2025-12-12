# -*- coding: utf-8 -*-
import collections
import datetime
import time

import fs.info
import fs.smbfs
import functools
import humanize
import io
import os
import polars as pl
from loguru import logger
from typing import Tuple, List, Set, DefaultDict, Dict
from .symbol import SymbolGuesser, SymbolDetail
from .base import Period
from .cache import Cache


class Parquets:
    def __init__(self, fs_url: str, pks: Tuple = ('symbol_id', 'datetime'), logger: bool = True):
        self.fs_url: str = fs_url
        self.fs: fs.smbfs.SMBFS = fs.open_fs(fs_url=fs_url)
        self.pks: Tuple = pks
        assert len(self.pks) >= 2
        self.ext: str = 'parquet'
        self.cache: Cache | None = None
        self.logger: bool = logger

    def save_parquet(self, df: pl.DataFrame, period: Period):
        # 按票分组
        df_grouped = df.group_by(pl.col(self.pks[0]))
        for (symbol_id,), sdf in df_grouped:
            assert isinstance(symbol_id, str)
            sd: SymbolDetail = SymbolGuesser.guess_symbol_detail(original_symbol_id=symbol_id)
            assert sd
            sdf: pl.DataFrame
            self.save_symbol_parquet(sd=sd, df=sdf, period=period)

    def save_symbol_parquet(self, sd: SymbolDetail | str, df: pl.DataFrame, period: Period):
        if isinstance(sd, str):
            assert '/' not in sd
            assert '\\' not in sd
        match period:
            case Period.OneMinute | Period.OneHour | Period.OneDay:
                # 按年分组
                df_grouped = df.group_by(pl.col(self.pks[1]).dt.truncate(every='1y'))
                for (year,), ydf in df_grouped:
                    year: datetime.datetime
                    ydf: pl.DataFrame
                    if isinstance(sd, str):
                        path_parquet: str = f'/{sd}/{period.value}/{year.strftime("%Y")}.{self.ext}'
                    else:
                        path_parquet: str = f'/{sd.exchange.name}/{sd.instrument_id}/{period.value}/' \
                                            f'{year.strftime("%Y")}.{self.ext}'
                    assert self._update_parquet(path=path_parquet, df=ydf)
            case Period.Tick | Period.OneSecond:
                # tick按月分组
                df_grouped = df.group_by(pl.col(self.pks[1]).dt.truncate(every='1mo'))
                for (month,), mdf in df_grouped:
                    month: datetime.datetime
                    mdf: pl.DataFrame
                    if isinstance(sd, str):
                        monthly_parquet: str = f'/{sd}/{period.value}/{month.strftime("%Y-%m")}.{self.ext}'
                        yearly_parquet: str = f'/{sd}/{period.value}/{month.strftime("%Y")}.{self.ext}'
                    else:
                        monthly_parquet: str = f'/{sd.exchange.name}/{sd.instrument_id}/{period.value}/' \
                                               f'{month.strftime("%Y-%m")}.{self.ext}'
                        yearly_parquet: str = f'/{sd.exchange.name}/{sd.instrument_id}/{period.value}/' \
                                              f'{month.strftime("%Y")}.{self.ext}'
                    if self.fs.isfile(path=yearly_parquet):
                        path_parquet = yearly_parquet
                    else:
                        path_parquet = monthly_parquet
                    assert self._update_parquet(path=path_parquet, df=mdf)
            case _:
                raise ValueError(period)

    def _update_parquet(self, path: str, df: pl.DataFrame) -> bool:
        size1: int = 0
        if self.fs.isfile(path):
            b: bytes = self.fs.readbytes(path=path)
            exists: pl.DataFrame = pl.read_parquet(source=b)
            size1: int = len(b)
            ndf = df.join(exists, on=self.pks, how='anti')
            if ndf.height == 0:
                # if self.logger:
                #     logger.warning(f'无新数据: {path}')
                return True
            df = pl.concat(items=[df, ndf])
            del ndf
        df = df.sort(by=self.pks)
        path_tmp: str = f'{path}.tmp'
        self.fs.makedirs(path=os.path.dirname(path), recreate=True)
        bio = io.BytesIO()
        df.write_parquet(file=bio, compression='zstd')
        del df
        size2: int = bio.tell()
        bio.seek(0)
        self.fs.upload(path=path_tmp, file=bio)
        bio.close()
        self.fs.move(src_path=path_tmp, dst_path=path, overwrite=True)
        if self.logger:
            if size1:
                logger.info(f'合并成功: {path} {humanize.naturalsize(size1)} -> {humanize.naturalsize(size2)}')
            else:
                logger.info(f'写入成功: {path} {humanize.naturalsize(size2)}')
        return True

    # def pack_parquets(self):
    #     for root, dirs, files in self.fs.walk(search='depth'):
    #         ds: List[str] = root.strip('/').split('/')
    #         if len(ds) == 3:
    #             files: List[fs.info.Info] = [x for x in files if x.name.endswith('.' + self.ext)]
    #             if files:
    #                 self.pack_path_parquets(path=root)
    #
    # def pack_path_parquets(self, path: str):
    #     ds: List[str] = path.strip('/').split('/')
    #     assert len(ds) == 3
    #     exchange_id, instrument_id, _period = ds
    #     period = Period(_period)
    #     filenames: List[str] = [x for x in self.fs.listdir(path=path) if x.endswith(self.ext)]
    #     if not filenames:
    #         return
    #     dst_filename: str = f'{period.value}.{self.ext}'
    #     combines: Set[str] = set(filenames) - {max(set(filenames) - {dst_filename})}
    #     if not combines - {dst_filename}:
    #         return
    #     logger.debug(f'准备合并: {len(combines)} -> {path}/{dst_filename}')
    #     dfs: List[pl.DataFrame] = []
    #     for name in combines:
    #         df: pl.DataFrame = pl.read_parquet(source=self.fs.readbytes(path=f'{path}/{name}'))
    #         dfs.append(df)
    #     df: pl.DataFrame = pl.concat(items=dfs)
    #     df: pl.DataFrame = df.sort(by=self.pks[1])
    #     path_tmp: str = f'{path}/{dst_filename}.tmp'
    #     with self.fs.open(path=path_tmp, mode='wb') as f:
    #         f: io.BytesIO
    #         df.write_parquet(file=f, compression='zstd')
    #     del df
    #     self.fs.move(src_path=path_tmp, dst_path=f'{path}/{dst_filename}', overwrite=True)
    #     for name in combines:
    #         if name != dst_filename:
    #             self.fs.remove(path=f'{path}/{name}')
    #     logger.debug(f'成功合并: {len(combines)} -> {path}/{dst_filename}')

    def get_max_datetime(self, sd: SymbolDetail, period: Period) -> datetime.datetime | None:
        path_parquets: str = f'/{sd.exchange.name}/{sd.instrument_id}/{period.value}'
        if not self.fs.isdir(path=path_parquets):
            return None
        filenames: List[str] = self.fs.listdir(path=path_parquets)
        filenames: Set[str] = {x for x in filenames if x.endswith(f'.{self.ext}')} - {f'{period.value}.{self.ext}'}
        if not filenames:
            return None
        filename: str = max(filenames)
        path_parquet: str = f'{path_parquets}/{filename}'
        df: pl.DataFrame = pl.read_parquet(source=self.fs.readbytes(path=path_parquet))
        return df[self.pks[1]].max()

    def merge_parquets(self, cache: Cache):
        """将非年度文件合并成年度文件"""
        if cache != self.cache:
            self.cache = cache
        caches: Dict[str, int] = self.cache.items(dataset='processed')
        formats: Dict[int, str] = {
            len(datetime.datetime.now().strftime(fmt)): fmt for fmt in ['%Y-%m-%d', '%Y-%m', '%Y']
        }
        for sr in self.fs.listdir(path='/'):
            if not self.fs.isdir(path=sr):
                continue
            elif time.time() - caches.get(f'/{sr}', 0) <= 7 * 86400:
                if self.logger:
                    logger.debug(f'skip folder: /{sr}')
                continue
            for i, (root, dirs, files) in enumerate(self.fs.walk(sr, search='depth')):
                if time.time() - caches.get(root, 0) <= 7 * 86400:
                    continue
                ds: List[str] = root.strip('/').split('/')
                if len(ds) >= 2 and ds[-1].lower() in {Period.Tick.value, Period.OneSecond.value}:
                    if self.logger:
                        logger.debug(f'[{i}]{root}')
                    yearly: DefaultDict[int, List[str]] = collections.defaultdict(list)
                    for file in sorted(files, key=lambda x: x.name):
                        ymd, ext = os.path.splitext(file.name)
                        if ext == f'.{self.ext}':
                            dt = datetime.datetime.strptime(ymd, formats[len(ymd)])
                            yearly[dt.year].append(file.make_path(root))
                    for year, combines in yearly.items():
                        if year >= max(yearly):
                            continue
                        # 开始合并
                        dst_path: str = f'{root}/{year}.{self.ext}'
                        if combines == [dst_path]:
                            continue
                        try:
                            self.merge_to(combines=combines, dst_path=dst_path)
                            break
                        except Exception as e:
                            logger.exception(e)
                if len(ds) >= 2:
                    self.cache.set(dataset='processed', key=root, value=int(time.time()))
            self.cache.set(dataset='processed', key=f'/{sr}', value=int(time.time()))

    def merge_to(self, combines: List[str], dst_path: str):
        if len(combines) > 1:
            if self.logger:
                logger.info(f'准备合并为: {dst_path}')
            dfs: List[pl.DataFrame] = []
            for path in sorted(combines):
                df: pl.DataFrame = pl.read_parquet(source=self.fs.readbytes(path=path))
                dfs.append(df)
            df: pl.DataFrame = pl.concat(items=dfs)
            dfs.clear()
            df: pl.DataFrame = df.unique(subset=self.pks)
            df: pl.DataFrame = df.sort(by=self.pks)
            path_tmp: str = f'{dst_path}.tmp'
            with self.fs.open(path=path_tmp, mode='wb') as f:
                f: io.BytesIO
                df.write_parquet(file=f, compression='zstd')
                if self.logger:
                    logger.debug(f'成功合并: [{len(combines):2d}] {humanize.naturalsize(f.tell())} {dst_path}')
            del df
            self.fs.move(src_path=path_tmp, dst_path=dst_path, overwrite=True)
            for file in combines:
                if os.path.basename(file).lower() != os.path.basename(dst_path).lower():
                    self.fs.remove(path=file)
        else:
            if combines[0].lower() != dst_path.lower():
                self.fs.move(src_path=combines[0], dst_path=dst_path, overwrite=True)
