"""
Arbitbot - Simple Multi-Exchange Crypto Arbitrage Detector
"""

__version__ = "0.2.1"
__author__ = "Hung-Ching-Lee"

from .detector import ArbitrageDetector, show_gui, CRYPTO_PAIRS, ALL_EXCHANGES

__all__ = [
    "ArbitrageDetector",
    "show_gui",
    "CRYPTO_PAIRS",
    "ALL_EXCHANGES",
]
