import socket
import concurrent.futures
import argparse
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def parse_arguments():
    parser = argparse.ArgumentParser(description='Advanced Port Scanner')
    parser.add_argument('ip', type=str, help='IP address to scan')
    parser.add_argument('--start-port', type=int, default=1, help='Starting port number (default: 1)')
    parser.add_argument('--end-port', type=int, default=65535, help='Ending port number (default: 65535)')
    parser.add_argument('--threads', type=int, default=100, help='Number of threads to use (default: 100)')
    parser.add_argument('--timeout', type=float, default=1.0, help='Socket timeout in seconds (default: 1.0)')
    return parser.parse_args()

def scan_port(ip, port, timeout):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(timeout)
        result = sock.connect_ex((ip, port))
        return port, result == 0

def port_scanner(ip, start_port, end_port, max_threads, timeout):
    ports = range(start_port, end_port + 1)
    open_ports = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = {executor.submit(scan_port, ip, port, timeout): port for port in ports}
        for future in concurrent.futures.as_completed(futures):
            port, is_open = future.result()
            if is_open:
                open_ports.append(port)
                logging.info(f"Port {port} is open")

    logging.info(f"Scan completed at {datetime.now()}")
    logging.info(f"Open ports: {open_ports}")
    return open_ports

def main():
    args = parse_arguments()
    logging.info(f"Starting scan on {args.ip} from port {args.start_port} to {args.end_port} with {args.threads} threads")
    open_ports = port_scanner(args.ip, args.start_port, args.end_port, args.threads, args.timeout)
    logging.info(f"Open ports found: {open_ports}")

if __name__ == "__main__":
    main()