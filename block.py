# block
import hashlib
import pickle

class Block:
    def __init__(self, number, transactions, previous_hash):
        """
        Initialize a Block object.

        :param number: Position of the block.
        :param transactions: List of transactions between peers.
        :param previous_hash: Hash of the previous block.
        """
        self.number = number # Position of block
        self.nonce = 0  # Nonce for mining
        # print(f"Data contains: {transactions}")
        self.data = transactions  # Transactions between peers
        self.previous_hash = previous_hash  # Hash of the previous block
        self.hash = None  # Hash of the current block (to be calculated)

    def calculate_hash(self):
        """
        Calculate the hash of the block based on its attributes.
        """
        encoded_block = f"{self.number}{self.nonce}{self.data}{self.previous_hash}{self.hash}".encode()
        self.hash = hashlib.sha256(encoded_block).hexdigest()
    
    def mine_block(self, mined_signature):
        """
        Mine the block until the hash starts with the specified signature.

        :param mined_signature: Signature to be matched for mining.
        :return: The mined block with its header.
        """
        while True:
            self.nonce += 1
            self.calculate_hash()
            if self.hash.startswith(mined_signature):
                block_data = pickle.dumps(self)
                block_with_header = b"BLOCK:" + block_data
                # print("Block mined with hash: ", self.hash)
                return block_with_header
            




    # def calculate_hash(self):
    #     while True:
    #         encoded_block = f"{self.number}{self.nonce}{self.data}{self.previous_hash}{self.hash}".encode()
    #         try_hash = hashlib.sha256(encoded_block).hexdigest()
    #         if self.hash.startswith("00"):
    #             self.hash = try_hash
    
