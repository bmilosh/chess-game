import unittest

from model.board_for_testing import Board
from model.checkmate_checker import LegalMovesGetter
from model.pieces import *


class TestLegalMovesGetter(unittest.TestCase):
    """
    1 - enemy
    -1 - teammate
    0 - empty
    """
    checking_pieces = {'black': [], 'white': []}

    def test_should_get_legal_pawn_moves_black(self):
        b = Board()
        lgm_getter = LegalMovesGetter(b.board)
        kp = [(7, 4), (0, 4)]
        checking_pieces = {'black': [], 'white': []}

        lgm = lgm_getter.get_pawn_legal_moves(b.board[6][0], kp[0], checking_pieces)
        self.assertEqual({(5, 0), (4, 0)}, set(lgm))

        b.board[5][1] = Pawn("white")
        b.board[5][3] = Pawn("white")
        lgm = lgm_getter.get_pawn_legal_moves(b.board[6][2], kp[0], checking_pieces)
        self.assertEqual({(5, 1), (5, 3), (5, 2), (4, 2)}, set(lgm))

        # Pinned pawn
        b.board[4][1] = Bishop("white")
        lgm = lgm_getter.get_pawn_legal_moves(b.board[6][3], kp[0], checking_pieces)
        self.assertEqual([], lgm)

        # blocked pawn
        lgm = lgm_getter.get_pawn_legal_moves(b.board[6][1], kp[0], checking_pieces)
        self.assertEqual([], lgm)

    def test_should_get_legal_pawn_moves_white(self):
        b = Board()
        lgm_getter = LegalMovesGetter(b.board)
        kp = [(7, 4), (0, 4)]
        checking_pieces = {'black': [], 'white': []}

        lgm = lgm_getter.get_pawn_legal_moves(b.board[1][3], kp[1], checking_pieces)
        self.assertEqual({(2, 3), (3, 3)}, set(lgm))

        b.board[2][3] = Pawn("white")
        b.board[2][3].rank, b.board[2][3].file = 2, 3
        lgm = lgm_getter.get_pawn_legal_moves(b.board[2][3], kp[1], checking_pieces)
        self.assertEqual({(3, 3)}, set(lgm))

        b.board[2][6] = Pawn("black")
        lgm = lgm_getter.get_pawn_legal_moves(b.board[1][7], kp[1], checking_pieces)
        self.assertEqual({(2, 6), (2, 7), (3, 7)}, set(lgm))

        b.board[2][1] = Pawn("black")
        b.board[2][2] = Pawn("black")
        lgm = lgm_getter.get_pawn_legal_moves(b.board[1][1], kp[1], checking_pieces)
        self.assertEqual({(2, 2)}, set(lgm))

        b.board[2][5] = Rook("black")
        lgm = lgm_getter.get_pawn_legal_moves(b.board[1][4], kp[1], checking_pieces)
        self.assertEqual({(2, 5), (2, 4), (3, 4)}, set(lgm))

        b.board[2][4] = Pawn("black")
        lgm = lgm_getter.get_pawn_legal_moves(b.board[1][4], kp[1], checking_pieces)
        self.assertEqual({(2, 5)}, set(lgm))

        # Pinned pawn
        b.board[2][4] = Queen("black")
        lgm = lgm_getter.get_pawn_legal_moves(b.board[1][4], kp[1], checking_pieces)
        self.assertEqual([], lgm)
