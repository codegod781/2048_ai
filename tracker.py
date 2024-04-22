class Tracker:
    def __init__(self):
        self.online = []  # List of active peers
        # tracker should have its own class

    def add_peer(self, peer):
        # Add a new peer to the network
        self.tracker.append(peer)
        pass

    def remove_peer(self, peer):
        # Remove a peer from the network
        self.tracker.pop(peer)
        pass