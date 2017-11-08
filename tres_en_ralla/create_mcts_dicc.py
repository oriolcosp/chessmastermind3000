import copy
import deepdish as dd
import numpy as np
from tres_en_ralla import getWinner

dic = {}

def mcts_write(taulell, player, turn):
    tup = tuple(map(tuple, taulell))
    if tup in dic:
        return dic[ tup ]

    s = None
    w = getWinner(taulell) 
    if w == player:
        s = 1
    if w == -player:
        s = -1

    if s is None:
        n = 0
        v = 0
        for i in range(3):
            for j in range(3):
                if taulell[i, j] == 0:
                    n += 1
                    t = copy.deepcopy(taulell)
                    t[i, j] = turn
                    v += mcts_write(t, player, -turn)
        if n > 0:
            s = v / n
        else:
            s = 0
    dic[ tup ] = s
    return( s )

mcts_write(np.zeros((3,3)), 1, 1)

dd.io.save('full_tree.h5', dic)
