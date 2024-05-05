**Test 1: Invalid bets**  
If a player tries to place a non-numeric bet or place a negative bet, the output notifies the player that the bet is invalid, and the player is prompted to place a bet again.  If a player tries to bet more than they have, the output notifies the player that they do not have enough money to bet the desired amount.

**Test 2: No single-player rounds of poker**  
A round of poker will not start until at least two players have joined the network.  Only then can the players place bets.  After a round of poker has finished, the next round will not start until at least two players are ready, which consists of players who agree to play again and new players who join the network.

**Test 3: Multiple winners for a round of poker**  
To prevent forking from occurring, if two or more people win a round of poker, the winner who is first on the list of players on the network from the tracker mines a new block, appends this block to their blockchain, and broadcasts their blockchain to the other players.  The next winner on this list then repeats this same process.  This occurs until all winners have mined a new block on the blockchain.

**Test 4: Player joining the network after all players have placed a bet for the round**  

-----------If a new player joins the network while the existing players have already been prompted if they won the round or not, the new player will wait until the next round before placing a bet.

**Test 5: Gracefully exit the program**  
If we input Ctrl-C for a peer, the peer will be removed from the tracker after the timeout occurs.  If the peer exits after placing a bet, the bet will remain in the pool as it is tracked by the other players on the network.
If we input Ctrl-C for a tracker, the tracker will close its socket.
