Skrip otomatisasi untuk memantau **tiket baru** dari sistem osTicket internal dan mengirimkan notifikasi ke **Telegram** setiap 5 menit.

---

## Fitur
- 🔐 Auto-login ke halaman osTicket internal
- 🔎 Scrape data tiket (ID, subject, pengirim, waktu)
- 📬 Kirim notifikasi ke Telegram (menggunakan Bot API)
- ⚙️ Berjalan tanpa tampilan browser (headless mode)

---

## ⚙️ Persyaratan
- Python >= 3.8
- Google Chrome
- ChromeDriver (otomatis terinstal via `webdriver_manager`)
- Akun Telegram + Bot Token

---