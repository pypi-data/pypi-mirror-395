"""
工具函數模組
"""

import logging
from datetime import datetime
from typing import Optional


def setup_logging(log_file: Optional[str] = None) -> logging.Logger:
    """
    設置日誌
    
    Args:
        log_file: 日誌文件路徑，如果為 None 則只輸出到控制台
        
    Returns:
        Logger 對象
    """
    logger = logging.getLogger('arbitbot')
    logger.setLevel(logging.DEBUG)

    # 控制台處理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)

    # 文件處理器
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_format = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(file_format)
        logger.addHandler(file_handler)

    return logger


def calculate_profit_percentage(buy_price: float, sell_price: float) -> float:
    """
    計算利潤百分比
    
    Args:
        buy_price: 買入價
        sell_price: 賣出價
        
    Returns:
        利潤百分比
    """
    if buy_price <= 0:
        return 0
    return ((sell_price - buy_price) / buy_price) * 100


def format_price(price: float, decimals: int = 2) -> str:
    """格式化價格"""
    return f"{price:.{decimals}f}"


def format_timestamp(timestamp: datetime) -> str:
    """格式化時間戳"""
    if isinstance(timestamp, datetime):
        return timestamp.strftime("%Y-%m-%d %H:%M:%S")
    return str(timestamp)
