import socket
import threading,os
from colorama import Fore, init

init()

banner = f"""{Fore.MAGENTA}


    ____  ____  ____  ______   _____ _________    _   ___   ____________ 
   / __ \/ __ \/ __ \/_  __/  / ___// ____/   |  / | / / | / / ____/ __ 
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
                with self.lock:
                    s.send(b'Hello\r\n') 
                    banner = s.recv(1024).decode().strip()
                    if "400 Bad Request" in banner:
                     print(f"[{Fore.GREEN}+{Fore.RESET}] {port} --- OPEN | Invalid Banner")
                     with open("open.txt", "a") as file:
                        file.write(f"{port} \n")
                        file.close()                        
                    else:
                        
                     print(f"[{Fore.GREEN}+{Fore.RESET}] {port} --- OPEN  | Banner -> {banner}")
                     with open("open.txt", "a") as file:
                        file.write(f"{port} \n")
                        file.close()
                        
            s.close()
        except Exception as e:
            with self.lock:
                print(f"[!] Error on port {port}: {e}")

    def scan(self, threads=200):
        print(f"Scanning {self.host} with {threads} threads...\n")
        print(banner)

        def worker():
            while True:
                port = q.get()
                self.scan_port(port)
                q.task_done()

        from queue import Queue
        q = Queue()

        for _ in range(threads):
            t = threading.Thread(target=worker, daemon=True)
            t.start()

        for port in range(1, 65536):
            q.put(port)

        q.join()
        print("\nScan completed.")





cmd = input("Host/IP: ")
cmd2 = int(input("Threads: "))
os.system("cls")
scanner = PortScanner(cmd)
scanner.scan(threads=cmd2)
