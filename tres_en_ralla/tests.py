from ann_bot import beta_three
from mcts_bot import omega_three
from tres_en_ralla import TresEnRalla
from bots import humanBot
from bots import randomBot
from play_3nr_and_save import evalua
from bots import smartBot
import copy
import deepdish as dd
import numpy as np

tnr = TresEnRalla()
omg = omega_three('full_tree.h5', print_moves = False )

#tnr.playGame( humanBot, omg.getPlay  )
#tnr.playGame( omg.getPlay, humanBot )


b3 = beta_three('model4.h5', 'test', print_moves = False )


evalua(300, b3.getPlay, randomBot)
evalua(300, omg.getPlay, randomBot)

evalua(300, b3.getPlay, omg.getPlay)

evalua(300, omg.getPlay, b3.getPlay)

# tmp = tnr.playGame( mctsBot, humanBot )


# 

# evalua(300, b3.getPlay, smartBot)

# #tmp = tnr.playGame( smartBot, humanBot )
# tmp = tnr.playGame( humanBot , b3.getPlay)
# tmp = tnr.playGame( b3.getPlay, humanBot )

# i = 10

# # b4 = beta_three('model' + str(i+2) + '.h5', 'test')
# evalua(300, b3.getPlay, smartBot)



