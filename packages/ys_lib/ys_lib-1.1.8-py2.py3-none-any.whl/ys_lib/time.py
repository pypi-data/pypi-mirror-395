# -*- coding: utf-8 -*-
import time


class Time:
    # 多次取样计算基准时间
    _reference_time = min([int(time.time() * 10 ** 9) - time.perf_counter_ns() for _ in range(10000)])

    @classmethod
    def time_ns(cls) -> int:
        """获取纳秒时间戳"""
        return cls._reference_time + time.perf_counter_ns()

    @classmethod
    def time_us(cls) -> int:
        """获取微秒时间戳"""
        return cls.time_ns() // 1000

    @classmethod
    def time_ms(cls) -> int:
        """获取毫秒时间戳"""
        return cls.time_ns() // 1000_000
