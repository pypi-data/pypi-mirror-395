# Arbitbot - Multi-Exchange Crypto Arbitrage Detector

A powerful tool to detect cryptocurrency arbitrage opportunities across multiple exchanges in real-time using CCXT.

## Features

✨ **Real-time Arbitrage Detection**
- Monitors 14+ cryptocurrencies across 9 major exchanges
- Complete pairing mode: generates all A→B combinations for maximum opportunity coverage
- Real data only - no simulations or mock data

🚀 **Multi-Exchange Support**
- Binance, Bybit, OKX, KuCoin, Huobi, Gate, Kraken, Coinbase, Bitfinex
- Concurrent price fetching with built-in rate limiting
- Automatic exchange connection management

📊 **Advanced Features**
- Configurable profit threshold (0.01% - 5.0%)
- Customizable taker fees per exchange
- Real-time result display with top 10 opportunities
- Concurrent processing for fast detection

🔔 **Telegram Notifications**
- Push notifications for profitable arbitrage opportunities
- HTML-formatted messages with detailed profit information
- Configurable alerts

## Installation

### From PyPI
```bash
pip install arbitbot
```

### From Source
```bash
git clone https://github.com/Hung-Ching-Lee/Arbitbot.git
cd Arbitbot
pip install -e .
```

## Quick Start

### 1. Interactive Jupyter Notebook (Recommended)

```bash
jupyter notebook Arbitbot_Interactive.ipynb
```

Then:
1. Select exchanges to monitor (multi-select)
2. Choose cryptocurrencies (multi-select)
3. Set minimum profit threshold
4. Configure Telegram (optional)
5. Click "🚀 Start Detection"

### 2. Python Script

```python
from arbitbot import ArbitrageDetector, send_telegram_notification

# Initialize detector
detector = ArbitrageDetector()

# Set fees for exchanges
detector.fees = {
    'binance': 0.001,
    'bybit': 0.0007,
    'okx': 0.0008,
}

# Initialize exchanges
exchanges = ['binance', 'bybit', 'okx']
detector.initialize_exchanges(exchanges)

# Define cryptocurrency to monitor
crypto = {'symbol': 'BTC/USDT', 'name': 'Bitcoin'}

# Get prices from all exchanges
price_data = detector.get_crypto_all_prices(crypto, exchanges)

# Find arbitrage opportunities
opportunities = detector.find_all_arbitrage_pairs(price_data)

# Filter by profit threshold
profitable = [op for op in opportunities if op['profit_percent'] >= 0.5]

# Print results
for op in profitable:
    print(f"Buy {op['symbol']} at {op['buy_exchange']} for \${op['buy_price']:.6f}")
    print(f"Sell at {op['sell_exchange']} for \${op['sell_price']:.6f}")
    print(f"Profit: {op['profit_percent']:.4f}%\n")

# Send Telegram notification
if profitable:
    best = max(profitable, key=lambda x: x['profit_percent'])
    msg = f"Arbitrage: Buy {best['buy_exchange']} @ \${best['buy_price']:.6f}, Sell {best['sell_exchange']} @ \${best['sell_price']:.6f}, Profit: {best['profit_percent']:.4f}%"
    send_telegram_notification(TOKEN, CHAT_ID, msg)
```

## Telegram Configuration

### Get Bot Token
1. Message [@BotFather](https://t.me/BotFather) on Telegram
2. Send `/newbot` and follow instructions
3. Copy the token provided

### Get Chat ID
1. Message [@userinfobot](https://t.me/userinfobot)
2. Reply will contain your Chat ID
3. Send any message to your bot to activate it

## Supported Cryptocurrencies

BTC, ETH, XRP, DOGE, SOL, ADA, DOT, LTC, BCH, LINK, VET, TRX, MATIC, AVAX

## Supported Exchanges

Binance, Bybit, OKX, KuCoin, Huobi, Gate, Kraken, Coinbase, Bitfinex

## API Reference

### ArbitrageDetector

```python
detector = ArbitrageDetector()
detector.initialize_exchanges(['binance', 'bybit'])
detector.fees = {'binance': 0.001, 'bybit': 0.0007}
price_data = detector.get_crypto_all_prices(crypto, exchanges)
opportunities = detector.find_all_arbitrage_pairs(price_data)
```

### Telegram Notifications

```python
from arbitbot import send_telegram_notification
send_telegram_notification(token, chat_id, message)
```

## Requirements

- Python ≥ 3.8
- ccxt ≥ 1.80.0
- requests ≥ 2.28.0
- pandas ≥ 1.5.0

## License

MIT License

## Disclaimer

⚠️ Cryptocurrency trading involves substantial risk. This tool is for educational purposes only. Always test with small amounts before actual trading.
