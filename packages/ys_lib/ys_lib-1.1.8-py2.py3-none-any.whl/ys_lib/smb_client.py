# -*- coding: utf-8 -*-
import humanize
import io
import math
import os
import re
import time
import urllib.parse
import uuid
from smb.SMBConnection import SMBConnection
from smb.smb_structs import OperationFailure
from smb.base import SharedFile, NotConnectedError
from loguru import logger
from typing import AnyStr, IO, Iterator, List, SupportsBytes, Tuple


class SmbClient(SMBConnection):
    def __init__(
        self,
        host: str,
        port: int,
        username: str,
        password: str,
        mount_point: str,
        base_path: str,
    ):
        self.smb_host: str = host
        self.smb_port: int = port
        self.smb_username: str = username
        self.smb_password: str = password
        self.service_name: str = mount_point
        self.reload_at: float = 0
        self.base_path: str = os.path.normpath(base_path)
        assert self.base_path
        assert not self.base_path.startswith(os.pardir)
        super().__init__(
            username=self.smb_username,
            password=self.smb_password,
            my_name="",
            remote_name="",
            is_direct_tcp=True,
        )

    @classmethod
    def from_uri(cls, uri: AnyStr) -> 'SmbClient':
        """从uri创建本类"""
        # uri: str = 'smb://username:password@host:port/mount_point/base_path'
        sp = urllib.parse.urlsplit(uri)
        assert sp.scheme.lower() == 'smb'
        rs = re.findall(r'([^\\/]+)', sp.path)
        return cls(
            host=sp.hostname,
            port=sp.port or 445,
            username=sp.username,
            password=sp.password,
            mount_point=rs[0],
            base_path='/'.join(rs[1:]),
        )

    def check_path(self, path: AnyStr) -> bool:
        """检查path是否是base_path的子路径"""
        parent: str = os.path.normpath(path)  # type: ignore
        if path == parent:
            return True
        while True:
            parent: str = os.path.dirname(parent)
            if parent == self.base_path:
                return True
            elif not parent:
                return False

    def reload(self, interval: float = 1.0):
        now: float = time.time()
        left: float = self.reload_at + interval - now
        if left > 0:
            time.sleep(left)
        self.reload_at = time.time()
        super().__init__(
            username=self.smb_username,
            password=self.smb_password,
            my_name="",
            remote_name="",
            is_direct_tcp=True,
        )
        assert self.connect(ip=self.smb_host, port=self.smb_port)

    def walk(self, top: AnyStr) -> Iterator[Tuple[AnyStr, List[AnyStr], List[AnyStr]]]:
        if self.isdir(top):
            items: List[SharedFile] = self.listPath(service_name=self.service_name, path=top)
            dirs: List[str] = []
            files: List[str] = []
            for item in items:
                if item.filename in [os.path.curdir, os.path.pardir]:
                    continue
                elif item.isDirectory:
                    dirs.append(item.filename)
                else:
                    files.append(item.filename)
            dirs.sort()
            files.sort()
            yield top, dirs, files
            for d in dirs:
                yield from self.walk(os.path.join(top, d))

    def listdir(self, path: AnyStr) -> List[SharedFile]:
        """列目录"""
        while True:
            try:
                return [
                    item
                    for item in self.listPath(service_name=self.service_name, path=path)
                    if item.filename not in {os.path.curdir, os.path.pardir}
                ]
            except (NotConnectedError, BrokenPipeError, ConnectionResetError):
                self.reload()
                logger.debug(f"SMB连接成功 PID={os.getpid()}")
                continue
            except Exception as e:
                logger.error(f"[{e.__class__.__name__}]{e}")
                raise e

    def isdir(self, path: AnyStr) -> bool:
        while True:
            try:
                fo: SharedFile = self.getAttributes(service_name=self.service_name, path=path)
                return fo.isDirectory
            except OperationFailure:
                return False
            except (NotConnectedError, BrokenPipeError, ConnectionResetError):
                self.reload()
                logger.debug(f"SMB连接成功 PID={os.getpid()}")
                continue
            except Exception as e:
                logger.error(f"[{e.__class__.__name__}]{e}")
                raise e

    def isfile(self, path: AnyStr) -> bool:
        while True:
            try:
                fo: SharedFile = self.getAttributes(service_name=self.service_name, path=path)
                return not fo.isDirectory
            except OperationFailure:
                return False
            except (NotConnectedError, BrokenPipeError, ConnectionResetError):
                self.reload()
                logger.debug(f"SMB连接成功 PID={os.getpid()}")
                continue
            except Exception as e:
                logger.error(f"[{e.__class__.__name__}]{e}")
                raise e

    def exists(self, path: AnyStr) -> bool:
        while True:
            try:
                self.getAttributes(service_name=self.service_name, path=path)
                return True
            except OperationFailure:
                return False
            except (NotConnectedError, BrokenPipeError, ConnectionResetError):
                self.reload()
                logger.debug(f"SMB连接成功 PID={os.getpid()}")
                continue
            except Exception as e:
                logger.error(f"[{e.__class__.__name__}]{e}")
                raise e

    def mkdir(self, name: AnyStr):
        assert self.check_path(path=name)
        self.createDirectory(service_name=self.service_name, path=name)

    def makedirs(self, name: AnyStr, exist_ok: bool = True):
        assert self.check_path(path=name)
        head, tail = os.path.split(name)
        if not tail:
            head, tail = os.path.split(head)
        if head and tail and not self.exists(head):
            try:
                self.makedirs(head, exist_ok=exist_ok)
            except FileExistsError:
                pass
            cdir = os.path.curdir
            if isinstance(tail, bytes):
                cdir = bytes(os.path.curdir, "ASCII")
            if tail == cdir:
                return
        try:
            self.mkdir(name)
        except OperationFailure:
            if not exist_ok or not self.isdir(name):
                raise

    def upload_file(self, path: AnyStr, data: AnyStr | SupportsBytes | IO):
        """上传一个已经完成的文件"""
        path: str = os.path.normpath(path)
        size: int = len(data) if isinstance(data, bytes) else 0
        assert self.check_path(path=path)
        tmp_path: str = os.path.join(os.path.dirname(path), f"{uuid.uuid4().hex}.tmp")  # type: ignore
        if isinstance(data, str):
            assert os.path.isfile(data), f"文件不存在 {data}"
            bio = io.FileIO(data)
        elif isinstance(data, bytes):
            bio = io.BytesIO(data)
        else:
            bio = data
        assert isinstance(bio, io.BytesIO | io.FileIO | io.BufferedReader)
        if bio.seekable():
            bio.seek(0)
        t1: float = time.time()
        while True:
            try:
                self.makedirs(name=os.path.dirname(tmp_path), exist_ok=True)
                size: int = self.storeFile(service_name=self.service_name, path=tmp_path, file_obj=bio)
                self.move(src=tmp_path, dst=path)
                elapse: float = time.time() - t1
                logger.debug(
                    f"文件上传成功 PID={os.getpid()} TIME={humanize.naturaldelta(elapse)} SIZE={humanize.naturalsize(size)} PATH={path}"
                )
                return
            except (NotConnectedError, BrokenPipeError, ConnectionResetError):
                self.reload()
                logger.debug(f"SMB连接成功 PID={os.getpid()}")
                continue
            except Exception as e:
                elapse: float = time.time() - t1
                logger.error(f"[{e.__class__.__name__}]{e}")
                logger.error(
                    f"文件上传失败 PID={os.getpid()} TIME={humanize.naturaldelta(elapse)} SIZE={humanize.naturalsize(size)} PATH={path}"
                )
                raise e
            finally:
                if isinstance(bio, (io.BytesIO, io.FileIO)):
                    bio.seek(0)

    def upload_dir(self, path: AnyStr, source: AnyStr):
        """上传目录"""
        path: str = os.path.normpath(path)
        assert self.check_path(path=path)
        assert os.path.isdir(source), "source必须为目录"
        t1: float = time.time()
        try:
            for f in os.listdir(source):
                remote: str = os.path.join(path, f)  # type: ignore
                local: str = os.path.join(source, f)  # type: ignore
                if os.path.isfile(local):
                    self.upload_file(path=remote, data=local)
                elif os.path.isdir(local):
                    self.upload_dir(path=remote, source=local)
        except Exception as e:
            elapse: float = time.time() - t1
            logger.error(f"[{e.__class__.__name__}]{e}")
            logger.error(f"上传目录失败 PID={os.getpid()} TIME={humanize.naturaldelta(elapse)} PATH={path}")
            raise e

    def download_file(self, path: AnyStr, target: AnyStr | io.IOBase | io.BufferedWriter | None = None) -> io.BytesIO | None:
        """下载一个文件"""
        path: str = os.path.normpath(path)
        assert self.check_path(path=path)
        if isinstance(target, str):
            os.makedirs(os.path.dirname(target), exist_ok=True)
            bio = open(target, mode="wb")
        elif isinstance(target, (io.IOBase, io.BufferedWriter)):
            bio = target
            bio.truncate(0)
        elif target is None:
            bio = io.BytesIO()
        else:
            raise TypeError("target类型错误")
        t1: float = time.time()
        while True:
            try:
                self.retrieveFile(service_name=self.service_name, path=path, file_obj=bio)
                elapse: float = time.time() - t1
                size: int = bio.tell()
                logger.debug(
                    f"文件下载成功 PID={os.getpid()} TIME={humanize.naturaldelta(elapse)} SIZE={humanize.naturalsize(size)} PATH={path}"
                )
                if target is None:
                    return bio
                else:
                    return None
            except (NotConnectedError, BrokenPipeError, ConnectionResetError):
                self.reload()
                logger.debug(f"SMB连接成功 PID={os.getpid()}")
                continue
            except Exception as e:
                elapse: float = time.time() - t1
                logger.error(f"[{e.__class__.__name__}]{e}")
                logger.error(f"文件下载失败 PID={os.getpid()} TIME={humanize.naturaldelta(elapse)} PATH={path}")
                raise e
            finally:
                bio.seek(0)

    def download_dir(self, path: AnyStr, target: AnyStr):
        """下载目录"""
        path: str = os.path.normpath(path)
        assert self.check_path(path=path)
        assert self.isdir(path=path), "path必须为目录"
        t1: float = time.time()
        try:
            for f in self.listdir(path=path):
                remote: str = os.path.join(path, f.filename)  # type: ignore
                local: str = os.path.join(target, f.filename)  # type: ignore
                if self.isfile(remote):
                    self.download_file(path=remote, target=local)
                elif self.isdir(remote):
                    self.download_dir(path=remote, target=local)
        except Exception as e:
            elapse: float = time.time() - t1
            logger.error(f"[{e.__class__.__name__}]{e}")
            logger.error(f"下载目录失败 PID={os.getpid()} TIME={humanize.naturaldelta(elapse)} PATH={path}")
            raise e

    def remove(self, path: AnyStr, recursive: bool = False):
        """删除文件或目录"""
        path: str = os.path.normpath(path)
        assert self.check_path(path=path)
        t1: float = time.time()
        while True:
            try:
                if self.isfile(path=path):
                    self.deleteFiles(service_name=self.service_name, path_file_pattern=path)
                    elapse: float = time.time() - t1
                    logger.trace(f"文件删除成功 PID={os.getpid()} TIME={humanize.naturaldelta(elapse)} PATH={path}")
                elif self.isdir(path=path):
                    if recursive:
                        for f in self.listdir(path=path):
                            fpath: str = os.path.join(path, f.filename)  # type: ignore
                            self.remove(path=fpath, recursive=recursive)
                    self.deleteDirectory(service_name=self.service_name, path=path)
                    elapse: float = time.time() - t1
                    logger.trace(f"目录删除成功 PID={os.getpid()} TIME={humanize.naturaldelta(elapse)} PATH={path}")
                return
            except (NotConnectedError, BrokenPipeError, ConnectionResetError):
                self.reload()
                logger.debug(f"SMB连接成功 PID={os.getpid()}")
                continue
            except Exception as e:
                elapse: float = time.time() - t1
                logger.error(f"[{e.__class__.__name__}]{e}")
                logger.error(f"文件删除失败 PID={os.getpid()} TIME={humanize.naturaldelta(elapse)} PATH={path}")
                raise e

    def rmtree(self, path: AnyStr):
        """递归删除"""
        path: str = os.path.normpath(path)
        assert self.check_path(path=path)
        if self.isfile(path):
            self.deleteFiles(service_name=self.service_name, path_file_pattern=path)
        elif self.isdir(path):
            items: List[SharedFile] = self.listPath(service_name=self.service_name, path=path)
            for item in items:
                if item.filename in [os.path.curdir, os.path.pardir]:
                    continue
                item_path: str = os.path.join(path, item.filename)  # type: ignore
                if not item.isDirectory:
                    self.deleteFiles(service_name=self.service_name, path_file_pattern=item_path)
                else:
                    self.rmtree(path=item_path)
            self.deleteDirectory(service_name=self.service_name, path=path)

    def move(self, src: AnyStr, dst: AnyStr, replace: bool = True):
        assert self.check_path(path=src)
        assert self.check_path(path=dst)
        while True:
            try:
                self.makedirs(os.path.dirname(dst), exist_ok=True)
                if self.isdir(src):
                    if self.isdir(dst):
                        # 合并目录
                        items: List[SharedFile] = self.listPath(service_name=self.service_name, path=src)
                        for item in items:
                            if item.filename in [os.path.curdir, os.path.pardir]:
                                continue
                            item_path: str = os.path.join(src, item.filename)  # type: ignore
                            self.move(src=item_path, dst=os.path.join(dst, item.filename))
                        self.deleteDirectory(service_name=self.service_name, path=src)
                        # self.rename(service_name=self.service_name, old_path=src, new_path=dst)
                    else:
                        # 移动目录
                        self.rename(service_name=self.service_name, old_path=src, new_path=dst)
                elif self.isfile(src):
                    basename: str = os.path.basename(src)  # type: ignore
                    if self.isdir(dst):
                        # 移动到目录中
                        self.rename(
                            service_name=self.service_name,
                            old_path=src,
                            new_path=os.path.join(dst, basename),  # type: ignore
                        )
                    else:
                        if not self.exists(dst):
                            self.rename(
                                service_name=self.service_name,
                                old_path=src,
                                new_path=dst,
                            )
                        elif self.isfile(dst) and replace:
                            # 移动并替换文件
                            self.remove(dst)
                            self.rename(
                                service_name=self.service_name,
                                old_path=src,
                                new_path=dst,
                            )
                return True
            except (NotConnectedError, BrokenPipeError, ConnectionResetError):
                self.reload()
                logger.debug(f"SMB连接成功 PID={os.getpid()}")
                continue
            except Exception as e:
                logger.error(f"[{e.__class__.__name__}]{e}")
                raise e

    def getsize(self, path: AnyStr) -> int:
        """获取文件大小"""
        if not self.exists(path):
            return -1
        sf: SharedFile = self.getAttributes(service_name=self.service_name, path=path)
        return sf.file_size

    def getmtime(self, path: AnyStr) -> float:
        """获取文件修改时间"""
        if not self.exists(path):
            return -math.inf
        sf: SharedFile = self.getAttributes(service_name=self.service_name, path=path)
        return sf.last_write_time

    def getctime(self, path: AnyStr) -> float:
        """获取文件创建时间"""
        if not self.exists(path):
            return -math.inf
        sf: SharedFile = self.getAttributes(service_name=self.service_name, path=path)
        return sf.create_time

    def getatime(self, path: AnyStr) -> float:
        """获取文件访问时间"""
        if not self.exists(path):
            return -math.inf
        sf: SharedFile = self.getAttributes(service_name=self.service_name, path=path)
        return sf.last_access_time
