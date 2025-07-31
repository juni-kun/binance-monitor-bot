# Binance Futures Monitor Bot

Bot Python ini memantau transaksi terakhir dari akun Binance Futures dan mengirimkan notifikasi detail ke channel Telegram.

## 📦 Fitur
- Deteksi trade baru (BUY/SELL)
- Menampilkan status PROFIT / LOSS
- Informasi: leverage, margin, entry price, PnL, dan balance setelah trade

## 🚀 Cara Penggunaan

### 1. Siapkan `.env`
Salin dari `.env.example` dan isi data Anda:
```
BINANCE_API_KEY=xxx
BINANCE_API_SECRET=xxx
TELEGRAM_BOT_TOKEN=xxx
```

### 2. Install dependencies
```
pip install requests python-dotenv python-telegram-bot
```

### 3. Jalankan bot
```
python binance.py
```

## 📸 Contoh Output Telegram
```
BTCUSDT | 🟢 LONG
✅ 📈 PROFIT
Waktu: 2025‑07‑25 18:39:12
Leverage: 20x
Size: 0.003 | Harga: 58800.00
Margin Entry: 8.82 USDT
Margin Total: 176.40 USDT
PNL: 4.52 USDT

💰 Wallet Sekarang: 203.89 USDT
```

## 📝 Catatan
- Gunakan akun sub-account ketika testing
- Simpan `last_trade_id` agar tidak hilang saat restart (opsional)
- Tambahkan logging jika ingin analisis performa
