
# peer_to_peer_network

from tracker import Tracker
import socket
from blockchain_wallet import BlockchainWallet
import pickle


class Peer:
    def __init__(self, tracker_addr):
        self.tracker_address = tracker_addr
        self.peer_socket = None
        self.connections = []
        self.blockchain = BlockchainWallet()


        # tracker should have its own class




    def connect_tracker(self):
        try:
            # Create a socket object
            self.peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Connect to the tracker
            self.peer_socket.connect(self.tracker_address)
            print("Connected to tracker at", self.tracker_address)
            
            # Notify tracker about joining the network
            self.peer_socket.send(b"Hello!")
            
            # You can add more logic here depending on your protocol
            
        except Exception as e:
            print("Error connecting to tracker:", e)

        data = self.peer_socket.recv(1024)

        # Break apart tracker
        data = data = self.peer_socket.recv(1024)
        active_peers = pickle.loads(data)

        # Connect to each peer in the list
        for peer_address in active_peers:
            if peer_address != self.my_address:
                self.connect_to_peer(peer_address)





    def add_connection(self, peer):
        # Add a new peer to the network
        self.tracker.append(peer)
        pass

    def remove_connection(self, peer):
        # Remove a peer from the network
        self.tracker.pop(peer)
        pass

    def broadcast_to_peers(self, message):
        # Broadcast a message to all peers
        pass

    def receive_from_peers(self):
        # Receive messages from peers
        pas

    def compare_last_hash(self):
        # Compare the last hash in each blockchain against peers
        pass

    def ping_peers(self):
        # Ping peers to verify their activity
        pass

