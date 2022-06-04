import unittest

from model.board_for_testing import Board
from model.checkmate_checker import CheckmateChecker
from model.legal_moves_getter import LegalMovesGetter
from model.pieces.bishop import Bishop
from model.pieces.king import King
from model.pieces.knight import Knight
from model.pieces.pawn import Pawn
from model.pieces.queen import Queen
from model.pieces.rook import Rook


class TestCheckmateChecker(unittest.TestCase):
    """
    1 - enemy
    -1 - teammate
    0 - empty
    """

    def test_should_verify_checkmate(self):
        b = Board()
        kp = [(7, 4), (0, 4)]
        kuc = [False, False]
        checking_pieces = {"black": [], "white": []}
        lmg = LegalMovesGetter(b.board)

        b.board[4][2] = Bishop("black")
        b.board[4][2].rank, b.board[4][2].file = 4, 2
        b.board[1][5] = Queen("black")
        b.board[1][5].rank, b.board[1][5].file = 1, 5
        b.black_active_pieces.extend([b.board[4][2], b.board[1][5]])
        checking_pieces["white"].append((b.board[1][5], (1, 5)))
        kuc[1] = True
        king = b.board[0][4]
        # print(*b.board, sep='\n')

        cmate_getter = CheckmateChecker()
        is_chkmate = cmate_getter.is_checkmate(
            king,
            checking_pieces,
            b.white_active_pieces,
            kp,
            kuc,
            "white",
            b.board,
            b.black_active_pieces,
        )
        self.assertEqual(True, is_chkmate)

        # Not a checkmate on black
        b.board[6][5] = 0
        b.board[4][7] = Queen("white")
        b.board[4][7].rank, b.board[4][7].file = 4, 7
        checking_pieces["black"].append((b.board[4][7], (4, 7)))
        checking_pieces["white"].clear()
        kuc = [True, False]
        king = b.board[7][4]
        is_chkmate = cmate_getter.is_checkmate(
            king,
            checking_pieces,
            b.black_active_pieces,
            kp,
            kuc,
            "black",
            b.board,
            b.white_active_pieces,
        )
        self.assertEqual(False, is_chkmate)

        # Check on black by two pieces. Not a checkmate
        b.board[6][4] = 0
        b.board[5][3] = Knight("white")
        b.board[5][3].rank, b.board[5][3].file = 5, 3
        checking_pieces["black"].append((b.board[5][3], (5, 3)))
        is_chkmate = cmate_getter.is_checkmate(
            king,
            checking_pieces,
            b.white_active_pieces,
            kp,
            kuc,
            "black",
            b.board,
            b.white_active_pieces,
        )
        self.assertEqual(False, is_chkmate)
