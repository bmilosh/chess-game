from model.pieces.king import King
from model.legal_moves_getter import LegalMovesGetter
from model.pieces.bishop import Bishop
from model.pieces.rook import Rook
from model.pieces.knight import Knight
from model.pieces.queen import Queen
from model.pieces.pawn import Pawn
from model.pieces.piece_interface import Piece

class CheckmateChecker:
    """
    Used to check if a king currently under check can 
    become safe.

    Checkmate means the check can't be evaded."""

    # def __init__(self, lmg: LegalMovesGetter) -> None:
    #     self.lmg = lmg

    def is_checkmate(self, king: King, checking_pieces: dict, active_pieces: list,
                     kings_positions: list[tuple], king_under_check, colour, board, opp_active_pieces, flipped=False) -> bool:
        if len(checking_pieces[colour]) > 1:
            if king.get_legal_moves(kings_positions, checking_pieces, \
                    board, flipped, king_under_check, opp_active_pieces):
                # There are legal ways for the king to get out of this check, hence it's not a checkmate.
                return False
            return True
        elif not checking_pieces[colour]:
            print("not under check**************")
            return False
        return self.get_legal_moves(active_pieces, kings_positions, king_under_check, checking_pieces, board, opp_active_pieces, flipped)

    def get_legal_moves(self, active_pieces: list[Piece], kings_positions, king_under_check, checking_pieces, board, opp_active_pieces, flipped=False) -> list:
        for piece in active_pieces:
            name = piece.name
            if name == 'king':
                legal_moves = piece.get_legal_moves(kings_positions, checking_pieces, \
                    board, flipped, king_under_check, opp_active_pieces)
            else:
                legal_moves = piece.get_legal_moves(kings_positions, checking_pieces, \
                    board, flipped, king_under_check)
            
            if legal_moves:
                return False
        return True
