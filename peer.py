
# peer_to_peer_network

import threading
from poker_player import Poker_Player
from tracker import Tracker
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
        # self.peer_socket = socket(AF_INET, SOCK_DGRAM)
        # self.peer_address = ('127.0.0.1', 50001)
        # self.my_port = self.peer_socket.getsockname()
        # print("port : ", self.my_port) 
        self.connections = []
        # self.blockchain = BlockchainWallet()


    def connect_tracker(self):
        self.node_socket.sendto(b'HELLO', self.tracker_address)
        data, _ = self.node_socket.recvfrom(1024)
        deserialized_data = pickle.loads(data)
        self.connections.clear()
        for entry in deserialized_data[1]:
            if entry[1] != self.node_socket.getsockname()[1]:
                self.connections.append((entry[0], entry[1]))

    def ping_tracker(self, tracker_address, node_socket):
        while True:
            node_socket.sendto(b'ALIVE', tracker_address)
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
        print("broadcasting")
        for entry in self.connections:
            message_to_peers = (header, payload)
            pickled_payload = pickle.dumps(message_to_peers) 
            self.node_socket.sendto(pickled_payload, entry)

    def receive_from_peers(self):
        print("recieving")
        while True:
            data, _ = self.node_socket.recvfrom(1024)
            decoded_data = pickle.loads(data)
            header = decoded_data[0]
            payload = decoded_data[1]
        
            if header == 'TRACKER': #up-to-date list from tracker
                # print("recieved from tracker")
                self.connections.clear()
                for entry in payload:
                    if entry[1] != self.node_socket.getsockname()[1]:
                        self.connections.append((entry[0], entry[1]))
                # print("list :", self.connections)


            if header == 'PEER':
                print(payload)
                BlockchainWallet.receive_data(payload, ((self.node_socket.getsockname()[0], self.node_socket.getsockname()[1])))
                # start_round = 1
                # if start_round == 1:
                #     poker_thread = threading.Thread(target=self.round_of_poker, args=())
                #     poker_thread.start()


            if header == 'BET':
                print('\n', payload, '\n')
                self.player.round_1.append(payload)
                


    def round_of_poker(self):
        print("poker thread")
            #ask for the players bet for the new round 
        bet = self.player.place_bet()
            #send name and corresponding bet to all the other players
        bet_touple = (self.player.player_name, bet)
        self.broadcast_to_peers('BET', bet_touple)
            #wait for all bets to be placed
        while len(self.player.round_1) < len(self.connections):
            pass
        print("all players have bet this round. Bets: ")


        self.player.round_1.append(bet_touple)
        print(self.player.round_1)
        win =  self.player.did_you_win()
        print("End of round")

        if win == 'y':
            pass
            #MINE NEW BLOCK
            # self.blockchain_wallet.
        pass


if __name__ == "__main__":
    try:
        peer = Peer()
        peer.connect_tracker()


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
