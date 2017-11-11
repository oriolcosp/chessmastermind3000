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
        self._max_depth = 2
        self._depth = 0
        self._turn = -1

        self._is_game_over_num = 0
        self._is_game_over_max = 0
        self._is_game_over_min = 0
    
        self._next_state_num = 0
        self._next_state_max = 0
        self._next_state_min = 0
    
        self._available_moves_num = 0
        self._available_moves_max = 0
        self._available_moves_min = 0

        self._next_node_num = 0
        self._next_node_max = 0
        self._next_node_min = 0

    #TODO set timestamps to check performance and spot bottlenecks
    def perform_move(self, board):
        self._depth = 0
        self._turn = board.turnnum
        start_time = time.time()

        self._is_game_over_num = 0
        self._is_game_over_max = 0
        self._is_game_over_min = 0

        self._next_state_num = 0
        self._next_state_max = 0
        self._next_state_min = 0

        self._available_moves_num = 0
        self._available_moves_max = 0
        self._available_moves_min = 0

        self._next_node_num = 0
        self._next_node_max = 0
        self._next_node_min = 0

        move = self._minimax(board)

        print("Next Node max: " + str(self._next_node_max))
        print("Next Node min: " + str(self._next_node_min))
        print("Next Node avg: " + str((self._next_node_max+self._next_node_min)/2))
        print("Next Node num: " + str(self._next_node_num))
        
        print("Is Game Over max: " + str(self._is_game_over_max))
        print("Is Game Over min: " + str(self._is_game_over_min))
        print("Is Game Over avg: " + str((self._is_game_over_max + self._is_game_over_min) / 2))
        print("Is Game Over num: " + str(self._is_game_over_num))
        
        print("Available Moves max: " + str(self._available_moves_max))
        print("Available Moves min: " + str(self._available_moves_min))
        print("Available Moves avg: " + str((self._available_moves_max + self._available_moves_min) / 2))
        print("Available Moves num: " + str(self._available_moves_num))
        
        print("Next state max: " + str(self._next_state_max))
        print("Next state min: " + str(self._next_state_min))
        print("Next state avg: " + str((self._next_state_max + self._next_state_min) / 2))
        print("Next state num: " + str(self._next_state_num))
        
        print("Number of steps: " + str(self._depth))
        print("Time taken: " + str((time.time() - start_time)))
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
        start_time = time.time()
        node = min(
            map(lambda move: self._max_play(self._next_state(board, move)),
                self._get_available_moves(board)))
        ttime = time.time() - start_time
        if not 0 < self._next_node_min < ttime :
            self._next_node_min = ttime
        if ttime > self._next_node_max:
            self._next_node_max = ttime
        self._next_node_num += 1
        print("Next Node: " + str(ttime))
        return node

    def _max_play(self, board):
        start_time = time.time()
        game_over = self._is_game_over(board)
        self._depth += 1
        if game_over != 0 or self._max_depth < board.turnnum - self._turn:
            return self._evaluate(board, game_over)
        node = max(
            map(lambda move: self._min_play(self._next_state(board, move)),
                self._get_available_moves(board)))

        ttime = time.time() - start_time
        if not 0 < self._next_node_min < ttime:
            self._next_node_min = ttime
        if ttime > self._next_node_max:
            self._next_node_max = ttime
        self._next_node_num += 1
        print("Next Node: " + str(ttime))
        return node

    def _next_state(self, board, move):
        start_time = time.time()
        board = board.move_no_check_valid(move)
        ttime = time.time() - start_time
        if not 0 < self._next_state_min < 0:
            self._next_state_min = ttime
        if ttime > self._next_state_max:
            self._next_state_max = ttime
        self._next_state_num += 1
        print("Next State: " + str(ttime))
        return board

    # Returns 1 if this player wins, -1 if this player loses and 0 if game is not over
    def _is_game_over(self, board):
        start_time = time.time()
        check_mate = board.is_check_mate()
        ttime = time.time() - start_time
        if not 0 < self._is_game_over_min < ttime:
            self._is_game_over_min = ttime
        if ttime > self._is_game_over_max:
            self._is_game_over_max = ttime
        self._is_game_over_num += 1
        print("Is Game Over: " + str(ttime))
        if check_mate:
            if board.turn == self._color:
                return -1
            else:
                return 1
        else:
            return 0

    def _get_available_moves(self, board):
        start_time = time.time()
        moves = board.get_all_moves()
        valid_moves = []
        for move in moves:
            if board.move(move):
                valid_moves.append(move)
        ttime = time.time() - start_time
        if not 0 < self._available_moves_min < ttime:
            self._available_moves_min = ttime
        if ttime > self._available_moves_max:
            self._available_moves_max = ttime
        self._available_moves_num += 1
        print("Available Moves: " + str(ttime))
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
