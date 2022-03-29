from model.board import Board


class Game:
    def __init__(self, board: Board) -> None:
        self.board = board

    def play(self):
        self.board.play()