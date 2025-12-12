# -*- coding: utf-8 -*-
import datetime
import functools
import statistics
from collections import OrderedDict
from typing import List, Tuple, Dict


class NavIndexes:
    """基金净值指标"""

    def __init__(self, values: Dict[datetime.date, float], r: float):
        """
        :param values: 每日复权净值序列
        :param r: 无风险利率
        """
        self.r: float = r
        assert len(values) >= 2
        self.start_date: datetime.date = min(values)
        self.end_date: datetime.date = max(values)
        # 检查完整性
        self.values: OrderedDict[datetime.date, float] = OrderedDict()
        for date, value in sorted(values.items()):
            assert isinstance(value, (int, float))
            self.values[date] = value
            assert value > 0
        start_year = datetime.date(year=self.start_date.year, month=1, day=1)
        end_year = datetime.date(year=self.end_date.year, month=12, day=31)
        # 平均每年天数,介于365与366之间
        self.annualized_days: float = (end_year - start_year).days / (
            self.end_date.year - self.start_date.year + 1
        )
        # 每年交易日天数,即每年有净值的天数,通常在250天左右
        self.annualized_trade_days: float = (
            (len(values) - 1)
            / (self.end_date - self.start_date).days
            * self.annualized_days
        )

    def calculate_indexs(self):
        """综合指标计算"""
        mdd, mdd_peak_date, mdd_date, mdd_recover_date = (
            self.max_draw_down
        )  # 累计收益率
        return {
            "mdd": mdd,  # 最大回撤比
            "mdd_peak_date": mdd_peak_date,  # 最大回撤起始日期
            "mdd_date": mdd_date,  # 最大回撤终止日期
            "mdd_recover_date": mdd_recover_date,  # 最大回撤修复日期
            "accumulated_return": self.accumulated_return,  # 累计收益率
            "annualized_return": self.annualized_return,  # 年化收益率
            "calmar_ratio": self.calmar_ratio,  # 卡玛比率
            "sharpe_ratio": self.sharpe_ratio,  # 夏普比率
            "sortino_ratio": self.sortino_ratio,  # 索提诺比率
            "average_daily_return": self.average_daily_return,  # 日均收益均值
            "stdev": self.stdev,  # 标准差
            "annualized_stdev": self.annualized_stdev,  # 年化标准差
            "downside_stdev": self.downside_stdev,  # 下行标准差
        }

    @property
    @functools.lru_cache()
    def max_draw_down(
        self,
    ) -> Tuple[float, datetime.date, datetime.date, datetime.date]:
        """
        计算最大回撤及修复时间
        :rtype: 最大回撤比, 最大回撤起始日期, 最大回撤终止日期, 最大回撤修复日期
        """
        mdd_date: datetime.date = self.start_date
        mdd: float = 0.0
        mdd_peak_date: datetime.date = self.start_date
        scan_peak_date: datetime.date = self.start_date
        scan_peak: float = 0.0
        mdd_high_spot: float = 0.0
        scan_minimum: float = 0.0
        mdd_recover_date: datetime.date = self.start_date
        for date, value in self.values.items():
            if value >= scan_peak:
                scan_peak = value
                scan_minimum = value
                scan_peak_date = date

            elif value < scan_minimum:
                scan_minimum = value
                last_minimum_date = date
                dd = (scan_peak - scan_minimum) / scan_peak
                if dd > mdd:
                    mdd = dd
                    mdd_high_spot = scan_peak
                    mdd_peak_date = scan_peak_date
                    mdd_date = last_minimum_date
                    mdd_recover_date = self.start_date
            if value >= mdd_high_spot and mdd_recover_date == self.start_date:
                mdd_recover_date = date
        return mdd, mdd_peak_date, mdd_date, mdd_recover_date

    @property
    @functools.lru_cache()
    def accumulated_return(self) -> float:
        """累计收益率"""
        v1: float = self.values[self.start_date]
        v2: float = self.values[self.end_date]
        return v2 / v1 - 1

    @property
    @functools.lru_cache()
    def annualized_return(self) -> float:
        """年化收益率"""
        days = (self.end_date - self.start_date).days
        if days == 0:
            return 0.0
        return self.accumulated_return / days * self.annualized_days

    @property
    @functools.lru_cache()
    def calmar_ratio(self) -> float:
        """卡玛比率"""
        if self.max_draw_down[0] == 0.0:
            return 0.0
        return self.annualized_return / self.max_draw_down[0]

    @property
    @functools.lru_cache()
    def sharpe_ratio(self):
        """夏普比率"""
        if self.annualized_stdev == 0.0:
            return 0.0
        return (self.annualized_return - self.r) / self.annualized_stdev

    @property
    @functools.lru_cache()
    def sortino_ratio(self) -> float:
        """索提诺比率"""
        if self.downside_stdev == 0.0:
            return 0.0
        return (self.annualized_return - self.r) / self.downside_stdev

    @property
    @functools.lru_cache()
    def daily_return(self) -> OrderedDict[datetime.date, float]:
        """日均收益"""
        dr: OrderedDict[datetime.date, float] = OrderedDict()
        last_value: float = self.values[self.start_date]
        for i, (date, value) in enumerate(self.values.items()):
            if i == 0:
                dr[date] = 0.0
            else:
                dr[date] = 1 - last_value / value
                last_value = value
        return dr

    @property
    @functools.lru_cache()
    def average_daily_return(self) -> float:
        """日均收益均值"""
        return statistics.mean(self.daily_return.values())

    @property
    @functools.lru_cache()
    def stdev(self) -> float:
        """标准差"""
        stdev: float = statistics.stdev(self.daily_return.values())
        assert stdev >= 0, "stdev should be greater than or equal to 0"
        return statistics.stdev(self.daily_return.values())

    @property
    @functools.lru_cache()
    def annualized_stdev(self) -> float:
        """年化标准差"""
        annualized_stdev: float = self.stdev * self.annualized_trade_days
        assert (
            annualized_stdev >= 0
        ), "annualized_stdev should be greater than or equal to 0"
        return annualized_stdev

    @property
    @functools.lru_cache()
    def downside_stdev(self) -> float:
        """下行标准差"""
        values: List[float] = [
            value * self.annualized_days
            for value in self.daily_return.values()
            if value < self.r
        ]
        if len(values) >= 2:
            return statistics.stdev(values)
        else:
            return 0.0
