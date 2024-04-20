# block
import hashlib

class Block:
    def __init__(self, number, nonce, data, previous_hash):
        self.number = number # Position of block
        self.nonce = 0  # Nonce for mining
        self.data = data  # Transactions between peers
        self.previous_hash = previous_hash  # Hash of the previous block
        self.hash = None  # Hash of the current block (to be calculated)

    def calculate_hash(self):
        encoded_block = f"{self.number}{self.nonce}{self.data}{self.previous_hash}{self.hash}".encode()
        self.hash = hashlib.sha256(encoded_block).hexdigest()
    
    def mine_block(self, mined_signature):
        while True:
            self.nonce += 1
            self.hash = self.calculate_hash()
            if self.hash.startswith(mined_signature):
                print("Block mined with hash: ", self.hash)
                break
        