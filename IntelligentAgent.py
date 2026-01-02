#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 10:03:22 2023

@author: karatemaster1
"""
from Grid       import Grid
from ComputerAI import ComputerAI
from Displayer  import Displayer
from BaseAI import BaseAI

import random


class IntelligentAgent(BaseAI):
    def init_(self):
        print("new agent!")
        
    def getMove(self, grid):
        move, utility = maximize(grid, 0, float('-inf'), float('inf'))
        return move
     
def maximize(state, depth, alpha, beta):
    
    if depth > 4 or terminalTest(state):
        return heuristics(state)

    maxUtility = float('-inf')
    bestMove = None
    
    for move in state.getAvailableMoves():
        
        posMove = move[0]
        utility = expecti(move[1], depth+1, alpha, beta)


        if utility > maxUtility:
            bestMove = posMove 
            maxUtility = utility
            
        if maxUtility >= beta:
            break

        if maxUtility > alpha:
            alpha = maxUtility
            
    if depth == 0:
        return bestMove, maxUtility
    else:
        return maxUtility

    
    
    
    
def expecti(state, depth, alpha, beta):
    if  terminalTest(state): #depth > 5 or
        return heuristics(state)

    
    minUtility = float('inf')
    total = 0
    n = 0

    for pos in state.getAvailableCells():
        posMove = state.clone()
        
        random_number = random.random()
        assign = 2
        if random_number < 0.1:
            assign = 4  # 90% chance of returning 2
            
        posMove.insertTile(pos, assign)
        utility = maximize(posMove, depth+1, alpha, beta)
        total += utility
        n=n+1
		
        if utility < minUtility:
            minUtility = utility
            
        if minUtility <= alpha:
            break

        if minUtility < beta:
            beta = minUtility
    
    average = total/n
    return average





def terminalTest(grid):
    return len(grid.getAvailableMoves())==0






def heuristics(grid):
    total = 0
    largest = 0
    
    for pos in grid.map:
        for i in pos:
            if i > largest:
                largest = i
            
    if largest > 256 and grid.map[0][2]>grid.map[0][0]:
        perfectBoard=[[8192, 16384, 32768, 65536],[4096, 2048, 1024, 512],[32, 64, 128, 256],[16,8,4,2]]
    else:
        perfectBoard=[[65536, 32768, 16384, 8192],[512, 1024, 2048, 4096],[256, 128, 64, 32],[2,4,8,16]]

    for i in range(4):
        for j in range(4):
            total = total + grid.map[i][j]*perfectBoard[i][j]
    
    
    
    if grid.map[0][0] == largest or grid.map[0][1] == largest or grid.map[0][2] == largest or grid.map[0][3] == largest:
        total += 16
    

    return total 

