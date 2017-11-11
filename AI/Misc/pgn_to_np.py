import chess.pgn
import copy
import numpy as np
import h5py

def save_file(filename, boards, results, turns):
    h5f = h5py.File(filename, 'w')
    h5f.create_dataset('boards', data=boards)
    h5f.create_dataset('results', data=results)
    h5f.create_dataset('turns', data=turns)
    h5f.close()


def get_coords(move):
    # Passa de coordenades 'e2e4' a x0, y0 -> x1, y1
    y0 = ord( move[0] ) - ord( 'a' )
    x0 = int( move[1] ) - 1
    y1 = ord( move[2] ) - ord( 'a' )
    x1 = int( move[3] ) - 1

    return( x0, y0, x1, y1 )


def pgn_to_np(filename, prefix):
    pgn = open(filename)

    bo = True
    i = 0
    boards = []
    results = []
    turns = []

    board = [ [b'wr', b'wn', b'wb', b'wq', b'wk', b'wb', b'wn', b'wr'],
        [b'wp', b'wp', b'wp', b'wp', b'wp', b'wp', b'wp', b'wp'],
        [b'', b'', b'', b'', b'', b'', b'', b''],
        [b'', b'', b'', b'', b'', b'', b'', b''],
        [b'', b'', b'', b'', b'', b'', b'', b''],
        [b'', b'', b'', b'', b'', b'', b'', b''],
        [b'bp', b'bp', b'bp', b'bp', b'bp', b'bp', b'bp', b'bp'],
        [b'br', b'bn', b'bb', b'bq', b'bk', b'bb', b'bn', b'br'] ]

    while( bo ):
        i += 1
        if i % 5000 == 0:
            # Guarda el progres, inicialitza variables
            save_file( prefix + str(i) + '.h5', boards, results, turns )

            boards = []
            results = []
            turns = []

        try:
            next_game = chess.pgn.read_game(pgn)
        except:
            break

        winner = next_game.headers['Result'].encode('ascii')
        #print( winner )

        brd = copy.deepcopy(board)

        mvs = next_game.main_line()
        j = 0
        for m in mvs:
            # if j > 3:
            #     bo = False
            #     break
            j += 1

            x0, y0, x1, y1 = get_coords( str( m ) ) 

            brd[x1][y1] = brd[x0][y0]
            brd[x0][y0] = b''

            boards = boards + [ copy.deepcopy(brd) ]
            results = results + [ winner ]
            turns = turns + [ b'b' if j % 2 == 1 else b'w' ]
    # print( np.array(boards) )
    # Guarda el progres
    save_file( prefix + str(i) + '.h5', boards, results, turns )

pgn_to_np( 'pgn_files/fics_2015.pgn', 'chess_games/fics_2015_' )
pgn_to_np( 'pgn_files/fics_2015.pgn', 'chess_games/fics_2016_' )

