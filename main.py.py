import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# === KONFIGURASI ===
USERNAME = ""
PASSWORD = ""
URL_LOGIN = ""
URL_TICKETS = ""

TELEGRAM_BOT_TOKEN = ""
TELEGRAM_CHAT_ID = ""

# === SETUP SELENIUM (HEADLESS MODE) ===
chrome_options = Options()
chrome_options.add_argument("--headless")  # Mode tanpa GUI
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Mulai browser
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# === LOGIN KE WEBSITE ===
def login():
    print("🔹 Membuka halaman login...")
    driver.get(URL_LOGIN)
    time.sleep(2)  # Tunggu loading
    
    try:
        # Masukkan username & password
        print("🔹 Mengisi form login...")
        driver.find_element(By.NAME, "userid").send_keys(USERNAME)
        driver.find_element(By.NAME, "passwd").send_keys(PASSWORD)
        driver.find_element(By.NAME, "passwd").send_keys(Keys.RETURN)
        time.sleep(3)

        # Cek apakah login berhasil atau gagal
        try:
            error_message = driver.find_element(By.CLASS_NAME, "error-message").text
            print(f"❌ Login gagal: {error_message}")
            return False
        except:
            print("✅ Login berhasil!")
            return True

    except Exception as e:
        print(f"⚠️ Error saat login: {e}")
        return False

# === CEK SEMUA TIKET BARU ===
def check_new_tickets():
    print("🔹 Mengecek tiket terbaru...")
    driver.get(URL_TICKETS)
    time.sleep(2)

    try:
        # Ambil semua elemen tiket
        tickets = driver.find_elements(By.CSS_SELECTOR, "a.Icon.webTicket.preview")
        subjects = driver.find_elements(By.CSS_SELECTOR, "div.link.truncate")
        senders = driver.find_elements(By.CSS_SELECTOR, "span.truncate")
        last_updates = driver.find_elements(By.XPATH, "//td[@align='center']")  # Mengambil elemen last update
        
        # Jika tidak ada tiket baru, hentikan proses
        if not tickets:
            print("✅ Tidak ada tiket baru.")
            return

        # Buat daftar tiket dalam format teks
        messages = ["🔔 **Daftar Tiket Baru** 🔔"]
        for i in range(len(tickets)):
            try:
                ticket_url = tickets[i].get_attribute("href")  # Ambil URL tiket
                ticket_id = ticket_url.split("=")[-1]  # Ambil ID tiket
                ticket_subject = subjects[i].text.strip() if i < len(subjects) else "Tidak ada subject"
                ticket_sender = senders[i].text.strip() if i < len(senders) else "Tidak ada nama"
                ticket_last_update = last_updates[i].text.strip() if i < len(last_updates) else "Tidak ada update"
                
                messages.append(
                    f"📌 **ID:** {ticket_id}\n"
                    f"📄 **Subject:** {ticket_subject}\n"
                    f"👤 **Dari:** {ticket_sender}\n"
                    f"🕒 **Last Updated:** {ticket_last_update}\n"
                    f"🔗 **Link:** {ticket_url}\n"
                    "--------------------"
                )
            except Exception as e:
                print(f"⚠️ Error saat mengambil detail tiket: {e}")

        # Kirim ke Telegram
        send_telegram_message("\n".join(messages))

    except Exception as e:
        print(f"⚠️ Error saat mengambil tiket: {e}")

# === KIRIM NOTIFIKASI TELEGRAM ===
def send_telegram_message(message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        data = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
        response = requests.post(url, data=data)
        if response.status_code == 200:
            print("✅ Notifikasi terkirim ke Telegram.")
        else:
            print(f"⚠️ Gagal mengirim notifikasi. Status: {response.status_code}")
    except Exception as e:
        print(f"⚠️ Error saat mengirim pesan Telegram: {e}")

# === LOOP CEK SETIAP 5 MENIT ===
if __name__ == "__main__":
    if login():
        while True:
            check_new_tickets()
            print("⏳ Menunggu 5 menit sebelum cek ulang...\n")
            time.sleep(300)  # Cek setiap 5 menit
    else:
        print("❌ Program dihentikan karena login gagal.")
