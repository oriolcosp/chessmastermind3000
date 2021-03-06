from .Board import *
from .GraphicalInterface import *
from .Player import *


class Game:
    def __init__(self, white_player, black_player):
        self._board_log = []
        self._move_log = []
        self._board_log.append(TestBoard())
        self._gui = GraphicalInterface(self._board_log[-1])
        self._white_player = white_player
        self._black_player = black_player


    def reset_game(self):
        self._board_log = []
        self._board_log.append(TestBoard())
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
        self._gui.end_game(board, stale_mate)

    def next_move(self):
        if self._board_log[-1].turn == Color.BLACK:
            move = self._black_player.perform_move(self._board_log[-1])
        else:
            move = self._white_player.perform_move(self._board_log[-1])
        return move
