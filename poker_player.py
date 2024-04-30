# poker game



from blockchain_wallet import BlockchainWallet


class Poker_Player:
    def __init__(self):
        self.player_name = self.create_player()
        #Every player starts off initially with 100 dollars? We can make this an initial input aswell
        self.money = 100
        self.wins = 0
        self.loss = 0
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
        return player_name
      
    
    def place_bet(self):
        bet = input("Please enter amount to bet: ")
        self.money = self.money - int(bet)
        return bet
    
    def did_you_win(self):
        while True:
            win = input("\nDid you win the round? (y/n): ")
            if win == 'y':
                self.wins += 1
                total_winnings = 0
                for bets in self.round_1:
                    total_winnings = total_winnings + int(bets[1])
                    self.money = self.money + int(bets[1])
                print("You won $", total_winnings)
                print("you now have $", self.money)
                break
            if win == 'n':
                self.loss += 1
                print("you now have $", self.money)
                break
        self.round_1.clear()
        return win
