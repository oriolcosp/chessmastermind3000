from .Board import *
from .Static import *


class Piece:
    def __init__(self, color, row, col):
        self._color = color
        self._steps = []
        self._value = 1
        self._last_turn_moved = -1
        self._sprite = "P"
        self._row = row
        self._col = col

    # TODO possible_moves es crida amb un boolea "collision", d'aquesta manera amb el mateix mètode
    # fem moviments possibles amb i sense bloqueig
    # Separar aquí same color i different color per poder desactivar una de les dues
    # Afegir una crida a un mètode abans d'afegir cada move que determini si hi ha escac (moviment ilegal)
    def possible_moves(self, board):
        moves = []
        for step in self._steps:
            row = self._row
            col = self._col
            no_collision = True
            no_out_boundaries = True
            while no_collision and no_out_boundaries:
                row += step[0]
                col += step[1]
                if row >= board.size or col >= board.size or row < 0 or col < 0:
                    no_out_boundaries = False
                else:
                    cell = board.get_cell(row, col)
                    if cell:
                        no_collision = False
                        if cell.color != self._color:
                            moves.append(Move(self, self._row, self._col, row, col))
                    else:
                        moves.append(Move(self, self._row, self._col, row, col))
        return moves

    def is_move_valid(self, move, board):
        if move in self.possible_moves(board):
            return board
        else:
            return None

    def is_menacing_cell(self, row, col, board):
        move = Move(self, self._row, self._col, row, col)
        moves = self.possible_moves(board)
        if move in moves:
            return True
        else:
            return False

    def update_status(self, board, move):
        self._last_turn_moved = board.turnnum

    def update_board_positions(self, board, move):
        board.set_cell(self, move.erow, move.ecol)
        board.set_cell(None, move.srow, move.scol)

    def __str__(self):
        if self._color == Color.WHITE:
            return "W" + self._sprite
        else:
            return "B" + self._sprite

    def __repr__(self):
        return self.__str__()

    @property
    def color(self):
        return self._color

    @property
    def last_turn_moved(self):
        return self._last_turn_moved

    @property
    def id(self):
        return self._sprite

    @property
    def color(self):
        return self._color

    def update_position(self, row, col):
        self._row = row
        self._col = col


class Pawn(Piece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)
        self._value = 1
        self._sprite = "P"
        self._turn_double_move = -1
        self._turn_ip_move = -1
        if color == Color.BLACK:
            self._steps = [[1, 0]]
            self._capture_steps = [[1, -1], [1, 1]]
            self._double_step = [2, 0]
        else:
            self._steps = [[-1, 0]]
            self._capture_steps = [[-1, -1], [-1, 1]]
            self._double_step = [-2, 0]

    @property
    def turn_double_move(self):
        return self._turn_double_move
    # TODO Override method with pawn movement. Care with: atac de peó, peó passat, captura al pas,
    # final de taula peó, salt doble al principi

    def possible_moves(self, board):
        moves = []
        moves += self._forward_moves(board)
        moves += self._capture_moves(board)
        moves += self._double_move(board)
        moves += self._in_passing_moves(board)
        return moves

    def _forward_moves(self, board):
        moves = []
        for step in self._steps:
            row = self._row
            col = self._col
            row += step[0]
            col += step[1]
            if not (row >= board.size or col >= board.size or row < 0 or col < 0):
                cell = board.get_cell(row, col)
                if not cell:
                    moves.append(Move(self, self._row, self._col, row, col))
        return moves

    def _capture_moves(self, board):
        moves = []
        for step in self._capture_steps:
            row = self._row
            col = self._col
            row += step[0]
            col += step[1]
            if not (row >= board.size or col >= board.size or row < 0 or col < 0):
                cell = board.get_cell(row, col)
                if cell:
                    if cell.color != self._color:
                        moves.append(Move(self, self._row, self._col, row, col))
        return moves

    def _double_move(self, board):
        moves = []
        row = self._row
        col = self._col
        row += self._double_step[0]
        col += self._double_step[1]
        if self.last_turn_moved == -1 and not (row >= board.size or col >= board.size or row < 0 or col < 0):
            cell = board.get_cell(row, col)
            if not cell:
                moves.append(Move(self, self._row, self._col, row, col))
        return moves

    def _in_passing_moves(self, board):
        moves = []
        for step in self._capture_steps:
            row = self._row
            col = self._col
            row += step[0]
            col += step[1]
            if not (row >= board.size or col >= board.size or row < 0 or col < 0):
                side_piece = board.get_cell(self._row, self._col + step[1])
                if side_piece and side_piece.id == self.id and side_piece.color != self.color \
                        and side_piece.turn_double_move == board.turnnum - 1:
                    cell = board.get_cell(row, col)
                    if not cell:
                        moves.append(Move(self, self._row, self._col, row, col))
        return moves

    def update_status(self, board, move):
        if move in self._double_move(board):
            self._turn_double_move = board.turnnum
        elif move in self._in_passing_moves(board):
            self._turn_ip_move = board.turnnum
        self._last_turn_moved = board.turnnum

    def update_board_positions(self, board, move):
        super().update_board_positions(board, move)
        if self._turn_ip_move == board.turnnum:
            board.set_cell(None, move.srow, move.ecol)
        if self._row == 0 or self._row == board.size - 1:
            board.set_cell(Queen(self._color, self._row, self._col), self._row, self._col)


class Rook(Piece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)
        self._value = 5
        self._sprite = "R"
        self._steps = [[-1, 0], [1, 0], [0, -1], [0, 1]]


class Bishop(Piece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)
        self._value = 3
        self._sprite = "B"
        self._steps = [[-1, 1], [1, 1], [-1, -1], [1, -1]]


class King(Piece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)
        self._value = 1000
        self._sprite = "G"
        self._steps = [[-1, 1], [1, 1], [-1, -1], [1, -1], [-1, 0], [1, 0], [0, -1], [0, 1]]

    # Method must be overwritten to not check castling moves. Checking them causes infinite recursion
    def is_menacing_cell(self, row, col, board):
        move = Move(self, self._row, self._col, row, col)
        moves = self._normal_moves(board)
        if move in moves:
            return True
        else:
            return False

    def possible_moves(self, board):
        moves = []
        moves += self._normal_moves(board)
        moves += self._right_castling(board)
        moves += self._left_castling(board)
        return moves

    def _normal_moves(self, board):
        moves = []
        for step in self._steps:
            row = self._row
            col = self._col
            row += step[0]
            col += step[1]
            if not (row >= board.size or col >= board.size or row < 0 or col < 0):
                cell = board.get_cell(row, col)
                if cell:
                    if cell.color != self._color:
                        moves.append(Move(self, self._row, self._col, row, col))
                else:
                    moves.append(Move(self, self._row, self._col, row, col))
        return moves

    def _right_castling(self, board):
        moves = []
        rook_col = board.size - 1
        step = 1
        moves += self._castling_moves(board, rook_col, step)
        return moves

    def _left_castling(self, board):
        moves = []
        rook_col = 0
        step = -1
        moves += self._castling_moves(board, rook_col, step)
        return moves

# TODO sembla que no funciona range de mes a menys
    def _castling_moves(self, board, rook_col, step):
        moves = []
        if self.last_turn_moved == -1:
            piece = board.get_cell(self._row, rook_col)
            if piece and piece.id == "R" and piece.last_turn_moved == -1 and piece.color == self.color:
                impossible_castling = False
                for col in range(self._col + step, rook_col - step, step):
                    if board.get_cell(self._row, col):
                        impossible_castling = True
                    if impossible_castling:
                        break
                for col in range(self._col, self._col + step * 2, step):
                    if board.is_cell_menaced(self._row, col, self._color):
                        impossible_castling = True
                if not impossible_castling:
                    moves.append(Move(self, self._row, self._col, self._row, self._col + step*2))
        return moves

    def update_board_positions(self, board, move):
        super().update_board_positions(board, move)
        if move.ecol - move.scol == -2:
            board.set_cell(board.get_cell(move.srow, 0), move.erow, move.ecol + 1)
            board.set_cell(None, move.srow, 0)
        if move.ecol - move.scol == 2:
            board.set_cell(board.get_cell(move.srow, board.size - 1), move.erow, move.ecol - 1)
            board.set_cell(None, move.srow, board.size - 1)


class Queen(Piece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)
        self._value = 9
        self._sprite = "Q"
        self._steps = [[-1, 1], [1, 1], [-1, -1], [1, -1], [-1, 0], [1, 0], [0, -1], [0, 1]]


class Knight(Piece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)
        self._value = 3
        self._sprite = "K"
        self._steps = [[-2, 1], [-2, -1], [2, -1], [2, 1], [-1, 2], [-1, -2], [1, -2], [1, 2]]

    # TODO Afegir enroque
    def possible_moves(self, board):
        moves = []
        for step in self._steps:
            row = self._row
            col = self._col
            row += step[0]
            col += step[1]
            if not (row >= board.size or col >= board.size or row < 0 or col < 0):
                cell = board.get_cell(row, col)
                if cell:
                    if cell.color != self._color:
                        moves.append(Move(self, self._row, self._col, row, col))
                else:
                    moves.append(Move(self, self._row, self._col, row, col))
        return moves


class Move:

    def __init__(self, piece, srow, scol, erow, ecol):
        self._piece = piece
        self._srow = srow
        self._erow = erow
        self._scol = scol
        self._ecol = ecol
        self._startStr = self.position_str(srow, scol)
        self._endStr = self.position_str(erow, ecol)

    def position_str (self, row, col):
        string = ''
        cols = ["A", "B", "C", "D", "E", "F", "G", "H"]
        string += str(cols[col])
        string += str(8-row)
        return string

    def __str__(self):
        string = str(self._piece)
        string += ": "
        string += self._startStr
        string += " - "
        string += self._endStr
        return string

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self._srow == other.srow and self._scol == other.scol and self._erow == other.erow and \
               self._ecol == other.ecol

    def __ne__(self, other):
        return not self.__eq__(other)

    @property
    def piece(self):
        return self._piece
    
    @property
    def erow(self):
        return self._erow

    @property
    def ecol(self):
        return self._ecol

    @property
    def srow(self):
        return self._srow

    @property
    def scol(self):
        return self._scol
