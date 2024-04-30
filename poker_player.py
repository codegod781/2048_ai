# poker game



from blockchain_wallet import BlockchainWallet


class Poker_Player:
    def __init__(self):
        self.player_name = self.create_player()
        self.players = []
        #Every player starts off initially with 100 dollars? We can make this an initial input aswell
        self.money = 100
        self.wins = None
        self.loss = None
        self.ledger =  BlockchainWallet(mining_complexity=2)
        self.hand = []
        self.round = 1
        self.round_1 = []
        self.round_2 = []
        self.round_3 = []


    def create_player(self):
        # Prompt the user for their player name
        player_name = input("Please enter your player name: ")
        print("Hello, " + player_name + "! Welcome to the game.")
        
        #Send message to a peer to recieve the up to date blockchain
        #Print out the current ledger (print to current score)

        return player_name
      
    
    def place_bet(self):
        bet = input("Please enter amount to bet: ")
        return bet
    
    def send_bet_to_peers(self, bet):
        bet_message = (self.player_name, bet)
        send_message = (b'BET', bet_message)
        return send_message
        
    def round_of_betting(self):
        #While true
        #if you recive a newly mined block
        #ask for the players bet for the new round 
        #send name and corresponding bet to all the other players
        #Fill in a table that is each players bets for that round
        #prompt to see if they won that round
        #update players money count
        #person that won the round mines a new block
        #   the newly minted block contains the list of players and how much money each lost to the winner

        pass



if __name__ == "__main__":
    print("main")