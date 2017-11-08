import numpy as np
from random import randint
from random import uniform
import copy

def randomBot( taulell, player ):
    # print( np.array( taulell, dtype=np.int8 ) )
    b = True
    while b:
        move = [ randint(0, 2), randint(0, 2) ]
        if taulell[ move[0] ][ move[1] ] == 0:
            b = False
    return move

def humanBot( taulell, player ):
    print( 'Your turn, player: ' + str(player) )
    print( np.array( taulell, dtype=np.int8 ) )
    b = True
    while (b):
        x = int( input('x: ') )
        y = int( input('y: ') )
        if taulell[x][y] == 0:
            b = False
        else:
            print('invalid coordinates')
    return( [x, y] )

def smartBot( taulell, player ):
    # best position
    taulell = np.array(taulell)
    if taulell[0, 0] == 0:
        return( [1, 1] )
    # check win condition
    for i in range(3):
        for j in range(3):
            if taulell[i, j] == 0:
                t = copy.deepcopy( np.array( taulell ) )
                t[i, j] = player
                if getWinner( t ) == player:
                    return( [i, j] )
    # check loose condition
    for i in range(3):
        for j in range(3):
            if taulell[i, j] == 0:
                t = copy.deepcopy( np.array( taulell ) )
                t[i, j] = player
                if getWinner( t ) == -player:
                    return( [i, j] )
    for i in [0, 2]:
        for j in [0, 2]:
            if taulell[i, j] == 0:
                return( [i, j] )
    for i in range(3):
        for j in range(3):
            if taulell[i, j] == 0:
                return( [i, j] )
