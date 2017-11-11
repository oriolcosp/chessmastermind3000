from play_3nr_and_save import genera_partides
from play_3nr_and_save import evalua
from perceptron_3nr import train_net

from bots import randomBot
from bots import humanBot
from ann_bot import beta_three
from mcts_bot import omega_three

import time

start = time.time()

data_file_random = 'data/partides_3nr.h5'
data_file_ann = 'data/partides_3nr_smart.h5'
model_file1 = 'data/model1.h5'
model_file2 = 'data/model2.h5'
N = 20000
N_w = 300

omg = omega_three('data/full_tree.h5', print_moves = False )

print( 'genera 1' )
# genera partides aleatories
genera_partides(N, randomBot, data_file_random)

# entrena perceptron1, winrate vs random
# print('entrena 1')
train_net(data_file_random, None, 'model' + str(1) + '.h5')

wr_random = []
wr_omg = []

b3 = beta_three('data/model' + str(1) + '.h5', 'train')
wr_random.append( evalua(N_w, b3.getPlay, randomBot) )
wr_omg.append( evalua(N_w, b3.getPlay, omg.getPlay) )

for i in range(0, 5):
    print( i )
    # genera partides vs ell mateix, winrate vs random, winrate vs v1
    b3 = beta_three('data/model' + str(i+1) + '.h5', 'train')
    genera_partides(N, b3.getPlay, 'partides_ann_' + str(i+1) + '.h5')

    # entrena perceptron1, winrate vs random
    train_net('data/partides_ann_' + str(i+1) + '.h5', 'data/model' + str(i+1) + '.h5', 'data/model' + str(i+2) + '.h5')
    b4 = beta_three('data/model' + str(i+2) + '.h5', 'test')
    wr_random.append( evalua(N_w, b4.getPlay, randomBot) )
    wr_omg.append( evalua(N_w, b4.getPlay, omg.getPlay) )

print( 'wr_random: ' + str(wr_random) )
print( 'wr_omg: ' + str(wr_omg) )

end = time.time()
print(end - start)
