# 📊 Binance Margin Trade Monitor Bot
Bot ini digunakan untuk memantau aktivitas trading Margin (termasuk Portfolio Margin) di Binance, mengirimkan notifikasi ke Telegram secara real-time saat ada trade baru, dan mencatat data tersebut ke Google Spreadsheet..

## 📦 Fitur
- Mendeteksi secara otomatis jenis akun: Portfolio Margin atau Cross Margin Biasa
- Mengambil data transaksi terakhir dari semua aset aktif (yang memiliki saldo/borrow)
- Mengirimkan notifikasi Telegram yang dilengkapi dengan:
- Simbol
- Arah trade (BUY / SELL)
- Profit / Loss
- Waktu transaksi
- Ukuran dan harga
- Komisi dan PNL
- Total wallet balance saat ini
- Menyimpan log ke Google Spreadsheet secara otomatis

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
pip install python-telegram-bot requests python-dotenv gspread oauth2client

```

### 3. Jalankan bot
```
python monitor_binance.py

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

## 🧩 Catatan
Jika terjadi kesalahan saat mengambil data dari API, pesan error akan dikirim ke Telegram.
Trade terakhir disimpan dengan last_trade_id sehingga trade yang sama tidak dikirim berulang.
Loop utama memiliki delay 15 detik per siklus

## 💡 Tips Tambahan
Ubah CHAT_ID menjadi ID atau username Telegram channel kamu (dengan awalan @).

Gunakan layanan seperti PM2 atau supervisord untuk menjalankan bot ini secara terus-menerus.

## 📬 Lisensi
Skrip ini bebas digunakan dan dimodifikasi untuk keperluan pribadi. Dilarang diperjualbelikan tanpa izin.
