import os
import time
import hmac
import hashlib
import requests
from dotenv import load_dotenv
from telegram import Bot

# 🟢 Tambahan Google Sheets
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def init_gsheet():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open("Binance Monitor").sheet1  # Ganti sesuai nama spreadsheet kamu
    return sheet

def save_to_sheet(sheet, data: list):
    sheet.append_row(data, value_input_option="RAW")

# 🟡 Load API & Token dari .env
load_dotenv()
API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET").encode()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = "@jurnalbitget"  # Ganti ke channel atau ID kamu

bot = Bot(token=BOT_TOKEN)
BASE_URL = "https://api.binance.com"

last_trade_id = None
account_type = None  # Akan di-set otomatis ke "pm" atau "margin"

def send_message(msg: str):
    bot.send_message(chat_id=CHAT_ID, text=msg, parse_mode="HTML")

def create_signature(query_string):
    return hmac.new(API_SECRET, query_string.encode(), hashlib.sha256).hexdigest()

def signed_request(path: str, params: str = ""):
    timestamp = int(time.time() * 1000)
    recv_window = 5000
    full_params = f"{params}&recvWindow={recv_window}&timestamp={timestamp}" if params else f"recvWindow={recv_window}&timestamp={timestamp}"
    signature = create_signature(full_params)
    url = f"{BASE_URL}{path}?{full_params}&signature={signature}"
    headers = {"X-MBX-APIKEY": API_KEY}
    response = requests.get(url, headers=headers, timeout=10)

    if not response.content or response.status_code != 200:
        raise Exception(f"❌ Error response:\n{response.status_code}\n{response.text}")

    return response.json()

def detect_account_type():
    try:
        signed_request("/sapi/v1/pm/myTrades", "symbol=BTCUSDT&limit=1")
        return "pm"
    except Exception:
        return "margin"

def get_wallet_balance():
    data = signed_request("/sapi/v1/margin/account")
    for asset in data["userAssets"]:
        if asset["asset"] == "USDT":
            return float(asset["netAsset"])
    return 0.0

def get_active_symbols():
    data = signed_request("/sapi/v1/margin/account")
    symbols = []
    for asset in data["userAssets"]:
        free = float(asset.get("free", 0))
        borrowed = float(asset.get("borrowed", 0))
        if free > 0 or borrowed > 0:
            symbols.append(asset["asset"] + "USDT")
    return list(set(symbols))

def fetch_latest_trade(symbol):
    path = "/sapi/v1/pm/myTrades" if account_type == "pm" else "/sapi/v1/margin/myTrades"
    trades = signed_request(path, f"symbol={symbol}&limit=1")
    return trades[-1] if trades else None

def monitor_margin_trades():
    global last_trade_id
    symbols = get_active_symbols()
    sheet = init_gsheet()  # ✅ inisialisasi Google Sheet sekali saat loop mulai

    for symbol in symbols:
        try:
            trade = fetch_latest_trade(symbol)
            if not trade:
                continue
            trade_id = trade.get("id")
            if trade_id == last_trade_id:
                continue
            last_trade_id = trade_id

            side = "🟢 BUY" if trade.get("isBuyer") else "🔴 SELL"
            price = float(trade.get("price", 0))
            qty = float(trade.get("qty", 0))
            quote_qty = float(trade.get("quoteQty", 0))
            pnl = float(trade.get("realizedPnl", 0)) if "realizedPnl" in trade else 0.0
            commission = float(trade.get("commission", 0))
            commission_asset = trade.get("commissionAsset", "")
            waktu = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(trade.get("time", 0) // 1000))
            balance = get_wallet_balance()

            result = (
                "❌ <b><u><i>📉 LOSS</i></u></b>" if pnl < 0 else
                "✅ <b><u><i>📈 PROFIT</i></u></b>" if pnl > 0 else
                "➖ <b><i>BREAK EVEN</i></b>"
            )

            msg = (
                f"<b>{symbol}</b> | {side}\n"
                f"{result}\n"
                f"Waktu: {waktu}\n"
                f"Harga: {price:.4f} | Size: {qty}\n"
                f"Margin Total: {quote_qty:.2f} USDT\n"
                f"Komisi: {commission} {commission_asset}\n"
                f"PNL: {pnl:.2f} USDT\n\n"
                f"<b>💰 Wallet Sekarang:</b> {balance:.2f} USDT"
            )
            send_message(msg)

            # ✅ Tambahkan ke spreadsheet
            save_to_sheet(sheet, [
                waktu, symbol, side, price, qty,
                quote_qty, commission, commission_asset, pnl, balance
            ])

            time.sleep(2)
        except Exception as err:
            send_message(f"⚠️ Gagal cek {symbol}:\n<pre>{err}</pre>")
            continue

if __name__ == "__main__":
    send_message("🚀 Bot monitoring Margin Binance dimulai...")
    try:
        account_type = detect_account_type()
        send_message(f"🔎 Mode akun terdeteksi: <b>{'Portfolio Margin' if account_type == 'pm' else 'Cross Margin Biasa'}</b>")
    except Exception as e:
        send_message(f"❌ Gagal deteksi akun:\n<pre>{e}</pre>")
        exit()

    while True:
        try:
            monitor_margin_trades()
            time.sleep(15)
        except Exception as e:
            send_message(f"❌ Error:\n<pre>{e}</pre>")
            time.sleep(30)
