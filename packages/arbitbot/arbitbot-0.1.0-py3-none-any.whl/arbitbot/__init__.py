"""
Arbitbot - Multi-Exchange Cryptocurrency Arbitrage Detection Tool
"""

__version__ = "0.1.0"
__author__ = "Hung-Ching-Lee"

from .detector import ArbitrageDetector
from .telegram_notifier import send_telegram_notification
from .config import CRYPTO_PAIRS, ALL_EXCHANGES, DEFAULT_FEES, CHECK_INTERVALS

__all__ = [
    "ArbitrageDetector",
    "send_telegram_notification",
    "CRYPTO_PAIRS",
    "ALL_EXCHANGES",
    "DEFAULT_FEES",
    "CHECK_INTERVALS",
]
