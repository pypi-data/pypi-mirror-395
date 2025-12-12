# -*- coding: utf-8 -*-
import os
import zipfile
import zstandard
from typing import IO, AnyStr, Iterator, Tuple, List


class TextReader:
    """多行文本分块读取器"""

    @classmethod
    def iter_zst_text(cls, f: AnyStr | IO, size: int = 64 * 1024 ** 2) -> Iterator[Tuple[str, str | None]]:
        path: str | None = None
        if isinstance(f, str):
            assert os.path.isfile(f)
            path: str = f
            fd: IO = open(f, mode='rb')
        else:
            fd: IO = f
        try:
            decompressor = zstandard.ZstdDecompressor().stream_reader(f)
            for text in cls.iter_stream_text(stream=decompressor, size=size):
                yield text, path
        finally:
            fd.close()

    @classmethod
    def iter_zip_text(cls, f: AnyStr | IO, size: int = 64 * 1024 ** 2) -> Iterator[Tuple[str, str | None]]:
        if isinstance(f, str):
            assert os.path.isfile(f)
        with zipfile.ZipFile(f) as zf:
            for zi in zf.infolist():
                if zi.is_dir():
                    continue
                with zf.open(zi) as stream:
                    for text in cls.iter_stream_text(stream=stream, size=size):
                        yield text, zi.filename

    @classmethod
    def iter_stream_text(cls, stream: IO, size: int = 64 * 1024 ** 2, encodings: Tuple = ('utf-8', 'gbk')) -> Iterator[str]:
        for payload in cls.iter_stream_bytes(stream=stream, size=size):
            for i, encoding in enumerate(encodings):
                try:
                    text: str = payload.decode(encoding)
                    yield text
                    break
                except Exception as e:
                    if i == len(encodings) - 1:
                        raise e

    @classmethod
    def iter_stream_bytes(cls, stream: IO, size: int = 64 * 1024 ** 2) -> Iterator[bytes]:
        tail: bytes = b''
        i: int = 0
        while segment := stream.read(size):  # 每次处理size大小的多行文本
            idx: int = segment.rfind(b'\n')
            payload: bytes = tail + segment[:idx + 1]
            tail: bytes = segment[idx + 1:]
            yield payload
            i += 1
