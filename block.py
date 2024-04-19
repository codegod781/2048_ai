# block

class Block:
    def __init__(self, nonce, data, previous_hash):
        self.nonce = nonce  # Nonce for mining
        self.data = data  # Transactions between peers
        self.previous_hash = previous_hash  # Hash of the previous block
        self.hash = None  # Hash of the current block (to be calculated)

    def calculate_hash(self):
        # Calculate the hash of the block based on its attributes
        pass
