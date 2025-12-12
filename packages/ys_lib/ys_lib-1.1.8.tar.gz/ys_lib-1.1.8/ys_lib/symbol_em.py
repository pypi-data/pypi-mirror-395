# -*- coding: utf-8 -*-
"""东方财富代码"""

import datetime
import pypinyin
import re
import requests
import string
from .exchange import Exchange
from .symbol import (
    SymbolType,
    SymbolSubType,
    StockType,
    FundType,
    BondType,
    FuturesType,
    OptionsType,
    WarrantsType,
    IndexType,
    DrType,
    SpotType,
    SymbolFlag,
)
from typing import Any, AnyStr, Dict, List, Set, Tuple
import concurrent.futures


Trans: Dict[int, int] = {
    ord(char) + 0xFEE0: ord(char) for char in string.digits + string.ascii_letters
}
EMMarkets = [
    0,
    1,
    2,
    8,
    10,
    11,
    12,
    46,
    47,
    50,
    90,
    100,
    101,
    102,
    103,
    104,
    105,
    106,
    107,
    108,
    109,
    110,
    111,
    112,
    113,
    114,
    115,
    116,
    118,
    119,
    120,
    121,
    122,
    123,
    124,
    125,
    128,
    130,
    131,
    132,
    133,
    134,
    139,
    140,
    141,
    142,
    144,
    150,
    151,
    153,
    154,
    155,
    156,
    157,
    158,
    159,  # 商品加权指数
    160,
    162,
    163,
    165,
    171,
    200,
    201,
    202,
    220,
    221,
    223,
    225,
    226,
    245,
    246,
    248,
    251,
    252,
    302,
    303,
    304,
    305,
    306,
    307,
    308,
    309,
    310,
    311,
    312,
    313,
    315,
    316,
    318,
    319,
    320,
    321,
    322,
    323,
    324,
    325,
    326,
    327,
    329,
    330,
    331,
    332,
    333,
    334,
    335,
    336,
    337,
    338,
    339,
    340,
    341,
    342,
    343,
    344,
    345,
    346,
    347,
    348,
    349,
    351,
    352,
    356,
]


DerivativesMarkets = {
    113: (SymbolType.FUTURES, Exchange.SHFE),
    114: (SymbolType.FUTURES, Exchange.DCE),
    115: (SymbolType.FUTURES, Exchange.CZCE),
    220: (SymbolType.FUTURES, Exchange.CFFEX),
    225: (SymbolType.FUTURES, Exchange.GFEX),
    142: (SymbolType.FUTURES, Exchange.INE),
    10: (SymbolType.OPTIONS, Exchange.SSE),
    12: (SymbolType.OPTIONS, Exchange.SZSE),
    140: (SymbolType.OPTIONS, Exchange.DCE),
    141: (SymbolType.OPTIONS, Exchange.CZCE),
    151: (SymbolType.OPTIONS, Exchange.SHFE),
    163: (SymbolType.OPTIONS, Exchange.INE),
    221: (SymbolType.OPTIONS, Exchange.CFFEX),
    226: (SymbolType.OPTIONS, Exchange.GFEX),
}


class KLineRecord:
    """K线数据类"""

    def __init__(self, kline: AnyStr, fields2: List[str]):
        r: Dict = dict(zip(fields2, kline.split(",")))
        self._datetime: datetime.datetime = datetime.datetime.strptime(
            r["f51"], "%Y-%m-%d"
        )
        self.date: str = self._datetime.strftime("%Y-%m-%d")
        self.open: float = float(r["f52"])
        self.close: float = float(r["f53"])
        self.high: float = float(r["f54"])
        self.low: float = float(r["f55"])
        self.volume: float = float(r["f56"])
        self.money: float = float(r["f57"])
        self.turnover_rate: float = float(r["f61"])
        self.open_interest: float = float(r["f63"])
        self.settlement_price: float = float(r["f65"])

    @property
    def raw_datetime(self) -> datetime.datetime:
        return self._datetime

    def to_list(self) -> List[Any]:
        return list([v for k, v in self.__dict__.items() if not k.startswith("_")])

    @property
    def yyyymmdd(self) -> str:
        return self._datetime.strftime("%Y%m%d")


class TrendRecord:
    """分时线数据类"""

    def __init__(self, trend: AnyStr, fields2: List[str]):
        r: Dict = dict(zip(fields2, trend.split(",")))
        self._datetime: datetime.datetime = datetime.datetime.strptime(
            r["f51"], "%Y-%m-%d %H:%M"
        )
        self.datetime: str = self._datetime.strftime("%Y-%m-%d %H:%M:%S")
        self.open: float = float(r["f52"])
        self.close: float = float(r["f53"])
        self.high: float = float(r["f54"])
        self.low: float = float(r["f55"])
        self.volume: float = float(r["f56"])
        self.money: float = float(r["f57"])
        self.open_interest: float = float(r["f59"])

    @property
    def raw_datetime(self) -> datetime.datetime:
        return self._datetime

    @property
    def date(self) -> str:
        return self._datetime.strftime("%Y-%m-%d")

    @property
    def time(self) -> str:
        return self._datetime.strftime("%H%M%S")

    def to_list(self) -> List[Any]:
        return list([v for k, v in self.__dict__.items() if not k.startswith("_")])

    @property
    def yyyymmdd(self) -> str:
        return self._datetime.strftime("%Y%m%d")


class EMParser:
    fmt_date: str = "%Y-%m-%d"
    fmt_time: str = "%H:%M:%S"
    fmt_datetime: str = f"{fmt_date} {fmt_time}"

    def __init__(self, record: Dict):
        self.record: Dict = record

    def strip(self, fn: str) -> Any:
        value: Any = self.record[fn]
        if isinstance(value, str) and value == "-":
            return
        return value

    def parse_base_info(self) -> Tuple[Exchange, SymbolSubType, SymbolFlag]:
        """从东方财富市场信息解析交易所及标的品种类型等信息"""
        m = self.m
        t = self.t
        s = self.s
        e = self.e
        f = self.f
        exchange: Exchange | None = None
        typ: SymbolSubType | None = None
        flg: SymbolFlag = SymbolFlag()

        if m in {0, 1}:
            if f & 2**2:
                flg.is_st = True
            if f & 2**3:
                flg.is_new = True
            if s & 2**19:
                flg.is_approval = True
            if s & 2**17:
                flg.is_registration = True
            if s & 2**9:
                flg.is_innovation_market = True
            if s & 2**8:
                flg.is_base_market = True
            if s & 2**7:
                flg.is_call_auction = True
            if s & 2**5:
                flg.is_market_making = True
            if s & 3:
                flg.is_pt = True

        if m == 0:
            exchange = Exchange.SZSE
            if t == 5:
                typ = IndexType.INDEX_OTHER
            elif t == 6:
                typ = StockType.STOCK_A
            elif t == 7:
                typ = StockType.STOCK_B
            elif t == 8:
                # [7, 9, 10, 11, 12, 13, 14, 15, 29]
                if e == 7:
                    typ = BondType.BOND_OTHER  # 政府债
                elif e == 9:
                    typ = BondType.BOND_ENTERPRISE
                elif e == 10:
                    typ = BondType.BOND_COMPANY
                elif e == 11:
                    typ = BondType.BOND_CONVERTIBLE
                elif e == 12:
                    typ = BondType.BOND_EXCHANGEABLE
                elif e == 13:
                    typ = BondType.BOND_ABS
                elif e == 14:
                    typ = BondType.BOND_BUYBACK
                elif e == 15:
                    typ = BondType.BOND_COMPANY  # 私募公司债
                elif e == 29:
                    typ = StockType.STOCK_P
            elif t == 10:
                if e == 16:
                    typ = FundType.FUND_ETF
                elif e == 97:
                    typ = FundType.FUND_REITS
            elif t == 80:
                typ = StockType.STOCK_G
            elif t == 81:
                if s & 2048:
                    # 北证A股
                    exchange = Exchange.BSE
                    typ = StockType.STOCK_A
                else:
                    exchange = Exchange.NEEQ
                    typ = StockType.STOCK_OTHER
        elif m == 1:
            exchange = Exchange.SSE
            # if e == 15:
            #     return exchange, stype  # 新标准券
            # elif e == 34:
            #     return exchange, stype  # 申购
            # elif e == 36:
            #     return exchange, stype  # 配号
            # elif e == 37:
            #     return exchange, stype  # 认购款
            # elif e == 44:
            #     return exchange, stype  # 配债
            # elif e == 48:
            #     return exchange, stype  # 分红代码
            # elif e == 49:
            #     return exchange, stype  # 转托管代码
            if t == 1:
                typ = IndexType.INDEX_OTHER
            elif t == 2:
                typ = StockType.STOCK_A
            elif t == 3:
                typ = StockType.STOCK_B
            elif t == 4:
                # [7, 9, 10, 11, 12, 14, 15, 29, 34, 36, 37, 44, 99]
                if e == 7:
                    typ = BondType.BOND_OTHER  # 政府债
                elif e == 9:
                    typ = BondType.BOND_ENTERPRISE  # 一般企业债
                elif e == 10:
                    typ = BondType.BOND_COMPANY  # 一般公司债
                elif e == 11:
                    typ = BondType.BOND_CONVERTIBLE  # 可转债
                elif e == 12:
                    typ = BondType.BOND_EXCHANGEABLE
                elif e == 14:
                    typ = BondType.BOND_BUYBACK
                elif e == 29:
                    typ = StockType.STOCK_P
                elif e == 99:
                    pass  # 定向可转债 属于私募债
            elif t == 9:
                # [16, 17, 20, 23, 34, 37, 46, 47, 48, 49, 97]
                if e == 16:
                    typ = FundType.FUND_ETF
                elif e == 17:
                    typ = FundType.FUND_LOF
                elif e == 20:
                    typ = FundType.FUND_BOND
                elif e == 23:
                    typ = FundType.FUND_HYBRID
                elif e == 46:
                    typ = FundType.FUND_OPEN  # 开放式
                elif e == 47:
                    pass
                elif e == 97:
                    typ = FundType.FUND_REITS
            elif t == 23:
                typ = StockType.STOCK_K
        elif m == 2:
            exchange = Exchange.CSI
            if t == 24:
                typ = IndexType.INDEX_OTHER
        elif m == 10:
            exchange = Exchange.SSE
            typ = OptionsType.OPTIONS_ETF
            if t == 173:
                flg.is_call = True
            elif t == 174:
                flg.is_put = True
        elif m == 12:
            exchange = Exchange.SZSE
            typ = OptionsType.OPTIONS_ETF
            if t == 178:
                flg.is_call = True
            elif t == 179:
                flg.is_put = True
        elif m == 128:
            exchange = Exchange.HKEX
            if t == 1:
                typ = StockType.STOCK_A  # 港股主板
            elif t == 2:
                typ = StockType.STOCK_A  # 港股主板
            elif t == 3:
                typ = StockType.STOCK_A  # 港股主板
            elif t == 4:
                typ = StockType.STOCK_G  # 港股创业板
            elif t == 5:
                typ = WarrantsType.WARRANTS_CBBC  # 港股牛熊证
            elif t == 6:
                typ = OptionsType.OPTIONS_STOCK  # 港股窝轮
            if s & 64:
                pass  # 人民币交易港股
            if s & 1:
                pass  # ADR
        if m in {124, 125, 305}:
            exchange = Exchange.HKEX
            typ = IndexType.INDEX_OTHER
        elif m == 101:
            exchange = Exchange.COMEX
            typ = FuturesType.FUTURES_COMMODITY
        elif m == 102:
            exchange = Exchange.NYMEX
            typ = FuturesType.FUTURES_COMMODITY
        elif m == 103:
            exchange = Exchange.CBOT
            if t in {12, 20}:
                typ = FuturesType.FUTURES_INDEX
            elif t in {13, 14, 15, 16, 17}:
                typ = FuturesType.FUTURES_BOND
            else:
                typ = FuturesType.FUTURES_COMMODITY
        elif m == 104:
            exchange = Exchange.SGX
            if t == 1:
                typ = FuturesType.FUTURES_INDEX
            else:
                typ = FuturesType.FUTURES_COMMODITY
        elif m == 105:
            exchange = Exchange.NASDAQ
            typ = StockType.STOCK_A
        elif m == 106:
            exchange = Exchange.NYSE
            typ = StockType.STOCK_A
        elif m == 107:
            exchange = Exchange.AMEX
            typ = StockType.STOCK_A
        elif m == 108:
            exchange = Exchange.NYBOT
            typ = FuturesType.FUTURES_COMMODITY
        elif m == 109:
            exchange = Exchange.LME
            typ = FuturesType.FUTURES_COMMODITY
        elif m == 110:
            exchange = Exchange.BMD
            typ = FuturesType.FUTURES_COMMODITY
        elif m == 111:
            exchange = Exchange.TOCOM
            typ = FuturesType.FUTURES_COMMODITY
        elif m == 112:
            exchange = Exchange.ICE
            typ = FuturesType.FUTURES_COMMODITY
        elif m == 113:
            exchange = Exchange.SHFE
            typ = FuturesType.FUTURES_COMMODITY
        elif m == 114:
            exchange = Exchange.DCE
            typ = FuturesType.FUTURES_COMMODITY
        elif m == 115:
            exchange = Exchange.CZCE
            typ = FuturesType.FUTURES_COMMODITY
        elif m == 116:
            # t = [0, 1, 2, 3, 4, 5, 6, 7]
            # e = [9, 10, 15]
            exchange = Exchange.HKEX
            if t == 0:
                pass
            elif t == 1:
                # e = [0, 8, 9, 10, 16, 17, 18]
                if e & 0:
                    typ = FundType.FUND_ETF
                elif e & 8:
                    typ = FundType.FUND_REITS
                elif e & 9:
                    typ = FundType.FUND_OTHER
                elif e & 10:
                    typ = FundType.FUND_ETF
                elif e & 16:
                    typ = FundType.FUND_ETF
                elif e & 17:
                    typ = FundType.FUND_BOND
                elif e & 18:
                    typ = FundType.FUND_DERIVATIVES
            elif t == 2:
                if e & 4:
                    typ = BondType.BOND_OTHER
            elif t == 3:
                # e = [0, 1, 2, 7]
                typ = StockType.STOCK_A
                if e & 2:
                    typ = StockType.STOCK_P
            elif t == 4:
                typ = StockType.STOCK_G
            elif t == 5:
                typ = WarrantsType.WARRANTS_CBBC
                if s & 2:
                    flg.is_call = True  # 牛证
                if s & 4:
                    flg.is_put = True  # 熊证
            elif t == 6:
                typ = OptionsType.OPTIONS_STOCK
                if s & 2:
                    flg.is_call = True  # 购
                if s & 4:
                    flg.is_put = True  # 沽
            elif t == 7:
                typ = WarrantsType.WARRANTS_INLINE
        elif m == 118:
            exchange = Exchange.SGE
            typ = SpotType.SPOT_COMMODITY
        elif m == 139:
            exchange = Exchange.HKEX
            typ = OptionsType.OPTIONS_FOREX
        elif m == 140:
            exchange = Exchange.DCE
            typ = OptionsType.OPTIONS_COMMODITY
        elif m == 141:
            exchange = Exchange.CZCE
            typ = OptionsType.OPTIONS_COMMODITY
        elif m == 142:
            exchange = Exchange.INE
            typ = FuturesType.FUTURES_COMMODITY
        elif m == 151:
            exchange = Exchange.SHFE
            typ = OptionsType.OPTIONS_COMMODITY
        elif m == 155:
            exchange = Exchange.LSE
            if t == 1:
                typ = StockType.STOCK_OTHER
            elif t == 2:
                typ = StockType.STOCK_P
            elif t == 3:
                typ = FundType.FUND_ETF
        elif m == 156:
            # s = [1, 5, 6, 7, 8]
            exchange = Exchange.LSE
            typ = DrType.DR_GDR
        elif m == 163:
            exchange = Exchange.INE
            typ = OptionsType.OPTIONS_COMMODITY
        elif m == 252:
            exchange = Exchange.SIX
            if t == 1:
                typ = DrType.DR_GDR
        elif m == 220:
            exchange = Exchange.CFFEX
            typ = FuturesType.FUTURES_COMMODITY
        elif m == 221:
            exchange = Exchange.CFFEX
            typ = OptionsType.OPTIONS_INDEX
        elif m == 225:
            exchange = Exchange.GFEX
            typ = FuturesType.FUTURES_COMMODITY
        elif m == 226:
            exchange = Exchange.GFEX
            typ = OptionsType.OPTIONS_COMMODITY
        elif m == 341:
            exchange = Exchange.LSE
            typ = IndexType.INDEX_OTHER

        if typ and typ.parent() == SymbolType.FUTURES:
            if s & 1:
                flg.is_main_perpetual_contract = True  # 主连合约
            elif s & 2:
                flg.is_second_main_perpetual_contract = True  # 次主连合约
            elif s & 4:
                flg.is_main_contract = True  # 主力合约
            elif s & 8:
                flg.is_second_main_contract = True  # 次主力合约

        return exchange, typ, flg

    def parse_str(self, fn) -> str | None:
        value: str | None = self.strip(fn=fn)
        if isinstance(value, str) and value and value != "-":
            return value.strip()

    def parse_int(self, fn: str) -> int | None:
        value: int | None = self.strip(fn=fn)
        if isinstance(value, int):
            return value

    def parse_float(self, fn: str) -> int | float | None:
        value: int | float | None = self.strip(fn=fn)
        if isinstance(value, (int, float)):
            return value

    def parse_yyyymmdd(self, fn: str) -> str | None:
        value: int | str | None = self.strip(fn=fn)
        if isinstance(value, int):
            value: str = str(value)
        if isinstance(value, str) and len(value) == 8:
            return datetime.datetime.strptime(value, "%Y%m%d").strftime(self.fmt_date)

    @property
    def m(self) -> int:
        return self.parse_int(fn="f13")

    @property
    def t(self) -> int:
        return self.parse_int(fn="f19")

    @property
    def s(self) -> int:
        return self.parse_int(fn="f111")

    @property
    def e(self) -> int:
        return self.parse_int(fn="f139")

    @property
    def f(self) -> int:
        return self.parse_int(fn="f148")

    @property
    def secid(self) -> str:
        return f"{self.m}.{self.code}"

    @property
    def trade_periods(self) -> Dict[str, List[List[str]]]:
        """解析交易时段"""

        def to_datetime(t: int) -> str:
            """时间转换YYYYmmddHHMM -> YYYY-mm-dd HH:MM:SS"""
            return datetime.datetime.strptime(str(t), "%Y%m%d%H%M").strftime(
                "%Y-%m-%d %H:%M:%S"
            )

        f400: Dict | None = self.strip(fn="f400")
        results: Dict[str, List[List[str]]] = {}
        if isinstance(f400, dict):
            for k, v in {"pre": "O", "after": "C"}.items():
                p: Dict | None = f400.get(k, {})
                if p and isinstance(p, dict):
                    results[v] = [[to_datetime(p[k]) for k in ["b", "e"]]]
                else:
                    results[v] = []
            ps = f400.get("periods", [])
            if ps and isinstance(ps, list):
                results["T"] = [[to_datetime(p[k]) for k in ["b", "e"]] for p in ps]
            else:
                results["T"] = []
        return results

    @property
    def trade_date(self) -> str | None:
        """返回正在进行或即将开始的交易日"""
        f400: Dict | None = self.strip(fn="f400")
        dates: Set[str] = set()
        if isinstance(f400, dict):
            for k, v in f400.items():
                if isinstance(v, dict):
                    for be in ["b", "e"]:
                        if be in v:
                            dates.add(v[be])
                elif isinstance(v, list):
                    for _v in v:
                        if isinstance(_v, dict):
                            for be in ["b", "e"]:
                                if be in _v:
                                    dates.add(_v[be])
        if dates:
            return datetime.datetime.strptime(str(max(dates)), "%Y%m%d%H%M").strftime(
                "%Y-%m-%d"
            )

    @property
    def code(self):
        """标的代码"""
        return self.parse_str(fn="f12")

    @property
    def instrument_id(self):
        """标的代码"""
        return self.parse_str(fn="f12")

    @property
    def pre_close(self) -> int | float | None:
        """昨收价"""
        return self.parse_float(fn="f18")

    @property
    def total_shares(self) -> int | float | None:
        """总股本"""
        return self.parse_float(fn="f38")

    @property
    def float_shares(self) -> int | float | None:
        """流通股本"""
        return self.parse_float(fn="f39")

    @property
    def lot_size(self) -> int | float | None:
        """每手股数"""
        return self.parse_float(fn="f324")

    @property
    def apply_code(self) -> str | None:
        """申购代码"""
        return self.parse_str(fn="f348")

    @property
    def name_cn(self) -> str | None:
        """中文名称"""
        return self.parse_str(fn="f14")

    @property
    def name_en(self) -> str | None:
        """英文名称"""
        return self.parse_str(fn="f422")

    @property
    def underlying_code(self) -> str | None:
        """基础证券代码"""
        # 可转债的正股代码为f232
        # ETF期权的ETF代码为f331
        return self.parse_str(fn="f232") or self.parse_str(fn="f331")

    @property
    def py(self) -> str | None:
        """拼音简称"""
        name_cn: str = self.name_cn
        if name_cn:
            py = "".join(
                pypinyin.lazy_pinyin(
                    re.sub(r"[\s,;.]", "", name_cn.translate(Trans)),
                    pypinyin.Style.FIRST_LETTER,
                )
            ).lower()
            return py

    @property
    def list_date(self) -> str | None:
        """上市日期"""
        return self.parse_yyyymmdd(fn="f26")

    @property
    def pre_settlement(self) -> float | int | None:
        """昨结价"""
        return self.parse_float(fn="f28")

    @property
    def settlement(self) -> float | int | None:
        """今结价"""
        return self.parse_float(fn="f145")

    @property
    def upper_limit_price(self) -> float | int | None:
        """涨停价"""
        return self.parse_float(fn="f350")

    @property
    def lower_limit_price(self) -> float | int | None:
        """跌停价"""
        return self.parse_float(fn="f351")

    @property
    def average_price(self) -> float | int | None:
        """成交均价"""
        return self.parse_float(fn="f352")

    @property
    def low(self) -> float | int | None:
        """最低价"""
        return self.parse_float(fn="f16") or self.parse_float(fn="f377")

    @property
    def high(self) -> float | int | None:
        """最高价"""
        return self.parse_float(fn="f15") or self.parse_float(fn="f378")

    @property
    def datetime(self) -> datetime.datetime | None:
        """行情时间"""
        t: int | None = self.parse_int(fn="f124")
        if t:
            return datetime.datetime.fromtimestamp(t)

    @property
    def close(self) -> float | int | None:
        """最新价"""
        return self.parse_float(fn="f2") or self.parse_float(fn="f277")

    @property
    def position(self) -> int | None:
        """持仓"""
        return self.parse_float(fn="f108")

    @property
    def money(self) -> float | None:
        """成交金额"""
        return self.parse_float(fn="f6")

    @property
    def volume(self) -> int | None:
        """成交量"""
        return self.parse_float(fn="f5")


class EMCrawler:
    session = requests.Session()
    session.headers["User-Agent"] = "Mozilla/5.0"

    # @classmethod
    # def clist_get(cls, markets: int | List[int], fields: str) -> List[EMParser]:
    #     """东财批量行情获取"""
    #     if isinstance(markets, int):
    #         markets: List[int] = [markets]
    #     else:
    #         for market in markets:
    #             assert isinstance(market, int)
    #     assert isinstance(fields, str)
    #     fields = ",".join(sorted(set(re.findall(r"(f\d+)", fields))))
    #     assert fields
    #     url: str = "https://push2.eastmoney.com/api/qt/clist/get"
    #     params: Dict = {
    #         "pn": 1,  # page_number 含义：当前页码，表示需要查询第几页。
    #         "pz": 1000000,  # page_size 含义：每页显示的记录条数（每页大小）。
    #         "po": 1,  # page_offset 含义：偏移量，表示从第几条记录开始查询。在 SQL 分页中，OFFSET 通常由 (page-1)*pageSize 计算得出.实际表示正序0/逆序1(未指定时默认0)!!!
    #         "np": 1,  # number_of_pages 含义：总页数（或总记录数），表示满足条件的数据总共有多少页。
    #         "ut": "bd1d9ddb04089700cf9c27f6f7426281",
    #         "fltt": 2,
    #         "invt": 2,
    #         "fs": ",".join([f"m:{market}" for market in markets]),
    #         "fields": fields,
    #     }
    #     r = cls.session.get(url=url, params=params)
    #     assert r.status_code == 200
    #     rj: Dict = r.json()
    #     assert rj["rc"] == 0
    #     data: Dict = rj["data"]
    #     diff: List[Dict] = data["diff"]
    #     print(f"total={data['total']} diff={len(diff)}")
    #     assert len(diff) == data["total"]
    #     records: List[EMParser] = []
    #     for record in diff:
    #         records.append(EMParser(record=record))
    #     return records

    @classmethod
    def clist_get(cls, markets: int | List[int], fields: str) -> List[EMParser]:
        """东财批量行情获取"""
        if isinstance(markets, int):
            markets: List[int] = [markets]
        else:
            for market in markets:
                assert isinstance(market, int)
        assert isinstance(fields, str)
        fields = ",".join(sorted(set(re.findall(r"(f\d+)", fields))))
        assert fields
        url: str = "https://push2.eastmoney.com/api/qt/clist/get"
        params: Dict = {
            "pn": 1,  # page_number 含义：当前页码，表示需要查询第几页。
            "pz": 200,  # page_size 含义：每页显示的记录条数（每页大小）。
            "po": 0,  # 表示正序0/逆序1(未指定时默认0)
            "np": 1,  # 表示diff类型：字典0/列表1(未指定时默认0)
            "ut": "bd1d9ddb04089700cf9c27f6f7426281",
            "fltt": 2,
            "invt": 2,
            "fs": ",".join([f"m:{market}" for market in markets]),
            "fields": fields,
            "fid": "f12",  # 按代码排序
        }
        all_records: List[EMParser] = []
        total = None

        def fetch_page(page_num):
            page_params = params.copy()
            page_params["pn"] = page_num
            try:
                r = cls.session.get(url=url, params=page_params)
                r.raise_for_status()  # 检查响应状态码
                rj: Dict = r.json()
                assert rj["rc"] == 0
                data: Dict = rj["data"]
                diff: List[Dict] = data["diff"]
                print(f"em get page={page_num} diff={len(diff)}")
                return [EMParser(record=record) for record in diff]
            except Exception as e:
                print(f"Error fetching page {page_num}: {e}")
                return []

        # 第一次请求获取总数量
        r = cls.session.get(url=url, params=params)
        r.raise_for_status()
        rj: Dict = r.json()
        assert rj["rc"] == 0
        data: Dict = rj["data"]
        total = data["total"]
        print(f"total={total}")

        # 计算总页数
        total_pages = (total + params["pz"] - 1) // params["pz"]

        # 使用线程池并发执行请求
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_to_page = {
                executor.submit(fetch_page, page_num): page_num
                for page_num in range(1, total_pages + 1)
            }
            for future in concurrent.futures.as_completed(future_to_page):
                page_num = future_to_page[future]
                try:
                    records = future.result()
                    all_records.extend(records)
                except Exception as exc:
                    print(f"{page_num} generated an exception: {exc}")

        assert len(all_records) == total, f"{len(all_records)} != {total}"
        return all_records
