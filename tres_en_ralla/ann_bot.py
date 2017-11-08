import numpy as np
from random import randint
from random import uniform
import copy
import deepdish as dd
from keras.models import load_model
from tres_en_ralla import weighted_choice

class beta_three():
    def __init__(self, filename, mode, print_moves = False):
        self.model = load_model(filename)
        self.mode = mode
        self.print_moves = print_moves

    def getPlay(self, taulell, player):
        moves = np.zeros(shape=(3,3))
        for i in range(3):
            for j in range(3):
                moves[i][j] = 0
                t = copy.deepcopy( np.array(taulell) )
                if t[i][j] == 0:
                    t[i][j] = player
                    
                    X_train_1s = (t == 1) * 1
                    X_train_m1s = (t == -1) * 1
                    X_train = np.row_stack( (X_train_1s, X_train_m1s) )
                    
                    num_pixels = X_train.shape[0] * X_train.shape[1]
                    X_train = X_train.reshape(1, num_pixels).astype('int8')

                    # X_train = X_train.reshape(1, 2, 3, 3).astype('int8')

                    prediction = self.model.predict( X_train )
                    moves[i, j] = prediction[0][ player + 1 ] + 0.1 * prediction[0][1]
        if self.print_moves:
            print( (moves**20) / ( moves**20 ).sum() )
        if self.mode == 'train':
            adict = dict( zip( range(9), moves.reshape(9)**3 ))
        else:
            adict = dict( zip( range(9), moves.reshape(9)**20 ))
        x = weighted_choice(  adict )
        i,j = x // 3, x % 3
        return( [i, j] )


