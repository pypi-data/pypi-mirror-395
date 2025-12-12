"""
Telegram Notification Module
"""

import requests
from typing import Optional


def send_telegram_notification(token: str, chat_id: str, message: str) -> bool:
    """Send Telegram notification with error handling.
    
    Args:
        token: Telegram Bot Token from @BotFather
        chat_id: Telegram Chat ID from @userinfobot
        message: Message to send (supports HTML formatting)
        
    Returns:
        True if successful, False otherwise
    """
    if not token or not chat_id:
        return False
    
    try:
        url = f'https://api.telegram.org/bot{token}/sendMessage'
        payload = {
            'chat_id': chat_id,
            'text': message,
            'parse_mode': 'HTML'
        }
        response = requests.post(url, json=payload, timeout=5)
        return response.status_code == 200
    except Exception as e:
        print(f'❌ Telegram send failed: {str(e)[:40]}')
        return False
