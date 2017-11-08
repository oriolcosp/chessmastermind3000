from .Static import *


# TODO Implement real graphical interface. Then implement mouse players with screen interaction
class GraphicalInterface:

    def __init__(self, board):
        self._board = board

    # TODO Correctly represent Turn color. Right now we are not getting correct string from print(board.turn)
    def draw_board(self, board):
        self._board = board
        print(" -----------------------------------------")
        for i in range(board.size):
            board_line = ""
            board_line += str(board.size-i) + "| "
            for j in range(board.size):
                if board.get_cell(i, j):
                    board_line += str(board.get_cell(i, j)) + " "
                else:
                    board_line += "   "
                board_line += "| "
            print(board_line)
            print(" -----------------------------------------")
        print("    A    B    C    D    E    F    G    H")
        print(board.turn)

    def end_game(self, board, draw):
        if draw:
            print("Game finished with draw")
        elif board.turn == Color.WHITE:
            print("Black Player Wins!")
        else:
            print("White Player Wins!")
