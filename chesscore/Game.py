from .Board import *
from .GraphicalInterface import *
from .Player import *

class Game:
    def __init__(self):
        self._boardLog = []
        self._boardLog.append(TestBoard())
        self._gui = GraphicalInterface(self._boardLog[-1])
        self._black_player = RandomPlayer(Color.BLACK)
        self._white_player = RandomPlayer(Color.WHITE)

    def reset_game(self):
        self._boardLog = []
        self._boardLog.append(Board())
        self._gui = GraphicalInterface(self._boardLog[-1])


    def play_game(self):
        check_mate = False
        self._gui.draw_board(self._boardLog[-1])
        while not check_mate:
            valid_move = False
            while not valid_move:
                move = self.next_move()
                board = self._boardLog[-1].move(move)
                if board:
                    valid_move = True
                    self._boardLog.append(board)
                else:
                    print("Invalid Move")
            check_mate = self.is_check_mate()
            self._gui.draw_board(self._boardLog[-1])
        self._gui.end_game

    # TODO Implement players
    def next_move(self):
        if self._boardLog[-1].turn == Color.BLACK:
            move = self._black_player.perform_move(self._boardLog[-1])
        else:
            move = self._white_player.perform_move(self._boardLog[-1])
        return move

    def is_check(self):
        pass

    def is_check_mate(self):
        return False
