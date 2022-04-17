import unittest

from model.board_for_testing import Board
from model.pieces.bishop import Bishop
from model.pieces.king import King
from model.pieces.knight import Knight
from model.pieces.pawn import Pawn
from model.pieces.queen import Queen
from model.pieces.rook import Rook
from model.square_validator import SquareValidator


class TestMovements(unittest.TestCase):
    """
    1 - enemy
    -1 - teammate
    0 - empty
    """
    checking_pieces = {'black': [], 'white': []}

    def test_should_check_piece_movement_black_pawn(self):
        pawn = Pawn(colour="black")
        b = Board()
        sqv = SquareValidator()
        kp = [(7, 4), (0, 4)]
        kuc = [False, False]
        checking_pieces = {'black': [], 'white': []}

        pawn.rank, pawn.file = 6, 0
        move = pawn.move('a7', 'a6', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(True, move)
        self.assertEqual(5, pawn.rank)
        self.assertEqual(0, pawn.file)

        pawn.rank, pawn.file = 6, 4
        move = pawn.move('e7', 'e5', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(True, move)
        self.assertEqual(4, pawn.rank)
        self.assertEqual(4, pawn.file)

        pawn.rank, pawn.file = 6, 5
        move = pawn.move('f7', 'f4', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(False, move)
        self.assertEqual(6, pawn.rank)
        self.assertEqual(5, pawn.file)

        pawn.rank, pawn.file = 6, 7
        move = pawn.move('h7', 'g7', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(False, move)
        self.assertEqual(6, pawn.rank)
        self.assertEqual(7, pawn.file)

    def test_should_check_piece_movement_white_pawn(self):
        pawn = Pawn(colour="white")
        b = Board()
        sqv = SquareValidator()
        kp = [(7, 4), (0, 4)]
        kuc = [False, False]
        checking_pieces = {'black': [], 'white': []}

        pawn.rank, pawn.file = 1, 0
        move = pawn.move('a2', 'a4', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(True, move)
        self.assertEqual(3, pawn.rank)
        self.assertEqual(0, pawn.file)

        b.board[2][1] = Pawn(colour="white")
        pawn.rank, pawn.file = 2, 1
        move = pawn.move('b3', 'b5', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(False, move)
        self.assertEqual(2, pawn.rank)
        self.assertEqual(1, pawn.file)

        b.board[5][6] = Pawn(colour="white")
        pawn.rank, pawn.file = 5, 6
        move = pawn.move('g6', 'g4', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(False, move)
        self.assertEqual(5, pawn.rank)
        self.assertEqual(6, pawn.file)

        # with self.assertRaises(ValueError):
        #     pawn.move('y2', 'a4', kp, kuc, b.board, sqv,
        #               checking_pieces=checking_pieces)
        #     pawn.move('a2', 'k4', kp, kuc, b.board, sqv,
        #               checking_pieces=checking_pieces)

        pawn.rank, pawn.file = 2, 1
        move = pawn.move('b3', 'b4', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(True, move)
        self.assertEqual(3, pawn.rank)
        self.assertEqual(1, pawn.file)

        pawn.rank, pawn.file = 3, 1
        b.board[3][1] = Pawn(colour="white")
        move = pawn.move('b4', 'b3', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(False, move)
        self.assertEqual(3, pawn.rank)
        self.assertEqual(1, pawn.file)

        b.board[3][0] = Pawn(colour="white")
        pawn.rank, pawn.file = 3, 0
        move = pawn.move('a4', 'a3', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(False, move)
        self.assertEqual(3, pawn.rank)
        self.assertEqual(0, pawn.file)

        # pawn.rank, pawn.file = 5, 6
        move = pawn.move('a4', 'b2', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(False, move)
        self.assertEqual(3, pawn.rank)
        self.assertEqual(0, pawn.file)

        move = pawn.move('a4', 'a6', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(False, move)
        self.assertEqual(3, pawn.rank)
        self.assertEqual(0, pawn.file)

        # Pretend its teammate is on the square it
        # wants to occupy.
        b.board[2][2] = -1
        pawn.rank, pawn.file = 1, 2
        move = pawn.move('c2', 'c3', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(False, move)
        self.assertEqual(1, pawn.rank)
        self.assertEqual(2, pawn.file)

    def test_should_check_piece_movement_knight(self):
        knight = Knight(colour="black")
        b = Board()
        sqv = SquareValidator()
        kp = [(7, 4), (0, 4)]
        kuc = [False, False]
        checking_pieces = {'black': [], 'white': []}

        knight.rank, knight.file = 7, 1
        move = knight.move('b8', 'a3', kp, kuc, b.board, sqv,
                           checking_pieces=checking_pieces)
        self.assertEqual(False, move)
        self.assertEqual(7, knight.rank)
        self.assertEqual(1, knight.file)

        move = knight.move('b8', 'a6', kp, kuc, b.board, sqv,
                           checking_pieces=checking_pieces)
        self.assertEqual(True, move)
        self.assertEqual(5, knight.rank)
        self.assertEqual(0, knight.file)

        knight.rank, knight.file = 0, 6
        move = knight.move('g1', 'f3', kp, kuc, b.board, sqv,
                           checking_pieces=checking_pieces)
        self.assertEqual(True, move)
        self.assertEqual(2, knight.rank)
        self.assertEqual(5, knight.file)

        # Pretend its teammate is on the square it
        # wants to occupy.
        b.board[3][3] = -1
        b.board[2][5] = Knight(colour="black")
        move = knight.move('f3', 'd4', kp, kuc, b.board, sqv,
                           checking_pieces=checking_pieces)
        self.assertEqual(False, move)
        self.assertEqual(2, knight.rank)
        self.assertEqual(5, knight.file)
        b.board[3][3] = 0

        knight.rank, knight.file = 0, 1
        move = knight.move('b1', 'a3', kp, kuc, b.board, sqv,
                           checking_pieces=checking_pieces)
        self.assertEqual(True, move)
        self.assertEqual(2, knight.rank)
        self.assertEqual(0, knight.file)

        b.board[2][0] = Knight("white")
        move = knight.move('a3', 'c4', kp, kuc, b.board, sqv,
                           checking_pieces=checking_pieces)
        self.assertEqual(True, move)
        self.assertEqual(3, knight.rank)
        self.assertEqual(2, knight.file)

        b.board[3][2] = Knight("white")
        move = knight.move('c4', 'c5', kp, kuc, b.board, sqv,
                           checking_pieces=checking_pieces)
        self.assertEqual(False, move)
        self.assertEqual(3, knight.rank)
        self.assertEqual(2, knight.file)

        b.board[6][3] = Knight("white")
        knight.rank, knight.file = 6, 3
        move = knight.move('d7', 'e4', kp, kuc, b.board, sqv,
                           checking_pieces=checking_pieces)
        self.assertEqual(False, move)
        self.assertEqual(6, knight.rank)
        self.assertEqual(3, knight.file)

    def test_should_check_piece_movement_rook(self):
        rook = Rook("white")
        b = Board()
        sqv = SquareValidator()
        kp = [(7, 4), (0, 4)]
        kuc = [False, False]
        checking_pieces = {'black': [], 'white': []}

        rook.rank, rook.file = 1, 0
        move = rook.move('a2', 'a4', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(True, move)
        self.assertEqual(3, rook.rank)
        self.assertEqual(0, rook.file)

        rook.rank, rook.file = 1, 1
        move = rook.move('b1', 'a4', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(False, move)
        self.assertEqual(1, rook.rank)
        self.assertEqual(1, rook.file)

        rook.rank, rook.file = 6, 4
        move = rook.move('e7', 'e7', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(False, move)
        self.assertEqual(6, rook.rank)
        self.assertEqual(4, rook.file)

        b.board[5][6] = Rook("black")
        rook.rank, rook.file, rook.colour = 5, 6, "black"
        # print(b.board[1][6])
        move = rook.move('g6', 'g2', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(True, move)
        self.assertEqual(1, rook.rank)
        self.assertEqual(6, rook.file)

        b.board[3][7] = Rook("black")
        rook.rank, rook.file = 3, 7
        move = rook.move('h4', 'a4', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(True, move)
        self.assertEqual(3, rook.rank)
        self.assertEqual(0, rook.file)

        rook.rank, rook.file = 1, 6
        move = rook.move('g2', 'h4', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(False, move)
        self.assertEqual(1, rook.rank)
        self.assertEqual(6, rook.file)

        b.board[3][5] = -1
        rook.rank, rook.file = 1, 4
        move = rook.move('e2', 'e5', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(True, move)
        self.assertEqual(4, rook.rank)
        self.assertEqual(4, rook.file)

        rook.rank, rook.file = 1, 5
        move = rook.move('f2', 'f5', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(False, move)
        self.assertEqual(1, rook.rank)
        self.assertEqual(5, rook.file)

        move = rook.move('f2', 'f4', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(False, move)

        move = rook.move('f2', 'f3', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(True, move)
        self.assertEqual(2, rook.rank)
        self.assertEqual(5, rook.file)

        b.board[3][0] = Rook("black")
        rook.rank, rook.file = 3, 0
        move = rook.move('a4', 'h4', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(False, move)
        self.assertEqual(3, rook.rank)
        self.assertEqual(0, rook.file)

        rook.rank, rook.file = 6, 5
        move = rook.move('f7', 'f3', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(False, move)
        self.assertEqual(6, rook.rank)
        self.assertEqual(5, rook.file)

    def test_should_check_piece_movement_bishop(self):
        bishop = Bishop("white")
        b = Board()
        sqv = SquareValidator()
        kp = [(7, 4), (0, 4)]
        kuc = [False, False]
        checking_pieces = {'black': [], 'white': []}
        b.board[6] = b.board[1] = [0] * 8

        bishop.rank, bishop.file = 0, 7
        move = bishop.move('h1', 'b6', kp, kuc, b.board, sqv,
                           checking_pieces=checking_pieces)
        self.assertEqual(False, move)
        self.assertEqual(0, bishop.rank)
        self.assertEqual(7, bishop.file)

        bishop.rank, bishop.file = 0, 1
        move = bishop.move('b1', 'd3', kp, kuc, b.board, sqv,
                           checking_pieces=checking_pieces)
        self.assertEqual(True, move)
        self.assertEqual(2, bishop.rank)
        self.assertEqual(3, bishop.file)

        bishop.rank, bishop.file = 0, 5
        move = bishop.move('f1', 'g8', kp, kuc, b.board, sqv,
                           checking_pieces=checking_pieces)
        self.assertEqual(False, move)
        self.assertEqual(0, bishop.rank)
        self.assertEqual(5, bishop.file)

        bishop.rank, bishop.file = 7, 5
        move = bishop.move('f8', 'f7', kp, kuc, b.board, sqv,
                           checking_pieces=checking_pieces)
        self.assertEqual(False, move)
        self.assertEqual(7, bishop.rank)
        self.assertEqual(5, bishop.file)

        b.board[7][7] = Bishop("black")
        b.board[1][1] = 0
        b.board[0][0] = 0
        b.board[6][6] = 0

        bishop.rank, bishop.file = 7, 7
        move = bishop.move('h8', 'a1', kp, kuc, b.board, sqv,
                           checking_pieces=checking_pieces)
        self.assertEqual(True, move)
        self.assertEqual(0, bishop.rank)
        self.assertEqual(0, bishop.file)

        b.board[0][0] = Bishop("white")
        move = bishop.move('a1', 'h8', kp, kuc, b.board, sqv,
                           checking_pieces=checking_pieces)
        self.assertEqual(True, move)
        self.assertEqual(7, bishop.rank)
        self.assertEqual(7, bishop.file)

        move = bishop.move('h8', 'a8', kp, kuc, b.board, sqv,
                           checking_pieces=checking_pieces)
        self.assertEqual(False, move)
        self.assertEqual(7, bishop.rank)
        self.assertEqual(7, bishop.file)

        b.board[3][3] = -1  # d4
        move = bishop.move('h8', 'a1', kp, kuc, b.board, sqv,
                           checking_pieces=checking_pieces)
        self.assertEqual(False, move)
        self.assertEqual(7, bishop.rank)
        self.assertEqual(7, bishop.file)

        move = bishop.move('h8', 'e5', kp, kuc, b.board, sqv,
                           checking_pieces=checking_pieces)
        self.assertEqual(True, move)
        self.assertEqual(4, bishop.rank)
        self.assertEqual(4, bishop.file)

        # validate checks
        new_board = Board()
        new_board.board[6] = [0] * 8
        new_board.board[1] = [0] * 8

        bishop.rank, bishop.file = 0, 5
        move = bishop.move('f1', 'b5', kp, kuc, new_board.board,
                           sqv, checking_pieces=checking_pieces)
        self.assertEqual(True, kuc[0])
        self.assertEqual(True, move)
        self.assertEqual(4, bishop.rank)
        self.assertEqual(1, bishop.file)

        kuc = [False, False]
        new_board.board[6][3] = Pawn("black")
        new_board.board[4][1] = Bishop("white")
        bishop.rank, bishop.file = 4, 1
        move = bishop.move('b5', 'c4', kp, kuc, new_board.board,
                           sqv, checking_pieces=checking_pieces)
        self.assertEqual(False, kuc[0])
        self.assertEqual(True, move)
        self.assertEqual(3, bishop.rank)
        self.assertEqual(2, bishop.file)

        new_board.board[4][1] = Bishop("white")
        new_board.board[6][3] = Pawn("black")
        bishop.rank, bishop.file = 4, 1
        move = bishop.move('b5', 'd7', kp, kuc, new_board.board,
                           sqv, checking_pieces=checking_pieces)
        self.assertEqual(True, kuc[0])
        self.assertEqual(True, move)
        self.assertEqual(6, bishop.rank)
        self.assertEqual(3, bishop.file)

    def test_should_check_piece_movement_queen(self):
        queen = Queen()
        b = Board()
        sqv = SquareValidator()
        kp = [(7, 4), (0, 4)]
        kuc = [False, False]
        checking_pieces = {'black': [], 'white': []}

        queen.rank, queen.file, queen.colour = 0, 1, "white"
        move = queen.move('b1', 'a3', kp, kuc, b.board, sqv,
                          checking_pieces=checking_pieces)
        self.assertEqual(False, move)
        self.assertEqual(0, queen.rank)
        self.assertEqual(1, queen.file)

        # Rook-like moves
        b.board[3][5] = -1  # f4
        queen.rank, queen.file = 1, 4
        move = queen.move('e2', 'e5', kp, kuc, b.board, sqv,
                          checking_pieces=checking_pieces)
        self.assertEqual(True, move)
        self.assertEqual(4, queen.rank)
        self.assertEqual(4, queen.file)

        queen.rank, queen.file, queen.colour = 1, 5, "black"
        move = queen.move('f2', 'f5', kp, kuc, b.board, sqv,
                          checking_pieces=checking_pieces)
        self.assertEqual(False, move)
        self.assertEqual(1, queen.rank)
        self.assertEqual(5, queen.file)

        queen.rank, queen.file = 6, 4
        move = queen.move('e7', 'e7', kp, kuc, b.board, sqv,
                          checking_pieces=checking_pieces)
        self.assertEqual(False, move)
        self.assertEqual(6, queen.rank)
        self.assertEqual(4, queen.file)

        b.board[3][7] = Queen("black")
        queen.rank, queen.file = 3, 7
        move = queen.move('h4', 'a4', kp, kuc, b.board, sqv,
                          checking_pieces=checking_pieces)
        self.assertEqual(False, move)
        self.assertEqual(3, queen.rank)
        self.assertEqual(7, queen.file)

        b.board[3][5] = 0

        # Bishop-like moves
        queen.rank, queen.file, queen.colour = 0, 7, "white"
        move = queen.move('h1', 'b6', kp, kuc, b.board, sqv,
                          checking_pieces=checking_pieces)
        self.assertEqual(False, move)
        self.assertEqual(0, queen.rank)
        self.assertEqual(7, queen.file)

        b.board[1][2] = 0
        queen.rank, queen.file = 0, 1
        move = queen.move('b1', 'd3', kp, kuc, b.board, sqv,
                          checking_pieces=checking_pieces)
        self.assertEqual(True, move)
        self.assertEqual(2, queen.rank)
        self.assertEqual(3, queen.file)

        queen.rank, queen.file = 1, 6
        move = queen.move('g2', 'e4', kp, kuc, b.board, sqv,
                          checking_pieces=checking_pieces)
        self.assertEqual(True, move)
        self.assertEqual(3, queen.rank)
        self.assertEqual(4, queen.file)

        b.board[5][5] = -1  # f6
        queen.rank, queen.file = 1, 1
        move = queen.move('b2', 'c3', kp, kuc, b.board, sqv,
                          checking_pieces=checking_pieces)
        self.assertEqual(True, move)
        self.assertEqual(2, queen.rank)
        self.assertEqual(2, queen.file)

        queen.rank, queen.file = 6, 6
        move = queen.move('g7', 'd4', kp, kuc, b.board, sqv,
                          checking_pieces=checking_pieces)
        self.assertEqual(False, move)
        self.assertEqual(6, queen.rank)
        self.assertEqual(6, queen.file)

        # b.board[0][6] = 0
        b.board[5][1] = Queen("black")
        b.board[1][5] = 0
        b.board[5][1].rank, b.board[5][1].file = 5, 1
        queen.rank, queen.file, queen.colour = 5, 1, "black"
        move = b.board[5][1].move('b6', 'g1', kp, kuc, b.board, sqv,
                                  checking_pieces=checking_pieces)
        self.assertEqual(True, move)
        self.assertEqual(0, b.board[5][1].rank)
        self.assertEqual(6, b.board[5][1].file)

        queen.rank, queen.file = 7, 3
        move = queen.move('d8', 'f6', kp, kuc, b.board, sqv,
                          checking_pieces=checking_pieces)
        self.assertEqual(False, move)
        self.assertEqual(7, queen.rank)
        self.assertEqual(3, queen.file)

    def test_should_check_piece_movement_king(self):
        king = King("white")
        b = Board()
        sqv = SquareValidator()
        kp = [(7, 4), (0, 4)]
        kuc = [False, False]
        b.board[6] = [0] * 8
        b.board[1] = [0] * 8
        checking_pieces = {'black': [], 'white': []}

        king.rank, king.file = 0, 1
        move = king.move('b1', 'a3', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(False, move)
        self.assertEqual(0, king.rank)
        self.assertEqual(1, king.file)

        king.rank, king.file = 0, 4
        move = king.move('e1', 'f2', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(True, move)
        self.assertEqual(1, king.rank)
        self.assertEqual(5, king.file)

        king.rank, king.file = 7, 7
        move = king.move('h8', 'h5', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(False, move)
        self.assertEqual(7, king.rank)
        self.assertEqual(7, king.file)

        b.board[6][4] = Knight("white")  # e6
        king.rank, king.file = 6, 2
        move = king.move('c7', 'c6', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(False, move)
        self.assertEqual(6, king.rank)
        self.assertEqual(2, king.file)

        # knight-protected squares
        b.board[3][6] = Knight("white")  # g4
        b.board[5][4] = King("black")  # e6
        king.rank, king.file = 5, 4
        move = king.move('e6', 'f6', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(False, move)
        self.assertEqual(5, king.rank)
        self.assertEqual(4, king.file)

        # queen-, bishop-, pawn-, king-, rook-protected squares
        b.board[2][2] = Queen("black")  # c3
        king.rank, king.file = 0, 6
        move = king.move('g1', 'h2', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(False, move)
        self.assertEqual(0, king.rank)
        self.assertEqual(6, king.file)

        king.rank, king.file, king.colour = 7, 6, "white"
        move = king.move('g8', 'h7', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(False, move)
        self.assertEqual(7, king.rank)
        self.assertEqual(6, king.file)

        king.rank, king.file = 6, 2
        move = king.move('c7', 'c8', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(False, move)
        self.assertEqual(6, king.rank)
        self.assertEqual(2, king.file)

        b.board[3][5] = King("black")  # f4
        king.rank, king.file = 3, 5
        move = king.move('f4', 'g5', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(True, move)
        self.assertEqual(4, king.rank)
        self.assertEqual(6, king.file)

        king.rank, king.file = 3, 5
        move = king.move('f4', 'g4', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(False, move)
        self.assertEqual(3, king.rank)
        self.assertEqual(5, king.file)


class TestCastling(unittest.TestCase):
    def test_should_check_castling_kingside(self):
        king = King()
        b = Board()
        sqv = SquareValidator()
        kp = [(7, 4), (0, 4)]
        kuc = [False, False]
        b.board[6] = b.board[1] = [0] * 8
        checking_pieces = {'black': [], 'white': []}

        # White
        king.can_castle = False
        move = b.board[0][4].move('e1', 'g1', kp, kuc, b.board, sqv,
                                  checking_pieces=checking_pieces)
        self.assertEqual(False, move)

        b.board[0][5] = 0
        b.board[0][6] = 0
        b.board[0][4].can_castle = False
        move = b.board[0][4].move('e1', 'g1', kp, kuc, b.board, sqv,
                                  checking_pieces=checking_pieces)
        # assume one of them has moved previously
        self.assertEqual(False, move)

        b.board[0][7].can_castle = False
        b.board[0][4].can_castle = True
        move = b.board[0][4].move('e1', 'g1', kp, kuc, b.board, sqv,
                                  checking_pieces=checking_pieces)
        self.assertEqual(False, move)

        b.board[0][7].can_castle = True
        move = b.board[0][4].move('e1', 'g1', kp, kuc, b.board, sqv,
                                  checking_pieces=checking_pieces)
        self.assertEqual(True, move)
        # self.assertEqual(True, isinstance(b.board[0][5], Rook))

        # Black
        b.board[7][4].can_castle = False
        move = b.board[7][4].move('e8', 'g8', kp, kuc, b.board, sqv,
                                  checking_pieces=checking_pieces)
        self.assertEqual(False, move)

        b.board[7][5] = 0
        b.board[7][6] = 0
        move = b.board[7][4].move('e8', 'g8', kp, kuc, b.board, sqv,
                                  checking_pieces=checking_pieces)
        self.assertEqual(False, move)

        b.board[7][7].can_castle = False
        b.board[7][4].can_castle = True
        move = b.board[7][4].move('e8', 'g8', kp, kuc, b.board, sqv,
                                  checking_pieces=checking_pieces)
        self.assertEqual(False, move)

        b.board[7][7].can_castle = True
        move = b.board[7][4].move('e8', 'g8', kp, kuc, b.board, sqv,
                                  checking_pieces=checking_pieces)
        self.assertEqual(True, move)

    def test_should_check_castling_queenside(self):
        king = King()
        b = Board()
        sqv = SquareValidator()
        kp = [(7, 4), (0, 4)]
        kuc = [False, False]
        b.board[6] = b.board[1] = [0] * 8
        checking_pieces = {'black': [], 'white': []}

        # White
        b.board[0][4].can_castle = False
        move = b.board[0][4].move('e1', 'c1', kp, kuc, b.board, sqv,
                                  checking_pieces=checking_pieces)
        self.assertEqual(False, move)

        b.board[0][1] = 0
        b.board[0][2] = 0
        b.board[0][3] = 0
        move = b.board[0][4].move('e1', 'c1', kp, kuc, b.board, sqv,
                                  checking_pieces=checking_pieces)
        # assume one of them has moved previously
        self.assertEqual(False, move)

        b.board[0][4].can_castle = True
        move = b.board[0][4].move('e1', 'c1', kp, kuc, b.board, sqv,
                                  checking_pieces=checking_pieces)
        # can't castle cos the queen threatens one of the squares
        self.assertEqual(False, move)

        kuc[1] = True
        move = b.board[0][4].move('e1', 'c1', kp, kuc, b.board, sqv,
                                  checking_pieces=checking_pieces)
        self.assertEqual(False, move)  # can't castle cos the king is in check

        kuc[1] = False
        b.board[7][3] = 0
        b.board[0][0].can_castle = False
        move = b.board[0][4].move('e1', 'c1', kp, kuc, b.board, sqv,
                                  checking_pieces=checking_pieces)
        self.assertEqual(False, move)  # can't castle cos the rook has moved

        b.board[0][0].can_castle = True
        move = b.board[0][4].move('e1', 'c1', kp, kuc, b.board, sqv,
                                  checking_pieces=checking_pieces)
        self.assertEqual(True, move)

        # Black
        b.board[7][4].can_castle = False
        move = b.board[7][4].move('e8', 'c8', kp, kuc, b.board, sqv,
                                  checking_pieces=checking_pieces)
        self.assertEqual(False, move)

        b.board[7][1] = 0
        b.board[7][2] = 0
        b.board[7][3] = 0
        move = b.board[7][4].move('e8', 'c8', kp, kuc, b.board, sqv,
                                  checking_pieces=checking_pieces)
        self.assertEqual(False, move)

        b.board[7][4].can_castle = True
        move = b.board[7][4].move('e8', 'c8', kp, kuc, b.board, sqv,
                                  checking_pieces=checking_pieces)
        self.assertEqual(True, move)
