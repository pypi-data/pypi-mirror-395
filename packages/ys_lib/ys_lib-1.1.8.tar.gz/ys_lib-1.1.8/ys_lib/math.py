# -*- coding: utf-8 -*-
import decimal
import math


def round_sf(value: float, sf: int = 3) -> float:
    """四舍五入，并保留N位有效数字"""
    if value == 0:
        return 0.0
    r: int = math.ceil(math.log10(value))
    _int: int = round(value * (10 ** (sf - r)))
    _dvd: int = 10 ** (sf - r)
    v = decimal.Decimal(_int) / decimal.Decimal(_dvd)
    return float(v)


def price_standardize(price: float, price_tick: float):
    """价格精度标准化"""
    _price_tick: decimal.Decimal = decimal.Decimal(str(price_tick))
    _price: decimal.Decimal = decimal.Decimal(str(price))
    price_s: decimal.Decimal = round(_price / _price_tick) * _price_tick
    return float(str(price_s))
