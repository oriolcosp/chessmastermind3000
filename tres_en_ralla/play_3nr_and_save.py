
import numpy as np
from random import randint
import copy
import time
import h5py
from tres_en_ralla import TresEnRalla


def genera_partides(N, bot1, filename):
    start = time.time()

    taulells = []
    results = []
    # N = 10000
    # N = 100
    for i in range(N):
        tnr = TresEnRalla()
        tmp = tnr.playGame( bot1, bot1 )
        taulells = taulells + (tmp['taulells'])
        results = results + [ tmp['winner'] ] * tmp['n_rounds']

    end = time.time()

    taulells = np.array( taulells )
    results = np.array( results )

    h5f = h5py.File(filename, 'w')
    h5f.create_dataset('taulells', data=taulells)
    h5f.create_dataset('results', data=results)
    h5f.close()


def evalua(N, bot1, bot2):
    results = []
    for i in range(N):
        tnr = TresEnRalla()
        if i % 2 == 0:
            tmp = tnr.playGame( bot1, bot2 )
            results.append(tmp['winner'])
        if i % 2 == 1:
            tmp = tnr.playGame( bot2, bot1 )
            results.append(-tmp['winner'])
    winrate = sum( np.array(results) == 1)/N + 0.5*sum( np.array(results) == 0)/N
    print('winrate: ' + str( winrate ) )
    return( winrate )

