import asyncio
import random
from playwright.async_api import async_playwright, Playwright

# --- KONFIGURASI ---

# Daftar perangkat yang akan dipilih secara acak.
# Anda bisa menambahkan nama lain dari dokumentasi Playwright.
DEVICES = [ 'Desktop Chrome HiDPI', 'Desktop Edge HiDPI', 
    'Desktop Firefox HiDPI', 'Desktop Safari', 'Desktop Chrome', 'Desktop Edge', 'Desktop Firefox'
]

PROXY_SERVER = "http://as.proxys5.net:6200"
PROXY_USERNAME = "58759783-zone-custom-sessid-Fik6mOzr-sessTime-15"
PROXY_PASSWORD = "AErmBDAD"

# Jumlah browser yang ingin dibuka bersamaan
INSTANCE_COUNT = 2

# Situs web untuk dikunjungi (situs ini akan menampilkan user agent dari perangkat)
TARGET_URL = "https://nusafintech.id/"

# --- FUNGSI ASYNCHRONOUS ---

async def run_instance(playwright: Playwright, instance_id: int):
    """
    Menjalankan satu instance browser dengan emulasi perangkat acak.
    """
    # 1. Pilih perangkat secara acak dari daftar
    selected_device_name = random.choice(DEVICES)
    device = playwright.devices[selected_device_name]
    
    print(f"🚀 [Instance {instance_id}] Memulai dengan perangkat: {selected_device_name}")
    
    browser = None
    try:
        # 2. Luncurkan browser
        browser = await playwright.firefox.launch(headless=False, proxy={
                "server": PROXY_SERVER,
                "username": PROXY_USERNAME,
                "password": PROXY_PASSWORD
            }, firefox_user_prefs={
            "media.peerconnection.enabled": False
        })
        
        # 3. Buat konteks baru dengan meniru perangkat yang dipilih
        context = await browser.new_context(**device)
        
        # Berikan izin lokasi jika ada pop-up (opsional, tapi bagus untuk perangkat mobile)
        await context.grant_permissions(["geolocation"])
        
        page = await context.new_page()
        
        # 4. Kunjungi situs target
        await page.goto(TARGET_URL, timeout=180000)
        
        print(f"   - [Instance {instance_id}] Berhasil membuka halaman dengan perangkat '{selected_device_name}'.")
        
        # Jaga agar browser tetap terbuka agar bisa dilihat
        await asyncio.sleep(420) # Tetap terbuka selama 60 detik

    except Exception as e:
        print(f"❌ [Instance {instance_id}] Terjadi kesalahan: {e}")
    finally:
        if browser:
            await browser.close()
            print(f"✅ [Instance {instance_id}] Browser ditutup.")

async def main():
    """
    Fungsi utama untuk menjalankan semua instance secara paralel.
    """
    async with async_playwright() as p:
        # Buat daftar tugas yang akan dijalankan
        tasks = [run_instance(p, i + 1) for i in range(INSTANCE_COUNT)]
        # Jalankan semua tugas secara bersamaan
        await asyncio.gather(*tasks)

# --- EKSEKUSI SCRIPT ---

if __name__ == "__main__":
    print(f"--- Menjalankan {INSTANCE_COUNT} instance browser secara paralel ---")
    asyncio.run(main())
    print("--- Semua pekerjaan telah selesai. ---")