import numpy as np
import h5py
import os, glob

def save_file(filename, boards, results, turns):
    h5f = h5py.File(filename, 'w')
    h5f.create_dataset('boards', data=boards)
    h5f.create_dataset('results', data=results)
    h5f.create_dataset('turns', data=turns)
    h5f.close()

files = glob.glob(os.path.join("/Users/vcastillo/PycharmProjects/chessmastermind3000/AI/Misc/chess_games/", "*.*"))

for datafile in files:
    file_name = datafile.split(".")[0]
    h5f = h5py.File(datafile,'r')
    boards = h5f['boards'][:]
    results = h5f['results'][:]
    turns = h5f['turns'][:]
    h5f.close()


    boards = np.array(boards, dtype = "str")
    piece_type = ["wp", "wr", "wn",  "wb",  "wq",  "wk",  "bp",  "br",  "bn",  "bb",  "bq",  "bk"]
    new_boards = list(map(lambda board: list(map(lambda type: (board == type).astype(np.int8), piece_type)), boards))

    save_file( file_name + "_processed" + ".h5", new_boards, results, turns )