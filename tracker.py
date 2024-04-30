import pickle
from socket import *
import threading
import time

class Tracker:
    def __init__(self):
        #list of adresses and there current state of connection
        #(address of active peer, itterations since last 'ALIVE' confirmation)
        self.online = [] 
        self.stop_event = threading.Event()

    def peer_manager(self, node_socket):

        while not self.stop_event.is_set():
            data, addr = node_socket.recvfrom(2048)
            
            #if you recieve a new entry
            if data == b'HELLO':
                print("new entry")
                entry = [addr[0], addr[1], 0]
                self.online.append(entry)
                b = 'TRACKER'
                message_to_peers = (b, self.online)
                pickled_list = pickle.dumps(message_to_peers)
                for peer in self.online:
                    print("send to: ", peer)
                    node_socket.sendto(pickled_list, (peer[0], peer[1]))

            #if you recieve confirmation of alive
            if data == b'ALIVE':
                for peer in self.online:
                    peer[2]=peer[2]+1
                    if  addr[1] == peer[1]:
                        peer[2] = 0
                        print("ALIVE:", peer[1])
                    if  peer[2] == 5:
                        print("KILLING:", peer[1])
                        #remove peer 
                        self.online.remove(peer)
                        b = 'TRACKER'
                        message_to_peers = (b, self.online)
                        pickled_list = pickle.dumps(message_to_peers) 
                        for peer in self.online:
                            node_socket.sendto(pickled_list, (peer[0], peer[1]))


            print(self.online)
            time.sleep(1)
            

if __name__ == "__main__":
    try:
        tracker = Tracker()
        server_address = ('127.0.0.1', 50000)
        node_socket = socket(AF_INET, SOCK_DGRAM)
        node_socket.bind(server_address)
        tracker.peer_manager(node_socket)
        while True:
            time.sleep(1)

    except KeyboardInterrupt as e:
        print(f"Terminating Tracker...")
        tracker.stop_event.set()
        print(f"Tracker Terminated")
