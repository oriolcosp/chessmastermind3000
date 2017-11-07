from abc import ABCMeta, abstractmethod
from . import Static
import random


class Player:
    def __init__(self, color):
        self._color=color
    def perform_move(self,color): pass


class KeyboardPlayer(Player):

    def __init__(self,color):
        super().__init__(color)

    def perform_move(self,board): pass


class RandomPlayer(Player):
    def __init__(self, color):
        super().__init__(color)

    def perform_move(self, board):
        moves = board.get_all_moves()
        print(moves)
        move = random.choice(moves)
        print(move)
        if not moves:
            print("No possible Moves!")
        input("Continue")
        return move
