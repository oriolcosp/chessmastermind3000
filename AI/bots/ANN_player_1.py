import random
from .Piece import *
import time
from Player import Player
import numpy as np
from keras.models import load_model
from utils import weighted_choice

class RandomPlayer(Player):
    def __init__(self, color, filename):
        super().__init__(color)
        self.model = load_model(filename)

    def perform_move(self, board):
        moves = board.get_all_moves()
        scores = np.zeros( len(monves) )
        i = 0
        for m in moves:
            board_m = board.move_no_check_valid(move)
            scores[i] = ev_ann(board, self._color)
            i += 1
        x = weighted_choice( scores )
        return( moves[x] )

    def ev_ann(self, board, color):
        # xx
        codi_vanessa
        # transform
        num_pixels = X_train.shape[1] * X_train.shape[2] * X_train.shape[3]
        X_train = X_train.reshape(X_train.shape[0], num_pixels).astype('int8')

        # evaluate
        prediction = self.model.predict( X_train )

        color!!
        score = prediction[0][ player + 1 ] + 0.1 * prediction[0][1]

        return( score )

