# 📊 Binance Margin Trade Monitor Bot

Bot ini digunakan untuk memantau aktivitas trading **Margin** (termasuk Portfolio Margin) di Binance, mengirimkan notifikasi ke Telegram secara real-time saat ada trade baru, dan mencatat data tersebut ke Google Spreadsheet.

---

## 🚀 Fitur

- Mendeteksi otomatis jenis akun: **Portfolio Margin** atau **Cross Margin**
- Mengambil data trade terbaru dari aset-aset aktif
- Kirim notifikasi Telegram dengan detail:
  - Simbol, arah (BUY/SELL), PNL, waktu, harga, ukuran, komisi
- Menyimpan data trade ke Google Spreadsheet

---

## 📁 Struktur File

```bash
.
├── credentials.json         # Google Service Account key
├── .env                     # Berisi API dan token pribadi
├── monitor_binance.py       # Skrip utama bot

📦 Dependency
Install dependency Python berikut:
pip install python-telegram-bot requests python-dotenv gspread oauth2client

⚙️ Setup
1. .env
Buat file .env:
BINANCE_API_KEY=your_binance_api_key
BINANCE_API_SECRET=your_binance_api_secret
TELEGRAM_BOT_TOKEN=your_telegram_bot_token

2. Google Sheets Setup
Buat file credentials.json dari Google Cloud (Service Account)

Share Spreadsheet ke email Service Account tersebut

Buat Google Sheet bernama Binance Monitor atau sesuaikan di skrip

🖥️ Menjalankan Bot
python monitor_binance.py
Bot akan:

Menampilkan pesan di Telegram bahwa monitoring dimulai

Mendeteksi jenis akun

Mulai memantau trade terbaru dan mengirimkannya ke Telegram + Spreadsheet

🔔 Contoh Notifikasi Telegram
BTCUSDT | 🟢 BUY
✅ 📈 PROFIT
Waktu: 2025-07-30 19:42:12
Harga: 57890.5000 | Size: 0.001
Margin Total: 57.89 USDT
Komisi: 0.03 BNB
PNL: 1.24 USDT

💰 Wallet Sekarang: 843.19 USDT


⚠️ Catatan
Gunakan ID channel atau username Telegram yang benar di CHAT_ID

Delay monitoring: 15 detik per siklus

Trade yang sama tidak akan dikirim 2 kali (dilacak lewat last_trade_id)

Error akan dikirim ke Telegram secara otomatis

🧩 Tips Tambahan
Gunakan PM2 atau screen untuk menjalankan bot terus-menerus

Bisa dijalankan dari PC, VPS, maupun Android dengan Termux

