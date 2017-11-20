import numpy as np
import h5py
import pandas as pd

def chess_to_numpy(file_name):
    h5f = h5py.File('AI/Misc/chess_games2/fics_2016_end_50000.h5','r')
    boards = h5f['boards'][:]
    results = h5f['results'][:]
    turns = h5f['turns'][:]
    h5f.close()

    boards = np.array(boards, dtype = "str")
    piece_type = ["wp", "wr", "wn",  "wb",  "wq",  "wk",  "bp",  "br",  "bn",  "bb",  "bq",  "bk"]
    new_boards = np.array( list(map(lambda board: list(map(lambda type: (board == type).astype(np.int8), piece_type)), boards)) )

    shp = new_boards.shape

    turns = np.array(turns, dtype = "str")
    turns = np.array(turns=="w", dtype = "int8")

    t_array = np.zeros( (shp[0], 1, shp[2], shp[3]) )
    t_array[turns.nonzero()] = 1

    new_boards = np.concatenate((new_boards, t_array ), axis = 1)

    results = np.array( pd.get_dummies(results) )

    return new_boards, results


