**Test 1: Invalid bets**
If a player tries to place a non-numeric bet or place a negative bet, the output notifies the player that the bet is invalid, and the player is prompted to place a bet again.  If a player tries to bet more than they have, the output notifies the player that they do not have enough money to bet the desired amount.

**Test 2: No single-player rounds of poker**
A round of poker will not start until at least two players have joined the network.  Only then can the players place bets.

**Test 3: Muliple winners for a round of poker**
To prevent forking from occurring, if two or more people win a round of poker, the winner who is first on the list of players on the network from the tracker mines a new block first, appends this block to their blockchain, and broadcasts their blockchain to the other players.  The next winner on this list then repeats this same process.  This occurs until all winners have mined a new block on the blockchain.

**Test 4: Player joining the network after all players have placed a bet for the round**

**Test 5: Out of two players, at the end of a round, one player chooses to play again while the other player chooses not to play again**