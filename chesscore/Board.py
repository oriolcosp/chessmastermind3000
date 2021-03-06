from chesscore.Piece import *
import copy
from .Static import Color


class Board:

    def __init__(self):
        self._size = 8
        self._l = [[None for row in range(0, self._size)] for col in range(0, self._size)]
        self._init_board()
        self._turn = Color.WHITE
        self._turnnum = 1
        self._sprite = "BoardPicture"
        self._check_mate = False
        self._stale_mate = False

    def _init_board(self):
        for i in range(self._size):
            self._l[1][i] = Pawn(Color.BLACK, 1, i)
            self._l[self._size - 2][i] = Pawn(Color.WHITE, self._size - 2, i)
        self._l[0][0] = Rook(Color.BLACK, 0, 0)
        self._l[0][self._size - 1] = Rook(Color.BLACK, 0, self._size - 1)
        self._l[self._size - 1][0] = Rook(Color.WHITE, self._size - 1, 0)
        self._l[self._size - 1][self._size - 1] = Rook(Color.WHITE, self._size - 1, self._size - 1)
        self._l[0][1] = Knight(Color.BLACK, 0, 1)
        self._l[0][self._size - 2] = Knight(Color.BLACK, 0, self._size - 2)
        self._l[self._size - 1][1] = Knight(Color.WHITE, self._size - 1, 1)
        self._l[self._size - 1][self._size - 2] = Knight(Color.WHITE, self._size - 1, self._size - 2)
        self._l[0][2] = Bishop(Color.BLACK, 0, 2)
        self._l[0][self._size - 3] = Bishop(Color.BLACK, 0, self._size - 3)
        self._l[self._size - 1][2] = Bishop(Color.WHITE, self._size - 1, 2)
        self._l[self._size - 1][self._size - 3] = Bishop(Color.WHITE, self._size - 1, self._size - 3)
        self._l[0][3] = King(Color.BLACK, 0, 3)
        self._l[0][self._size - 4] = Queen(Color.BLACK, 0, self._size - 4)
        self._l[self._size - 1][3] = King(Color.WHITE, self._size - 1, 3)
        self._l[self._size - 1][self._size - 4] = Queen(Color.WHITE, self._size - 1, self._size - 4)
        
    def get_cell(self, row, col):
        return self._l[row][col]

    def set_cell(self, piece, row, col):
        self._l[row][col] = piece
        if piece:
            piece.update_position(row, col)

    def get_all_moves(self):
        moves = []
        for row in range(self._size):
            for col in range(self._size):
                if self._l[row][col] and self._l[row][col].color == self._turn:
                    piece_move = self._l[row][col].possible_moves(self)
                    if piece_move:
                        moves += piece_move
        return moves

    def move(self, move):
        board = copy.deepcopy(self)
        piece = board.get_cell(move.srow, move.scol)
        if not piece:
            return None
        if piece.color != board.turn:
            return None
        if move not in piece.possible_moves(board):
            return None
        piece.update_status(board, move)
        piece.update_board_positions(board, move)
        board.add_turn()
        if self._turn == Color.BLACK:
            board.turn = Color.WHITE
        else:
            board.turn = Color.BLACK
        if board.is_legal_board():
            return board
        else:
            return None

    def move_no_check_valid(self, move):
        board = copy.deepcopy(self)
        piece = board.get_cell(move.srow, move.scol)
        piece.update_status(board, move)
        piece.update_board_positions(board, move)
        board.add_turn()
        if self._turn == Color.BLACK:
            board.turn = Color.WHITE
        else:
            board.turn = Color.BLACK
        return board

    def is_legal_board(self):
        if self._turn == Color.BLACK:
            return not self.is_check(Color.WHITE)
        else:
            return not self.is_check(Color.BLACK)

    # TODO this can be much more optimal. Redo
    def is_check(self, color):
        king_row = -1
        king_col = -1
        king_found = False
        for row in range(self._size):
            for col in range(self._size):
                piece = self._l[row][col]
                if piece and piece.color == color and piece.id == "G":
                    king_row = row
                    king_col = col
                    king_found = True
                    break
            if king_found:
                break
        is_check = self.is_cell_menaced(king_row, king_col, color)
        return is_check

    def is_cell_menaced(self, menaced_row, menaced_col, color):
        is_menaced = False
        for row in range(self._size):
            for col in range(self._size):
                piece = self._l[row][col]
                if piece and piece.color != color and not (menaced_row == row and menaced_col == col):
                    if piece.is_menacing_cell(menaced_row, menaced_col, self):
                        is_menaced = True
                        break
            if is_menaced:
                break
        return is_menaced

    def is_check_mate(self):
        no_legal_moves = True
        for move in self.get_all_moves():
            board = self.move(move)
            if board:
                no_legal_moves = False
                break
        if no_legal_moves:
            if self.is_check(self._turn):
                self._check_mate = True
                self._stale_mate = False
            else:
                self._check_mate = False
                self._stale_mate = True
        else:
            self._check_mate = False
            self._stale_mate = False
        return self._check_mate

    def is_stale_mate(self):
        return self._stale_mate

    @property
    def l(self):
        return self._l

    @l.setter
    def l(self, l):
        self._l = l

    @property
    def turnnum(self):
        return self._turnnum

    def add_turn(self):
        self._turnnum += 1

    @property
    def turn(self):
        return self._turn

    @turn.setter
    def turn(self, turn):
        self._turn = turn

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, size):
        self._size = size


class TestBoard(Board):
    def __init__(self):
        super().__init__()

    def _init_board(self):
        for i in range(self._size):
            self._l[1][i] = Pawn(Color.BLACK, 1, i)
            self._l[self._size - 2][i] = Pawn(Color.WHITE, self._size - 2, i)
        self._l[0][0] = Rook(Color.BLACK, 0, 0)
        self._l[0][self._size - 1] = Rook(Color.BLACK, 0, self._size - 1)
        self._l[self._size - 1][0] = Rook(Color.WHITE, self._size - 1, 0)
        self._l[self._size - 1][self._size - 1] = Rook(Color.WHITE, self._size - 1, self._size - 1)
        self._l[0][1] = Knight(Color.BLACK, 0, 1)
        self._l[0][self._size - 2] = Knight(Color.BLACK, 0, self._size - 2)
        self._l[self._size - 1][1] = Knight(Color.WHITE, self._size - 1, 1)
        self._l[self._size - 1][self._size - 2] = Knight(Color.WHITE, self._size - 1, self._size - 2)
        self._l[0][2] = Bishop(Color.BLACK, 0, 2)
        self._l[0][self._size - 3] = Bishop(Color.BLACK, 0, self._size - 3)
        self._l[4][5] = Bishop(Color.WHITE, 4, 5)
        self._l[self._size - 1][self._size - 3] = Bishop(Color.WHITE, self._size - 1, self._size - 3)
        self._l[0][3] = King(Color.BLACK, 0, 3)
        self._l[0][self._size - 4] = Queen(Color.BLACK, 0, self._size - 4)
        self._l[self._size - 1][3] = King(Color.WHITE, self._size - 1, 3)
        self._l[3][0] = Queen(Color.WHITE,3 ,0 )

