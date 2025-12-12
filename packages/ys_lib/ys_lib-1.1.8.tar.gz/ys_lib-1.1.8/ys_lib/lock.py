# -*- coding: utf-8 -*-
import asyncio
import threading
import time


class SyncRWLock:
    """同步读写锁,单写多读"""
    def __init__(self, reentrant: bool = True):
        self.readers: int = 0  # 读取者数量
        self.reentrant: bool = reentrant
        if reentrant:
            self.r_lock: threading.RLock = threading.RLock()
            self.w_lock: threading.RLock = threading.RLock()
        else:
            self.r_lock: threading.Lock = threading.Lock()
            self.w_lock: threading.Lock = threading.Lock()

    def read_acquire(self):
        """获取读锁"""
        with self.r_lock:
            self.readers += 1
            if self.readers == 1:
                self.w_lock.acquire()

    def read_release(self):
        """释放读锁"""
        with self.r_lock:
            self.readers -= 1
            if self.readers == 0:
                self.w_lock.release()

    def write_acquire(self):
        """获取写锁"""
        self.w_lock.acquire()

    def write_release(self):
        """释放写锁"""
        self.w_lock.release()

    def __enter__(self):
        """仅针对读锁的上下文"""
        self.read_acquire()
        return None

    def __exit__(self, exc_type, exc, tb):
        """仅针对读锁的上下文"""
        self.read_release()


class AsyncRWLock:
    """异步读写锁,单写多读"""
    def __init__(self):
        self.readers: int = 0  # 读取者数量
        self.r_lock: asyncio.Lock = asyncio.Lock()
        self.w_lock: asyncio.Lock = asyncio.Lock()

    async def read_acquire(self):
        """获取读锁"""
        async with self.r_lock:
            self.readers += 1
            if self.readers == 1:
                await self.w_lock.acquire()

    async def read_release(self):
        """释放读锁"""
        async with self.r_lock:
            self.readers -= 1
            if self.readers == 0:
                self.w_lock.release()

    async def write_acquire(self):
        """获取写锁"""
        await self.w_lock.acquire()

    async def write_release(self):
        """释放写锁"""
        self.w_lock.release()

    async def __aenter__(self):
        """仅针对读锁的上下文"""
        await self.read_acquire()
        return None

    async def __aexit__(self, exc_type, exc, tb):
        """仅针对读锁的上下文"""
        await self.read_release()
