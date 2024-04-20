# blockchain_wallet
from block import Block
from socket import *
import pickle


RED = '\033[91m'
RESET = '\033[0m'

class BlockchainWallet:
    def __init__(self, mining_complexity):
        self.ledger = {}  # Initialize an empty ledger
        self.blockchain = []  # Initialize an empty blockchain (list of blocks)
        self.tracker = []  # Initialize an empty tracker for peers
        if mining_complexity > 0:
            self.mined_signature = '0' * mining_complexity
        else:
            self.mined_signature = '0'

    def broadcast_block(self, block):
        pickled_block = pickle.dumps(block)
        return pickled_block

    def receive_block(self, pickled_block):
        # Receive a block from a peer, verify its validity, and add it to the blockchain
        block = pickle.loads(pickled_block)
        if block.number == len(self.blockchain) + 1:
            if block.hash.startswith(self.mined_signature):
                if block.previous_hash.startswith(self.mined_signature):
                    self.update_ledger(block.data)
                    self.blockchain.append(block)
                else:
                    print(f"Error: Received block's previous hash starts with {block.previous_hash[:len(self.mined_signature)]}")
            else:
                print(f"Error: block's hash starts with {block.hash[:len(self.mined_signature)]}")
        
        elif block.number > len(self.blockchain) + 1:
            print(f"\033[91mError: Expected sequence number {len(self.blockchain)} but received
                  one {block.number}")
            self.resolve_fork() # At this point we know we don't have the longest chain anymore so there is a fork

    def update_ledger(self, from_node, to_node, amount):
        '''
        Damian here, I made it soe the key to the ledger is the address of a node
        and the value is the amount of money they have. If you guys want to implement a transaction
        history I think it would be better to make it a seperate function that takes in a node's address
        and searches backwards through the blockchain for any transaction which involved the node.
        Append each transaction to a list and then you have a list from most recent to oldest transaction.
        '''
        self.ledger[from_node] -= amount
        self.ledger[to_node] += amount

    def resolve_fork(self):
        # Resolve forks by going with the longest chain
        '''
        Damian here, my idea is that we have to implement some kind of header here
        the we use to identify if something is a block, blockchain, or a request
        for a blockchain/blockchain info. We use this header then to call the appropriate function
        in this class allowing us to process the data. However, we may need a buffer to hold data
        depending on how fast objects are send to the node.
        '''
        pass

    def update_tracker(self, tracker_list):
        self.tracker = tracker_list

    def node_life_support(self, tracker_message):
        '''
        Damian here, I made it so that this function handles decoding and interpreting messages.
        So just send the raw messages received to this function and it will handle it.
        '''
        decoded_message = pickle.loads(tracker_message)
        if isinstance(decoded_message, str):
            if decoded_message == 'INA':
                return pickle.dumps('NIA')
        elif isinstance(decoded_message, list):
            self.update_tracker(decoded_message)
            return 'NULL'

    def send_last_hash_to_peers(self):
        # Send the last hash code to all peers
        pass


