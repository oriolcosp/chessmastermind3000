import sys
import os

sys.path.append( os.path.join( os.path.join(os.path.dirname(__file__), '..'), '..'))
from chesscore.Piece import *
from chesscore.Board import *
from chesscore.Player import Player

import time
import numpy as np
from keras.models import load_model
from AI.utils import weighted_choice

class value_ann_player(Player):
    def __init__(self, color, filename):
        super().__init__(color)
        # self.model = load_model(filename)

    def ev_ann(self, board, color):
        # xx
        return( np.random.rand() )
        codi_vanessa
        # transform
        num_pixels = X_train.shape[1] * X_train.shape[2] * X_train.shape[3]
        X_train = X_train.reshape(X_train.shape[0], num_pixels).astype('int8')

        # evaluate
        prediction = self.model.predict( X_train )

        # color!!
        score = prediction[0][ player + 1 ] + 0.1 * prediction[0][1]

        return( score )

    def perform_move(self, board):
        moves = board.get_all_moves()
        scores ={}
        i = 0
        for m in moves:
            board_m = board.move_no_check_valid(m)
            scores[i] = self.ev_ann(board, self._color)
            i += 1
        print( scores )
        x = weighted_choice( scores )
        return( moves[x] )

