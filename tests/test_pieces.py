import unittest

from model.board_for_testing import Board
from model.pieces import *
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

        move = pawn.move('a7', 'a6', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(True, move)
        move = pawn.move('e7', 'e5', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(True, move)
        move = pawn.move('f7', 'f4', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(False, move)
        move = pawn.move('h7', 'g7', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(False, move)

    def test_should_check_piece_movement_white_pawn(self):
        pawn = Pawn(colour="white")
        b = Board()
        sqv = SquareValidator()
        kp = [(7, 4), (0, 4)]
        kuc = [False, False]
        checking_pieces = {'black': [], 'white': []}

        move = pawn.move('a2', 'a4', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(True, move)
        b.board[2][1] = Pawn(colour="white")
        move = pawn.move('b3', 'b5', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(False, move)
        b.board[5][6] = Pawn(colour="white")
        move = pawn.move('g6', 'g4', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(False, move)
        with self.assertRaises(ValueError):
            pawn.move('y2', 'a4', kp, kuc, b.board, sqv,
                      checking_pieces=checking_pieces)
            pawn.move('a2', 'k4', kp, kuc, b.board, sqv,
                      checking_pieces=checking_pieces)
        move = pawn.move('b3', 'b4', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(True, move)
        b.board[3][1] = Pawn(colour="white")
        move = pawn.move('b4', 'b3', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(False, move)
        b.board[3][0] = Pawn(colour="white")
        move = pawn.move('a4', 'a3', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(False, move)
        move = pawn.move('a4', 'b2', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(False, move)
        move = pawn.move('a4', 'a6', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(False, move)

        # Pretend its teammate is on the square it
        # wants to occupy.
        b.board[2][2] = -1
        move = pawn.move('c2', 'c3', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(False, move)

    def test_should_check_piece_movement_knight(self):
        knight = Knight(colour="black")
        b = Board()
        sqv = SquareValidator()
        kp = [(7, 4), (0, 4)]
        kuc = [False, False]
        checking_pieces = {'black': [], 'white': []}

        move = knight.move('b8', 'a3', kp, kuc, b.board, sqv,
                           checking_pieces=checking_pieces)
        self.assertEqual(False, move)
        move = knight.move('b8', 'a6', kp, kuc, b.board, sqv,
                           checking_pieces=checking_pieces)
        self.assertEqual(True, move)
        move = knight.move('g1', 'f3', kp, kuc, b.board, sqv,
                           checking_pieces=checking_pieces)
        self.assertEqual(True, move)

        # Pretend its teammate is on the square it
        # wants to occupy.
        b.board[3][3] = -1
        b.board[2][5] = Knight(colour="black")
        move = knight.move('f3', 'd4', kp, kuc, b.board, sqv,
                           checking_pieces=checking_pieces)
        self.assertEqual(False, move)
        b.board[3][3] = 0

        move = knight.move('b1', 'a3', kp, kuc, b.board, sqv,
                           checking_pieces=checking_pieces)
        self.assertEqual(True, move)
        b.board[2][0] = Knight("white")
        move = knight.move('a3', 'c4', kp, kuc, b.board, sqv,
                           checking_pieces=checking_pieces)
        self.assertEqual(True, move)
        b.board[3][2] = Knight("white")
        move = knight.move('c4', 'c5', kp, kuc, b.board, sqv,
                           checking_pieces=checking_pieces)
        self.assertEqual(False, move)
        b.board[6][3] = Knight("white")
        move = knight.move('d7', 'e4', kp, kuc, b.board, sqv,
                           checking_pieces=checking_pieces)
        self.assertEqual(False, move)

    def test_should_check_piece_movement_rook(self):
        rook = Rook("white")
        b = Board()
        sqv = SquareValidator()
        kp = [(7, 4), (0, 4)]
        kuc = [False, False]
        checking_pieces = {'black': [], 'white': []}

        move = rook.move('a2', 'a4', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(True, move)
        move = rook.move('b1', 'a4', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(False, move)
        move = rook.move('e7', 'e7', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(False, move)
        b.board[5][6] = Rook("black")
        move = rook.move('g6', 'g2', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(True, move)
        b.board[3][7] = Rook("black")
        move = rook.move('h4', 'a4', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(True, move)
        move = rook.move('g2', 'h4', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(False, move)

        b.board[3][5] = -1
        move = rook.move('e2', 'e5', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(True, move)
        move = rook.move('f2', 'f5', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(False, move)
        move = rook.move('f2', 'f4', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(False, move)
        move = rook.move('f2', 'f3', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(True, move)
        b.board[3][0] = Rook("black")
        move = rook.move('a4', 'h4', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(False, move)
        move = rook.move('f7', 'f3', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(False, move)

    def test_should_check_piece_movement_bishop(self):
        bishop = Bishop("white")
        b = Board()
        sqv = SquareValidator()
        kp = [(7, 4), (0, 4)]
        kuc = [False, False]
        checking_pieces = {'black': [], 'white': []}
        b.board[6] = b.board[1] = [0] * 8

        move = bishop.move('h1', 'b6', kp, kuc, b.board, sqv,
                           checking_pieces=checking_pieces)
        self.assertEqual(False, move)
        move = bishop.move('b1', 'd3', kp, kuc, b.board, sqv,
                           checking_pieces=checking_pieces)
        self.assertEqual(True, move)
        move = bishop.move('f1', 'g8', kp, kuc, b.board, sqv,
                           checking_pieces=checking_pieces)
        self.assertEqual(False, move)
        move = bishop.move('f8', 'f7', kp, kuc, b.board, sqv,
                           checking_pieces=checking_pieces)
        self.assertEqual(False, move)
        b.board[7][7] = Bishop("black")
        b.board[1][1] = 0
        b.board[0][0] = 0
        b.board[6][6] = 0
        move = bishop.move('h8', 'a1', kp, kuc, b.board, sqv,
                           checking_pieces=checking_pieces)
        self.assertEqual(True, move)
        b.board[0][0] = Bishop("white")
        move = bishop.move('a1', 'h8', kp, kuc, b.board, sqv,
                           checking_pieces=checking_pieces)
        self.assertEqual(True, move)
        move = bishop.move('h8', 'a8', kp, kuc, b.board, sqv,
                           checking_pieces=checking_pieces)
        self.assertEqual(False, move)

        b.board[3][3] = -1  # d4
        move = bishop.move('h8', 'a1', kp, kuc, b.board, sqv,
                           checking_pieces=checking_pieces)
        self.assertEqual(False, move)
        move = bishop.move('h8', 'e5', kp, kuc, b.board, sqv,
                           checking_pieces=checking_pieces)
        self.assertEqual(True, move)

        # validate checks
        new_board = Board()
        new_board.board[6] = new_board.board[1] = [0] * 8
        new_board.board[1][4] = 0
        new_board.board[6][3] = 0
        move = bishop.move('f1', 'b5', kp, kuc, new_board.board,
                           sqv, checking_pieces=checking_pieces)
        self.assertEqual(True, kuc[0])

        kuc = [False, False]
        new_board.board[6][3] = Pawn("black")
        new_board.board[4][1] = Bishop("white")
        move = bishop.move('b5', 'c4', kp, kuc, new_board.board,
                           sqv, checking_pieces=checking_pieces)
        self.assertEqual(False, kuc[0])
        new_board.board[4][1] = Bishop("white")
        new_board.board[6][3] = Pawn("black")
        move = bishop.move('b5', 'd7', kp, kuc, new_board.board,
                           sqv, checking_pieces=checking_pieces)
        self.assertEqual(True, kuc[0])

    def test_should_check_piece_movement_queen(self):
        queen = Queen()
        b = Board()
        sqv = SquareValidator()
        kp = [(7, 4), (0, 4)]
        kuc = [False, False]
        checking_pieces = {'black': [], 'white': []}

        move = queen.move('b1', 'a3', kp, kuc, b.board, sqv,
                          checking_pieces=checking_pieces)
        self.assertEqual(False, move)

        # Rook-like moves
        b.board[3][5] = -1  # f4
        move = queen.move('e2', 'e5', kp, kuc, b.board, sqv,
                          checking_pieces=checking_pieces)
        self.assertEqual(True, move)
        move = queen.move('f2', 'f5', kp, kuc, b.board, sqv,
                          checking_pieces=checking_pieces)
        self.assertEqual(False, move)
        move = queen.move('e7', 'e7', kp, kuc, b.board, sqv,
                          checking_pieces=checking_pieces)
        self.assertEqual(False, move)
        b.board[3][7] = Queen("black")
        move = queen.move('h4', 'a4', kp, kuc, b.board, sqv,
                          checking_pieces=checking_pieces)
        self.assertEqual(False, move)
        b.board[3][5] = 0

        # Bishop-like moves
        move = queen.move('h1', 'b6', kp, kuc, b.board, sqv,
                          checking_pieces=checking_pieces)
        self.assertEqual(False, move)
        b.board[1][2] = 0
        move = queen.move('b1', 'd3', kp, kuc, b.board, sqv,
                          checking_pieces=checking_pieces)
        self.assertEqual(True, move)
        move = queen.move('g2', 'e4', kp, kuc, b.board, sqv,
                          checking_pieces=checking_pieces)
        self.assertEqual(True, move)

        b.board[5][5] = -1  # f6
        move = queen.move('b2', 'c3', kp, kuc, b.board, sqv,
                          checking_pieces=checking_pieces)
        self.assertEqual(True, move)
        move = queen.move('g7', 'd4', kp, kuc, b.board, sqv,
                          checking_pieces=checking_pieces)
        self.assertEqual(False, move)
        # b.board[0][6] = 0
        b.board[5][1] = Queen("black")
        b.board[1][5] = 0
        move = queen.move('b6', 'g1', kp, kuc, b.board, sqv,
                          checking_pieces=checking_pieces)
        self.assertEqual(True, move)
        move = queen.move('d8', 'f6', kp, kuc, b.board, sqv,
                          checking_pieces=checking_pieces)
        self.assertEqual(False, move)

    def test_should_check_piece_movement_king(self):
        king = King()
        b = Board()
        sqv = SquareValidator()
        kp = [(7, 4), (0, 4)]
        kuc = [False, False]
        b.board[6] = b.board[1] = [0] * 8
        checking_pieces = {'black': [], 'white': []}

        move = king.move('b1', 'a3', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(False, move)
        move = king.move('e1', 'f2', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(True, move)
        move = king.move('h8', 'h5', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(False, move)
        b.board[6][2] = Knight("white")  # e6
        move = king.move('c7', 'c6', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(False, move)

        # knight-protected squares
        b.board[3][6] = Knight("white")  # g4
        b.board[5][4] = King("black")  # e6
        move = king.move('e6', 'f6', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(False, move)

        # queen-, bishop-, pawn-, king-, rook-protected squares
        b.board[2][2] = Queen("black")  # c3
        move = king.move('g1', 'h2', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(False, move)
        move = king.move('g8', 'h7', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(False, move)
        move = king.move('c7', 'c8', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(False, move)
        b.board[3][5] = King("black")  # f4
        move = king.move('f4', 'g5', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(False, move)
        move = king.move('f4', 'g4', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(False, move)


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
        move = king.move('e1', 'g1', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(False, move)
        b.board[0][5] = 0
        b.board[0][6] = 0
        move = king.move('e1', 'g1', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(False, move)  # assume one of them has moved previously
        b.board[0][7].can_castle = False 
        king.can_castle = True
        move = king.move('e1', 'g1', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(False, move)
        b.board[0][7].can_castle = True
        move = king.move('e1', 'g1', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(True, move)
        # self.assertEqual(True, isinstance(b.board[0][5], Rook))

        # Black
        king.can_castle = False
        move = king.move('e8', 'g8', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(False, move)
        
        b.board[7][5] = 0
        b.board[7][6] = 0
        move = king.move('e8', 'g8', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(False, move)
        b.board[7][7].can_castle = False
        king.can_castle = True
        move = king.move('e8', 'g8', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(False, move)
        b.board[7][7].can_castle = True
        move = king.move('e8', 'g8', kp, kuc, b.board, sqv,
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
        king.can_castle = False
        move = king.move('e1', 'c1', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(False, move)
        b.board[0][1] = 0
        b.board[0][2] = 0
        b.board[0][3] = 0
        move = king.move('e1', 'c1', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(False, move)  # assume one of them has moved previously
        king.can_castle = True
        move = king.move('e1', 'c1', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(False, move)  # can't castle cos the queen threatens one of the squares
        kuc[1] = True
        move = king.move('e1', 'c1', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(False, move)  # can't castle cos the king is in check
        kuc[1] = False
        b.board[7][3] = 0
        b.board[0][0].can_castle = False 
        move = king.move('e1', 'c1', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(False, move)  # can't castle cos the rook has moved
        b.board[0][0].can_castle = True
        move = king.move('e1', 'c1', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(True, move)

        # Black
        king.can_castle = False
        move = king.move('e8', 'c8', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(False, move)
        
        b.board[7][1] = 0
        b.board[7][2] = 0
        b.board[7][3] = 0
        move = king.move('e8', 'c8', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(False, move)
        # b.board[7][0].can_castle = True
        king.can_castle = True
        move = king.move('e8', 'c8', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(True, move)
