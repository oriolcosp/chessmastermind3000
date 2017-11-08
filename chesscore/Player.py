import random
from .Piece import *
import time

class Player:

    def __init__(self, color):
        self._color = color
        if self._color == Color.BLACK:
            self._other_color = Color.WHITE
        else:
            self._other_color = Color.BLACK

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
        move = random.choice(moves)
        if not moves:
            print("No possible Moves!")
        return move


class AIMinimaxPlayer(Player):

    def __init__(self, color):
        super().__init__(color)
        self._max_depth = 1
        self._depth = 0

    #TODO set timestamps to check performance and spot bottlenecks
    def perform_move(self, board):
        self._depth = 0
        self._turn = board.turnnum
        start_time = time.time()
        move = self._minimax(board)
        print("Number of steps: " + str(self._depth))
        print("Time taken: "+ str((time.time() - start_time)))
        return move[0]

    def _minimax(self, board):
        return max(
            map(lambda move: (move, self._min_play(self._next_state(board, move))),
                self._get_available_moves(board)),
            key=lambda x: x[1])

    def _min_play(self, board):
        game_over = self._is_game_over(board)
        self._depth += 1
        if game_over != 0 or self._max_depth < board.turnnum - self._turn:
            return self._evaluate(board, game_over)
        return min(
            map(lambda move: self._max_play(self._next_state(board, move)),
                self._get_available_moves(board)))

    def _max_play(self, board):
        game_over = self._is_game_over(board)
        self._depth += 1
        if game_over != 0 or self._max_depth < board.turnnum - self._turn:
            return self._evaluate(board, game_over)
        return max(
            map(lambda move: self._min_play(self._next_state(board, move)),
                self._get_available_moves(board)))

    def _next_state(self, board, move):
        return board.move_no_check_valid(move)

    # Returns 1 if this player wins, -1 if this player loses and 0 if game is not over
    def _is_game_over(self, board):
        if board.is_check_mate():
            if board.turn == self._color:
                return -1
            else:
                return 1
        else:
            return 0

    def _get_available_moves(self, board):
        moves = board.get_all_moves()
        valid_moves = []
        for move in moves:
            if board.move(move):
                valid_moves.append(move)
        return valid_moves

    # Gameover is 1 if this player wins, -1 if this player loses and 0 if game is not
    # finished. This function returns inf if player wins and -inf if player loses. Calculates board otherwise
    def _evaluate(self, board, gameover):
        if gameover == 1:
            return float('inf')
        elif gameover == -1:
            return float('-inf')
        else:
            return self._calculate_score(board)

    # Calculates the score for this player. This is, gets the value of this color's board and substracts the value of other color's board
    def _calculate_score(self, board):
        return self._calculate_color(board, self._color) - self._calculate_color(board, self._other_color)

    # TODO Calculates board value for a given color
    def _calculate_color(self, board, color):
        if board.is_cell_menaced(4, 2, color):
            return 1000
        else:
            return random.choice(range(-10, 10))
