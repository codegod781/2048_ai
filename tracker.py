from socket import *
import threading
import time

class Tracker:
    def __init__(self):
        self.online = []  # List of active peers
        self.stop_event = threading.Event()

    def peer_manager(self, connection, node_address):
        while not self.stop_event.is_set():
            connection.sendall('INA'.encode())
            try:
                connection.recv(2048)
                time.sleep(5.0)
            except connection.timeout:
                self.online.remove(node_address)

def __main__():
    try:
        tracker = Tracker()
        server_address = ('127.0.0.1', 50000)
        node_socket = socket(AF_INET, SOCK_STREAM)
        node_socket.bind(server_address)
        node_socket.listen(5)
        while True:
            connection, node_address = node_socket.accept()
            tracker.append(node_address)
            connection.sendall(tracker.online)
            connection.settimeout(5.0)
            node_thread = threading.Thread(target=tracker.peer_manager, args=(connection , node_address, node_address))
            node_thread.start()
    except KeyboardInterrupt as e:
        print(f"Terminating Tracker...")
        tracker.stop_event.set()
        node_thread.join()
        print(f"Tracker Terminated")