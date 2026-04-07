import socket
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, init

init(autoreset=True)

def scan(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.1)
            if s.connect_ex((ip, port)) == 0:
                print(f"{Fore.GREEN}[+] SUCCESS: Port {port} is OPEN")
    except: pass

target = input(f"{Fore.CYAN}Target IP: ")
with ThreadPoolExecutor(max_workers=100) as ex:
    for p in range(1, 1025):
        ex.submit(scan, target, p)
