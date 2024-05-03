
# peer_to_peer_network

import threading
from poker_player import Poker_Player
from tracker import Tracker
from block import Block
from socket import *
from blockchain_wallet import BlockchainWallet
import pickle
import time


class Peer:
    def __init__(self):
        self.player = Poker_Player()
        self.node_socket = socket(AF_INET, SOCK_DGRAM)
        self.port = self.node_socket.getsockname()[1]
        self.tracker_address = ('127.0.0.1', 50000)
        self.blockchain_wallet = BlockchainWallet(mining_complexity=2)
        self.connections = []
        self.playerlist = []
        self.new_player = False
      


    def connect(self):
        header = 'HELLO'
        message = (header, self.player.player_name)
        self.node_socket.sendto(pickle.dumps(message), self.tracker_address)
        data, _ = self.node_socket.recvfrom(1024)
        deserialized_data = pickle.loads(data)
        self.connections.clear()
        for entry in deserialized_data[1]:
            self.playerlist.append(entry[1])
            if entry[0][1] != self.node_socket.getsockname()[1]:
                self.connections.append((entry[0][0], entry[0][1]))
        
        message = ("I need blockchain")
        self.broadcast_to_peers('CONNECT', message)
                
   

    def ping_tracker(self, tracker_address, node_socket):
        while True:
            message = pickle.dumps(b'ALIVE')
            node_socket.sendto(message, tracker_address)
            time.sleep(2)

    def add_connection(self, peer):
        # Add a new peer to the network
        self.tracker.append(peer)
        pass

    def remove_connection(self, peer):
        # Remove a peer from the network
        self.tracker.pop(peer)
        pass

    def broadcast_to_peers(self, header, payload):
        # print("broadcasting")
        for addr in self.connections:
            # print("entry :", addr)
            message_to_peers = (header, payload)
            pickled_payload = pickle.dumps(message_to_peers) 
            self.node_socket.sendto(pickled_payload, addr)

    def receive_from_peers(self):
        print("recieving")
        while True:
            data, addr = self.node_socket.recvfrom(1024)
            decoded_data = pickle.loads(data)
            header = decoded_data[0]
            payload = decoded_data[1]
        
            if header == 'TRACKER': #up-to-date list from tracker
                # print("recieved from tracker")
                self.connections.clear()
                for entry in payload:
                    self.playerlist.append(entry[1])
                    if entry[0][1] != self.node_socket.getsockname()[1]:
                        self.connections.append((entry[0][0], entry[0][1]))
                # print("list :", self.connections)

            if header == 'CONNECT':
                self.new_player = True

            if header == 'BLOCKCHAIN':
                if len(self.blockchain_wallet.blockchain) == 0:
                    self.blockchain_wallet.blockchain = payload
                    print("blockchain received")

            if header == 'PEER':
                # print(payload)
                chain = self.blockchain_wallet.receive_data(payload, ((self.node_socket.getsockname()[0], self.node_socket.getsockname()[1])))
                # print("message to wallet : ", payload[0])
                # print("sending to : ", addr)
                if payload[0] == b'GET_BLOCKCHAIN':
                    pickled_payload = pickle.dumps(chain) 
                    self.broadcast_to_peers('BET', pickled_payload)
                    
            if header == 'BET':
                print(("recieved bet: "), payload)
                self.player.round_1.append(payload)

            if header == 'DONE':
                self.player.round_1_done.append(payload)



    def round_of_poker(self):
        self.player.round_1.clear()

        if self.new_player == True:
            self.broadcast_to_peers('BLOCKCHAIN', self.blockchain_wallet.blockchain)
            self.new_player = False


        bet = self.player.place_bet()
        bet_touple = (self.player.player_name, bet)
        self.broadcast_to_peers('BET', bet_touple)
        
        while len(self.player.round_1) < len(self.connections):
            pass
        print("all players have bet this round. Bets: \n",  self.player.round_1)

        win =  self.player.did_you_win()
        self.broadcast_to_peers('DONE', win)

        if win == 'y':
            self.winner()

        self.blockchain_wallet.print_wallet()

        print("End of round")
            


    def winner(self):
        while len(self.player.round_1_done) < len(self.connections):
                pass
            # Insert order to mine blocks
        for player in self.playerlist:
            if player == self.player.player_name:
                break
            time.sleep(1.0)

        if len(self.blockchain_wallet.blockchain) == 0:
            prev_hash = "00"
        else:
            prev_hash = self.blockchain_wallet.blockchain[-1].hash
        number_of_winners = 0
        for response in self.player.round_1_done:
            if response == "y":
                number_of_winners += 1
        if number_of_winners > 1:
            for i in range(0, self.player.round_1):
                self.player.round_1[i] = (self.player.round_1[i][0], self.player.round_1[i][1] / number_of_winners)
        
        data_to_add = str(self.player.player_name) + " recieved (from, amount)" + str(self.player.round_1)
        my_block = Block(len(self.blockchain_wallet.blockchain)+1, data_to_add, prev_hash)
        new_block = my_block.mine_block("00")
        self.blockchain_wallet.receive_data(new_block, "127.0.0.1")
        self.broadcast_to_peers('PEER', new_block)

    def new_data(self):
        pass


if __name__ == "__main__":
    try:
        peer = Peer()
        peer.connect()


        node_thread = threading.Thread(target = peer.ping_tracker, args=(peer.tracker_address, peer.node_socket,))
        node_thread.start()   

        receive_thread = threading.Thread(target = peer.receive_from_peers, args=())
        receive_thread.start()


        # peer.broadcast_to_peers('PEER',"hello")



        

        while True:
            peer.round_of_poker()
            time.sleep(2)
        
    except KeyboardInterrupt:
        print("Closing connection to tracker...")
        peer.node_socket.close()
        print("Connection closed.")
