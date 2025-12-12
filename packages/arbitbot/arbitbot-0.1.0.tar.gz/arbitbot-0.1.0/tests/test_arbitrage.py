"""
測試套利機器人
"""

import pytest
from arbitbot.arbitrage import ArbitrageBot, Opportunity
from arbitbot.utils import calculate_profit_percentage


def test_calculate_profit_percentage():
    """測試利潤計算"""
    profit = calculate_profit_percentage(100, 105)
    assert profit == 5.0
    
    profit = calculate_profit_percentage(100, 100.5)
    assert profit == 0.5


def test_opportunity_creation():
    """測試 Opportunity 對象創建"""
    opp = Opportunity(
        symbol='BTC/USDT',
        buy_exchange='binance',
        sell_exchange='bybit',
        buy_price=30000,
        sell_price=30150,
        profit_percentage=0.5
    )
    
    assert opp.symbol == 'BTC/USDT'
    assert opp.profit_percentage == 0.5
    assert 'BTC/USDT' in str(opp)


def test_arbitrage_bot_initialization():
    """測試套利機器人初始化"""
    bot = ArbitrageBot(exchanges=['binance', 'bybit'], profit_threshold=0.5)
    assert bot.profit_threshold == 0.5
    assert bot.opportunities == []


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
