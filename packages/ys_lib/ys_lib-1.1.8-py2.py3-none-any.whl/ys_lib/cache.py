# -*- coding: utf-8 -*-
import datetime
import decimal
import inspect
import lz4.frame
import math
import os
import pickle
import re
import sqlite3
import threading
import time
from typing import Any, Set, List, Tuple, Dict


class Cache:
    """持久化TTL缓存"""

    def __init__(self, path: str = None):
        current_frame = inspect.currentframe()
        caller_frame = current_frame.f_back
        caller_file = caller_frame.f_code.co_filename
        if not path:
            path: str = f'_{os.path.splitext(os.path.basename(caller_file))[0]}.db3'
        self.path: str = os.path.join(os.path.dirname(caller_file), path)
        self.default_dataset: str = 'DEFAULT'
        self.compress_min_size: int = max(64, len(lz4.frame.compress(b'\x00')))
        self.conn = sqlite3.connect(self.path, check_same_thread=False)
        self.lock = threading.RLock()
        # self.conn.execute('PRAGMA auto_vacuum = FULL')
        self.datasets: Set[str] = self.get_tables()
        self.upgrade_tables()

    def get_tables(self) -> Set[str]:
        """获取所有数据集"""
        with self.lock:
            cursor = self.conn.cursor()
            r = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            return {row[0] for row in r.fetchall()}

    def upgrade_tables(self):
        """升级表到最新版本"""
        with self.lock:
            updated: bool = False
            for dataset in self.datasets:
                cursor = self.conn.cursor()
                r = cursor.execute(f"PRAGMA table_info({dataset});")
                cols: List[str] = [x[1] for x in r.fetchall()]
                if 'encoding' not in cols:
                    self.conn.execute(f'ALTER TABLE `{dataset}` ADD COLUMN `encoding` INTEGER;')
                    self.conn.execute(f'UPDATE `{dataset}` SET `encoding` = 5;')
                    updated |= True
            if updated:
                self.conn.commit()

    def create_table(self, dataset: str) -> None:
        """创建数据集"""
        with self.lock:
            assert not re.findall(r'\s', dataset)
            self.conn.execute(f"""CREATE TABLE IF NOT EXISTS `{dataset}` (
                `key` TEXT PRIMARY KEY NOT NULL,
                `value` BLOB,
                `encoding` INTEGER NOT NULL,
                `expired_at` REAL NOT NULL
            )""")
            self.conn.execute(f"""CREATE INDEX IF NOT EXISTS expired_at ON `{dataset}` (`expired_at`)""")
            self.conn.commit()

    def encode_value(self, value: Any) -> Tuple[Any, int]:
        """数据编码"""
        if value is None:
            return value, 0     # 原始数据
        elif isinstance(value, bool):
            return value, 64
        elif isinstance(value, datetime.datetime):
            return value.strftime('%Y-%m-%d %H:%M:%S.%f'), 65
        elif isinstance(value, datetime.date):
            return value, 66
        elif isinstance(value, decimal.Decimal):
            return str(value), 67
        elif isinstance(value, int):
            if - 2 ** 63 <= value <= 2 ** 63 - 1:
                return value, 0  # 原始数据
            else:
                return str(value), 68
        elif isinstance(value, float):
            return value, 0     # 原始数据
        elif isinstance(value, str):
            value: bytes = value.encode('utf-8')
            if len(value) <= self.compress_min_size:
                return value, 1     # 字符串utf-8编码
            else:
                return lz4.frame.compress(value), 2     # 字符串utf-8编码并压缩
        elif isinstance(value, bytes):
            if len(value) <= self.compress_min_size:
                return value, 0     # 原始数据
            else:
                return lz4.frame.compress(value), 3     # 仅压缩
        else:
            payload: bytes = pickle.dumps(value)
            if len(payload) <= self.compress_min_size:
                return payload, 4                         # 仅序列化
            else:
                return lz4.frame.compress(payload), 5     # 序列化并压缩

    @classmethod
    def decode_value(cls, value: Any, encoding: int) -> Any:
        """数据解码"""
        match encoding:
            case 0:
                return value
            case 1:
                return value.decode('utf-8')
            case 2:
                return lz4.frame.decompress(value).decode('utf-8')
            case 3:
                return lz4.frame.decompress(value)
            case 4:
                return pickle.loads(value)
            case 5:
                return pickle.loads(lz4.frame.decompress(value))
            case 64:
                return bool(value)
            case 65:
                return datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S.%f')
            case 66:
                return datetime.datetime.strptime(value, '%Y-%m-%d').date()
            case 67:
                return decimal.Decimal(value)
            case 68:
                return int(value)
            case _:
                raise ValueError(encoding)

    def set(self, dataset: str = None, key: str = '', value: Any = None, expire: float = math.inf) -> None:
        """设置键值"""
        with self.lock:
            if not dataset:
                dataset = self.default_dataset
            assert isinstance(dataset, str), 'dataset必须是字符串'
            assert dataset, 'dataset不能为空'
            assert isinstance(key, str), 'key必须是字符串'
            assert key, 'key不能为空'
            if dataset not in self.datasets:
                self.create_table(dataset=dataset)
                self.datasets.clear()
                self.datasets.update(self.get_tables())
            payload, encoding = self.encode_value(value=value)
            sql: str = f"""REPLACE INTO `{dataset}` (`key`, `value`, `encoding`, `expired_at`) VALUES(?,?,?,?)"""
            self.conn.execute(sql, (key, payload, encoding, time.time() + expire))
            self.conn.commit()

    def rename(self, dataset: str = None, key: str = '', new_key: str = '') -> None:
        """重命名键值"""
        with self.lock:
            if not dataset:
                dataset = self.default_dataset
            assert isinstance(dataset, str), 'dataset必须是字符串'
            assert dataset, 'dataset不能为空'
            assert isinstance(key, str), 'key必须是字符串'
            assert key, 'key不能为空'
            assert isinstance(new_key, str), 'new_key必须是字符串'
            assert new_key, 'new_key不能为空'
            if key == new_key:
                return
            if dataset not in self.datasets:
                self.create_table(dataset=dataset)
                self.datasets.clear()
                self.datasets.update(self.get_tables())
            sql: str = f"""UPDATE `{dataset}` SET `key` = ? WHERE `key` = ?"""
            self.conn.execute(sql, (new_key, key))
            self.conn.commit()

    def update(self, dataset: str = None, items: Dict[str, Any] = None, expire: float = math.inf) -> None:
        """批量设置键值"""
        with self.lock:
            if not dataset:
                dataset = self.default_dataset
            assert isinstance(dataset, str), 'dataset必须是字符串'
            assert dataset, 'dataset不能为空'
            assert isinstance(items, dict), 'items必须是字典'
            if not items:
                return
            for key in items.keys():
                assert isinstance(key, str), 'key必须是字符串'
                assert key, 'key不能为空'
            if dataset not in self.datasets:
                self.create_table(dataset=dataset)
                self.datasets.clear()
                self.datasets.update(self.get_tables())
            ps: List[Tuple] = []
            now = time.time()
            for key, value in items.items():
                payload, encoding = self.encode_value(value=value)
                ps.append((key, payload, encoding, now + expire))
            sql: str = f"""REPLACE INTO `{dataset}` (`key`, `value`, `encoding`, `expired_at`) VALUES(?,?,?,?)"""
            self.conn.executemany(sql, ps)
            self.conn.commit()

    def add(self, dataset: str = None, key: str = '', value: Any = None, expire: float = math.inf) -> None:
        """添加值到集合中"""
        with self.lock:
            if not dataset:
                dataset = self.default_dataset
            assert isinstance(dataset, str), 'dataset必须是字符串'
            assert dataset, 'dataset不能为空'
            assert isinstance(key, str), 'key必须是字符串'
            assert key, 'key不能为空'
            rs: Set = self.get(dataset=dataset, key=key) or set()
            try:
                hash(value)
                rs.add(value)
            except TypeError:
                rs.update(value)
            self.set(dataset=dataset, key=key, value=rs, expire=expire)

    def delete(self, dataset: str = None, key: str | List[str] = None) -> None:
        """删除键值对"""
        with self.lock:
            if not dataset:
                dataset = self.default_dataset
            assert isinstance(dataset, str), 'dataset必须是字符串'
            assert dataset, 'dataset不能为空'
            assert key, 'key不能为空'
            if isinstance(key, str):
                key: List[str] = [key]
            elif isinstance(key, list):
                for k in key:
                    assert isinstance(k, str), 'key列表元素必须是字符串'
                    assert k, 'key列表元素不能为空'
            else:
                raise ValueError('key必须是字符串或字符串列表')
            if dataset in self.datasets:
                placeholders: str = ', '.join(['?'] * len(key))
                sql: str = f"""DELETE FROM `{dataset}` WHERE `key` IN ({placeholders})"""
                self.conn.execute(sql, key)
                self.conn.commit()

    def get(self, dataset: str = None, key: str = '') -> Any | None:
        """获取键值"""
        r = None
        with self.lock:
            if not dataset:
                dataset = self.default_dataset
            assert isinstance(dataset, str), 'dataset必须是字符串'
            assert dataset, 'dataset不能为空'
            assert isinstance(key, str), 'key必须是字符串'
            assert key, 'key不能为空'
            if dataset in self.datasets:
                cursor = self.conn.cursor()
                sql: str = f"""SELECT `value`, `encoding` FROM `{dataset}` WHERE `key` = ? AND `expired_at` > ?"""
                r = cursor.execute(sql, (key, time.time()))
                r = r.fetchone()
        if r is None:
            return r
        else:
            value, encoding = r
            return self.decode_value(value=value, encoding=encoding)

    def keys(self, dataset: str = None) -> List[str] | None:
        """列出所有键名"""
        with self.lock:
            if not dataset:
                dataset = self.default_dataset
            assert isinstance(dataset, str), 'dataset必须是字符串'
            assert dataset, 'dataset不能为空'
            if dataset in self.datasets:
                cursor = self.conn.cursor()
                sql: str = f"""SELECT `key` FROM `{dataset}` WHERE `expired_at` > ?"""
                r = cursor.execute(sql, (time.time(), ))
                result: List[str] = []
                for (key, ) in r.fetchall():
                    result.append(key)
                return result

    def items(self, dataset: str = None) -> Dict:
        """列出所有键值对"""
        rs: List[Tuple] = []
        result: Dict[str, Any] = {}
        with self.lock:
            if not dataset:
                dataset = self.default_dataset
            assert isinstance(dataset, str), 'dataset必须是字符串'
            assert dataset, 'dataset不能为空'
            if dataset in self.datasets:
                cursor = self.conn.cursor()
                sql: str = f"""SELECT `key`, `value`, `encoding` FROM `{dataset}` WHERE `expired_at` > ?"""
                r = cursor.execute(sql, (time.time(), ))
                rs = r.fetchall()
        for key, value, encoding in rs:
            result[key] = self.decode_value(value=value, encoding=encoding)
        return result

    def drop_table(self, dataset: str):
        """删除数据集"""
        with self.lock:
            assert isinstance(dataset, str), 'dataset必须是字符串'
            assert dataset, 'dataset不能为空'
            if dataset in self.datasets:
                sql: str = f"""DROP TABLE IF EXISTS `{dataset}`"""
                self.conn.execute(sql)
                self.conn.commit()
                self.datasets.discard(dataset)

    def vacuum(self, force: bool = True):
        with self.lock:
            key_vacuum_at: str = '__VACUUM__'
            vacuum_at: int | None = self.get(key=key_vacuum_at)
            if force or not vacuum_at or time.time() - vacuum_at >= 86400:
                self.conn.execute('VACUUM')
                self.set(key=key_vacuum_at, value=int(time.time()))

    def close(self):
        with self.lock:
            self.conn.commit()
            for dataset in self.datasets:
                sql: str = f"DELETE FROM `{dataset}` WHERE `expired_at` <= ?"
                self.conn.execute(sql, (int(time.time()), ))
            self.vacuum(force=False)
            self.conn.close()
