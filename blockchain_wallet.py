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

    def receive_data(self, pickled_data, node_address):
        # Receive data in the form of a block, blockchain, or message
        headers = {
            b"BLOCK:": len(b"BLOCK:"),
            b"BLOCKCHAIN": len(b"BLOCKCHAIN")
        }

        header_length = None
        for header, length in header.items():
            if pickled_data.startswith(header):
                header_length = length
                break

        header = pickled_data[:header_length]
        data = pickled_data[header_length:]

        if header == b"BLOCK:":
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
                self.resolve_fork(node_address) # At this point we know we don't have the longest chain anymore so there is a fork
        elif header == b"BLOCKCHAIN":
            self.request_blockchain(node_address)
        else:
            print("Unknown header received.")

    def request_blockchain(self, node_address):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((node_address[0], node_address[1]))
                request_message = b"GET_BLOCKCHAIN"
                s.sendall(request_message)
                blockchain_data = self.recv_until_delimiter(s)
                received_blockchain = pickle.loads(blockchain_data)
                for block in received_blockchain:
                    if block.number == len(self.blockchain) + 1:
                        if block.hash.startswith(self.mined_signature):
                            if block.previous_hash.startswith(self.mined_signature):
                                self.update_ledger(block.data)
                                self.blockchain.append(block)
                            else:
                                print(f"Error: Received block's previous hash starts with {block.previous_hash[:len(self.mined_signature)]}")
                        else:
                            print(f"Error: Block's hash starts with {block.hash[:len(self.mined_signature)]}")
                    elif block.number > len(self.blockchain) + 1:
                        print(f"Error: Expected sequence number {len(self.blockchain)} but received one {block.number}")
                        self.resolve_fork(node_address)
        except ConnectionError as e:
            print(f"Error sending blockchain to {node_address}: {e}")

            

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

    def recv_until_delimiter(self, connection, delimiter=b'Z`G!g0d$2mC2', buffer_size=4096):
        data = b""
        while True:
            chunk = connection.recv(buffer_size)
            data += chunk
            if delimiter in data:
                break
        return data


    def resolve_fork(self, node_address):
        # Resolve forks by going with the longest chain
        '''
        Damian here, my idea is that we have to implement some kind of header here
        the we use to identify if something is a block, blockchain, or a request
        for a blockchain/blockchain info. We use this header then to call the appropriate function
        in this class allowing us to process the data. However, we may need a buffer to hold data
        depending on how fast objects are send to the node.
        '''
        request_message = "GET_BLOCKCHAIN"
        try:
            with socket.socket(socket.AF_IET, socket.SOCK_STREAM) as s:
                s.connect((node_address[0], node_address[1]))
                s.sendall(request_message.encode())
                blockchain_data = self.recv_until_delimiter(s)
                received_blockchain = pickle.loads(blockchain_data)
                for block in received_blockchain:
                    self.receive_block(pickle.dumps(block), node_address)
        except ConnectionError as e:
            print(f"Error connecting to node sat {node_address}: {e}")

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


