from model.pieces.bishop import Bishop
from model.pieces.king import King
from model.pieces.knight import Knight
from model.pieces.pawn import Pawn
from model.pieces.queen import Queen
from model.pieces.rook import Rook


class Board:
    def __init__(self) -> None:
        self.board = [[0] * 8 for _ in range(8)]
        self.white_active_pieces = []
        self.black_active_pieces = []
        for rank in range(7, -1, -1):
            for file in range(8):
                if rank == 1:
                    self.board[7 - rank][file] = Pawn(colour="black")
                elif rank == 6:
                    self.board[7 - rank][file] = Pawn(colour="white")
                # rooks
                if (rank, file) in [(0, 0), (0, 7)]:
                    self.board[7 - rank][file] = Rook(colour="black")
                elif (rank, file) in [(7, 0), (7, 7)]:
                    self.board[7 - rank][file] = Rook(colour="white")
                # knights
                elif (rank, file) in [(0, 1), (0, 6)]:
                    self.board[7 - rank][file] = Knight(colour="black")
                elif (rank, file) in [(7, 1), (7, 6)]:
                    self.board[7 - rank][file] = Knight(colour="white")
                # bishops
                elif (rank, file) in [(0, 2), (0, 5)]:
                    self.board[7 - rank][file] = Bishop(colour="black")
                elif (rank, file) in [(7, 2), (7, 5)]:
                    self.board[7 - rank][file] = Bishop(colour="white")
                # queens
                elif (rank, file) == (0, 3):
                    self.board[7 - rank][file] = Queen(colour="black")
                elif (rank, file) == (7, 3):
                    self.board[7 - rank][file] = Queen(colour="white")
                # kings
                elif (rank, file) == (0, 4):
                    self.board[7 - rank][file] = King(colour="black")
                elif (rank, file) == (7, 4):
                    self.board[7 - rank][file] = King(colour="white")

                if self.board[7 - rank][file]:
                    p = self.board[7 - rank][file]
                    if p.colour == "white":
                        self.white_active_pieces.append(p)
                    else:
                        self.black_active_pieces.append(p)
                    self.board[7 - rank][file].rank, self.board[7 - rank][file].file = (
                        7 - rank,
                        file,
                    )
