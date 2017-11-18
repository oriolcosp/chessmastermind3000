from chesscore.Game import Game
from .Player import *


class Main(object):

    def start_game(self):
        white_player = AIMinimaxPlayer(Color.WHITE)
        black_player = KeyboardPlayer(Color.BLACK)
        game = Game(white_player, black_player)
        game.play_game()


if __name__ == '__main__':
    Main().start_game()