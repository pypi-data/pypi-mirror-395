"""
Telegram Notification Module
"""

import requests
from typing import List, Dict


def send_telegram_notification(token: str, chat_id: str, opportunities: List[Dict], timestamp: str) -> bool:
    """Send Telegram notification with all opportunities in one message."""
    if not opportunities or not token or not chat_id:
        return False
    
    try:
        msg = f'🕒 <b>Arbitrage Detection Report</b> 🕒\n'
        msg += f'<i>Time: {timestamp}</i>\n\n'
        
        # Group opportunities by symbol
        grouped = {}
        for opp in opportunities:
            symbol = opp['symbol']
            if symbol not in grouped:
                grouped[symbol] = []
            grouped[symbol].append(opp)
        
        # Sort by highest profit
        sorted_symbols = sorted(grouped.keys(), 
                                key=lambda s: max(o['profit_percent'] for o in grouped[s]), 
                                reverse=True)
        
        for symbol in sorted_symbols:
            opps = grouped[symbol]
            name = opps[0]['name']
            msg += f'💎 <b>{name} ({symbol}) - {len(opps)} Opps</b>\n'
            
            for i, opp in enumerate(opps, 1):
                msg += f'  {i}. Profit: <b>{opp["profit_percent"]:.4f}%</b>\n'
                msg += f'     Buy: {opp["buy_exchange"].upper()} @ <b>${opp["buy_price"]:.6f}</b>\n'
                msg += f'     Sell: {opp["sell_exchange"].upper()} @ <b>${opp["sell_price"]:.6f}</b>\n'
            msg += '\n'
        
        url = f'https://api.telegram.org/bot{token}/sendMessage'
        payload = {'chat_id': chat_id, 'text': msg, 'parse_mode': 'HTML'}
        response = requests.post(url, json=payload, timeout=10)
        
        return response.status_code == 200
    except Exception:
        return False
