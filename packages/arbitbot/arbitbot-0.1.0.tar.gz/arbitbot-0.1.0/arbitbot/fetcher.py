"""
CCXT 價格獲取模組
"""

import ccxt
import logging
from typing import Dict, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class PriceFetcher:
    """使用 CCXT 獲取交易所價格"""

    def __init__(self, exchange_names: List[str]):
        """
        初始化 PriceFetcher
        
        Args:
            exchange_names: 交易所名稱列表 (如 ['binance', 'bybit'])
        """
        self.exchanges = {}
        for name in exchange_names:
            try:
                exchange_class = getattr(ccxt, name)
                self.exchanges[name] = exchange_class()
                logger.info(f"✓ 成功連接交易所: {name}")
            except AttributeError:
                logger.error(f"✗ 交易所不存在: {name}")
            except Exception as e:
                logger.error(f"✗ 連接交易所 {name} 失敗: {e}")

    def get_price(self, exchange_name: str, symbol: str) -> Optional[Dict]:
        """
        獲取單一交易所的價格
        
        Args:
            exchange_name: 交易所名稱
            symbol: 交易對 (如 'BTC/USDT')
            
        Returns:
            包含 bid, ask, timestamp 的字典，或 None
        """
        if exchange_name not in self.exchanges:
            logger.warning(f"交易所 {exchange_name} 未初始化")
            return None

        try:
            exchange = self.exchanges[exchange_name]
            ticker = exchange.fetch_ticker(symbol)
            return {
                'exchange': exchange_name,
                'symbol': symbol,
                'bid': ticker.get('bid'),
                'ask': ticker.get('ask'),
                'last': ticker.get('last'),
                'timestamp': datetime.fromtimestamp(ticker['timestamp'] / 1000),
            }
        except Exception as e:
            logger.error(f"獲取 {exchange_name} {symbol} 價格失敗: {e}")
            return None

    def get_prices_for_symbol(self, symbol: str) -> Dict[str, Dict]:
        """
        獲取某個交易對在所有交易所的價格
        
        Args:
            symbol: 交易對 (如 'BTC/USDT')
            
        Returns:
            {交易所名稱: 價格字典}
        """
        prices = {}
        for exchange_name in self.exchanges.keys():
            price = self.get_price(exchange_name, symbol)
            if price:
                prices[exchange_name] = price
        return prices

    def get_prices_batch(self, symbols: List[str]) -> Dict[str, Dict[str, Dict]]:
        """
        批量獲取多個交易對的價格
        
        Args:
            symbols: 交易對列表
            
        Returns:
            {交易對: {交易所: 價格字典}}
        """
        all_prices = {}
        for symbol in symbols:
            all_prices[symbol] = self.get_prices_for_symbol(symbol)
        return all_prices
