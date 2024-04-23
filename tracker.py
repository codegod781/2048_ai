import pickle
from socket import *
import threading
import time

class Tracker:
    def __init__(self):
        #list of adresses and there current state of connection
        #(address of active peer, itterations 'ALIVE' confirmation)
        self.online = []  # List of active peers
        self.stop_event = threading.Event()

    # def peer_manager(self, connection, node_address):
    def peer_manager(self, node_socket):
        # while not self.stop_event.is_set():
        #     connection.sendall('INA'.encode())
        #     try:
        #         connection.recv(2048)
        #         time.sleep(5.0)
        #     except connection.timeout:
        #         self.online.remove(node_address)

        while not self.stop_event.is_set():
            data, addr = node_socket.recvfrom(2048)
            if data == b'INA':
                entry = [addr[1], 0]
                self.online.append(entry)
                pickled_list = pickle.dumps(self.online)
                node_socket.sendto(pickled_list, addr)
            if data == b'ALIVE':
                for peer in self.online:
                    peer[1]=peer[1]+1
                    if addr[1] == peer[0]:
                        peer[1] = 0
                        print("ALIVE:", peer[0])
                    if peer[1] == 5:
                        print("KILLING:", peer[0])
                        self.online.remove(peer)

            print(self.online)
            time.sleep(1)
            

if __name__ == "__main__":
    print("running")
    try:
        tracker = Tracker()
        server_address = ('127.0.0.1', 50000)
        # node_socket = socket(AF_INET, SOCK_STREAM)
        node_socket = socket(AF_INET, SOCK_DGRAM)
        node_socket.bind(server_address)
        tracker.peer_manager(node_socket)
        # node_thread = threading.Thread(target=tracker.peer_manager, args=(connection , node_address, node_address))
        # node_thread = threading.Thread(target=tracker.peer_manager, args=(node_socket,))
        # node_thread.start()
        # node_socket.listen(5)
        while True:
            # connection, node_address = node_socket.accept()
            # tracker.append(node_address)
            # connection.sendall(tracker.online)
            # connection.settimeout(5.0)
            # node_thread = threading.Thread(target=tracker.peer_manager, args=(connection , node_address, node_address))
            # node_thread.start()
            time.sleep(1)
    except KeyboardInterrupt as e:
        print(f"Terminating Tracker...")
        tracker.stop_event.set()
        # node_thread.join()
        print(f"Tracker Terminated")

# if __name__ == "__main__":
#     main()