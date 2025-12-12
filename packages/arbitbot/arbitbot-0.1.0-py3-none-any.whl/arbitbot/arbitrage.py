"""
套利檢測和計算模組
"""

import logging
from typing import Dict, List, Optional, Tuple
from .fetcher import PriceFetcher
from .utils import calculate_profit_percentage

logger = logging.getLogger(__name__)


class Opportunity:
    """套利機會"""

    def __init__(self, symbol: str, buy_exchange: str, sell_exchange: str,
                 buy_price: float, sell_price: float, profit_percentage: float):
        self.symbol = symbol
        self.buy_exchange = buy_exchange
        self.sell_exchange = sell_exchange
        self.buy_price = buy_price
        self.sell_price = sell_price
        self.profit_percentage = profit_percentage

    def __str__(self):
        return (f"{self.symbol} | "
                f"買:{self.buy_exchange}@{self.buy_price:.2f} -> "
                f"賣:{self.sell_exchange}@{self.sell_price:.2f} | "
                f"利潤:{self.profit_percentage:.2f}%")

    def to_dict(self):
        return {
            'symbol': self.symbol,
            'buy_exchange': self.buy_exchange,
            'sell_exchange': self.sell_exchange,
            'buy_price': self.buy_price,
            'sell_price': self.sell_price,
            'profit_percentage': self.profit_percentage,
        }


class ArbitrageBot:
    """套利機器人"""

    def __init__(self, exchanges: List[str], profit_threshold: float = 0.5):
        """
        初始化套利機器人
        
        Args:
            exchanges: 交易所名稱列表
            profit_threshold: 利潤閾值 (百分比)
        """
        self.fetcher = PriceFetcher(exchanges)
        self.profit_threshold = profit_threshold
        self.opportunities = []

    def find_opportunities(self, symbols: List[str]) -> List[Opportunity]:
        """
        尋找套利機會
        
        Args:
            symbols: 交易對列表
            
        Returns:
            Opportunity 對象列表
        """
        self.opportunities = []
        prices = self.fetcher.get_prices_batch(symbols)

        for symbol, exchange_prices in prices.items():
            if len(exchange_prices) < 2:
                logger.warning(f"⚠ {symbol} 數據不足，跳過")
                continue

            opportunities = self._find_opportunities_for_symbol(symbol, exchange_prices)
            self.opportunities.extend(opportunities)

        return self.opportunities

    def _find_opportunities_for_symbol(self, symbol: str, exchange_prices: Dict) -> List[Opportunity]:
        """查找單個交易對的套利機會"""
        opportunities = []
        exchanges = list(exchange_prices.keys())

        for i, buy_ex in enumerate(exchanges):
            for sell_ex in exchanges[i + 1:]:
                # 場景1: 在 buy_ex 買入，在 sell_ex 賣出
                opp1 = self._calculate_opportunity(
                    symbol, buy_ex, sell_ex,
                    exchange_prices[buy_ex], exchange_prices[sell_ex]
                )
                if opp1:
                    opportunities.append(opp1)

                # 場景2: 在 sell_ex 買入，在 buy_ex 賣出
                opp2 = self._calculate_opportunity(
                    symbol, sell_ex, buy_ex,
                    exchange_prices[sell_ex], exchange_prices[buy_ex]
                )
                if opp2:
                    opportunities.append(opp2)

        return opportunities

    def _calculate_opportunity(self, symbol: str, buy_ex: str, sell_ex: str,
                               buy_data: Dict, sell_data: Dict) -> Optional[Opportunity]:
        """計算單一套利機會"""
        buy_price = buy_data.get('ask')  # 買入價用 ask
        sell_price = sell_data.get('bid')  # 賣出價用 bid

        if not buy_price or not sell_price:
            return None

        profit_percentage = calculate_profit_percentage(buy_price, sell_price)

        if profit_percentage >= self.profit_threshold:
            return Opportunity(
                symbol=symbol,
                buy_exchange=buy_ex,
                sell_exchange=sell_ex,
                buy_price=buy_price,
                sell_price=sell_price,
                profit_percentage=profit_percentage
            )

        return None

    def get_best_opportunities(self, limit: int = 5) -> List[Opportunity]:
        """獲取最優的套利機會"""
        sorted_opps = sorted(self.opportunities,
                            key=lambda x: x.profit_percentage, reverse=True)
        return sorted_opps[:limit]
