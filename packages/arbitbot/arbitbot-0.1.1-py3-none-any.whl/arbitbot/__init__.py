"""
Arbitbot - Simple Multi-Exchange Crypto Arbitrage Detector
"""

__version__ = "0.1.0"
__author__ = "Hung-Ching-Lee"

from .detector import ArbitrageDetector
from .telegram_notifier import send_telegram_notification
from .config import CRYPTO_PAIRS, ALL_EXCHANGES, DEFAULT_FEES

__all__ = [
    "ArbitrageDetector",
    "send_telegram_notification",
    "CRYPTO_PAIRS",
    "ALL_EXCHANGES",
    "DEFAULT_FEES",
]
