
# peer_to_peer_network

import threading
from tracker import Tracker
from socket import *
from blockchain_wallet import BlockchainWallet
import pickle
import time


class Peer:
    def __init__(self):

        self.node_socket = socket(AF_INET, SOCK_DGRAM)
        self.port = self.node_socket.getsockname()[1]
        self.tracker_address = ('127.0.0.1', 50000)
        self.blockchain_wallet = BlockchainWallet(mining_complexity=2)
        # self.peer_socket = socket(AF_INET, SOCK_DGRAM)
        # self.peer_address = ('127.0.0.1', 50001)
        # self.my_port = self.peer_socket.getsockname()
        # print("port : ", self.my_port) 
        self.connections = []
        # self.blockchain = BlockchainWallet()


        # tracker should have its own class

    def connect_tracker(self):
        print("tracker addr: ", self.tracker_address)
        self.node_socket.sendto(b'HELLO', self.tracker_address)
        data, addr = self.node_socket.recvfrom(1024)
        deserialized_data = pickle.loads(data)
        header = deserialized_data[0]
        print("header : ", header)
        list = deserialized_data[1]
        i=0
        self.connections.clear()
        for entry in list:
            self.connections.append((entry[0], entry[1]))
        print("list :", self.connections)

        
    def add_connection(self, peer):
        # Add a new peer to the network
        self.tracker.append(peer)
        pass

    def remove_connection(self, peer):
        # Remove a peer from the network
        self.tracker.pop(peer)
        pass

    def broadcast_to_peers(self):
        print("broadcasting")
        print("my port is : ", self.node_socket.getsockname()[1])
        while True:
            for entry in self.connections:
                if entry[1] != self.node_socket.getsockname()[1]:
                    print('peer address: ', entry)
                    b = b'PEER'
                    message = "hello from " + str(self.node_socket.getsockname()[1])
                    message_to_peers = (b, message)
                    pickled_payload = pickle.dumps(message_to_peers) 
                    self.node_socket.sendto(pickled_payload, entry)
                time.sleep(2)

    def receive_from_peers(self):
        print("recieving")
        while True:
            data, _ = self.node_socket.recvfrom(1024)
            decoded_data = pickle.loads(data)
            header = decoded_data[0]
            payload = decoded_data[1]
        
            if header == b'TRACKER': #up-to-date list from tracker
                i=0
                self.connections.clear()
                for entry in payload:
                    self.connections.append((entry[0], entry[1]))
                print("list :", self.connections)
            if header == b'PEER':
                print("Node "self.node_socket.getsockname)
                BlockchainWallet.receive_data(payload, ((self.node_socket.getsockname()[0], self.node_socket.getsockname()[1])))
                print(payload)



                

    def compare_last_hash(self):
        # Compare the last hash in each blockchain against peers
        pass

    def ping_tracker(self, tracker_address, node_socket):

        while True:
            node_socket.sendto(b'ALIVE', tracker_address)
            time.sleep(2)



if __name__ == "__main__":
    try:
        peer = Peer()
        peer.connect_tracker()


        node_thread = threading.Thread(target = peer.ping_tracker, args=(peer.tracker_address, peer.node_socket,))
        node_thread.start()   

        peer_thread = threading.Thread(target = peer.receive_from_peers, args=())
        peer_thread.start()

        peer.broadcast_to_peers()

        # peer_thread = threading.Thread(target = peer.broadcast_to_peers, args=())
        # peer_thread.start()




        while True:
            time.sleep(2)
        
    except KeyboardInterrupt:
        print("Closing connection to tracker...")
        peer.node_socket.close()
        print("Connection closed.")
