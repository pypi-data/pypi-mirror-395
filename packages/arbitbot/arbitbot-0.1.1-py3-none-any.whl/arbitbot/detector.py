"""
Arbitrage Detection Engine
"""

import ccxt
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List


class ArbitrageDetector:
    """Multi-exchange arbitrage detector using CCXT"""
    
    def __init__(self):
        self.fees: Dict[str, float] = {}
        self.clients: Dict[str, object] = {}
    
    def initialize_exchanges(self, exchanges: List[str]) -> None:
        """Initialize CCXT exchange clients with rate limiting."""
        self.clients = {}
        timeout_ms = 10000
        
        for exchange_id in exchanges:
            try:
                exchange_class = getattr(ccxt, exchange_id)
                self.clients[exchange_id] = exchange_class({
                    'timeout': timeout_ms,
                    'enableRateLimit': True,
                })
            except Exception:
                pass
    
    def get_crypto_all_prices(self, crypto: Dict, exchanges: List[str]) -> Dict:
        """Get real bid/ask prices from multiple exchanges via CCXT."""
        prices = {}
        unified_symbol = crypto['symbol']
        
        for exchange_id in exchanges:
            exchange = self.clients.get(exchange_id)
            if not exchange:
                continue
            
            try:
                ticker = exchange.fetch_ticker(unified_symbol, params={'timeout': 5000})
                bid_price = ticker.get('bid')
                ask_price = ticker.get('ask')
                
                if bid_price is not None and ask_price is not None:
                    prices[exchange_id] = {
                        'bid': bid_price,
                        'ask': ask_price,
                    }
            except Exception:
                pass
        
        return {
            'symbol': unified_symbol,
            'name': crypto['name'],
            'prices': prices
        }
    
    def find_all_arbitrage_pairs(self, price_data: Dict, current_fees: Dict) -> List[Dict]:
        """Find all arbitrage opportunities A->B across exchanges."""
        opportunities = []
        symbol = price_data['symbol']
        name = price_data['name']
        exchanges = list(price_data['prices'].keys())
        
        for i in range(len(exchanges)):
            for j in range(len(exchanges)):
                if i == j:
                    continue
                
                buy_ex = exchanges[i]
                sell_ex = exchanges[j]
                
                buy_price = price_data['prices'][buy_ex].get('ask')
                sell_price = price_data['prices'][sell_ex].get('bid')
                
                buy_fee = current_fees.get(buy_ex, 0)
                sell_fee = current_fees.get(sell_ex, 0)
                
                if buy_price and sell_price and buy_price > 0:
                    net_sell_price = sell_price * (1 - sell_fee)
                    net_profit_ratio = (net_sell_price - buy_price) / buy_price
                    profit_percent = net_profit_ratio * 100
                    
                    opportunities.append({
                        'symbol': symbol,
                        'name': name,
                        'buy_exchange': buy_ex,
                        'sell_exchange': sell_ex,
                        'buy_price': buy_price,
                        'sell_price': sell_price,
                        'buy_fee': buy_fee,
                        'sell_fee': sell_fee,
                        'net_sell_price': net_sell_price,
                        'profit_percent': profit_percent,
                    })
        
        return opportunities
