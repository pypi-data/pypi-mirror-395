"""
Telegram 通知模組
"""

import logging
import requests
from typing import Optional, Dict, List
from .arbitrage import Opportunity

logger = logging.getLogger(__name__)


class TelegramNotifier:
    """Telegram 通知器"""

    def __init__(self, token: str, chat_id: str):
        """
        初始化 Telegram 通知器
        
        Args:
            token: Telegram Bot Token
            chat_id: 目標 Chat ID
        """
        self.token = token
        self.chat_id = chat_id
        self.api_url = f"https://api.telegram.org/bot{token}/sendMessage"

    def send_message(self, text: str) -> bool:
        """
        發送文本消息
        
        Args:
            text: 消息文本
            
        Returns:
            是否發送成功
        """
        if not self.token or not self.chat_id:
            logger.warning("⚠ Telegram 配置不完整，跳過發送")
            return False

        try:
            payload = {
                'chat_id': self.chat_id,
                'text': text,
                'parse_mode': 'HTML'
            }
            response = requests.post(self.api_url, json=payload, timeout=10)
            if response.status_code == 200:
                logger.info("✓ Telegram 消息已發送")
                return True
            else:
                logger.error(f"✗ Telegram 發送失敗: {response.text}")
                return False
        except Exception as e:
            logger.error(f"✗ Telegram 發送異常: {e}")
            return False

    def notify_opportunity(self, opportunity: Opportunity) -> bool:
        """通知單個套利機會"""
        message = self._format_opportunity_message(opportunity)
        return self.send_message(message)

    def notify_opportunities(self, opportunities: List[Opportunity]) -> bool:
        """通知多個套利機會"""
        if not opportunities:
            return False

        message = self._format_opportunities_message(opportunities)
        return self.send_message(message)

    @staticmethod
    def _format_opportunity_message(opp: Opportunity) -> str:
        """格式化單個套利機會的消息"""
        return (
            f"🔔 <b>發現套利機會</b>\n\n"
            f"<b>交易對:</b> {opp.symbol}\n"
            f"<b>買入:</b> {opp.buy_exchange.upper()} @ ${opp.buy_price:.2f}\n"
            f"<b>賣出:</b> {opp.sell_exchange.upper()} @ ${opp.sell_price:.2f}\n"
            f"<b>利潤:</b> <code>{opp.profit_percentage:.2f}%</code>"
        )

    @staticmethod
    def _format_opportunities_message(opportunities: List[Opportunity]) -> str:
        """格式化多個套利機會的消息"""
        header = f"🔔 <b>發現 {len(opportunities)} 個套利機會</b>\n\n"
        items = []
        for i, opp in enumerate(opportunities, 1):
            item = (
                f"<b>{i}. {opp.symbol}</b>\n"
                f"  買: {opp.buy_exchange.upper()}@${opp.buy_price:.2f}\n"
                f"  賣: {opp.sell_exchange.upper()}@${opp.sell_price:.2f}\n"
                f"  利潤: <code>{opp.profit_percentage:.2f}%</code>\n"
            )
            items.append(item)
        return header + "\n".join(items)
