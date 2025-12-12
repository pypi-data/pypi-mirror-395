# -*- coding: utf-8 -*-
"""国内外交易品种类型枚举"""
import functools
import re
from dataclasses import dataclass
from enum import Enum
from typing import Dict, FrozenSet, List, Tuple
from ys_lib import Exchange


class SymbolSubType(Enum):
    def parent(self) -> 'SymbolType':
        """获取当前的父类型"""
        return SymbolType(self.__class__)


class StockType(SymbolSubType):
    """股票"""
    STOCK_A = '以人民币交易的股票（主板）'  # 主板A股 SH:ASH
    STOCK_B = '以美元交易的股票'  # 主板B股 SH:BSH
    STOCK_K = '以人民币交易的股票（科创板）'  # 科创板 SH:KSH
    STOCK_G = '创业板'  # 创业板GEM SZ:GEM
    STOCK_P = '优先股'  # SH:OPS,PPS SZ:33
    STOCK_OTHER = '其它股票'  # SH:OEQ,OPS,PPS


class FundType(SymbolSubType):
    """基金"""
    FUND_CLOSE = '封闭式基金'  # SH:CEF
    FUND_OPEN = '开放式基金'  # SH:OEF
    FUND_ETF = '交易所交易基金'  # SH:EBS
    FUND_LOF = 'LOF基金'  # SH:LOF
    FUND_REITS = '公募REITs'  # SH:RET
    FUND_STOCK = '股票基金'
    FUND_BOND = '债券型基金'
    FUND_DERIVATIVES = '衍生品基金'
    FUND_HYBRID = '混合型基金'
    FUND_FOF = 'FOF基金'
    FUND_OTHER = '其它基金'  # SH:OFN


class BondType(SymbolSubType):
    """债券"""
    BOND_NATIONAL = '国债、地方债、政府支持债、政策性金融债'  # SH:GBF
    BOND_ENTERPRISE = '企业债'  # SH:CBF
    BOND_CONVERTIBLE = '可转换企业债'  # SH:CCF
    BOND_EXCHANGEABLE = '可交换债'
    BOND_COMPANY = '公司债、企业债、可交换债、政府支持债'  # SH:CPF
    BOND_BUYBACK = '质押式回购'  # SH:CRP SZ:12
    BOND_ABS = '资产支持证券'
    BOND_OTHER = '其它债券'  # SH:DST,DVP,OBD,WIT,QRP,AMP,TCB


class OptionsType(SymbolSubType):
    """期权"""
    OPTIONS_STOCK = '个股期权'  # SZ:29
    OPTIONS_ETF = 'ETF期权'  # SZ:30
    OPTIONS_INDEX = '指数期权'  # CFFEX
    OPTIONS_COMMODITY = '商品期权'
    OPTIONS_FOREX = '外汇期权'
    OPTIONS_OTHER = '其他期权'


class DrType(SymbolSubType):
    """存托凭证"""
    DR_GDR = '全球存托凭证'
    DR_OTHER = '其他存托凭证'


class IndexType(SymbolSubType):
    """指数"""
    INDEX_OTHER = '其他指数'


class FuturesType(SymbolSubType):
    """期货"""
    FUTURES_STOCK = '股票期货'
    FUTURES_INDEX = '指数期货'
    FUTURES_COMMODITY = '商品期货'
    FUTURES_BOND = '债券期货'
    FUTURES_OTHER = '其他期货'


class WarrantsType(SymbolSubType):
    """权证"""
    WARRANTS_CBBC = '牛熊证'
    WARRANTS_INLINE = '界内证'
    WARRANTS_OTHER = '其他权证'


class BlockType(SymbolSubType):
    """板块"""
    BLOCK_CONCEPT = '概念板块'
    BLOCK_REGION = '地域板块'
    BLOCK_INDUSTRY = '行业板块'
    BLOCK_OTHER = '其他板块'


class SpotType(SymbolSubType):
    """现货"""
    SPOT_COMMODITY = '商品现货'
    SPOT_OTHER = '其他现货'


class CombinationType(SymbolSubType):
    """组合"""
    COMBINATION_SP = '期货跨期组合'
    COMBINATION_SPC = '期货跨品种组合'
    COMBINATION_OTHER = '其他组合'


class SymbolType(Enum):
    """基础类别"""
    STOCK = StockType
    BOND = BondType
    FUND = FundType
    INDEX = IndexType
    FUTURES = FuturesType
    OPTIONS = OptionsType
    WARRANTS = WarrantsType
    DR = DrType
    SPOT = SpotType
    BLOCK = BlockType
    COMBINATION = CombinationType


@dataclass
class SymbolFlag:
    is_st: bool | None = None                       # 风险警示=True
    is_new: bool | None = None                      # 新股=True
    is_approval: bool | None = None                 # 核准制=True
    is_registration: bool | None = None             # 注册制=True
    is_base_market: bool | None = None              # 基础层=True
    is_innovation_market: bool | None = None        # 创新层=True
    is_call_auction: bool | None = None             # 集合竞价=True
    is_market_making: bool | None = None            # 做市=True
    is_pt: bool | None = None                       # 两网及退市=True
    is_call: bool | None = None                     # 看涨=True
    is_put: bool | None = None                      # 看跌=True
    is_northbound: bool | None = None               # 北向=True
    is_southbound: bool | None = None               # 南向=True
    is_main_contract: bool | None = None            # 主力合约=True
    is_second_main_contract: bool | None = None     # 次主力合约=True
    is_main_perpetual_contract: bool | None = None          # 主力永续合约=True
    is_second_main_perpetual_contract: bool | None = None   # 次主力永续合约=True


class SymbolDetail:
    def __init__(self, original_symbol_id: str, exchange: Exchange, instrument_id: str, instrument_type: SymbolType,
                 instrument_name: str = '', product_id: str = '', underlying_symbol: 'SymbolDetail' = None,
                 instrument_id1: str = '', instrument_id2: str = '', expired: bool = False
                 ):
        self.original_symbol_id: str = original_symbol_id
        self.exchange: Exchange = exchange
        self.instrument_id: str = instrument_id
        self.symbol_id: str = f'{instrument_id}.{exchange.value.acronym}'
        self.instrument_type: SymbolType = instrument_type
        self.instrument_name: str = instrument_name
        self.product_id: str = product_id      # 期货/期权合约对应的产品
        self.underlying_symbol: SymbolDetail | None = underlying_symbol   # 期权合约对应的期货合约
        self.instrument_id1: str = instrument_id1       # 跨期合约/跨产品合约 合约1
        self.instrument_id2: str = instrument_id2       # 跨期合约/跨产品合约 合约2
        self.expired: bool = expired

    def __repr__(self):
        return f'{self.__class__.__name__}({self.symbol_id}, {self.original_symbol_id}, {self.instrument_type.name}, {self.instrument_name}, {self.product_id})'


# 国内期货交易所
DomesticFuturesExchanges: FrozenSet[Exchange] = frozenset({
    Exchange.CZCE, Exchange.DCE, Exchange.SHFE, Exchange.INE, Exchange.CFFEX, Exchange.GFEX,
})


# 国内期权交易所
DomesticOptionsExchanges: FrozenSet[Exchange] = frozenset({
    Exchange.CZCE, Exchange.DCE, Exchange.SHFE, Exchange.INE, Exchange.CFFEX, Exchange.GFEX,
    Exchange.SSE, Exchange.SZSE,
})


class SymbolGuesser:
    """代码猜解器"""

    @classmethod
    @functools.lru_cache(maxsize=2**16)
    def guess_symbol_detail(cls, original_symbol_id: str) -> SymbolDetail | None:
        index: int = original_symbol_id.find('.')
        if index <= 0:
            return
        a: str = original_symbol_id[:index]
        b: str = original_symbol_id[index + 1:]
        eb: Exchange | None = Exchange.find(market_id=b)
        ea: Exchange | None = Exchange.find(market_id=a)
        if eb and ea:
            return
        elif eb:
            iid: str = a
            exchange: Exchange = eb
        elif ea:
            iid: str = b
            exchange: Exchange = ea
        else:
            return
        l_iid: int = len(iid)
        if exchange == Exchange.SSE:
            if l_iid == 8 and iid.startswith('1'):
                instrument_type = SymbolType.OPTIONS
            elif l_iid == 6 and iid.startswith('000'):
                instrument_type = SymbolType.INDEX
            elif l_iid == 6 and iid.startswith('5'):
                instrument_type = SymbolType.FUND
            elif l_iid == 6 and iid.startswith(('6', '9')):
                instrument_type = SymbolType.STOCK
            elif l_iid == 6 and iid.startswith(('100', '11', '204', '1260')):
                instrument_type = SymbolType.BOND
            else:
                return
            return SymbolDetail(
                original_symbol_id=original_symbol_id,
                exchange=exchange,
                instrument_id=iid,
                instrument_type=instrument_type,
            )
        elif exchange == Exchange.SZSE:
            if len(iid) == 8 and iid.startswith('9'):
                instrument_type = SymbolType.OPTIONS
            elif l_iid == 6 and iid.startswith('399'):
                instrument_type = SymbolType.INDEX
            elif l_iid == 6 and iid.startswith(('15', '16', '18')):
                instrument_type = SymbolType.FUND
            elif l_iid == 6 and iid.startswith(('2', '0', '3')):
                instrument_type = SymbolType.STOCK
            elif l_iid == 6 and iid.startswith(('12', '131', '1150')):
                instrument_type = SymbolType.BOND
            else:
                return
            return SymbolDetail(
                original_symbol_id=original_symbol_id,
                exchange=exchange,
                instrument_id=iid,
                instrument_type=instrument_type,
            )
        elif exchange == Exchange.BSE:
            if l_iid == 6 and iid.startswith('899'):
                instrument_type = SymbolType.INDEX
            elif l_iid == 6 and iid.startswith('82'):
                instrument_type = SymbolType.BOND
            elif l_iid == 6 and iid.startswith(('43', '83', '87')):
                instrument_type = SymbolType.STOCK
            else:
                return
            return SymbolDetail(
                original_symbol_id=original_symbol_id,
                exchange=exchange,
                instrument_id=iid,
                instrument_type=instrument_type,
            )
        elif exchange == Exchange.HKEX:
            if l_iid == 5:
                match iid[0]:
                    case '0' | '8':         # 港股主板
                        instrument_type = SymbolType.STOCK
                    case '1' | '2':         # 港股涡轮
                        instrument_type = SymbolType.WARRANTS
                    case '4' | '5' | '6':   # 港股牛熊证
                        instrument_type = SymbolType.OPTIONS
                    case _:
                        return
                return SymbolDetail(
                    original_symbol_id=original_symbol_id,
                    exchange=exchange,
                    instrument_id=iid,
                    instrument_type=instrument_type,
                )
        elif exchange in DomesticFuturesExchanges:
            # 不管期货还是期权 先分交易所大小写规格化一下
            match exchange:
                case Exchange.SHFE | Exchange.INE | Exchange.DCE | Exchange.GFEX:
                    code = iid.lower()
                case Exchange.CZCE | Exchange.CFFEX:
                    code = iid.upper()
                case _:
                    code = iid

            # 尝试匹配 期货
            match exchange:
                case Exchange.CZCE:
                    rs: List[Tuple[str, str]] = re.findall(r'^([A-Z]+)(\d{3,4})$', code, re.IGNORECASE)
                case _:
                    rs: List[Tuple[str, str]] = re.findall(r'^([A-Z]+)(\d{4})$', code, re.IGNORECASE)
            if rs:
                product_id, ym = rs[0]
                if exchange == Exchange.CZCE:
                    ym: str = ym[-3:]
                if 1 <= int(ym) % 100 <= 12:
                    return SymbolDetail(
                        original_symbol_id=original_symbol_id,
                        exchange=exchange,
                        instrument_id=f'{product_id}{ym}',
                        instrument_type=SymbolType.FUTURES,
                        product_id=product_id,
                    )

            # 尝试匹配 期货加权
            rs: List[Tuple[str, str]] = re.findall(r'^([a-zA-Z]+)(JQ00|8888)$', code, re.IGNORECASE)
            if rs:
                product_id, _ = rs[0]
                return SymbolDetail(
                    original_symbol_id=original_symbol_id,
                    exchange=exchange,
                    instrument_id=f'{product_id}8888',
                    instrument_type=SymbolType.FUTURES,
                    product_id=product_id,
                )

            # 尝试匹配 期货主连
            rs = re.findall(r'^([a-zA-Z]+)(00|9999)$', code, re.IGNORECASE)
            if rs:
                product_id, _ = rs[0]
                return SymbolDetail(
                    original_symbol_id=original_symbol_id,
                    exchange=exchange,
                    instrument_id=f'{product_id}9999',
                    instrument_type=SymbolType.FUTURES,
                    product_id=product_id,
                )

            # 尝试匹配 期权
            match exchange:
                case Exchange.CZCE:
                    rs: List[Tuple[str, str, str, str, str]] = re.findall(
                        r'^([A-Z]+?)(\d{3,4})-?(MS)?([CP])-?(\d+)$', code, re.IGNORECASE)
                case _:
                    rs: List[Tuple[str, str, str, str, str]] = re.findall(
                        r'^([A-Z]+?)(\d{4})-?(MS)?-?([CP])-?(\d+)$', code, re.IGNORECASE)
            if rs:
                product_id, ym, ms, cp, ep = rs[0]
                if exchange == Exchange.CZCE:
                    ym: str = ym[-3:]
                if 1 <= int(ym) % 100 <= 12:
                    cp: str = cp.upper()   # C / P
                    match exchange:
                        case Exchange.DCE | Exchange.GFEX:
                            # y2407-C-8700 si2408-C-16200
                            assert not ms, code
                            code = f'{product_id.lower()}{ym}-{cp}-{ep}'
                        case Exchange.SHFE | Exchange.INE:
                            # sc2406C640
                            assert not ms, code
                            code = f'{product_id.lower()}{ym}{cp}{ep}'
                        case Exchange.CZCE:
                            # AP410C7300 SR507MSC6400
                            code = f'{product_id.upper()}{ym}{ms}{cp}{ep}'
                        case Exchange.CFFEX:
                            # MO2406-C-3800
                            assert not ms, code
                            code = f'{product_id.upper()}{ym}-{cp}-{ep}'
                        case _:
                            assert not ms, code
                            code = code
                    return SymbolDetail(
                        original_symbol_id=original_symbol_id,
                        exchange=exchange,
                        instrument_id=code,
                        instrument_type=SymbolType.OPTIONS,
                        product_id=product_id,
                        underlying_symbol=cls.guess_symbol_detail(
                            original_symbol_id=f'{product_id}{ym}.{exchange.value.acronym}'
                        ),
                    )

            # 尝试匹配跨期合约
            rs: List[Tuple[str, str, str]] = re.findall(
                r'^(SP|SPD)\s+([A-Z]+\d{3,4})&([A-Z]+\d{3,4})$', code, re.IGNORECASE)
            if rs:
                a, i1, i2 = rs[0]
                sd1 = cls.guess_symbol_detail(original_symbol_id=f'{i1}.{exchange.name}')
                sd2 = cls.guess_symbol_detail(original_symbol_id=f'{i2}.{exchange.name}')
                if sd1 and sd2 and sd1.product_id == sd2.product_id:
                    b: str = {Exchange.CZCE: 'SPD', Exchange.DCE: 'SP', Exchange.GFEX: 'SP'}.get(exchange, a)
                    return SymbolDetail(
                        original_symbol_id=original_symbol_id,
                        exchange=exchange,
                        instrument_id=f'{b.upper()} {sd1.instrument_id}&{sd2.instrument_id}',
                        instrument_type=SymbolType.COMBINATION,
                        product_id=sd1.product_id,
                        instrument_id1=sd1.instrument_id,
                        instrument_id2=sd2.instrument_id,
                    )

            # 尝试匹配跨产品合约
            rs: List[Tuple[str, str, str]] = re.findall(
                r'^(SPC|IPS|SP)\s+([A-Z]+\d{3,4})&([A-Z]+\d{3,4})$', code, re.IGNORECASE)
            if rs:
                a, i1, i2 = rs[0]
                sd1 = cls.guess_symbol_detail(original_symbol_id=f'{i1}.{exchange.name}')
                sd2 = cls.guess_symbol_detail(original_symbol_id=f'{i2}.{exchange.name}')
                if sd1 and sd2:
                    b: str = {Exchange.CZCE: 'IPS', Exchange.DCE: 'SPC', Exchange.GFEX: 'SPC'}.get(exchange, a)
                    return SymbolDetail(
                        original_symbol_id=original_symbol_id,
                        exchange=exchange,
                        instrument_id=f'{b.upper()} {sd1.instrument_id}&{sd2.instrument_id}',
                        instrument_type=SymbolType.COMBINATION,
                        instrument_id1=sd1.instrument_id,
                        instrument_id2=sd2.instrument_id,
                    )

    @classmethod
    def test(cls):
        """验证"""
        # 上交所
        sd = cls.guess_symbol_detail(original_symbol_id='600000.SH')
        assert sd.symbol_id == '600000.SSE'
        assert sd.instrument_type == SymbolType.STOCK

        sd = cls.guess_symbol_detail(original_symbol_id='688192.SH')
        assert sd.symbol_id == '688192.SSE'
        assert sd.instrument_type == SymbolType.STOCK

        sd = cls.guess_symbol_detail(original_symbol_id='900906.SH')
        assert sd.symbol_id == '900906.SSE'
        assert sd.instrument_type == SymbolType.STOCK

        sd = cls.guess_symbol_detail(original_symbol_id='10006167.SHO')
        assert sd.symbol_id == '10006167.SSE'
        assert sd.instrument_type == SymbolType.OPTIONS

        sd = cls.guess_symbol_detail(original_symbol_id='10006168.SH')
        assert sd.symbol_id == '10006168.SSE'
        assert sd.instrument_type == SymbolType.OPTIONS

        sd = cls.guess_symbol_detail(original_symbol_id='510300.SH')
        assert sd.symbol_id == '510300.SSE'
        assert sd.instrument_type == SymbolType.FUND

        sd = cls.guess_symbol_detail(original_symbol_id='508018.SH')
        assert sd.symbol_id == '508018.SSE'
        assert sd.instrument_type == SymbolType.FUND

        sd = cls.guess_symbol_detail(original_symbol_id='204001.SH')
        assert sd.symbol_id == '204001.SSE'
        assert sd.instrument_type == SymbolType.BOND

        sd = cls.guess_symbol_detail(original_symbol_id='110059.SH')
        assert sd.symbol_id == '110059.SSE'
        assert sd.instrument_type == SymbolType.BOND

        sd = cls.guess_symbol_detail(original_symbol_id='000001.SH')
        assert sd.symbol_id == '000001.SSE'
        assert sd.instrument_type == SymbolType.INDEX

        # 深交所
        sd = cls.guess_symbol_detail(original_symbol_id='000001.SZ')
        assert sd.symbol_id == '000001.SZSE'
        assert sd.instrument_type == SymbolType.STOCK

        sd = cls.guess_symbol_detail(original_symbol_id='300282.SZ')
        assert sd.symbol_id == '300282.SZSE'
        assert sd.instrument_type == SymbolType.STOCK

        sd = cls.guess_symbol_detail(original_symbol_id='002746.SZ')
        assert sd.symbol_id == '002746.SZSE'
        assert sd.instrument_type == SymbolType.STOCK

        sd = cls.guess_symbol_detail(original_symbol_id='200029.SZ')
        assert sd.symbol_id == '200029.SZSE'
        assert sd.instrument_type == SymbolType.STOCK

        sd = cls.guess_symbol_detail(original_symbol_id='90002795.SZO')
        assert sd.symbol_id == '90002795.SZSE'
        assert sd.instrument_type == SymbolType.OPTIONS

        sd = cls.guess_symbol_detail(original_symbol_id='90002796.SZ')
        assert sd.symbol_id == '90002796.SZSE'
        assert sd.instrument_type == SymbolType.OPTIONS

        sd = cls.guess_symbol_detail(original_symbol_id='159919.SZ')
        assert sd.symbol_id == '159919.SZSE'
        assert sd.instrument_type == SymbolType.FUND

        sd = cls.guess_symbol_detail(original_symbol_id='180301.SZ')
        assert sd.symbol_id == '180301.SZSE'
        assert sd.instrument_type == SymbolType.FUND

        sd = cls.guess_symbol_detail(original_symbol_id='131810.SZ')
        assert sd.symbol_id == '131810.SZSE'
        assert sd.instrument_type == SymbolType.BOND

        sd = cls.guess_symbol_detail(original_symbol_id='123008.SZ')
        assert sd.symbol_id == '123008.SZSE'
        assert sd.instrument_type == SymbolType.BOND

        sd = cls.guess_symbol_detail(original_symbol_id='399001.SZ')
        assert sd.symbol_id == '399001.SZSE'
        assert sd.instrument_type == SymbolType.INDEX

        # 北交所
        sd = cls.guess_symbol_detail(original_symbol_id='873122.BJ')
        assert sd.symbol_id == '873122.BSE'
        assert sd.instrument_type == SymbolType.STOCK

        sd = cls.guess_symbol_detail(original_symbol_id='430510.BJE')
        assert sd.symbol_id == '430510.BSE'
        assert sd.instrument_type == SymbolType.STOCK

        # 上期所
        sd = cls.guess_symbol_detail(original_symbol_id='fu2405.SF')
        assert sd.symbol_id == 'fu2405.SHFE'
        assert sd.instrument_type == SymbolType.FUTURES

        sd = cls.guess_symbol_detail(original_symbol_id='SC2406-C-520.SF')
        assert sd.symbol_id == 'sc2406C520.SHFE'
        assert sd.instrument_type == SymbolType.OPTIONS

        # 能源所
        sd = cls.guess_symbol_detail(original_symbol_id='BC2407.INE')
        assert sd.symbol_id == 'bc2407.INE'
        assert sd.instrument_type == SymbolType.FUTURES

        sd = cls.guess_symbol_detail(original_symbol_id='SC2406-C-570.INE')
        assert sd.symbol_id == 'sc2406C570.INE'
        assert sd.instrument_type == SymbolType.OPTIONS

        # 大商所
        sd = cls.guess_symbol_detail(original_symbol_id='A2405.DF')
        assert sd.symbol_id == 'a2405.DCE'
        assert sd.instrument_type == SymbolType.FUTURES

        sd = cls.guess_symbol_detail(original_symbol_id='A2407C4050.DCE')
        assert sd.symbol_id == 'a2407-C-4050.DCE'
        assert sd.instrument_type == SymbolType.OPTIONS

        # 郑商所
        sd = cls.guess_symbol_detail(original_symbol_id='Oi409.ZF')
        assert sd.symbol_id == 'OI409.CZCE'
        assert sd.instrument_type == SymbolType.FUTURES

        sd = cls.guess_symbol_detail(original_symbol_id='ap411-c-8900.CZCE')
        assert sd.symbol_id == 'AP411C8900.CZCE'
        assert sd.instrument_type == SymbolType.OPTIONS

        # 广期所
        sd = cls.guess_symbol_detail(original_symbol_id='si2410.GF')
        assert sd.symbol_id == 'si2410.GFEX'
        assert sd.instrument_type == SymbolType.FUTURES

        sd = cls.guess_symbol_detail(original_symbol_id='si2406P10600.GFEX')
        assert sd.symbol_id == 'si2406-P-10600.GFEX'
        assert sd.instrument_type == SymbolType.OPTIONS

        # 中金所
        sd = cls.guess_symbol_detail(original_symbol_id='t2406.IF')
        assert sd.symbol_id == 'T2406.CFFEX'
        assert sd.instrument_type == SymbolType.FUTURES

        sd = cls.guess_symbol_detail(original_symbol_id='HO2406C3000.CCFX')
        assert sd.symbol_id == 'HO2406-C-3000.CFFEX'
        assert sd.instrument_type == SymbolType.OPTIONS

        # 主连
        sd = cls.guess_symbol_detail(original_symbol_id='t00.IF')
        assert sd.symbol_id == 'T9999.CFFEX'
        assert sd.instrument_type == SymbolType.FUTURES

        sd = cls.guess_symbol_detail(original_symbol_id='t9999.IF')
        assert sd.symbol_id == 'T9999.CFFEX'
        assert sd.instrument_type == SymbolType.FUTURES

        # 指数
        sd = cls.guess_symbol_detail(original_symbol_id='tJQ00.IF')
        assert sd.symbol_id == 'T8888.CFFEX'
        assert sd.instrument_type == SymbolType.FUTURES

        sd = cls.guess_symbol_detail(original_symbol_id='t8888.IF')
        assert sd.symbol_id == 'T8888.CFFEX'
        assert sd.instrument_type == SymbolType.FUTURES

        # 港股
        sd = cls.guess_symbol_detail(original_symbol_id='HK.00700')
        assert sd.symbol_id == '00700.HKEX'
        assert sd.instrument_type == SymbolType.STOCK

        sd = cls.guess_symbol_detail(original_symbol_id='HK.29951')
        assert sd.symbol_id == '29951.HKEX'
        assert sd.instrument_type == SymbolType.WARRANTS

        sd = cls.guess_symbol_detail(original_symbol_id='HK.69994')
        assert sd.symbol_id == '69994.HKEX'
        assert sd.instrument_type == SymbolType.OPTIONS

        sd = cls.guess_symbol_detail(original_symbol_id='00700.HGT')
        assert sd.symbol_id == '00700.HKEX'
        assert sd.instrument_type == SymbolType.STOCK

        sd = cls.guess_symbol_detail(original_symbol_id='00700.SGT')
        assert sd.symbol_id == '00700.HKEX'
        assert sd.instrument_type == SymbolType.STOCK

        #
        assert not cls.guess_symbol_detail(original_symbol_id='t01.IF')
        assert not cls.guess_symbol_detail(original_symbol_id='t012.IF')
        assert not cls.guess_symbol_detail(original_symbol_id='tjq01.IF')
        assert not cls.guess_symbol_detail(original_symbol_id='000700.SGT')

        #
        sd = cls.guess_symbol_detail(original_symbol_id='IPS cf001&Cy2001.ZF')
        assert sd.symbol_id == 'IPS CF001&CY001.CZCE'
        assert sd.instrument_type == SymbolType.COMBINATION

        sd = cls.guess_symbol_detail(original_symbol_id='sp A2311&a2401.DF')
        assert sd.symbol_id == 'SP a2311&a2401.DCE'
        assert sd.instrument_type == SymbolType.COMBINATION

        sd = cls.guess_symbol_detail(original_symbol_id='SpC A1403&m1403.DF')
        assert sd.symbol_id == 'SPC a1403&m1403.DCE'
        assert sd.instrument_type == SymbolType.COMBINATION

        sd = cls.guess_symbol_detail(original_symbol_id='spd   ap411&ap2504.ZF')
        assert sd.symbol_id == 'SPD AP411&AP504.CZCE'
        assert sd.instrument_type == SymbolType.COMBINATION

        sd = cls.guess_symbol_detail(original_symbol_id='sp fg2408&fg2409.CZCE')
        assert sd.symbol_id == 'SPD FG408&FG409.CZCE'
        assert sd.instrument_type == SymbolType.COMBINATION

        sd = cls.guess_symbol_detail(original_symbol_id='spc fg2408&sa2408.CZCE')
        assert sd.symbol_id == 'IPS FG408&SA408.CZCE'
        assert sd.instrument_type == SymbolType.COMBINATION

        sd = cls.guess_symbol_detail(original_symbol_id='sp sp2409&sp2410.DCE')
        assert sd.symbol_id == 'SP sp2409&sp2410.DCE'
        assert sd.instrument_type == SymbolType.COMBINATION

        sd = cls.guess_symbol_detail(original_symbol_id='SPC v2407&pp2407.DCE')
        assert sd.symbol_id == 'SPC v2407&pp2407.DCE'
        assert sd.instrument_type == SymbolType.COMBINATION

        sd = cls.guess_symbol_detail(original_symbol_id='sp si2409&si2410.GFEX')
        assert sd.symbol_id == 'SP si2409&si2410.GFEX'
        assert sd.instrument_type == SymbolType.COMBINATION

        sd = cls.guess_symbol_detail(original_symbol_id='SP SF1705&SM1705.CZCE')
        assert sd.symbol_id == 'IPS SF705&SM705.CZCE'
        assert sd.instrument_type == SymbolType.COMBINATION

        sd = cls.guess_symbol_detail(original_symbol_id='SR507MSC6400.CZCE')
        assert sd.symbol_id == 'SR507MSC6400.CZCE'
        assert sd.instrument_type == SymbolType.OPTIONS


if __name__ == '__main__':
    SymbolGuesser.test()
