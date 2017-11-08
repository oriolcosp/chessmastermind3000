import numpy as np
from random import randint
from random import uniform
import copy
import deepdish as dd

def weighted_choice(choices):
   total = sum(w for c, w in choices.items())
   r = uniform(0, total)
   upto = 0
   for c, w in choices.items():
      if upto + w >= r:
         return c
      upto += w
   assert False, "Shouldn't get here"

def getWinner(taulell):
        winner = 0
        m1 = max( np.array( taulell, dtype=np.int8 ).sum(axis = 1) )
        m2 = max( np.array( taulell, dtype=np.int8 ).sum(axis = 0) )
        m3 = taulell[0][0] + taulell[1][1] + taulell[2][2]
        m4 = taulell[2][0] + taulell[1][1] + taulell[0][2]
        m = max( [ m1, m2, m3, m4 ] )
        if m == 3:
            winner = 1
        m1 = min( np.array( taulell, dtype=np.int8 ).sum(axis = 1) )
        m2 = min( np.array( taulell, dtype=np.int8 ).sum(axis = 0) )
        m = min( [ m1, m2, m3, m4 ] )
        if m == -3:
            winner = -1
        return winner

class TresEnRalla():
    def playGame(self, bot1, bot2):
        taulell = [ [0, 0, 0], [0, 0, 0], [0, 0, 0] ]
        ts = []
        i = 0
        winner = 0
        while (i < 9 and winner == 0):
            if i % 2 == 0:
                coords = bot1( taulell, (-1) ** i )
                taulell[ coords[0] ][ coords[1] ] = (-1) ** i
            if i % 2 == 1:
                coords = bot2( taulell, (-1) ** i )
                taulell[ coords[0] ][ coords[1] ] = (-1) ** i
            i += 1
            ts.append( copy.deepcopy( taulell ) )
            winner = getWinner( taulell )
        return { 'winner': winner, 'taulells': ts, 'n_rounds': i }

