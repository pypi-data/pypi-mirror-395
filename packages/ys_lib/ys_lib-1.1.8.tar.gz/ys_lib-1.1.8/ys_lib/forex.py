# -*- coding: utf-8 -*-
"""外汇基础货币枚举"""
import enum


class Currency(enum.Enum):
    AUD = enum.auto()
    BRL = enum.auto()
    CAD = enum.auto()
    CHF = enum.auto()
    CNH = enum.auto()
    CZK = enum.auto()
    DKK = enum.auto()
    EUR = enum.auto()
    GBP = enum.auto()
    HKD = enum.auto()
    JPY = enum.auto()
    MXN = enum.auto()
    NOK = enum.auto()
    NZD = enum.auto()
    PLN = enum.auto()
    RUB = enum.auto()
    SEK = enum.auto()
    SGD = enum.auto()
    TRY = enum.auto()
    USD = enum.auto()
    XAG = enum.auto()
    XAU = enum.auto()
    XPD = enum.auto()
    XPT = enum.auto()
    ZAR = enum.auto()


class Forex:
    def __init__(self, symbol: str):
        assert len(symbol) == 6
        self.currency1: Currency = Currency[symbol[:3].upper()]
        self.currency2: Currency = Currency[symbol[3:].upper()]
        self.symbol: str = f'{self.currency1.name}{self.currency2.name}'

    def __repr__(self):
        return self.symbol
