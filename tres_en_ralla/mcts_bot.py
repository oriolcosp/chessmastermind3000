import copy
import deepdish as dd
import numpy as np
from tres_en_ralla import getWinner
from tres_en_ralla import weighted_choice

class omega_three():
    def __init__(self, filename, print_moves = False):
        self.dic = dd.io.load('full_tree.h5')
        self.print_moves = print_moves

    def getPlay(self, taulell, player):
        moves = np.zeros(shape=(3,3))
        for i in range(3):
            for j in range(3):
                moves[i][j] = -1
                t = copy.deepcopy( np.array(taulell) )
                if t[i][j] == 0:
                    t[i][j] = player
                    
                    prediction = self.dic[  tuple(map(tuple, t)) ] 
                    moves[i, j] = prediction * player

        if self.print_moves:
            print( (moves**20) / ( moves**20 ).sum() )

        adict = dict( zip( range(9), (moves + 1).reshape(9)**100 ))
        x = weighted_choice(  adict )
        i,j = x // 3, x % 3
        return( [i, j] )

