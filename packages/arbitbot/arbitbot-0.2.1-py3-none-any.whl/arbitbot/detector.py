import ipywidgets as widgets
from IPython.display import display, clear_output, HTML
import pandas as pd
from datetime import datetime
import time
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import ccxt
import sys
import matplotlib.pyplot as plt
import random
import threading
from requests.exceptions import RequestException

# ----------------------------------------------------
# 📌 Terminal Font Configuration (Based on your Ubuntu setup for Chinese display)
# Setting Chinese font for matplotlib
try:
    plt.rcParams['font.sans-serif'] = ['WenQuanYi Micro Hei']
    plt.rcParams['axes.unicode_minus'] = False
except Exception:
    # Fallback in case font is not found
    pass
# ----------------------------------------------------

# --- Config and Utilities ---
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

ALL_EXCHANGES = ['binance', 'bybit', 'okx', 'kucoin', 'huobi', 'gate', 'kraken', 'coinbase', 'bitfinex']

# 核心類別
class ArbitrageDetector:
    def __init__(self):
        self.fees = {}
        self.clients = {}
        self.unified_symbols = {c['symbol']: c['name'] for c in CRYPTO_PAIRS}
        # 移除了 self.detector 實例化，現在在 show_gui() 中創建

    def initialize_exchanges(self, exchanges):
        """Initializes CCXT exchange clients and enables rate limiting."""
        self.clients = {}
        timeout_ms = 10000
        for exchange_id in exchanges:
            try:
                exchange_class = getattr(ccxt, exchange_id)
                self.clients[exchange_id] = exchange_class({
                    'timeout': timeout_ms,
                    'enableRateLimit': True,
                })
            except Exception as e:
                pass

    def get_crypto_all_prices(self, crypto, exchanges):
        """Fetches the real bid and ask prices from exchanges using CCXT."""
        prices = {}
        unified_symbol = crypto['symbol']
        # 這裡由於依賴於全域變數 profit_threshold，這個方法必須在 show_gui() 中定義或傳入 profit_threshold

        # --- 為了讓 ArbitrageDetector 可以匯入和獨立，我們假設它不直接依賴於 UI 變數 ---
        # 由於您提供的代碼中 ArbitrageDetector.find_all_arbitrage_pairs 依賴於 UI 變數 profit_threshold，
        # 為了修正，我們需要將這些變數作為參數傳遞給偵測方法。
        # 為了最小化改動，我將所有 UI 相關變數移入 show_gui() 的作用域。

        # 這裡不需要修改，因為 find_all_arbitrage_pairs 內部依賴 get_current_fees，
        # 而 get_current_fees 依賴 UI 變數，所以我們會在 show_gui() 中定義這些邏輯。
        # 此處僅保留價格獲取方法。
        # ---
        
        for exchange_id in exchanges:
            exchange = self.clients.get(exchange_id)
            if not exchange:
                continue

            try:
                # Use a shorter timeout for individual fetches within the thread
                ticker = exchange.fetch_ticker(unified_symbol, params={'timeout': 5000})

                bid_price = ticker.get('bid')
                ask_price = ticker.get('ask')

                if bid_price is not None and ask_price is not None:
                    prices[exchange_id] = {
                        'bid': bid_price,
                        'ask': ask_price,
                    }

            except ccxt.ExchangeNotAvailable:
                pass
            except ccxt.DDoSProtection or ccxt.RateLimitExceeded:
                pass
            except Exception:
                pass

        return {
            'symbol': unified_symbol,
            'name': crypto['name'],
            'prices': prices
        }

    # 由於 find_all_arbitrage_pairs 依賴於全域 UI 變數，它必須與 UI 邏輯放在一起，
    # 否則這個類別就不能獨立於 UI 運作。我們將其保留在類別中，但確保在 show_gui 函式內部傳遞所需的 UI 依賴。
    def find_all_arbitrage_pairs(self, price_data, get_current_fees_func, profit_threshold_value):
        """Calculates all arbitrage opportunities."""
        opportunities = []
        symbol = price_data['symbol']
        exchanges = list(price_data['prices'].keys())

        current_fees = get_current_fees_func() # 使用傳入的 fees 函式

        for i in range(len(exchanges)):
            for j in range(len(exchanges)):
                if i == j:
                    continue

                buy_ex = exchanges[i]
                sell_ex = exchanges[j]

                buy_price = price_data['prices'][buy_ex].get('ask')
                sell_price = price_data['prices'][sell_ex].get('bid')

                # Taker Fee
                buy_fee = current_fees.get(buy_ex, 0)
                sell_fee = current_fees.get(sell_ex, 0)

                if buy_price and sell_price and buy_price > 0:
                    
                    # Net price = Sell Price * (1 - Taker Fee)
                    net_sell_price = sell_price * (1 - sell_fee)
                    
                    # Net Profit Ratio (considering selling fee)
                    net_profit_ratio = (net_sell_price - buy_price) / buy_price
                    profit_percent = net_profit_ratio * 100

                    if profit_percent >= profit_threshold_value: # 使用傳入的 threshold 值
                        opportunities.append({
                            'symbol': symbol,
                            'name': price_data['name'], 
                            'buy_exchange': buy_ex,
                            'sell_exchange': sell_ex,
                            'buy_price': buy_price,
                            'sell_price': sell_price,
                            'buy_fee': buy_fee,
                            'sell_fee': sell_fee,
                            'net_sell_price': net_sell_price,
                            'profit_percent': profit_percent,
                        })
        return opportunities


# --- UI 元件、函式和執行邏輯包裝在 show_gui 函式中 ---

# 定義一個主函式來初始化並顯示 GUI
def show_gui():
    
    # 由於這些變數必須在整個 UI/執行流程中可見，所以必須在 show_gui 作用域內定義
    
    # --------------------------------------
    # 📌 1. UI Component Definition (Widgets)
    # --------------------------------------

    ## 🏆 Title
    title = widgets.HTML(
        '<div style="background-color:#6A5ACD; color:white; padding:10px; border-radius:8px; text-align:center;">'
        '<h2>🚀 Cross-Exchange Arbitrage Detector (CCXT)</h2>'
        '</div>'
    )

    ## 1️⃣ Exchange Selection
    exchange_selector = widgets.SelectMultiple(
        options=ALL_EXCHANGES,
        value=['binance', 'bybit', 'okx'],
        description='',
        layout=widgets.Layout(width='150px', height='250px')
    )

    exchange_display = widgets.Textarea(
        value='binance, bybit, okx',
        placeholder='Selected...',
        disabled=True,
        layout=widgets.Layout(width='180px', height='250px')
    )

    exchange_button = widgets.Button(
        description='✅ Confirm',
        button_style='success',
        layout=widgets.Layout(width='150px', height='30px')
    )

    def update_exchange_display(b):
        exchange_display.value = ', '.join(exchange_selector.value) if exchange_selector.value else '(None)'
    exchange_button.on_click(update_exchange_display)

    exchange_box = widgets.VBox([
        widgets.HTML('<b style="font-size:14px;">1️⃣ Exchanges</b>'),
        widgets.HBox([
            widgets.VBox([widgets.HTML('<span style="font-size:12px;">Available:</span>'), exchange_selector]),
            widgets.VBox([widgets.HTML('<span style="font-size:12px;">Selected:</span>'), exchange_display]),
        ], layout=widgets.Layout(gap='10px')),
        exchange_button
    ])


    ## 2️⃣ Crypto Selection
    crypto_symbols = [f"{c['symbol']} - {c['name']}" for c in CRYPTO_PAIRS]
    crypto_selector = widgets.SelectMultiple(
        options=crypto_symbols,
        value=[crypto_symbols[0], crypto_symbols[1], crypto_symbols[2]] if len(crypto_symbols) >= 3 else crypto_symbols,
        description='',
        layout=widgets.Layout(width='200px', height='250px')
    )

    selected_initial_symbols = [text.split(' - ')[0] for text in crypto_selector.value]
    crypto_display = widgets.Textarea(
        value='\n'.join(selected_initial_symbols),
        placeholder='Selected...',
        disabled=True,
        layout=widgets.Layout(width='120px', height='250px')
    )

    crypto_button = widgets.Button(
        description='✅ Confirm',
        button_style='success',
        layout=widgets.Layout(width='150px', height='30px')
    )

    def update_crypto_display(b):
        selected_symbols = [text.split(' - ')[0] for text in crypto_selector.value]
        crypto_display.value = '\n'.join(selected_symbols) if selected_symbols else '(None)'
    crypto_button.on_click(update_crypto_display)

    crypto_box = widgets.VBox([
        widgets.HTML('<b style="font-size:14px;">2️⃣ Cryptos</b>'),
        widgets.HBox([
            widgets.VBox([widgets.HTML('<span style="font-size:12px;">Available:</span>'), crypto_selector]),
            widgets.VBox([widgets.HTML('<span style="font-size:12px;">Selected:</span>'), crypto_display]),
        ], layout=widgets.Layout(gap='10px')),
        crypto_button
    ])

    row1 = widgets.HBox([exchange_box, crypto_box], layout=widgets.Layout(gap='50px', margin='5px 0'))


    ## 🔧 Taker Fees
    fee_widgets = {}
    initial_fees = {ex: 0.001 for ex in ALL_EXCHANGES}
    initial_fees['bybit'] = 0.0007
    initial_fees['okx'] = 0.0008

    for ex in ALL_EXCHANGES:
        fee_widgets[ex] = widgets.BoundedFloatText(
            value=initial_fees.get(ex, 0.001),
            min=0.0,
            max=0.01,
            step=0.0001,
            description=ex.capitalize(),
            style={'description_width': '80px'},
            layout=widgets.Layout(width='160px')
        )

    fee_row1 = widgets.HBox([fee_widgets[ex] for ex in ALL_EXCHANGES[:5]], layout=widgets.Layout(gap='15px'))
    fee_row2 = widgets.HBox([fee_widgets[ex] for ex in ALL_EXCHANGES[5:]], layout=widgets.Layout(gap='15px'))

    fee_box = widgets.VBox([
        widgets.HTML('<b style="font-size:14px;">3️⃣ Taker Fees:</b>'),
        fee_row1,
        fee_row2
    ], layout=widgets.Layout(border='1px solid #555', padding='10px', margin='10px 0'))


    ## 4️⃣ Parameters & Telegram
    profit_threshold = widgets.FloatSlider(
        value=0.5,
        min=0.01,
        max=5.0,
        step=0.01,
        description='Min Profit %',
        style={'description_width': '100px'},
        readout_format='.2f',
        layout=widgets.Layout(width='350px')
    )

    check_interval = widgets.Dropdown(
        options={'30s': 30, '1min': 60, '5min': 300, '10min': 600, '30min': 1800, '1hr': 3600},
        value=30,
        description='Interval',
        style={'description_width': '100px'},
        layout=widgets.Layout(width='220px')
    )

    enable_telegram = widgets.Checkbox(
        value=False,
        description='Enable TG Notifications',
        indent=False,
        layout=widgets.Layout(width='200px')
    )

    tg_token_input = widgets.Password(
        placeholder='Telegram Bot Token',
        description='Token:',
        style={'description_width': '60px'},
        layout=widgets.Layout(width='300px')
    )

    tg_chat_id_input = widgets.Text(
        placeholder='Telegram Chat ID',
        description='Chat ID:',
        style={'description_width': '60px'},
        layout=widgets.Layout(width='200px')
    )

    settings_box = widgets.HBox([
        widgets.VBox([
            widgets.HTML('<b style="font-size:14px;">4️⃣ Parameters</b>'),
            widgets.HBox([profit_threshold, check_interval], layout=widgets.Layout(gap='30px'))
        ]),
        widgets.VBox([
            widgets.HTML('<b style="font-size:14px;">5️⃣ Telegram</b>'),
            widgets.HBox([enable_telegram], layout=widgets.Layout(gap='10px')),
            widgets.HBox([tg_token_input, tg_chat_id_input], layout=widgets.Layout(gap='10px'))
        ])
    ], layout=widgets.Layout(gap='60px', margin='10px 0'))


    ## ▶️ Run Button
    run_button = widgets.Button(
        description='🚀 Start Detection',
        button_style='success',
        layout=widgets.Layout(width='180px', height='40px')
    )

    button_box = widgets.HBox([run_button], layout=widgets.Layout(justify_content='center', margin='15px 0'))


    ## 🖥️ Output Areas
    table_output = widgets.Output(layout=widgets.Layout(width='100%', border='2px solid #3CB371', padding='15px', height='500px', overflow_y='auto'))
    output_area = widgets.Output(layout=widgets.Layout(width='100%', border='2px solid #999', padding='15px', height='1000px', overflow_y='auto'))


    # --- Main Layout ---
    main_layout = widgets.VBox([
        title,
        widgets.HTML('<hr style="margin: 10px 0; border: 1px solid #ddd;">'),
        row1,
        widgets.HTML('<hr style="margin: 10px 0; border: 1px solid #ddd;">'),
        fee_box,
        widgets.HTML('<hr style="margin: 10px 0; border: 1px solid #ddd;">'),
        settings_box,
        widgets.HTML('<hr style="margin: 10px 0; border: 1px solid #ddd;">'),
        button_box,
        widgets.HTML('<b>📈 Arbitrage Opportunities (Top 10)</b>'),
        table_output,
        widgets.HTML('<b>💻 Log / Console Output</b>'),
        output_area,
    ], layout=widgets.Layout(width='100%'))


    # --------------------------------------
    # 📌 2. Event Handler Logic (定義在 show_gui 內部，以存取 UI 變數)
    # --------------------------------------

    # 確保 fees 函式可以存取到 fee_widgets
    def get_current_fees():
        return {ex: fee_widgets[ex].value for ex in ALL_EXCHANGES}

    # Telegram Notification 函式
    def send_telegram_notification(token, chat_id, opportunities, current_time):
        """Sends a single Telegram message containing the timestamp and all opportunities for the batch."""
        if not opportunities:
            return

        if not token or not chat_id:
            print('❌ TG Error: Token or Chat ID is empty')
            return
        
        # Build the message
        msg = f'🕒 <b>Arbitrage Detection Report</b> 🕒\n'
        msg += f'<i>Time: {current_time}</i>\n\n'
        
        # Group opportunities by symbol
        grouped_opportunities = {}
        for opp in opportunities:
            symbol = opp['symbol']
            if symbol not in grouped_opportunities:
                grouped_opportunities[symbol] = []
            grouped_opportunities[symbol].append(opp)
        
        # Sort groups by the highest profit within the group for better display order
        sorted_symbols = sorted(grouped_opportunities.keys(), 
                                key=lambda s: max(opp['profit_percent'] for opp in grouped_opportunities[s]), 
                                reverse=True)

        for symbol in sorted_symbols:
            opps = grouped_opportunities[symbol]
            name = opps[0]['name']
            msg += f'💎 <b>{name} ({symbol}) - {len(opps)} Opportunities</b>\n'
            
            # List all arbitrage opportunities for this coin
            for i, opp in enumerate(opps):
                # Format output
                buy_ex = opp["buy_exchange"].capitalize()
                sell_ex = opp["sell_exchange"].capitalize()
                profit = f'{opp["profit_percent"]:.4f}%'
                buy_price = f'{opp["buy_price"]:.6f}'
                sell_price = f'{opp["sell_price"]:.6f}'

                # Highlight profit and prices
                msg += f'  {i+1}. Net Profit: <b>{profit}</b>\n'
                msg += f'     Buy: {buy_ex} @ <b>${buy_price}</b>\n'
                msg += f'     Sell: {sell_ex} @ <b>${sell_price}</b>\n'
            msg += '\n'

        try:
            url = f'https://api.telegram.org/bot{token}/sendMessage'
            payload = {'chat_id': chat_id, 'text': msg, 'parse_mode': 'HTML'}
            response = requests.post(url, json=payload, timeout=10)
            
            if response.status_code == 200:
                print(f'✅ TG Sent: {len(opportunities)} opportunities in one message')
            else:
                print(f'❌ TG API Error: {response.status_code} - {response.text}')

        except Exception as e:
            print(f'❌ TG Connection Error: {e}')


    # 實例化 ArbitrageDetector (必須在 UI 元件定義之後，才能被 on_run_clicked 存取)
    detector = ArbitrageDetector()

    running = False
    running_lock = threading.Lock()

    # 主執行函式
    def on_run_clicked(b):
        nonlocal running
        global detector # 讓 on_run_clicked 可以存取到 show_gui 作用域內的 detector

        with running_lock:
            if running:
                with output_area: clear_output(); print('⚠️ Detection is already running. Please interrupt the kernel to stop.')
                return
            running = True

        run_button.disabled = True

        exchanges_str = exchange_display.value
        cryptos_symbols_str = crypto_display.value

        exchanges = [e.strip() for e in exchanges_str.split(',') if e.strip() and e.strip() != '(None)']
        selected_symbols = [s.strip() for s in cryptos_symbols_str.split('\n') if s.strip() and s.strip() != '(None)']
        selected_cryptos = [c for c in CRYPTO_PAIRS if c['symbol'] in selected_symbols]


        threshold = profit_threshold.value
        interval = check_interval.value
        enable_tg = enable_telegram.value
        tg_token = tg_token_input.value if enable_tg else ''
        tg_chat_id = tg_chat_id_input.value if enable_tg else ''

        if not exchanges:
            with output_area: clear_output(); print('❌ Select exchanges first')
            with running_lock: running = False; run_button.disabled = False; return
        if not selected_cryptos:
            with output_area: clear_output(); print('❌ Select cryptos first')
            with running_lock: running = False; run_button.disabled = False; return
        if enable_tg and (not tg_token or not tg_chat_id):
            with output_area: clear_output(); print('❌ TG config incomplete (Token or Chat ID missing)')
            with running_lock: running = False; run_button.disabled = False; return

        detector.fees = get_current_fees()
        detector.initialize_exchanges(exchanges)

        with output_area:
            clear_output()
            print('--- Arbitrage Detector Initialized ---')
            print(f'🚨 Stop: interrupt Jupyter kernel')
            print(f'Exchanges: {len(exchanges)} | Cryptos: {len(selected_cryptos)}')
            print(f'Min Profit: {threshold}% | Interval: {interval}s')
            print(f'Telegram: {"Enabled" if enable_tg else "Disabled"}')
            print('------------------------------------')


        iteration = 0
        while True:
            with running_lock:
                if not running: break

            iteration += 1
            round_opportunities = []
            current_batch_time = datetime.now()
            current_batch_time_str = current_batch_time.strftime("%Y-%m-%d %H:%M:%S")

            with output_area:
                clear_output(wait=True)
                print(f'🔄 #{iteration} | {current_batch_time_str} | Fetching Prices via CCXT...')

            max_price_workers = 20 # Limit threads to prevent excessive requests
            with ThreadPoolExecutor(max_workers=max_price_workers) as executor:
                # Submit all crypto price fetching tasks
                futures = {executor.submit(detector.get_crypto_all_prices, crypto, exchanges): crypto for crypto in selected_cryptos}

                for future in as_completed(futures):
                    with running_lock:
                        if not running: break

                    crypto = futures[future]
                    unified_symbol = crypto['symbol']

                    try:
                        price_data = future.result()

                        if not price_data or not price_data.get('prices') or len(price_data['prices']) < 2:
                            with output_area: print(f'⚠️ {unified_symbol}: Not enough valid price data received (skipping calculation)')
                            continue

                        log_msg = f"🔎 {unified_symbol} Prices:"
                        for ex, p in price_data['prices'].items():
                            ask = f"{p['ask']:.6f}" if p['ask'] is not None else 'N/A'
                            bid = f"{p['bid']:.6f}" if p['bid'] is not None else 'N/A'
                            log_msg += f" {ex[:4]}={ask}/{bid}"
                        with output_area: print(log_msg)

                        # 注意這裡調用 find_all_arbitrage_pairs 時，傳遞了 UI 相關的依賴
                        all_pairs = detector.find_all_arbitrage_pairs(price_data, get_current_fees, threshold)
                        profitable_pairs = [p for p in all_pairs if p['profit_percent'] >= threshold]

                        if profitable_pairs:
                            # Sort by profit for log output and later TG formatting
                            profitable_pairs.sort(key=lambda x: x['profit_percent'], reverse=True)
                            round_opportunities.extend(profitable_pairs)
                            with output_area: print(f'✅ {unified_symbol}: Found {len(profitable_pairs)} opportunities, Max: {profitable_pairs[0]["profit_percent"]:.4f}%')
                        else:
                            with output_area: print(f'ℹ️ {unified_symbol}: No opportunities > {threshold}%')

                    except Exception as e:
                        with output_area: print(f'❌ {unified_symbol} General Error during processing: {str(e)}')
                
                with running_lock:
                    if not running: break

            # --- TG Notification (One message per batch) ---
            if enable_tg and round_opportunities:
                send_telegram_notification(tg_token, tg_chat_id, round_opportunities, current_batch_time_str)
            # ---------------------------------------------

            if not running: break

            # Display results table
            with table_output:
                clear_output(wait=True)
                if round_opportunities:
                    # Use DataFrame for display (Top 10)
                    df = pd.DataFrame(round_opportunities).sort_values('profit_percent', ascending=False).head(10)
                    
                    df_display = df[['symbol', 'buy_exchange', 'sell_exchange', 'buy_price', 'sell_price', 'buy_fee', 'sell_fee', 'profit_percent']].copy()

                    df_display.columns = ['Crypto', 'Buy', 'Sell', 'Ask Price (Buy)', 'Bid Price (Sell)', 'Buy Fee (%)', 'Sell Fee (%)', 'Profit (%)']

                    # Formatting for display
                    df_display['Profit (%)'] = df_display['Profit (%)'].round(4)
                    df_display['Buy Fee (%)'] = (df_display['Buy Fee (%)'] * 100).round(4)
                    df_display['Sell Fee (%)'] = (df_display['Sell Fee (%)'] * 100).round(4)
                    df_display['Ask Price (Buy)'] = df_display['Ask Price (Buy)'].round(6)
                    df_display['Bid Price (Sell)'] = df_display['Bid Price (Sell)'].round(6)
                    
                    df_display['Buy'] = df_display['Buy'].str.capitalize()
                    df_display['Sell'] = df_display['Sell'].str.capitalize()

                    html_table = df_display.to_html(index=False, classes='table table-striped', float_format='%.6f')
                    display(HTML(f'<b>Found Total: {len(round_opportunities)} | Displaying Top {len(df_display)}</b><br>{html_table}'))
                else:
                    print(f'ℹ️ {current_batch_time_str}: No opportunities found above the minimum profit threshold.')

            time.sleep(interval)

        with output_area: print('⏹ Stopped.')
        run_button.disabled = False


    # --------------------------------------
    # 📌 3. 執行 GUI 顯示
    # --------------------------------------
    run_button.on_click(on_run_clicked)
    display(main_layout)

    # 為了讓外部可以存取 detector 物件 (例如用於停止執行緒)，我們將其作為 show_gui 的屬性
    show_gui.detector = detector
    show_gui.running_lock = running_lock
    show_gui.output_area = output_area
    show_gui.run_button = run_button
    show_gui.running = running # 初始狀態

    # 修正後的 find_all_arbitrage_pairs 需要的參數變更，必須在此處調整
    # 這裡將 ArbitrageDetector.find_all_arbitrage_pairs 替換為一個閉包函式，以捕捉 UI 變數

# --------------------------------------
# 📌 4. 檔案保護，讓程式碼可以被匯入
# --------------------------------------
if __name__ == '__main__':
    # 僅在直接運行 detector.py 時執行 GUI
    show_gui()