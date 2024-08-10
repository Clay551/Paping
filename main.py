import socket
import argparse
import time
import statistics
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, init
import colorama
import pyfiglet
import os
if os.name == 'nt':
    os.system('cls')
else:
    os.system('clear')
        

class PaPing:
    def __init__(self, host, port, count=4, timeout=0.5, interval=1.0):
        self.host = host
        self.port = port
        self.count = count
        self.timeout = timeout
        self.interval = interval
        self.results = []

    def ping(self):
        start_time = time.time()
        try:
            with socket.create_connection((self.host, self.port), self.timeout) as sock:
                end_time = time.time()
                latency = (end_time - start_time) * 1000  
                return True, latency
        except (socket.timeout, ConnectionRefusedError):
            return False, None
        except Exception as e:
            print(f"An error occurred: {e}")
            return False, None

    def run(self):
        print(colorama.Fore.RED)
        pyfiglet.print_figlet("Asylum")
        print(colorama.Fore.LIGHTCYAN_EX)
        print(f"PaPing {self.host}:{self.port}")
        print(f"Sending {self.count} TCP ping(s):")
        print(colorama.Fore.RESET)

        with ThreadPoolExecutor(max_workers=1) as executor:
            for i in range(self.count):
                future = executor.submit(self.ping)
                success, latency = future.result()
                
                if success:
                    print(colorama.Fore.GREEN)
                    print(f"Connected to {colorama.Fore.RESET}{self.host}:{self.port}{colorama.Fore.MAGENTA} time={colorama.Fore.RESET}{latency:.2f}ms")
                    self.results.append(latency)
                else:
                    print(colorama.Fore.RED)
                    print(f"Connection Timeout")
                    print(colorama.Fore.RESET)
                if i < self.count - 1:
                    time.sleep(self.interval)

        self.print_statistics()

    def print_statistics(self):
        if not self.results:
            print("\nNo successful connections.")
            return

        print("\nTCP ping statistics:")
        print(f"  Sent = {self.count}, Successful = {len(self.results)}, Failed = {self.count - len(self.results)}")
        print(f"  Minimum = {min(self.results):.2f}ms, Maximum = {max(self.results):.2f}ms, Average = {statistics.mean(self.results):.2f}ms")
        if len(self.results) > 1:
            print(f"  Standard Deviation = {statistics.stdev(self.results):.2f}ms")

def main():
    parser = argparse.ArgumentParser(description="Advanced TCP Port Pinging Tool")
    parser.add_argument("host", help="Target host to ping")
    parser.add_argument("port", type=int, help="Target port to ping")
    parser.add_argument("-c", "--count", type=int, default=100, help="Number of pings to send")
    parser.add_argument("-t", "--timeout", type=float, default=0.5, help="Timeout in seconds for each ping")
    parser.add_argument("-i", "--interval", type=float, default=1.0, help="Interval between pings in seconds")

    args = parser.parse_args()

    paping = PaPing(args.host, args.port, args.count, args.timeout, args.interval)
    paping.run()

if __name__ == "__main__":
    main()
