# -*- coding: utf-8 -*-
"""国内交易所及部分国外交易所枚举"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Set
# https://www.iso20022.org/market-identifier-codes
# https://www.tradinghours.com/mic?country[]=CN&page=1#results


@dataclass(frozen=True)
class ExchangeDetail:
    acronym: str
    mic: str = ''
    extra_ids: List[str] = field(default_factory=list)   # 其他行情源的市场代码
    en_name: str = ''
    cn_name: str = ''
    website: str = ''

    @property
    def market_ids(self) -> Set[str]:
        extra_ids = {*self.extra_ids, self.acronym}
        if self.mic:
            extra_ids.add(self.mic)
        return extra_ids


class Exchange(Enum):
    """交易所简称枚举"""
    BSE = ExchangeDetail(acronym='BSE', mic='BJSE', extra_ids=['BJ', 'BJE', 'BJEX'], en_name='BEIJING STOCK EXCHANGE', cn_name='北京证券交易所', website='www.bse.cn')
    CFFEX = ExchangeDetail(acronym='CFFEX', mic='CCFX', extra_ids=['IF', 'CFX'], en_name='CHINA FINANCIAL FUTURES EXCHANGE', cn_name='中国金融期货交易所', website='www.cffex.com.cn')
    NEEQ = ExchangeDetail(acronym='NEEQ', mic='NEEQ', en_name='NATIONAL EQUITIES EXCHANGE AND QUOTATIONS', cn_name='全国中小企业股份转让系统', website='www.neeq.com.cn')
    SGE = ExchangeDetail(acronym='SGE', mic='SGEX', en_name='SHANGHAI GOLD EXCHANGE', cn_name='上海黄金交易所', website='www.sge.sh')
    CFETS = ExchangeDetail(acronym='CFETS', mic='XCFE', en_name='CHINA FOREIGN EXCHANGE TRADE SYSTEM', cn_name='中国外汇交易系统', website='www.chinamoney.com.cn')
    SSE = ExchangeDetail(acronym='SSE', mic='XSHG', extra_ids=['SH', 'SHO', 'SHOP'], en_name='SHANGHAI STOCK EXCHANGE', cn_name='上海证券交易所', website='www.szse.cn')
    SZSE = ExchangeDetail(acronym='SZSE', mic='XSHE', extra_ids=['SZ', 'SZO', 'SZOP'], en_name='SHENZHEN STOCK EXCHANGE', cn_name='深圳证券交易所', website='www.szse.cn')
    CSI = ExchangeDetail(acronym='CSI', mic='', en_name='CHINA SECURITIES INDEX', cn_name='中证指数', website='www.csindex.com.cn')
    SHFE = ExchangeDetail(acronym='SHFE', mic='XSGE', extra_ids=['SF', 'SHF'], en_name='SHANGHAI FUTURES EXCHANGE', cn_name='上海期货交易所', website='www.shfe.com.cn')
    INE = ExchangeDetail(acronym='INE', mic='XINE', en_name='SHANGHAI INTERNATIONAL ENERGY EXCHANGE', cn_name='上海国际能源交易中心', website='www.ine.cn')
    DCE = ExchangeDetail(acronym='DCE', mic='XDCE', extra_ids=['DF'], en_name='DALIAN COMMODITY EXCHANGE', cn_name='大连商品交易所', website='www.dce.com.cn')
    CZCE = ExchangeDetail(acronym='CZCE', mic='XZCE', extra_ids=['ZF', 'ZCE'], en_name='ZHENGZHOU COMMODITY EXCHANGE', cn_name='郑州商品交易所', website='www.czce.com.cn')
    GFEX = ExchangeDetail(acronym='GFEX', mic='', extra_ids=['GF', 'GFE'], en_name='GUANGZHOU COMMODITY EXCHANGE', cn_name='广州商品交易所', website='www.gfex.com.cn')
    CBOT = ExchangeDetail(acronym='CBOT', mic='CBTS', en_name='CME SWAPS MARKETS (CBOT)', cn_name='芝加哥期货交易所', website='www.cmegroup.com')
    COMEX = ExchangeDetail(acronym='COMEX', mic='CECS', en_name='CME SWAPS MARKETS (COMEX)', cn_name='纽约商品交易所', website='www.cmegroup.com')
    CME = ExchangeDetail(acronym='CME', mic='CMES', en_name='CME SWAPS MARKETS (CME)', cn_name='芝加哥商业交易所', website='www.cmegroup.com')
    NYMEX = ExchangeDetail(acronym='NYMEX', mic='NYMS', en_name='CME SWAPS MARKETS (NYMEX)', cn_name='纽约商品交易所', website='www.cmegroup.com')
    NYBOT = ExchangeDetail(acronym='NYBOT', mic='', en_name='THE NEW YORK BOARD OF TRADE', cn_name='纽约期货交易所', website='www.nybot.com')
    LME = ExchangeDetail(acronym='LME', mic='XLME', en_name='LONDON METAL EXCHANGE', cn_name='伦敦金属交易所', website='www.lme.co.uk')
    TOCOM = ExchangeDetail(acronym='TOCOM', mic='XTKT', en_name='TOKYO COMMODITY EXCHANGE', cn_name='东京商品交易所', website='www.tocom.or.jp')
    SICOM = ExchangeDetail(acronym='SICOM', mic='XSCE', en_name='SINGAPORE COMMODITY EXCHANGE', cn_name='新加坡商品交易所', website='www.sgx.com')
    HKEX = ExchangeDetail(acronym='HKEX', mic='XHKG', extra_ids=['HK', 'HGT', 'SGT'], en_name='HONG KONG EXCHANGES AND CLEARING LTD', cn_name='香港交易及结算所', website='www.hkex.com.hk')
    NASDAQ = ExchangeDetail(acronym='NASDAQ', mic='XNAS', en_name='NASDAQ - ALL MARKETS', cn_name='纳斯达克股票电子交易市场', website='www.nasdaq.com')
    NYSE = ExchangeDetail(acronym='NYSE', mic='XNYS', en_name='NEW YORK STOCK EXCHANGE, INC.', cn_name='纽约证券交易所', website='www.nyse.com')
    AMEX = ExchangeDetail(acronym='AMEX', mic='XASE', en_name='NYSE MKT LLC', cn_name='美国证券交易所', website='www.nyse.com')
    LSE = ExchangeDetail(acronym='LSE', mic='XLON', en_name='LONDON STOCK EXCHANGE', cn_name='伦敦证券交易所', website='www.lodonstockexchange.com')
    SIX = ExchangeDetail(acronym='SIX', mic='XSWX', en_name='SIX SWISS EXCHANGE', cn_name='瑞士证券交易所', website='www.six-group.com')
    ICE = ExchangeDetail(acronym='ICE', mic='', en_name='INTERCONTINENTAL EXCHANGE', cn_name='洲际交易所', website='www.theice.com')
    BMD = ExchangeDetail(acronym='BMD', mic='XKLS', en_name='BURSA MALAYSIA DERIVATIVES', cn_name='马来西亚衍生品交易所', website='www.bursamalaysia.com')
    SGX = ExchangeDetail(acronym='SGX', mic='XSES', en_name='SINGAPORE EXCHANGE', cn_name='新加坡交易所', website='www.sgx.com')

    @classmethod
    def find(cls, market_id: str) -> ExchangeDetail | None:
        """通过交易市场代码匹配返回交易所枚举"""
        return ExchangeMap.get(market_id)


ExchangeMap: Dict[str, Exchange] = {}

# 数据完整性和一致性检验
for e in Exchange:
    assert e.value.acronym == e.name
    for m in e.value.market_ids:
        ExchangeMap[m] = e
