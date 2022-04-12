import unittest

from model.board_for_testing import Board
from model.legal_moves_getter import LegalMovesGetter
from model.pieces import *


class TestLegalMovesGetter(unittest.TestCase):
    """
    1 - enemy
    -1 - teammate
    0 - empty
    """

    def test_should_get_legal_pawn_moves_black(self):
        b = Board()
        lgm_getter = LegalMovesGetter(b.board)
        kp = [(7, 4), (0, 4)]
        checking_pieces = {'black': [], 'white': []}

        lgm = lgm_getter.get_pawn_legal_moves(b.board[6][0], kp, checking_pieces)
        self.assertEqual({(5, 0), (4, 0)}, set(lgm))

        b.board[5][1] = Pawn("white")
        b.board[5][3] = Pawn("white")
        lgm = lgm_getter.get_pawn_legal_moves(b.board[6][2], kp, checking_pieces)
        self.assertEqual({(5, 1), (5, 3), (5, 2), (4, 2)}, set(lgm))

        # Pinned pawn
        b.board[4][1] = Bishop("white")
        lgm = lgm_getter.get_pawn_legal_moves(b.board[6][3], kp, checking_pieces)
        self.assertEqual([], lgm)

        # blocked pawn
        lgm = lgm_getter.get_pawn_legal_moves(b.board[6][1], kp, checking_pieces)
        self.assertEqual([], lgm)

    def test_should_get_legal_pawn_moves_white(self):
        b = Board()
        lgm_getter = LegalMovesGetter(b.board)
        kp = [(7, 4), (0, 4)]
        checking_pieces = {'black': [], 'white': []}

        lgm = lgm_getter.get_pawn_legal_moves(b.board[1][3], kp, checking_pieces)
        self.assertEqual({(2, 3), (3, 3)}, set(lgm))

        b.board[2][3] = Pawn("white")
        b.board[2][3].rank, b.board[2][3].file = 2, 3
        lgm = lgm_getter.get_pawn_legal_moves(b.board[2][3], kp, checking_pieces)
        self.assertEqual({(3, 3)}, set(lgm))

        b.board[2][6] = Pawn("black")
        lgm = lgm_getter.get_pawn_legal_moves(b.board[1][7], kp, checking_pieces)
        self.assertEqual({(2, 6), (2, 7), (3, 7)}, set(lgm))

        b.board[2][1] = Pawn("black")
        b.board[2][2] = Pawn("black")
        lgm = lgm_getter.get_pawn_legal_moves(b.board[1][1], kp, checking_pieces)
        self.assertEqual({(2, 2)}, set(lgm))

        b.board[2][5] = Rook("black")
        lgm = lgm_getter.get_pawn_legal_moves(b.board[1][4], kp, checking_pieces)
        self.assertEqual({(2, 5), (2, 4), (3, 4)}, set(lgm))

        b.board[2][4] = Pawn("black")
        lgm = lgm_getter.get_pawn_legal_moves(b.board[1][4], kp, checking_pieces)
        self.assertEqual({(2, 5)}, set(lgm))

        # Pinned pawn
        b.board[2][4] = Queen("black")
        lgm = lgm_getter.get_pawn_legal_moves(b.board[1][4], kp, checking_pieces)
        self.assertEqual([], lgm)

    def test_should_get_legal_rook_moves(self):
        b = Board()
        lgm_getter = LegalMovesGetter(b.board)
        kp = [(7, 4), (0, 4)]
        checking_pieces = {'black': [], 'white': []}

        lgm = lgm_getter.get_rook_legal_moves(b.board[0][0], kp, checking_pieces)
        self.assertEqual([], lgm)

        b.board[4][3] = Rook("white")
        b.board[4][3].rank, b.board[4][3].file = 4, 3
        lgm = lgm_getter.get_rook_legal_moves(b.board[4][3], kp, checking_pieces)
        true_moves = {(5, 3), (6, 3), (3, 3), (2, 3), (4, 4), (4, 5), (4, 6), (4, 7), (4, 2), (4, 1), (4, 0)}
        self.assertEqual(true_moves, set(lgm))

    def test_should_get_legal_bishop_moves(self):
        b = Board()
        lgm_getter = LegalMovesGetter(b.board)
        kp = [(7, 4), (0, 4)]
        checking_pieces = {'black': [], 'white': []}

        b.board[4][3] = Bishop("white")
        b.board[4][3].rank, b.board[4][3].file = 4, 3
        lgm = lgm_getter.get_bishop_legal_moves(b.board[4][3], kp, checking_pieces)
        true_moves = {(5, 4), (6, 5), (5, 2), (6, 1), (3, 2), (2, 1), (3, 4), (2, 5)}
        self.assertEqual(true_moves, set(lgm))

    def test_should_get_legal_queen_moves(self):
        b = Board()
        lgm_getter = LegalMovesGetter(b.board)
        kp = [(7, 4), (0, 4)]
        checking_pieces = {'black': [], 'white': []}

        b.board[4][3] = Queen("white")
        b.board[4][3].rank, b.board[4][3].file = 4, 3
        lgm = lgm_getter.get_queen_legal_moves(b.board[4][3], kp, checking_pieces)
        true_moves = {(5, 4), (6, 5), (5, 2), (6, 1), (3, 2), (2, 1), (3, 4), (2, 5), \
                    (5, 3), (6, 3), (3, 3), (2, 3), (4, 4), (4, 5), (4, 6), (4, 7), (4, 2), (4, 1), (4, 0)}
        self.assertEqual(true_moves, set(lgm))

    def test_should_get_legal_knight_moves(self):
        b = Board()
        lgm_getter = LegalMovesGetter(b.board)
        kp = [(7, 4), (0, 4)]
        checking_pieces = {'black': [], 'white': []}

        lgm = lgm_getter.get_knight_legal_moves(b.board[0][1], kp, checking_pieces)
        self.assertEqual({(2, 0), (2, 2)}, set(lgm))

        lgm = lgm_getter.get_knight_legal_moves(b.board[7][6], kp, checking_pieces)
        self.assertEqual({(5, 7), (5, 5)}, set(lgm))

        b.board[4][5] = Knight("black")
        b.board[4][5].rank, b.board[4][5].file = 4, 5
        lgm = lgm_getter.get_knight_legal_moves(b.board[4][5], kp, checking_pieces)
        true_moves = {(5, 7), (3, 7), (2, 6), (2, 4), (3, 3), (5, 3)}
        self.assertEqual(true_moves, set(lgm))

        # Pinned knight
        b.board[7][7] = Rook("white")
        b.board[7][5] = 0
        lgm = lgm_getter.get_knight_legal_moves(b.board[7][6], kp, checking_pieces)
        self.assertEqual([], lgm)

    def test_should_get_legal_king_moves(self):
        b = Board()
        lgm_getter = LegalMovesGetter(b.board)
        kp = [(7, 4), (0, 4)]
        kuc = [False, False]
        checking_pieces = {'black': [], 'white': []}

        lgm = lgm_getter.get_king_legal_moves(b.board[0][4], kp, checking_pieces, kuc)
        self.assertEqual([], lgm)

        lgm = lgm_getter.get_king_legal_moves(b.board[7][4], kp, checking_pieces, kuc)
        self.assertEqual([], lgm)

        # Castling black king
        b.board[7][6] = b.board[7][5] = 0
        lgm = lgm_getter.get_king_legal_moves(b.board[7][4], kp, checking_pieces, kuc)
        self.assertEqual({(7, 5), (7, 6)}, set(lgm))

        # Castling white king - kingside
        b.board[0][6] = b.board[0][5] = 0
        lgm = lgm_getter.get_king_legal_moves(b.board[0][4], kp, checking_pieces, kuc)
        self.assertEqual({(0, 5), (0, 6)}, set(lgm))

        # Castling white king - kingside or queenside
        b.board[0][1] = b.board[0][2] = b.board[0][3] = 0
        lgm = lgm_getter.get_king_legal_moves(b.board[0][4], kp, checking_pieces, kuc)
        self.assertEqual({(0, 5), (0, 6), (0, 3), (0, 2)}, set(lgm))

        b.board[3][2] = King("white")
        kp[1] = (3, 2)
        b.board[3][2].rank, b.board[3][2].file = 3, 2
        lgm = lgm_getter.get_king_legal_moves(b.board[3][2], kp, checking_pieces, kuc)
        true_moves = {(4, 2), (4, 3), (3, 3), (2, 3), (2, 2), (2, 1), (3, 1), (4, 1)}
        self.assertEqual(true_moves, set(lgm))

        b.board[5][2] = King("black")
        kp[0] = (5, 2)
        b.board[5][2].rank, b.board[5][2].file = 5, 2
        lgm = lgm_getter.get_king_legal_moves(b.board[5][2], kp, checking_pieces, kuc)
        true_moves = {(5, 1), (5, 3)}
        self.assertEqual(true_moves, set(lgm))

        b.board[4][7] = King("white")
        b.board[4][7].rank, b.board[4][7].file = 4, 7
        # Open up the black queen to take away some squares from this king
        b.board[6][4] = 0
        lgm = lgm_getter.get_king_legal_moves(b.board[4][7], kp, checking_pieces, kuc)
        # There are black pawns on g7 and h7, leaving only one square for the king
        self.assertEqual([(3, 6)], lgm)

        # Open up the light bishop to take away the last available square from this king
        b.board[6][3] = 0
        lgm = lgm_getter.get_king_legal_moves(b.board[4][7], kp, checking_pieces, kuc)
        self.assertEqual([], lgm)
