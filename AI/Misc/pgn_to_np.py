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


def pgn_to_np(filename, prefix, freq, endings):
    pgn = open(filename)

    bo = True
    i = 0
    k = 0
    boards = []
    results = []
    turns = []

    boards_end = []
    results_end = []
    turns_end = []

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

        if i > 1 and endings:
            boards_end = boards_end + [ copy.deepcopy(brd) ]
            results_end = results_end + [ winner ]
            turns_end = turns_end + [ b'b' if j % 2 == 1 else b'w' ]

            if i % 50000 == 0:
                save_file( prefix + 'end_' + str(i) + '.h5', boards_end, results_end, turns_end )

                boards_end = []
                results_end = []
                turns_end = []

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
            # if k > 300:
            #     bo = False
            #     print( turns )
            #     break
            j += 1
            k += 1

            x0, y0, x1, y1 = get_coords( str( m ) ) 

            brd[x1][y1] = brd[x0][y0]
            brd[x0][y0] = b''

            if k % freq == 0:
                boards = boards + [ copy.deepcopy(brd) ]
                results = results + [ winner ]
                turns = turns + [ b'b' if j % 2 == 1 else b'w' ]
                if k % (freq*5000*40) == 0:
                    # Guarda el progres, inicialitza variables
                    save_file( prefix + str(k) + '.h5', boards, results, turns )

                    boards = []
                    results = []
                    turns = []

    # print( np.array(boards) )
    # Guarda el progres
    save_file( prefix + str(k) + '.h5', boards, results, turns )
    save_file( prefix + 'end_' + str(i) + '.h5', boards_end, results_end, turns_end )

def count_games(filename):
    pgn = open(filename)

    bo = True
    i = 0
    j = 0
    games = set()

    while( bo ):
        i += 1
        if (i % 10000 == 0):
            print( i )
        try:
            next_game = chess.pgn.read_game(pgn)
            if next_game.headers['FICSGamesDBGameNo'] in games:
                break
            else:
                games.add( next_game.headers['FICSGamesDBGameNo'] )
        except:
            break
    print( i )

pgn_to_np( 'pgn_files/fics_2016.pgn', 'chess_games2/fics_2016_', 5, True )
pgn_to_np( 'pgn_files/fics_2015.pgn', 'chess_games2/fics_2015_', 5, True )
