import time
import os
import random
import threading
from playwright.sync_api import sync_playwright, Error

# --- KONFIGURASI SCRIPT ---
# URL website yang ingin dikunjungi
TARGET_URL = "https://browserleaks.com" # Situs yang bagus untuk verifikasi
EXTENSION_FOLDER_NAME = "webrtc_control" 
script_dir = os.path.dirname(os.path.abspath(__file__))
PATH_TO_EXTENSION = os.path.join(script_dir, EXTENSION_FOLDER_NAME)
# Daftar proxy baru Anda
PROXY_LIST = [
    "na.proxys5.net:6200:58759783-zone-custom-sessid-tNFrV2ry-sessTime-15:AErmBDAD",
    "na.proxys5.net:6200:58759783-zone-custom-sessid-odpNj6Q4-sessTime-15:AErmBDAD",
    "na.proxys5.net:6200:58759783-zone-custom-sessid-Zu6E962R-sessTime-15:AErmBDAD",
    "na.proxys5.net:6200:58759783-zone-custom-sessid-ZlW8a9st-sessTime-15:AErmBDAD",
    "na.proxys5.net:6200:58759783-zone-custom-sessid-HbtBuIK5-sessTime-15:AErmBDAD",
    "na.proxys5.net:6200:58759783-zone-custom-sessid-HIpCBxgI-sessTime-15:AErmBDAD",
    "na.proxys5.net:6200:58759783-zone-custom-sessid-3nPX0W2T-sessTime-15:AErmBDAD",
    "na.proxys5.net:6200:58759783-zone-custom-sessid-I7f4Sun1-sessTime-15:AErmBDAD",
    "na.proxys5.net:6200:58759783-zone-custom-sessid-pBwxW60O-sessTime-15:AErmBDAD",
    "na.proxys5.net:6200:58759783-zone-custom-sessid-xNm7PYOV-sessTime-15:AErmBDAD",
    "na.proxys5.net:6200:58759783-zone-custom-sessid-eY7geRrf-sessTime-15:AErmBDAD",
    "na.proxys5.net:6200:58759783-zone-custom-sessid-Qi6Zs6Ar-sessTime-15:AErmBDAD",
    "na.proxys5.net:6200:58759783-zone-custom-sessid-yWlgW4xy-sessTime-15:AErmBDAD",
    "na.proxys5.net:6200:58759783-zone-custom-sessid-cJSrk6lZ-sessTime-15:AErmBDAD",
    "na.proxys5.net:6200:58759783-zone-custom-sessid-NpF6zk8P-sessTime-15:AErmBDAD",
    "na.proxys5.net:6200:58759783-zone-custom-sessid-CoHAKrtn-sessTime-15:AErmBDAD",
    "na.proxys5.net:6200:58759783-zone-custom-sessid-LbWoQKsk-sessTime-15:AErmBDAD",
    "na.proxys5.net:6200:58759783-zone-custom-sessid-MlFzwUVF-sessTime-15:AErmBDAD",
    "na.proxys5.net:6200:58759783-zone-custom-sessid-XvA0ffaa-sessTime-15:AErmBDAD",
    "na.proxys5.net:6200:58759783-zone-custom-sessid-HRcqSVIt-sessTime-15:AErmBDAD",
    "na.proxys5.net:6200:58759783-zone-custom-sessid-ltb5Rr00-sessTime-15:AErmBDAD",
    "na.proxys5.net:6200:58759783-zone-custom-sessid-E1SXQt6A-sessTime-15:AErmBDAD",
    "na.proxys5.net:6200:58759783-zone-custom-sessid-zRRivbLh-sessTime-15:AErmBDAD",
    "na.proxys5.net:6200:58759783-zone-custom-sessid-UablYNRs-sessTime-15:AErmBDAD",
    "na.proxys5.net:6200:58759783-zone-custom-sessid-elaY9bhE-sessTime-15:AErmBDAD",
    "na.proxys5.net:6200:58759783-zone-custom-sessid-hsJ9vgAB-sessTime-15:AErmBDAD",
    "na.proxys5.net:6200:58759783-zone-custom-sessid-kiLdj2Sg-sessTime-15:AErmBDAD",
    "na.proxys5.net:6200:58759783-zone-custom-sessid-OEjRi6Do-sessTime-15:AErmBDAD",
    "na.proxys5.net:6200:58759783-zone-custom-sessid-nBjGYcjk-sessTime-15:AErmBDAD",
    "na.proxys5.net:6200:58759783-zone-custom-sessid-OBG0URc5-sessTime-15:AErmBDAD",
    "na.proxys5.net:6200:58759783-zone-custom-sessid-Upi2fHqJ-sessTime-15:AErmBDAD",
    "na.proxys5.net:6200:58759783-zone-custom-sessid-55ROSWhB-sessTime-15:AErmBDAD",
    "na.proxys5.net:6200:58759783-zone-custom-sessid-mRMWEJt9-sessTime-15:AErmBDAD",
    "na.proxys5.net:6200:58759783-zone-custom-sessid-utqbFFle-sessTime-15:AErmBDAD",
    "na.proxys5.net:6200:58759783-zone-custom-sessid-UjcrJw8P-sessTime-15:AErmBDAD",
    "na.proxys5.net:6200:58759783-zone-custom-sessid-sAg3tlBQ-sessTime-15:AErmBDAD",
    "na.proxys5.net:6200:58759783-zone-custom-sessid-yBdCLuex-sessTime-15:AErmBDAD",
    "na.proxys5.net:6200:58759783-zone-custom-sessid-C7Yczr2Y-sessTime-15:AErmBDAD",
    "na.proxys5.net:6200:58759783-zone-custom-sessid-Q9vlvdoh-sessTime-15:AErmBDAD",
    "na.proxys5.net:6200:58759783-zone-custom-sessid-Ldt4r0W5-sessTime-15:AErmBDAD",
    "na.proxys5.net:6200:58759783-zone-custom-sessid-E5ecOvIm-sessTime-15:AErmBDAD",
    "na.proxys5.net:6200:58759783-zone-custom-sessid-khB1I4DP-sessTime-15:AErmBDAD",
    "na.proxys5.net:6200:58759783-zone-custom-sessid-EpFTV5Eo-sessTime-15:AErmBDAD",
    "na.proxys5.net:6200:58759783-zone-custom-sessid-F6T5v8uf-sessTime-15:AErmBDAD",
    "na.proxys5.net:6200:58759783-zone-custom-sessid-Kl4ohrys-sessTime-15:AErmBDAD",
    "na.proxys5.net:6200:58759783-zone-custom-sessid-7u9sB11X-sessTime-15:AErmBDAD",
    "na.proxys5.net:6200:58759783-zone-custom-sessid-Hn3sOk1n-sessTime-15:AErmBDAD",
    "na.proxys5.net:6200:58759783-zone-custom-sessid-hl3YTx6s-sessTime-15:AErmBDAD",
    "na.proxys5.net:6200:58759783-zone-custom-sessid-tmnJI8Es-sessTime-15:AErmBDAD",
    "na.proxys5.net:6200:58759783-zone-custom-sessid-pxy2Lcwj-sessTime-15:AErmBDAD",
    "na.proxys5.net:6200:58759783-zone-custom-sessid-HqmYgF7q-sessTime-15:AErmBDAD",
    "na.proxys5.net:6200:58759783-zone-custom-sessid-nmRskT6W-sessTime-15:AErmBDAD",
    "na.proxys5.net:6200:58759783-zone-custom-sessid-hPJGVUcy-sessTime-15:AErmBDAD",
    "na.proxys5.net:6200:58759783-zone-custom-sessid-jVq2gtrq-sessTime-15:AErmBDAD",
    "na.proxys5.net:6200:58759783-zone-custom-sessid-Ohaff14a-sessTime-15:AErmBDAD",
    "na.proxys5.net:6200:58759783-zone-custom-sessid-sI7GPpj0-sessTime-15:AErmBDAD",
    "na.proxys5.net:6200:58759783-zone-custom-sessid-Fq99dtnn-sessTime-15:AErmBDAD",
    "na.proxys5.net:6200:58759783-zone-custom-sessid-ilUFRHFX-sessTime-15:AErmBDAD",
    "na.proxys5.net:6200:58759783-zone-custom-sessid-8tGFtYw4-sessTime-15:AErmBDAD",
    "na.proxys5.net:6200:58759783-zone-custom-sessid-u91sbNbO-sessTime-15:AErmBDAD",
    "na.proxys5.net:6200:58759783-zone-custom-sessid-PprGNh1M-sessTime-15:AErmBDAD",
    "na.proxys5.net:6200:58759783-zone-custom-sessid-XDi4QyQf-sessTime-15:AErmBDAD",
    "na.proxys5.net:6200:58759783-zone-custom-sessid-acp2pZtR-sessTime-15:AErmBDAD",
    "na.proxys5.net:6200:58759783-zone-custom-sessid-hcizbWum-sessTime-15:AErmBDAD",
    "na.proxys5.net:6200:58759783-zone-custom-sessid-ygceUfHQ-sessTime-15:AErmBDAD",
    "na.proxys5.net:6200:58759783-zone-custom-sessid-shlO84nw-sessTime-15:AErmBDAD",
    "na.proxys5.net:6200:58759783-zone-custom-sessid-ClkUhg5E-sessTime-15:AErmBDAD",
    "na.proxys5.net:6200:58759783-zone-custom-sessid-euZFBBI7-sessTime-15:AErmBDAD",
    "na.proxys5.net:6200:58759783-zone-custom-sessid-RYazX6ZS-sessTime-15:AErmBDAD",
    "na.proxys5.net:6200:58759783-zone-custom-sessid-SHxTzSaE-sessTime-15:AErmBDAD",
    "na.proxys5.net:6200:58759783-zone-custom-sessid-BjYgUm9a-sessTime-15:AErmBDAD",
    "na.proxys5.net:6200:58759783-zone-custom-sessid-kpQYGntD-sessTime-15:AErmBDAD",
    "na.proxys5.net:6200:58759783-zone-custom-sessid-ScWuBazG-sessTime-15:AErmBDAD",
    "na.proxys5.net:6200:58759783-zone-custom-sessid-zPcN7A1a-sessTime-15:AErmBDAD",
    "na.proxys5.net:6200:58759783-zone-custom-sessid-iY9unbeu-sessTime-15:AErmBDAD",
    "na.proxys5.net:6200:58759783-zone-custom-sessid-HAg9xHHU-sessTime-15:AErmBDAD",
    "na.proxys5.net:6200:58759783-zone-custom-sessid-7ik6jRlQ-sessTime-15:AErmBDAD",
    "na.proxys5.net:6200:58759783-zone-custom-sessid-jYPDJ2eQ-sessTime-15:AErmBDAD",
    "na.proxys5.net:6200:58759783-zone-custom-sessid-CYvpSnsm-sessTime-15:AErmBDAD",
    "na.proxys5.net:6200:58759783-zone-custom-sessid-2UE9aPti-sessTime-15:AErmBDAD",
    "na.proxys5.net:6200:58759783-zone-custom-sessid-HLj5htIE-sessTime-15:AErmBDAD",
    "na.proxys5.net:6200:58759783-zone-custom-sessid-7xULRQZK-sessTime-15:AErmBDAD",
    "na.proxys5.net:6200:58759783-zone-custom-sessid-w7creRen-sessTime-15:AErmBDAD",
    "na.proxys5.net:6200:58759783-zone-custom-sessid-hGun0awq-sessTime-15:AErmBDAD",
    "na.proxys5.net:6200:58759783-zone-custom-sessid-VUhMsU3Y-sessTime-15:AErmBDAD",
    "na.proxys5.net:6200:58759783-zone-custom-sessid-d6OKpDiY-sessTime-15:AErmBDAD",
    "na.proxys5.net:6200:58759783-zone-custom-sessid-15wAstGd-sessTime-15:AErmBDAD",
    "na.proxys5.net:6200:58759783-zone-custom-sessid-qKlUqyGS-sessTime-15:AErmBDAD",
    "na.proxys5.net:6200:58759783-zone-custom-sessid-xbdmJzAL-sessTime-15:AErmBDAD",
    "na.proxys5.net:6200:58759783-zone-custom-sessid-HCBsxqCI-sessTime-15:AErmBDAD",
    "na.proxys5.net:6200:58759783-zone-custom-sessid-9BNAxaQB-sessTime-15:AErmBDAD",
    "na.proxys5.net:6200:58759783-zone-custom-sessid-IqjAlFz9-sessTime-15:AErmBDAD",
    "na.proxys5.net:6200:58759783-zone-custom-sessid-jjRzguAu-sessTime-15:AErmBDAD",
    "na.proxys5.net:6200:58759783-zone-custom-sessid-CrKDrjZj-sessTime-15:AErmBDAD",
    "na.proxys5.net:6200:58759783-zone-custom-sessid-Qy9kcoFS-sessTime-15:AErmBDAD",
    "na.proxys5.net:6200:58759783-zone-custom-sessid-Pl0V1gmE-sessTime-15:AErmBDAD",
    "na.proxys5.net:6200:58759783-zone-custom-sessid-EhdPOfoB-sessTime-15:AErmBDAD",
    "na.proxys5.net:6200:58759783-zone-custom-sessid-jcatCsv1-sessTime-15:AErmBDAD",
    "na.proxys5.net:6200:58759783-zone-custom-sessid-ExYZvkQK-sessTime-15:AErmBDAD",
    "na.proxys5.net:6200:58759783-zone-custom-sessid-86NNAghO-sessTime-15:AErmBDAD",
]
DURATION_MINUTES = 7
NUM_INSTANCES = 2
# --- AKHIR KONFIGURASI ---

# Daftar device yang Anda minta untuk dirotasi
USER_REQUESTED_DEVICES = [
    'Blackberry PlayBook', 'Blackberry PlayBook landscape', 'BlackBerry Z30', 
    'BlackBerry Z30 landscape', 'Galaxy Note 3', 'Galaxy Note 3 landscape', 
    'Galaxy Note II', 'Galaxy Note II landscape', 'Galaxy S III', 
    'Galaxy S III landscape', 'Galaxy S5', 'Galaxy S5 landscape', 'Galaxy S8', 
    'Galaxy S8 landscape', 'Galaxy S9+', 'Galaxy S9+ landscape', 'Galaxy S24', 
    'Galaxy S24 landscape', 'Galaxy A55', 'Galaxy A55 landscape', 'Galaxy Tab S4', 
    'Galaxy Tab S4 landscape', 'Galaxy Tab S9', 'Galaxy Tab S9 landscape', 
    'iPad (gen 5)', 'iPad (gen 5) landscape', 'iPad (gen 6)', 
    'iPad (gen 6) landscape', 'iPad (gen 7)', 'iPad (gen 7) landscape', 'iPad (gen 11)',
    'iPad (gen 11) landscape', 'iPad Mini', 'iPad Mini landscape', 'iPad Pro 11', 
    'iPad Pro 11 landscape', 'iPhone 6', 'iPhone 6 landscape', 'iPhone 6 Plus', 
    'iPhone 6 Plus landscape', 'iPhone 7', 'iPhone 7 landscape', 'iPhone 7 Plus', 
    'iPhone 7 Plus landscape', 'iPhone 8', 'iPhone 8 landscape', 'iPhone 8 Plus', 
    'iPhone 8 Plus landscape', 'iPhone SE', 'iPhone SE landscape', 'iPhone SE (3rd gen)',
    'iPhone SE (3rd gen) landscape', 'iPhone X', 'iPhone X landscape', 'iPhone XR', 
    'iPhone XR landscape', 'iPhone 11', 'iPhone 11 landscape', 'iPhone 11 Pro', 
    'iPhone 11 Pro landscape', 'iPhone 11 Pro Max', 'iPhone 11 Pro Max landscape', 
    'iPhone 12', 'iPhone 12 landscape', 'iPhone 12 Pro', 'iPhone 12 Pro landscape', 
    'iPhone 12 Pro Max', 'iPhone 12 Pro Max landscape', 'iPhone 12 Mini', 
    'iPhone 12 Mini landscape', 'iPhone 13', 'iPhone 13 landscape', 'iPhone 13 Pro', 
    'iPhone 13 Pro landscape', 'iPhone 13 Pro Max', 'iPhone 13 Pro Max landscape', 
    'iPhone 13 Mini', 'iPhone 13 Mini landscape', 'iPhone 14', 'iPhone 14 landscape', 
    'iPhone 14 Plus', 'iPhone 14 Plus landscape', 'iPhone 14 Pro', 
    'iPhone 14 Pro landscape', 'iPhone 14 Pro Max', 'iPhone 14 Pro Max landscape', 
    'iPhone 15', 'iPhone 15 landscape', 'iPhone 15 Plus', 'iPhone 15 Plus landscape', 
    'iPhone 15 Pro', 'iPhone 15 Pro landscape', 'iPhone 15 Pro Max', 
    'iPhone 15 Pro Max landscape', 'Kindle Fire HDX', 'Kindle Fire HDX landscape', 
    'LG Optimus L70', 'LG Optimus L70 landscape', 'Microsoft Lumia 550', 'Microsoft Lumia 550 landscape',
    'Microsoft Lumia 950', 'Microsoft Lumia 950 landscape', 'Nexus 10', 
    'Nexus 10 landscape', 'Nexus 4', 'Nexus 4 landscape', 'Nexus 5', 
    'Nexus 5 landscape', 'Nexus 5X', 'Nexus 5X landscape', 'Nexus 6', 
    'Nexus 6 landscape', 'Nexus 6P', 'Nexus 6P landscape', 'Nexus 7', 
    'Nexus 7 landscape', 'Nokia Lumia 520', 'Nokia Lumia 520 landscape', 
    'Nokia N9', 'Nokia N9 landscape', 'Pixel 2', 'Pixel 2 landscape', 
    'Pixel 2 XL', 'Pixel 2 XL landscape', 'Pixel 3', 'Pixel 3 landscape', 
    'Pixel 4', 'Pixel 4 landscape', 'Pixel 4a (5G)', 'Pixel 4a (5G) landscape', 
    'Pixel 5', 'Pixel 5 landscape', 'Pixel 7', 'Pixel 7 landscape', 'Moto G4', 
    'Moto G4 landscape', 'Desktop Chrome HiDPI', 'Desktop Edge HiDPI', 
    'Desktop Firefox HiDPI', 'Desktop Safari', 'Desktop Chrome', 'Desktop Edge', 'Desktop Firefox'
]

def get_valid_devices(playwright_instance):
    """Memfilter daftar device, hanya menyisakan yang didukung Playwright."""
    supported_devices = playwright_instance.devices
    valid_devices = [name for name in USER_REQUESTED_DEVICES if name in supported_devices]
    # ... (logika untuk melewati device yang tidak ditemukan bisa ditambahkan di sini)
    return valid_devices

def run_instance(instance_id: int, proxy_str: str, device_name: str):
    """Fungsi untuk menjalankan satu instance browser dengan rotasi."""
    print(f"--- [Instance {instance_id}] Memulai ---")
    
    try:
        # Format proxy baru: host:port:user:pass
        host, port, user, password = proxy_str.strip().split(':')
    except ValueError:
        print(f"❌ [Instance {instance_id}] Format proxy salah. Membatalkan.")
        return

    browser = None
    try:
        with sync_playwright() as p:
            device_config = p.devices[device_name]
            
            print(f"[Instance {instance_id}] Menggunakan Proxy: {host}:{port}")
            print(f"[Instance {instance_id}] Emulasi Device: {device_name}")

            browser = p.chromium.launch_persistent_context(
                headless=False,
                proxy={
                    # --- PERUBAHAN 1: Gunakan 'socks5' untuk proxy jenis ini ---
                    "server": f"socks5://{host}:{port}",
                    "username": user,
                    "password": password
                },
                args=[
                    # Argumen untuk memuat ekstensi dari path yang ditentukan
                    f'--load-extension={PATH_TO_EXTENSION}',
                    # Argumen (opsional) untuk memastikan hanya ekstensi ini yang dimuat
                    f'--disable-extensions-except={PATH_TO_EXTENSION}',
                ]
            )

            # --- PERUBAHAN 2: Emulasi lokasi dinonaktifkan, kembali ke emulasi device saja ---
            context = browser.new_context(**device_config)
            page = context.new_page()
            
            print(f"[Instance {instance_id}] Mengunjungi: {TARGET_URL} untuk verifikasi...")
            page.goto(TARGET_URL, wait_until="domcontentloaded", timeout=90000)
            
            print(f"✅ [Instance {instance_id}] Berhasil. Browser akan ditutup dalam {DURATION_MINUTES} menit.")
            time.sleep(DURATION_MINUTES * 60)
            
            print(f"⏹️ [Instance {instance_id}] Waktu habis. Menutup browser.")

    except Error as e:
        print(f"❌ [Instance {instance_id}] Error Playwright: {e}")
    except Exception as e:
        print(f"❌ [Instance {instance_id}] Error umum: {e}")
    finally:
        if browser:
            browser.close()

if __name__ == "__main__":
    if not PROXY_LIST or not PROXY_LIST[0]:
        print("⚠️ Peringatan: Daftar proxy kosong.")
    else:
        with sync_playwright() as p:
            VALID_DEVICES = get_valid_devices(p)

        if not VALID_DEVICES:
            print("❌ Error: Tidak ada device valid yang bisa digunakan.")
        else:
            threads = []
            print(f"🚀 Memulai {NUM_INSTANCES} instance browser...")
            for i in range(NUM_INSTANCES):
                random_proxy = random.choice(PROXY_LIST)
                random_device_name = random.choice(VALID_DEVICES)
                thread = threading.Thread(target=run_instance, args=(i + 1, random_proxy, random_device_name))
                threads.append(thread)
                thread.start()
                time.sleep(3)
            
            for thread in threads:
                thread.join()
            
            print("🎉 Semua pekerjaan telah selesai.")