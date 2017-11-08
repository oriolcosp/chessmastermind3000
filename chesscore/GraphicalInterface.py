class GraphicalInterface:

    def __init__(self, board):
        self._board = board

    def draw_board(self, board):
        self._board = board
        print(" -----------------------------------------")
        for i in range(board.size):
            board_line = ""
            board_line += str(board.size-i) + "| "
            for j in range(board.size):
                if board.l[i][j]:
                    board_line += str(board.l[i][j]) + " "
                else:
                    board_line += "   "
                board_line += "| "
            print(board_line)
            print(" -----------------------------------------")
        print("    A    B    C    D    E    F    G    H")
        print(str(board.turn))

    def end_game(self, victory, draw):
        if victory:
            print("Game with victory!")
        if draw:
            print("Game finished with draw")