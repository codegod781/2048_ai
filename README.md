[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/-Lgd7v9y)
# CSEE 4119 Spring 2024, Class Project
## Team name: Net-not-working
## Team members: (Patrick Cronin, codegod781), (Damian Washel, Reaver16), (Jonathan Eng, Jochengi)
## 

First, run tracker.py using the internal IP address and port of the virtual machine.  Then, run peer.py using the internal IP address and port of the tracker for each peer and enter the player's name.  Once at least two players have joined, players can place a bet.  After all players on the network have placed a bet, they respond to the prompt asking if the player won the round or not.  After all players on the network have responded, if there is only one winner, then that player wins the sum of all bets placed for that round.  If there are two or more winners, the money is split evenly among the winners.  The player is then prompted with whether they would like to play again.  If the players would like to play again, they continue placing bets after enough players are ready.  More players can join during the betting stage of each round.

block.py initializes the block and has a function that mines the block.  blockchain_and_wallet_test.py is used for testing the blockchain.  blockchain_wallet.py is a class used by the peer to receive data in the form of blocks and blockchains.  main.py is responsible for running the program as a whole.  peer.py is responsible for the functionality of a peer, which includes receiving data, broadcasting data, contacting the tracker, and broadcasting bets to other players.  poker_player.py is responsible for running the poker game, including prompting input from the peers (name of players, bets, game outcome).  tracker.py contains the tracker that peers refer to get the connections of other players in the network.

When players join the network, they are given $100 to start with.
# 2048_ai
# 2048_ai
