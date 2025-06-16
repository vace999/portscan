import socket
import threading
import os
from colorama import Fore, init
from queue import Queue

init()

ascii_banner = f"""{Fore.MAGENTA}

    ____  ____  ____  ______   _____ _________    _   ___   ____________ 
   / __ \/ __ \/ __ \/_  __/  / ___// ____/   |  / | / / | / / ____/ __ \\
  / /_/ / / / / /_/ / / /     \__ \/ /   / /| | /  |/ /  |/ / __/ / /_/ /
 / ____/ /_/ / _, _/ / /     ___/ / /___/ ___ |/ /|  / /|  / /___/ _, _/ 
/_/    \____/_/ |_| /_/     /____/\____/_/  |_/_/ |_/_/ |_/_____/_/ |_|  

                                                           Coded by @belmala
{Fore.RESET}
"""

class PortScanner:
    def __init__(self, host):
        self.host = host
        self.lock = threading.Lock()

    def scan_port(self, port):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.2)
            result = s.connect_ex((self.host, port))
            if result == 0:
                try:
                    s.send(b'Hello\r\n')
                    banner = s.recv(1024).decode(errors="ignore").strip()
                except:
                    banner = "No banner received"

                with self.lock:
                    if "400 Bad Request" in banner:
                        print(f"[{Fore.GREEN}+{Fore.RESET}] {port} --- OPEN | Invalid Banner")
                    else:
                        print(f"[{Fore.GREEN}+{Fore.RESET}] {port} --- OPEN  | Banner -> {banner}")

                    with open("open.txt", "a") as file:
                        file.write(f"{port}\n")
            s.close()
        except Exception as e:
            with self.lock:
                print(f"[!] Error on port {port}: {e}")

    def scan(self, threads=200):
        print(f"Scanning {self.host} with {threads} threads...\n")
        print(ascii_banner)

        from queue import Queue
        q = Queue()

        def worker():
            while True:
                port = q.get()
                self.scan_port(port)
                q.task_done()

        for _ in range(threads):
            t = threading.Thread(target=worker, daemon=True)
            t.start()

        for port in range(1, 65536):
            q.put(port)

        q.join()
        print("\nScan completed.")


# === Main Runtime ===
cmd = input("Host/IP: ")
cmd2 = int(input("Threads: "))
os.system("cls" if os.name == "nt" else "clear")

scanner = PortScanner(cmd)
scanner.scan(threads=cmd2)
