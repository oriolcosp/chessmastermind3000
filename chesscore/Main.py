from chesscore.Game import Game


class Main(object):

    def start_game(self):
        game = Game()
        game.play_game()


if __name__ == '__main__':
    Main().start_game()