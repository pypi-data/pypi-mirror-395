"""
Configuration and Constants
"""

CRYPTO_PAIRS = [
    {'symbol': 'BTC/USDT', 'name': 'Bitcoin'},
    {'symbol': 'ETH/USDT', 'name': 'Ethereum'},
    {'symbol': 'XRP/USDT', 'name': 'Ripple'},
    {'symbol': 'DOGE/USDT', 'name': 'Dogecoin'},
    {'symbol': 'SOL/USDT', 'name': 'Solana'},
    {'symbol': 'ADA/USDT', 'name': 'Cardano'},
    {'symbol': 'DOT/USDT', 'name': 'Polkadot'},
    {'symbol': 'LTC/USDT', 'name': 'Litecoin'},
    {'symbol': 'BCH/USDT', 'name': 'Bitcoin Cash'},
    {'symbol': 'LINK/USDT', 'name': 'Chainlink'},
    {'symbol': 'VET/USDT', 'name': 'VeChain'},
    {'symbol': 'TRX/USDT', 'name': 'TRON'},
    {'symbol': 'MATIC/USDT', 'name': 'Polygon'},
    {'symbol': 'AVAX/USDT', 'name': 'Avalanche'},
]

ALL_EXCHANGES = [
    'binance', 'bybit', 'okx', 'kucoin', 'huobi', 
    'gate', 'kraken', 'coinbase', 'bitfinex'
]

DEFAULT_FEES = {
    'binance': 0.001,
    'bybit': 0.0007,
    'okx': 0.0008,
    'kucoin': 0.001,
    'huobi': 0.002,
    'gate': 0.0015,
    'kraken': 0.0016,
    'coinbase': 0.004,
    'bitfinex': 0.001,
}
