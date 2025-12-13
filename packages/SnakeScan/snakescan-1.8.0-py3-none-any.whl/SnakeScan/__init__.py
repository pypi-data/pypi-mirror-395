"""IPv4 address scanner for collecting address information.Scan or get the IPv4 address from the IPv6 host"""

__version__ = "1.8.0"
import socket
from time import sleep
from termcolor import colored
from threading import Thread


class Watcher:
    def __init__(self, host, port_user, timeout=1):
        # Initialized class and variables host, port, and delay.
        self.host = host  # localhost
        self.port_user = port_user  # 80
        self.timeout = timeout  # 2 or 2.0
        self.work = False  # run value

    def run(self):
        # Basic process of connecting to a host and checking the port
        previous = None
        while self.work:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    connection = sock.connect_ex((self.host, self.port_user))
                if previous != connection:
                    if connection == 0:
                        print(
                            f"{colored(f'Service is up {self.host}-->|{self.port_user}|','light_green')}"
                        )
                    else:
                        print(
                            f"{colored(f'Service is down {self.host}-->|{self.port_user}|','light_red')}"
                        )
                    previous = connection
            except Exception as e:
                print(f"Unable to create scanner object:{e}")
            sleep(self.timeout)

    def start(self):
        # Run a port check to see if it is running or offline.
        self.work = True
        self.thread = Thread(target=self.run)
        self.thread.start()

    def stop(self):
        # Stops port checking
        self.work = False
        self.thread.join()
