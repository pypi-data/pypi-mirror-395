# -*- coding: utf-8 -*-
import enum
from enum import EnumMeta, Enum
from typing import Any, Dict


class ByKey(EnumMeta):
    map: Dict[str, Any] = {}

    def __getattribute__(cls, name: str):
        value = super().__getattribute__(name)
        if isinstance(value, cls):
            value = cls.map[name]
        return value

    @classmethod
    def check(cls, obj: enum.EnumMeta):
        """一致性检查"""
        errors: str = ",".join(sorted(set(cls.map) - {c.name for c in obj}))  # type: ignore
        if errors:
            raise ValueError(f"{obj.__class__.__name__}缺少枚举项: {errors}")
        errors: str = ",".join(sorted({c.name for c in obj} - set(cls.map)))  # type: ignore
        if errors:
            raise ValueError(f"{obj.__class__.__name__}非法枚举项: {errors}")


class Period(enum.Enum):
    Transaction = 'trans'
    Tick = 'tick'
    OneSecond = '1s'
    OneMinute = '1m'
    OneHour = '1h'
    OneDay = '1d'
