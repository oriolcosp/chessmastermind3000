import random
from .Piece import *


class Player:

    def __init__(self, color):
        self._color = color

    def perform_move(self, color): pass


class KeyboardPlayer(Player):

    def __init__(self, color):
        super().__init__(color)
        self._possible_cols = ["A", "B", "C", "D", "E", "F", "G", "H"]
        self._possible_rows = ["1", "2", "3", "4", "5", "6", "7", "8"]

    def perform_move(self, board):
        no_valid_input = True
        while no_valid_input:
            text = input("Write move (format: e1a4) \n")
            if text[0].upper() in self._possible_cols and text[2].upper() in self._possible_cols and text[1] \
                    in self._possible_rows and text[3] in self._possible_rows:
                    no_valid_input = False
            else:
                print("Input not valid")
        srow = board.size - int(text[1])
        erow = board.size - int(text[3])
        scol = self._letter_to_col(text[0])
        ecol = self._letter_to_col(text[2])
        return Move(board.get_cell(srow, scol), srow, scol, erow, ecol)

    def _letter_to_col(self, text):
        return {
            'A': 0,
            'B': 1,
            'C': 2,
            'D': 3,
            'E': 4,
            'F': 5,
            'G': 6,
            'H': 7,
        }.get(text.upper(), 10)


class RandomPlayer(Player):
    def __init__(self, color):
        super().__init__(color)

    def perform_move(self, board):
        moves = board.get_all_moves()
        print(moves)
        # print(moves)
        move = random.choice(moves)
        # print(move)
        if not moves:
            print("No possible Moves!")
        # input("Continue")
        return move
