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
    checking_pieces = {'b': [], 'w': []}

    def test_should_check_piece_movement_black_pawn(self):
        pawn = Pawn()
        b = Board()
        sqv = SquareValidator()
        kp = [(7, 4), (0, 4)]
        kuc = [False, False]
        checking_pieces = {'b': [], 'w': []}

        move = pawn.move('a7', 'a6', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(True, move)
        move = pawn.move('e8', 'e7', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(False, move)
        move = pawn.move('e7', 'e5', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(True, move)
        move = pawn.move('f7', 'f4', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(False, move)
        move = pawn.move('h7', 'g7', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(False, move)
        b.board[2][0] = 'w_pa'
        move = pawn.move('a3', 'a5', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(False, move)
        b.board[5][6] = 'w_pa'
        move = pawn.move('g6', 'g4', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(False, move)

    def test_should_check_piece_movement_white_pawn(self):
        pawn = Pawn()
        b = Board()
        sqv = SquareValidator()
        kp = [(7, 4), (0, 4)]
        kuc = [False, False]
        checking_pieces = {'b': [], 'w': []}

        move = pawn.move('a2', 'a4', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(True, move)
        with self.assertRaises(ValueError):
            pawn.move('y2', 'a4', kp, kuc, b.board, sqv,
                      checking_pieces=checking_pieces)
            pawn.move('a2', 'k4', kp, kuc, b.board, sqv,
                      checking_pieces=checking_pieces)
        move = pawn.move('b2', 'b3', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(True, move)
        move = pawn.move('b3', 'b3', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(False, move)
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
        knight = Knight()
        b = Board()
        sqv = SquareValidator()
        kp = [(7, 4), (0, 4)]
        kuc = [False, False]
        checking_pieces = {'b': [], 'w': []}

        move = knight.move('b8', 'a3', kp, kuc, b.board, sqv,
                           checking_pieces=checking_pieces)
        self.assertEqual(False, move)
        move = knight.move('g1', 'f3', kp, kuc, b.board, sqv,
                           checking_pieces=checking_pieces)
        self.assertEqual(True, move)

        # Pretend its teammate is on the square it
        # wants to occupy.
        b.board[3][3] = -1
        move = knight.move('f3', 'd4', kp, kuc, b.board, sqv,
                           checking_pieces=checking_pieces)
        self.assertEqual(False, move)
        b.board[3][3] = 0

        move = knight.move('b1', 'a3', kp, kuc, b.board, sqv,
                           checking_pieces=checking_pieces)
        self.assertEqual(True, move)
        move = knight.move('a3', 'c4', kp, kuc, b.board, sqv,
                           checking_pieces=checking_pieces)
        self.assertEqual(True, move)
        move = knight.move('c4', 'c5', kp, kuc, b.board, sqv,
                           checking_pieces=checking_pieces)
        self.assertEqual(False, move)
        move = knight.move('d7', 'e4', kp, kuc, b.board, sqv,
                           checking_pieces=checking_pieces)
        self.assertEqual(False, move)

    def test_should_check_piece_movement_rook(self):
        rook = Rook()
        b = Board()
        sqv = SquareValidator()
        kp = [(7, 4), (0, 4)]
        kuc = [False, False]
        checking_pieces = {'b': [], 'w': []}

        move = rook.move('a2', 'a4', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(True, move)
        move = rook.move('b1', 'a4', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(False, move)
        move = rook.move('e7', 'e7', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(False, move)
        b.board[5][6] = 'b_ro'
        move = rook.move('g6', 'g2', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(True, move)
        b.board[3][7] = 'b_ro'
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
        move = rook.move('a4', 'h4', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(False, move)
        move = rook.move('f7', 'f3', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(False, move)

    def test_should_check_piece_movement_bishop(self):
        bishop = Bishop()
        b = Board()
        sqv = SquareValidator()
        kp = [(7, 4), (0, 4)]
        kuc = [False, False]
        checking_pieces = {'b': [], 'w': []}
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
        b.board[7][7] = 'b_bi'
        b.board[1][1] = 0
        b.board[0][0] = 0
        b.board[6][6] = 0
        move = bishop.move('h8', 'a1', kp, kuc, b.board, sqv,
                           checking_pieces=checking_pieces)
        self.assertEqual(True, move)
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
        new_board.board[6][3] = 'b_pa'
        move = bishop.move('b5', 'c4', kp, kuc, new_board.board,
                           sqv, checking_pieces=checking_pieces)
        self.assertEqual(False, kuc[0])
        new_board.board[4][1] = 'w_bi'
        new_board.board[6][3] = 'b_pa'
        move = bishop.move('b5', 'd7', kp, kuc, new_board.board,
                           sqv, checking_pieces=checking_pieces)
        self.assertEqual(True, kuc[0])

    def test_should_check_piece_movement_queen(self):
        queen = Queen()
        b = Board()
        sqv = SquareValidator()
        kp = [(7, 4), (0, 4)]
        kuc = [False, False]
        checking_pieces = {'b': [], 'w': []}

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
        b.board[3][7] = 'b_qu'
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
        b.board[5][1] = 'b_qu'
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
        checking_pieces = {'b': [], 'w': []}

        move = king.move('b1', 'a3', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(False, move)
        move = king.move('e1', 'f2', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(True, move)
        move = king.move('h8', 'h5', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(False, move)
        b.board[6][2] = 'w_ki'  # e6
        move = king.move('c7', 'c6', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(False, move)

        # knight-protected squares
        b.board[3][6] = 'w_kn'  # g4
        b.board[5][4] = 'b_ki'  # e6
        move = king.move('e6', 'f6', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(False, move)

        # queen-, bishop-, pawn-, king-, rook-protected squares
        b.board[2][2] = 'b_qu'  # c3
        move = king.move('g1', 'h2', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(False, move)
        move = king.move('g8', 'h7', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(False, move)
        move = king.move('c7', 'c8', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(False, move)
        b.board[3][5] = 'b_ki'  # f4
        move = king.move('f4', 'g5', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(False, move)
        move = king.move('f4', 'g4', kp, kuc, b.board, sqv,
                         checking_pieces=checking_pieces)
        self.assertEqual(False, move)
