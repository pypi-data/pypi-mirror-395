# -*- coding: utf-8 -*-
"""国内银行枚举"""
from collections import namedtuple
from enum import auto, Enum
from typing import List, Dict
from .base import ByKey

# https://www.swift.com/

field_names: List[str] = ["swift_code", "cn_name"]
BankDetail = namedtuple(typename="BankDetail", field_names=field_names)
tsv: str = """
BKCHCNBJ\t中国银行
ABOCCNBJ\t农业银行
PCBCCNBJ\t建设银行
COMMCNSH\t交通银行
CHBHCNBT\t渤海银行
CIBKCNBJ\t中信银行
CMBCCNBS\t招商银行
EVERCNBJ\t光大银行
MSBCCNBJ\t民生银行
HXBKCNBJ\t华夏银行
GDBKCN22\t广发银行
FJIBCNBA\t兴业银行
SPDBCNSH\t上海浦东发展银行
SDBCCNBJ\t国家开发银行
SZDBCNBS\t平安银行
HFBACNSD\t恒丰银行
HSBCCNSH\t汇丰银行（中国）有限公司
BEASCNSH\t东亚银行（中国）有限公司
SCBLCNSX\t渣打银行（中国）有限公司
HZCBCN2H\t杭州银行
HCCBCNBH\t哈尔滨银行
HASECNSH\t恒生银行
BJCNCNBJ\t北京银行
BKNBCN2N\t宁波银行
JZCBCNBJ\t锦州银行
CITICNSX\t花旗银行（中国）有限公司
DBSSCNSH\t星展银行（中国）有限公司
BKSHCNBJ\t河北银行
IBXHCNBA\t厦门国际银行
CBXMCNBA\t厦门银行
ZBBKCNBZ\t齐商银行
HSSYCNBH\t内蒙古银行
BOSHCNSH\t上海银行
WZCBCNSH\t温州银行
BOTKCNSH\t三菱东京日联银行（中国）有限公司
RZCBCNBD\t日照银行
BTCBCNBJ\t包头银行
IBKOCNBT\t韩国兴业银行（中国）有限公司
MHCBCNSH\t瑞穗银行（中国）有限公司
DEUTCNSH\t德意志银行（中国）有限公司
LWCBCNBJ\t莱商银行
ANZBCNSH\t澳大利亚及新西兰银行（中国）有限公司
SHBKCNBJ\t新韩银行（中国）有限公司
CZNBCNBJ\t国民银行（中国）有限公司
BKKBCNSH\t曼谷银行（中国）有限公司
CCBCCNBK\t长华商业银行
CKLBCNBJ\t昆仑银行
DYSHCNBJ\t东营银行
CIYUCNBA\t赤渝银行
FSBCCNSH\t富邦银行（中国）有限公司
ICBCCNBS\t大型国际商业银行
WPACCNSX\t西太平洋银行
QCCBCNBQ\t青岛银行
DECLCNBJ\t德州银行
FCBKCNSH\t第一商业银行
DSBACNBX\t大新银行（中国）有限公司
MSBKCN22\t摩根士丹利国际银行(中国)有限公司
TACBCNBS\t台湾合作银行
PSBCCNBJ\t中国邮政储蓄银行
BINHCN2N\t宁波商业银行
CHASCNBJ\t摩根大通银行（中国）有限公司
LCHBCN22\t创兴银行
UWCBCNSH\t国泰联合银行（中国）有限公司
YCCBCNBY\t宁夏银行
OUBKCNB1\t海外联合银行
LYCBCNBL\t临商银行
BOJJCNBJ\t九江银行
CHCCCNSS\t长沙银行
BOJSCNBN\t江苏银行
HNBKCNBS\t华南商业银行
KCCBCN2K\t富滇银行
SCBKCNBS\t上海商业银行
CRLYCNSH\t法国农业信贷银行（中国）有限公司
WFCBCNBN\t潍坊银行
RZBACNBJ\t瑞丰国际银行
UOVBCNSH\t联合海外银行（中国）有限公司
SBINCNSH\t印度国家银行
NJCBCNBN\t南京银行
BOFMCNBJ\t蒙特利尔银行（中国）有限公司
DLCBCNBD\t大连银行
BNPACNSH\t法国巴黎银行（中国）有限公司
SYCBCNBY\t盛京银行
TCCBCNBT\t天津银行
HRXJCNBC\t华容银行
MBTCCNBN\t大都会银行（中国）有限公司
RBOSCNS1\t苏格兰皇家银行
APGTCN21\t亚太银行
CTGBCN22\t重庆三峡银行
CCIBCNB1\t中国信贷产业银行
BOFMCNSH\t蒙特利尔银行（中国）有限公司
GDPBCN22\t广东南岳银行
SSVBCNSH\t浦发硅谷银行
ZCCBCN22\t珠海华润银行
WHCBCNBN\t汉口银行
WHBKCNBJ\t威海市商业银行
HVBKCNBJ\t友利银行（中国）有限公司
HFCBCNSH\t徽商银行
FXBKCNBJ\t阜新银行
TZBKCNBT\t泰州银行
YZBKCN2N\t鄞州银行
KWHKCNBS\t中信银行国际（中国）有限公司
SWEDCNSH\t瑞典银行
FZCBCNBS\t福建海下银行
BKJNCNBJ\t济宁银行
CQCBCN22\t重庆银行
COXICNBA\t联合商业银行
DEUTCNBJ\t德意志银行（中国）有限公司
YTCBCNSD\t烟台银行
ZJMTCNSH\t浙江民泰商业银行
NXBKCNBH\t南浔银行
EWBKCNSH\t华美银行（中国）有限公司
JHCBCNBJ\t金华银行
BOFMCN22\t蒙特利尔银行（中国）有限公司
LCOMCNBJ\t辽阳银行
GDHBCN22\t广东华兴银行
KRTHCNB1\t泰国国立银行
COBACNSX\t德国商业银行
YKCBCNBJ\t营口银行
SCBLCNB1\t渣打银行
SMBCCNSH\t三井住友银行（中国）有限公司
ZJCBCN2N\t浙商银行
CTBACNSH\t澳大利亚联邦银行
KREDCNSX\t比利时联合银行
LJBCCNBH\t龙江银行
BKQZCNBZ\t泉州银行
CBOCCNBC\t成都银行
CNMBCNBS\t中国商业银行
BSHLCNS1\t巴林银行
PASCCNSH\t锡耶纳蒙特银行
KWPBCNB1\t广东省银行
GZCBCN22\t广州银行
LSCCCNBL\t乐山市商业银行
GYCBCNSI\t贵阳银行
"""
BankDetails: List[BankDetail] = [BankDetail(*line.strip().split("\t")) for line in tsv.splitlines() if line]


class BySwiftCode(ByKey):
    map: Dict[str, BankDetail] = {getattr(item, field_names[0]): item for item in BankDetails}


class Bank(Enum):
    BKCHCNBJ = BySwiftCode.map['BKCHCNBJ']
    ABOCCNBJ = BySwiftCode.map['ABOCCNBJ']
    PCBCCNBJ = BySwiftCode.map['PCBCCNBJ']
    COMMCNSH = BySwiftCode.map['COMMCNSH']
    CHBHCNBT = BySwiftCode.map['CHBHCNBT']
    CIBKCNBJ = BySwiftCode.map['CIBKCNBJ']
    CMBCCNBS = BySwiftCode.map['CMBCCNBS']
    EVERCNBJ = BySwiftCode.map['EVERCNBJ']
    MSBCCNBJ = BySwiftCode.map['MSBCCNBJ']
    HXBKCNBJ = BySwiftCode.map['HXBKCNBJ']
    GDBKCN22 = BySwiftCode.map['GDBKCN22']
    FJIBCNBA = BySwiftCode.map['FJIBCNBA']
    SPDBCNSH = BySwiftCode.map['SPDBCNSH']
    SDBCCNBJ = BySwiftCode.map['SDBCCNBJ']
    SZDBCNBS = BySwiftCode.map['SZDBCNBS']
    HFBACNSD = BySwiftCode.map['HFBACNSD']
    HSBCCNSH = BySwiftCode.map['HSBCCNSH']
    BEASCNSH = BySwiftCode.map['BEASCNSH']
    SCBLCNSX = BySwiftCode.map['SCBLCNSX']
    HZCBCN2H = BySwiftCode.map['HZCBCN2H']
    HCCBCNBH = BySwiftCode.map['HCCBCNBH']
    HASECNSH = BySwiftCode.map['HASECNSH']
    BJCNCNBJ = BySwiftCode.map['BJCNCNBJ']
    BKNBCN2N = BySwiftCode.map['BKNBCN2N']
    JZCBCNBJ = BySwiftCode.map['JZCBCNBJ']
    CITICNSX = BySwiftCode.map['CITICNSX']
    DBSSCNSH = BySwiftCode.map['DBSSCNSH']
    BKSHCNBJ = BySwiftCode.map['BKSHCNBJ']
    IBXHCNBA = BySwiftCode.map['IBXHCNBA']
    CBXMCNBA = BySwiftCode.map['CBXMCNBA']
    ZBBKCNBZ = BySwiftCode.map['ZBBKCNBZ']
    HSSYCNBH = BySwiftCode.map['HSSYCNBH']
    BOSHCNSH = BySwiftCode.map['BOSHCNSH']
    WZCBCNSH = BySwiftCode.map['WZCBCNSH']
    BOTKCNSH = BySwiftCode.map['BOTKCNSH']
    RZCBCNBD = BySwiftCode.map['RZCBCNBD']
    BTCBCNBJ = BySwiftCode.map['BTCBCNBJ']
    IBKOCNBT = BySwiftCode.map['IBKOCNBT']
    MHCBCNSH = BySwiftCode.map['MHCBCNSH']
    DEUTCNSH = BySwiftCode.map['DEUTCNSH']
    LWCBCNBJ = BySwiftCode.map['LWCBCNBJ']
    ANZBCNSH = BySwiftCode.map['ANZBCNSH']
    SHBKCNBJ = BySwiftCode.map['SHBKCNBJ']
    CZNBCNBJ = BySwiftCode.map['CZNBCNBJ']
    BKKBCNSH = BySwiftCode.map['BKKBCNSH']
    CCBCCNBK = BySwiftCode.map['CCBCCNBK']
    CKLBCNBJ = BySwiftCode.map['CKLBCNBJ']
    DYSHCNBJ = BySwiftCode.map['DYSHCNBJ']
    CIYUCNBA = BySwiftCode.map['CIYUCNBA']
    FSBCCNSH = BySwiftCode.map['FSBCCNSH']
    ICBCCNBS = BySwiftCode.map['ICBCCNBS']
    WPACCNSX = BySwiftCode.map['WPACCNSX']
    QCCBCNBQ = BySwiftCode.map['QCCBCNBQ']
    DECLCNBJ = BySwiftCode.map['DECLCNBJ']
    FCBKCNSH = BySwiftCode.map['FCBKCNSH']
    DSBACNBX = BySwiftCode.map['DSBACNBX']
    MSBKCN22 = BySwiftCode.map['MSBKCN22']
    TACBCNBS = BySwiftCode.map['TACBCNBS']
    PSBCCNBJ = BySwiftCode.map['PSBCCNBJ']
    BINHCN2N = BySwiftCode.map['BINHCN2N']
    CHASCNBJ = BySwiftCode.map['CHASCNBJ']
    LCHBCN22 = BySwiftCode.map['LCHBCN22']
    UWCBCNSH = BySwiftCode.map['UWCBCNSH']
    YCCBCNBY = BySwiftCode.map['YCCBCNBY']
    OUBKCNB1 = BySwiftCode.map['OUBKCNB1']
    LYCBCNBL = BySwiftCode.map['LYCBCNBL']
    BOJJCNBJ = BySwiftCode.map['BOJJCNBJ']
    CHCCCNSS = BySwiftCode.map['CHCCCNSS']
    BOJSCNBN = BySwiftCode.map['BOJSCNBN']
    HNBKCNBS = BySwiftCode.map['HNBKCNBS']
    KCCBCN2K = BySwiftCode.map['KCCBCN2K']
    SCBKCNBS = BySwiftCode.map['SCBKCNBS']
    CRLYCNSH = BySwiftCode.map['CRLYCNSH']
    WFCBCNBN = BySwiftCode.map['WFCBCNBN']
    RZBACNBJ = BySwiftCode.map['RZBACNBJ']
    UOVBCNSH = BySwiftCode.map['UOVBCNSH']
    SBINCNSH = BySwiftCode.map['SBINCNSH']
    NJCBCNBN = BySwiftCode.map['NJCBCNBN']
    BOFMCNBJ = BySwiftCode.map['BOFMCNBJ']
    DLCBCNBD = BySwiftCode.map['DLCBCNBD']
    BNPACNSH = BySwiftCode.map['BNPACNSH']
    SYCBCNBY = BySwiftCode.map['SYCBCNBY']
    TCCBCNBT = BySwiftCode.map['TCCBCNBT']
    HRXJCNBC = BySwiftCode.map['HRXJCNBC']
    MBTCCNBN = BySwiftCode.map['MBTCCNBN']
    RBOSCNS1 = BySwiftCode.map['RBOSCNS1']
    APGTCN21 = BySwiftCode.map['APGTCN21']
    CTGBCN22 = BySwiftCode.map['CTGBCN22']
    CCIBCNB1 = BySwiftCode.map['CCIBCNB1']
    BOFMCNSH = BySwiftCode.map['BOFMCNSH']
    GDPBCN22 = BySwiftCode.map['GDPBCN22']
    SSVBCNSH = BySwiftCode.map['SSVBCNSH']
    ZCCBCN22 = BySwiftCode.map['ZCCBCN22']
    WHCBCNBN = BySwiftCode.map['WHCBCNBN']
    WHBKCNBJ = BySwiftCode.map['WHBKCNBJ']
    HVBKCNBJ = BySwiftCode.map['HVBKCNBJ']
    HFCBCNSH = BySwiftCode.map['HFCBCNSH']
    FXBKCNBJ = BySwiftCode.map['FXBKCNBJ']
    TZBKCNBT = BySwiftCode.map['TZBKCNBT']
    YZBKCN2N = BySwiftCode.map['YZBKCN2N']
    KWHKCNBS = BySwiftCode.map['KWHKCNBS']
    SWEDCNSH = BySwiftCode.map['SWEDCNSH']
    FZCBCNBS = BySwiftCode.map['FZCBCNBS']
    BKJNCNBJ = BySwiftCode.map['BKJNCNBJ']
    CQCBCN22 = BySwiftCode.map['CQCBCN22']
    COXICNBA = BySwiftCode.map['COXICNBA']
    DEUTCNBJ = BySwiftCode.map['DEUTCNBJ']
    YTCBCNSD = BySwiftCode.map['YTCBCNSD']
    ZJMTCNSH = BySwiftCode.map['ZJMTCNSH']
    NXBKCNBH = BySwiftCode.map['NXBKCNBH']
    EWBKCNSH = BySwiftCode.map['EWBKCNSH']
    JHCBCNBJ = BySwiftCode.map['JHCBCNBJ']
    BOFMCN22 = BySwiftCode.map['BOFMCN22']
    LCOMCNBJ = BySwiftCode.map['LCOMCNBJ']
    GDHBCN22 = BySwiftCode.map['GDHBCN22']
    KRTHCNB1 = BySwiftCode.map['KRTHCNB1']
    COBACNSX = BySwiftCode.map['COBACNSX']
    YKCBCNBJ = BySwiftCode.map['YKCBCNBJ']
    SCBLCNB1 = BySwiftCode.map['SCBLCNB1']
    SMBCCNSH = BySwiftCode.map['SMBCCNSH']
    ZJCBCN2N = BySwiftCode.map['ZJCBCN2N']
    CTBACNSH = BySwiftCode.map['CTBACNSH']
    KREDCNSX = BySwiftCode.map['KREDCNSX']
    LJBCCNBH = BySwiftCode.map['LJBCCNBH']
    BKQZCNBZ = BySwiftCode.map['BKQZCNBZ']
    CBOCCNBC = BySwiftCode.map['CBOCCNBC']
    CNMBCNBS = BySwiftCode.map['CNMBCNBS']
    BSHLCNS1 = BySwiftCode.map['BSHLCNS1']
    PASCCNSH = BySwiftCode.map['PASCCNSH']
    KWPBCNB1 = BySwiftCode.map['KWPBCNB1']
    GZCBCN22 = BySwiftCode.map['GZCBCN22']
    LSCCCNBL = BySwiftCode.map['LSCCCNBL']
    GYCBCNSI = BySwiftCode.map['GYCBCNSI']


# 数据完整性和一致性检验
BySwiftCode.check(obj=Bank)
