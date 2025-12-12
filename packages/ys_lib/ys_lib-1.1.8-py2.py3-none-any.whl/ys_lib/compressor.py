# -*- coding: utf-8 -*-
import brotli
import humanize
import io
import lzma
import zlib
import zstandard
from enum import Enum
from loguru import logger


class Compressor(Enum):
    IDENTITY = 'identity'
    DEFLATE = 'deflate'
    GZIP = 'gzip'
    ZLIB = 'zlib'
    BR = 'br'
    ZSTD = 'zstd'

    def get_compressor(self, level: int = 1):
        """获取流式压缩对象"""
        if self == self.DEFLATE:
            return zlib.compressobj(level=level, method=zlib.DEFLATED, wbits=-zlib.MAX_WBITS)
        elif self == self.GZIP:
            return zlib.compressobj(level=level, method=zlib.DEFLATED, wbits=zlib.MAX_WBITS | 16)
        elif self == self.ZLIB:
            return zlib.compressobj(level=level, method=zlib.DEFLATED, wbits=zlib.MAX_WBITS)
        elif self == self.BR:
            return brotli.Compressor()
        elif self == self.ZSTD:
            return zstandard.ZstdCompressor(level)


class ZstdStreamCompressor:
    def __init__(self, size: int = -1, interval: int = -1, threads: int = 0, level: int = zstandard.STRATEGY_BTULTRA2):
        """
        with ZstdStreamCompressor(size=len(data1) + len(data2), interval=1024*1024) as sc:
            sc.update(data=data1)
            sc.update(data=data2)
            return sc.stream
        """
        self.stream: io.BytesIO = io.BytesIO()
        self.size: int = size
        self.interval: int = interval
        self.interval_count: int = 0
        self.compressor = zstandard.ZstdCompressor(level=level, threads=threads)
        self.chunker = self.compressor.chunker(size=self.size)
        self._origin_size: int = 0

    def update(self, data: bytes):
        """对原始数据流进行流式压缩"""
        assert isinstance(data, bytes)
        buffer = io.BytesIO(data)
        while block := buffer.read(16777216):
            self._origin_size += len(block)
            for compressed in self.chunker.compress(block):
                self.stream.write(compressed)
                self.log()
        return self.stream

    def log(self, force: bool = False):
        if self.interval >= 0 and (force or self.stream.tell() >= self.interval_count * self.interval):
            prefix: str = f'{self._origin_size / self.size:6.1%}' if self.size > 0 else ''
            logger.debug(f'[{prefix}]已压缩={humanize.naturalsize(self.stream.tell())} 压缩比={self.ratio:6.1%}')
            self.interval_count += 1

    @property
    def origin_size(self) -> int:
        """压缩前字节数"""
        return self._origin_size

    @property
    def compressed_size(self) -> int:
        """压缩后字节数"""
        return self.stream.tell()

    @property
    def ratio(self) -> float:
        """压缩率"""
        origin_size: int = self.origin_size
        size: int = self.compressed_size
        if origin_size > 0:
            return size / origin_size
        else:
            return 1.0

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None and exc_val is None and exc_tb is None:
            try:
                for compressed in self.chunker.flush():
                    self.stream.write(compressed)
                    self.log()
                for compressed in self.chunker.finish():
                    self.stream.write(compressed)
                    self.log(force=True)
            except Exception as e:
                self.stream.close()
                raise e
        else:
            self.stream.close()


class LzmaStreamCompressor:
    def __init__(self):
        self.stream: io.BytesIO = io.BytesIO()
        self.compressor = lzma.LZMACompressor(preset=lzma.PRESET_EXTREME)

    def update(self, data: bytes):
        """对原始数据流进行流式压缩"""
        assert isinstance(data, bytes)
        buffer = io.BytesIO(data)
        while block := buffer.read(16777216):
            compressed: bytes = self.compressor.compress(block)
            self.stream.write(compressed)
        return self.stream

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None and exc_val is None and exc_tb is None:
            try:
                self.stream.write(self.compressor.flush())
            except Exception as e:
                self.stream.close()
                raise e
        else:
            self.stream.close()
