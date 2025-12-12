# -*- coding: utf-8 -*-
import collections
import datetime
import threading
from abc import abstractmethod
import clickhouse_driver
import io
import os
import polars as pl
import requests
import time
import urllib.parse
import zstandard
from typing import Dict, Type, List, Any, Tuple, DefaultDict
from loguru import logger
from ys_lib.compressor import ZstdStreamCompressor
from ys_lib.interrupt_protect import KeyboardInterruptProtect


class FieldDetail:
    def __init__(self, name: str, read_dtype: Any = pl.Float64, dtype: Any = None,
                 convertor: pl.Expr = None, comment: str = '', drop: bool = False):
        self.name: str = name  # 字段名
        self.read_dtype: Any = read_dtype  # 从csv读入pl的数据类型
        self.dtype: Type | pl.Datetime = dtype or self.read_dtype  # 从csv读入pl的数据类型
        if convertor is not None:
            self.convertor: pl.Expr = convertor
        elif read_dtype != self.dtype:
            self.convertor = pl.col(name).cast(self.dtype)
        else:
            self.convertor = None
        self.comment: str = comment  # 备注
        self.drop: bool = drop  # 是否需要在数据库中丢弃该列

    @property
    def ch_type(self) -> str:
        """clickhouse中对应列的数据类型"""
        if self.dtype == pl.Datetime(time_unit='ms'):
            return 'DateTime64(3)'
        elif self.dtype == pl.Datetime(time_unit='us'):
            return 'DateTime64(6)'
        elif self.dtype == pl.Datetime(time_unit='ns'):
            return 'DateTime64(9)'
        else:
            return self.dtype.base_type().__name__

    @property
    def ch_codec(self) -> str:
        """clickhouse中对应列的编码类型"""
        if self.dtype.base_type() == pl.Datetime:
            codec = 'CODEC(DoubleDelta, ZSTD(9))'
        else:
            codec = 'CODEC(ZSTD(9))'
        return codec

    @property
    def ch_comment(self) -> str:
        """clickhouse中对应列的注释"""
        return f"COMMENT '{self.comment}'"

    def ch_column(self, nullable: bool = True) -> str:
        """clickhouse中对应列的创建语句"""
        ch_type: str = f'Nullable({self.ch_type})' if nullable else self.ch_type
        return f"`{self.name}` {ch_type} {self.ch_comment} {self.ch_codec}"


class DefaultFieldDetails:
    def __init__(self):
        self.fds: Dict[str, FieldDetail] = {}

    def add(self, fd: FieldDetail | List[FieldDetail]):
        if isinstance(fd, FieldDetail):
            fd = [fd]
        assert isinstance(fd, list)
        for _fd in fd:
            assert isinstance(_fd, FieldDetail)
            assert _fd.name not in self.fds
            self.fds[_fd.name] = _fd

    def get(self, name: str) -> FieldDetail:
        return self.fds.get(name)

    def __getitem__(self, item):
        return self.fds[item]


class QuoteStruct:
    subclasses: List = []
    fields: List[FieldDetail] = []
    priority_cols: List[str] = []

    def __class_getitem__(cls, item) -> FieldDetail:
        for fd in cls.fields:
            if fd.name == item:
                return fd
        raise ValueError()

    @classmethod
    def get(cls, item: str) -> FieldDetail:
        for fd in cls.fields:
            if fd.name == item:
                return fd

    @classmethod
    def read_dtypes(cls) -> Dict[str, Type]:
        """获取polars从csv加载时的类型"""
        return {fd.name: fd.read_dtype for fd in cls.fields}

    @classmethod
    def read_columns(cls) -> List[str]:
        """获取polars从csv加载时的列名列表"""
        return [fd.name for fd in cls.fields]

    @classmethod
    def convertors(cls, symbol: str = None) -> List[pl.Expr]:
        """polars的列类型转换"""
        pk1: str = cls.pk1()
        convertors: List[pl.Expr] = [fd.convertor for fd in cls.fields if fd.convertor is not None]
        for fd in cls.fields:
            if fd.name == pk1:
                if symbol:
                    convertors.append(pl.lit(symbol).alias(pk1))
                break
        else:
            assert symbol
            convertors.append(pl.lit(symbol).alias(pk1))
        return convertors

    @classmethod
    @abstractmethod
    def table_name(cls, *args, **kwargs) -> str:
        pass

    @classmethod
    def convertor_pk1(cls, symbol: str) -> pl.Expr:
        """polars添加symbol列"""
        return pl.lit(symbol).alias(cls.pk1())

    @classmethod
    def cols(cls) -> List[str]:
        return cls.priority_cols + [fd.name for fd in cls.fields if fd.name and fd.name not in cls.priority_cols]

    @classmethod
    def pk1(cls) -> str:
        return cls.priority_cols[0]

    @classmethod
    def pk2(cls) -> str:
        return cls.priority_cols[1]

    @classmethod
    def sql_create_table(cls, fds: DefaultFieldDetails, period: str = None):
        """建表语句"""
        cols: List[str] = []
        for i, name in enumerate(cls.cols()):
            fd: FieldDetail | None = fds.get(name) or cls.get(name)
            if not fd:
                assert i == 0, '非主键列不能为空'
                fd = FieldDetail(name=cls.pk1(), read_dtype=pl.String, dtype=pl.String)
            if i == 0:
                assert fd.dtype == pl.String
            elif i == 1 and len(cls.priority_cols) == 2:
                assert fd.dtype.is_integer() or fd.dtype.base_type() == pl.Datetime
            if not fd.drop:
                cols.append(fd.ch_column(nullable=name not in cls.priority_cols))
        tb: str = '\n' + ',\n'.join(cols)
        if len(cls.priority_cols) == 1:
            sql: str = f"""
                CREATE TABLE IF NOT EXISTS `{cls.table_name(period=period)}` ({tb})
                ENGINE = ReplacingMergeTree()
                PRIMARY KEY `{cls.pk1()}`
                ORDER BY `{cls.pk1()}`"""
        elif len(cls.priority_cols) >= 2:
            sql: str = f"""
                CREATE TABLE IF NOT EXISTS `{cls.table_name(period=period)}` ({tb})
                ENGINE = ReplacingMergeTree()
                PARTITION BY sipHash64(`{cls.pk1()}`) % 256
                PRIMARY KEY (`{cls.pk1()}`, `{cls.pk2()}`)
                ORDER BY (`{cls.pk1()}`, `{cls.pk2()}`)"""
        else:
            raise ValueError(cls.priority_cols)
        return sql


class KlinesStruct(QuoteStruct):
    """K线数据"""
    fields: List[FieldDetail] = []
    priority_cols: List[str] = ['symbol', 'datetime']

    @classmethod
    def table_name(cls, period: str | None = None) -> str:
        assert period
        return f'{cls.__name__}_{period}'


class SymbolStruct(QuoteStruct):
    """Symbol数据"""
    fields: List[FieldDetail] = []
    priority_cols: List[str] = ['symbol']

    @classmethod
    def table_name(cls, period: str | None = None) -> str:
        return cls.__name__


class TickStruct(QuoteStruct):
    """Tick数据"""
    fields: List[FieldDetail] = []
    priority_cols: List[str] = ['symbol', 'datetime']

    @classmethod
    def table_name(cls, period: str | None = None) -> str:
        return cls.__name__


class TradeStruct(QuoteStruct):
    """Trade数据"""
    fields: List[FieldDetail] = []
    priority_cols: List[str] = ['symbol', 'id']

    @classmethod
    def table_name(cls, period: str | None = None) -> str:
        return cls.__name__


class ClickHouse:
    def __init__(self, url: str, http_port: int = 8123, logger: bool = True):
        self.client = clickhouse_driver.Client.from_url(url=url)
        self.http_port: int = http_port
        sp = urllib.parse.urlsplit(url)
        self.database_name: str = os.path.basename(sp.path)
        assert not sp.path or sp.path == f'/{self.database_name}'
        self.url_http: str = f'http://{sp.hostname}:{http_port}'
        self.credential: Dict = {
            'user': sp.username,
            'password': sp.password,
        }
        self.table_locks: DefaultDict[str, threading.Lock] = collections.defaultdict(threading.Lock)
        self.execute = self.client.execute
        self.logger: bool = logger

    def bulk_insert(self, table_name: str, df: pl.DataFrame):
        columns: str = ', '.join([f'`{column}`' for column in df.columns])
        sql: str = f'INSERT INTO `{table_name}`({columns}) VALUES'
        with KeyboardInterruptProtect():
            if self.logger:
                logger.debug(f'[{table_name}]准备插入{df.height:12,d}条数据')
            t1: float = time.time()
            self.client.execute(query=sql, params=df.to_dicts())
            t2: float = time.time()
            if df.height and self.logger:
                logger.success(f'[{table_name}]成功插入{df.height:12,d}条数据 耗时{t2 - t1:0.0f}秒')

    def import_csv(self, table_name: str, csv: str, height: int = None):
        sql: str = f'INSERT INTO `{self.database_name}`.`{table_name}` FORMAT CSVWithNames'
        params: Dict = {
            'query': sql,
            **self.credential,
            'enable_http_compression': 1,
        }
        t1: float = time.time()
        if height is None:
            height: int = -1
            sio = io.StringIO(csv)
            while sio.readline():
                height += 1
        if not csv:
            if self.logger:
                logger.warning(f'{sql}: empty csv')
            return
        assert height >= 0
        csv: bytes = csv.encode('utf-8')
        with ZstdStreamCompressor(size=len(csv), level=zstandard.STRATEGY_FAST) as sc:
            sc.update(data=csv)
            stream: io.BytesIO = sc.stream
        with KeyboardInterruptProtect():
            r = requests.post(
                url=self.url_http,
                params=params,
                data=stream.getvalue(),
                headers={
                    'Content-Encoding': 'zstd',
                    'Accept-Encoding': 'zstd',
                },
            )
            t2: float = time.time()
        assert r.status_code == 200, f'[{r.status_code}]{r.text}'
        if r.text and self.logger:
            logger.info(r.text)
        if self.logger:
            logger.success(f'[{table_name}]成功插入{height:12,d}条数据 耗时{t2 - t1:0.0f}秒')

    def import_df(self, table_name: str, df: pl.DataFrame, pks: Tuple):
        """将polars.DataFrame导入ClickHouse,约束列为pks"""
        datetime_format: str = '%Y-%m-%d %H:%M:%S.%f'
        assert self.database_name
        assert pks and set(df.columns).issuperset(pks)
        # 按主键去重
        df = df.unique(subset=pks, maintain_order=True)
        if self.logger:
            logger.debug(f'[{table_name}]准备插入{df.height:12,d}条数据')
        # 通常第1主键为symbol
        pk1: str = pks[0]
        idx1: int = df.columns.index(pk1)
        assert df.dtypes[idx1] == pl.String
        pk1_vs = df[pk1].unique()
        outputs: str = ', '.join([f'`{pk}`' for pk in pks])
        sql = f"SELECT {outputs} FROM `{table_name}`"
        if pk1_vs.len() == 1:
            sql += f" WHERE `{pk1}` = '{pk1_vs.to_list()[0]}' "
        else:
            if pk1_vs.len() <= 1024:
                sql += f" WHERE `{pk1}` IN {pk1_vs.to_list()} "
        if len(pks) == 2:
            # 通常第2主键为id或datetime
            pk2: str = pks[1]
            idx2: int = df.columns.index(pk2)
            if df.dtypes[idx2].is_integer():
                pk2_min: int = df[pk2].min()
                pk2_max: int = df[pk2].max()
                sql += f"AND `{pk2}` BETWEEN {pk2_min} AND {pk2_max}"
            elif df.dtypes[idx2].base_type() == pl.Datetime:
                pk2_min: datetime.datetime = df[pk2].min()
                pk2_min: str = pk2_min.strftime(f'{datetime_format}')
                pk2_max: datetime.datetime = df[pk2].max()
                pk2_max: str = pk2_max.strftime(f'{datetime_format}')
                sql += f"AND `{pk2}` BETWEEN '{pk2_min}' AND '{pk2_max}'"
            elif df.dtypes[idx2] == pl.String:
                sql += f"AND `{pk2}` IN {df[pk2].unique().to_list()}"
            else:
                raise TypeError(df.dtypes[idx2])
        with self.table_locks[table_name]:
            rs: List[Tuple] = self.execute(sql, columnar=True)
            if rs:
                # 多列反选
                exists: pl.DataFrame = pl.DataFrame(dict(zip(pks, rs)))
                converts = []
                for pk in pks:
                    if exists[pk].dtype != df[pk].dtype:
                        converts.append(pl.col(pk).cast(df[pk].dtype))
                if converts:
                    exists = exists.with_columns(converts)
                df = df.join(exists, on=pks, how='anti')
            df = df.sort(by=pks)
            # 确定df转换为csv时候的时间格式
            return self.import_csv(
                table_name=table_name,
                csv=df.write_csv(include_header=True, datetime_format='%Y-%m-%d %H:%M:%S%.9f'),
                height=df.height
            )
