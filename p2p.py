
# peer_to_peer_network

from tracker import Tracker

class PeerToPeerNetwork:
    def __init__(self, tracker_addr):
        self.tracker_address = tracker_addr
        self.peer_socket = None
        self.connections = []

        # tracker should have its own class

    def read_tracker(self, tracker):
        for dest in tracker.online:



    def add_peer(self, peer):
        # Add a new peer to the network
        self.tracker.append(peer)
        pass

    def remove_peer(self, peer):
        # Remove a peer from the network
        self.tracker.pop(peer)
        pass

    def broadcast_to_peers(self, message):
        # Broadcast a message to all peers
        pass

    def receive_from_peers(self):
        # Receive messages from peers
        pass

    def compare_last_hash(self):
        # Compare the last hash in each blockchain against peers
        pass

    def ping_peers(self):
        # Ping peers to verify their activity
        pass

