from model.pieces import King
from model.legal_moves_getter import LegalMovesGetter


class CheckmateChecker:
    """
    Used to check if a king currently under check can 
    become safe.

    Checkmate means the check can't be evaded."""

    def __init__(self, lmg: LegalMovesGetter) -> None:
        self.lmg = lmg

    def is_checkmate(self, king: King, checking_pieces: dict, active_pieces: list, \
            kings_positions: list[tuple], king_under_check, colour, flipped=False) -> bool:
        if len(checking_pieces[colour]) > 1:
            if self.lmg.get_king_legal_moves(king, kings_positions, checking_pieces, king_under_check, flipped):
                # There are legal ways for the king to get out of this check, hence it's not a checkmate.
                return False
            return True
        elif not checking_pieces[colour]:
            return False
        return self.get_legal_moves(active_pieces, kings_positions, king_under_check, checking_pieces)

    def get_legal_moves(self, active_pieces, kings_positions, king_under_check, checking_pieces, flipped=False) -> list:
        for piece in active_pieces:
            name = piece.name
            if name == 'pawn':
                legal_moves = self.lmg.get_pawn_legal_moves(piece, kings_positions, checking_pieces, flipped)
            elif name == 'rook':
                legal_moves = self.lmg.get_rook_legal_moves(piece, kings_positions, checking_pieces)
            elif name == 'bishop':
                legal_moves = self.lmg.get_bishop_legal_moves(piece, kings_positions, checking_pieces)
            elif name == 'knight':
                legal_moves = self.lmg.get_knight_legal_moves(piece, kings_positions, checking_pieces)
            elif name == 'queen':
                legal_moves = self.lmg.get_queen_legal_moves(piece, kings_positions, checking_pieces)
            else:
                legal_moves = self.lmg.get_king_legal_moves(piece, kings_positions, checking_pieces, king_under_check, flipped)
            if legal_moves:
                return False
        return True

