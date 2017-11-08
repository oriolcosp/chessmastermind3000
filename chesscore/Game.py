from .Board import *
from .GraphicalInterface import *
from .Player import *

class Game:
    def __init__(self):
        self._board_log = []
        self._move_log = []
        self._board_log.append(Board())
        self._gui = GraphicalInterface(self._board_log[-1])
        self._black_player = KeyboardPlayer(Color.BLACK)
        self._white_player = KeyboardPlayer(Color.WHITE)

    def reset_game(self):
        self._board_log = []
        self._board_log.append(Board())
        self._gui = GraphicalInterface(self._board_log[-1])


    def play_game(self):
        check_mate = False
        stale_mate = False
        self._gui.draw_board(self._board_log[-1])
        while not (check_mate or stale_mate):
            valid_move = False
            while not valid_move:
                move = self.next_move()
                board = self._board_log[-1].move(move)
                if board:
                    valid_move = True
                    self._board_log.append(board)
                    self._move_log.append(move)
                else:
                    print("Invalid Move")
            check_mate = self._board_log[-1].is_check_mate()
            stale_mate = self._board_log[-1].is_stale_mate()
            self._gui.draw_board(self._board_log[-1])
        self._gui.end_game(check_mate, stale_mate)

    # TODO Implement players
    def next_move(self):
        if self._board_log[-1].turn == Color.BLACK:
            move = self._black_player.perform_move(self._board_log[-1])
        else:
            move = self._white_player.perform_move(self._board_log[-1])
        return move

    def is_check(self):
        pass

    def is_check_mate(self):
        return False
