from model.pieces import *
from model.discovered_checks import DiscoveredChecks


class CheckmateChecker:
    """
    Used to check if a king currently under check can 
    become safe.

    Checkmate means the check can't be evaded."""

    def __init__(self, checking_pieces: list, active_pieces: list, board: list[list]) -> None:
        self.checking_pieces = checking_pieces
        self.active_pieces = active_pieces
        self.lmg = LegalMovesGetter(board)
        self.is_checkmate = self.evaluate_check()

    def evaluate_check(self) -> bool:
        if len(self.checking_pieces) != 1:
            # king has to move, else it's game over.
            pass

    def get_blocking_squares(self) -> list:
        pass


class LegalMovesGetter:
    """
    Given a piece, it returns a list of all
    its available legal moves."""

    def __init__(self, board: list[list]) -> None:
        self.board = board
        self.dc = DiscoveredChecks()

    def get_square_occupant(self, str_int, stf_int, opp_col):
        try:
            occ = self.board[str_int][stf_int]
        except IndexError:
            raise
        else:
            if occ:
                return 1 if occ.colour == opp_col else -1
            return 0

    def get_pawn_legal_moves(self, p: Pawn, king_position: tuple, checking_pieces: dict) -> list:
        def get_occ(r, f):
            # r = r if col == "white" else -r
            if 0 <= p.rank + r <= 7 and 0 <= p.file + f <= 7:
                return self.get_square_occupant(p.rank + r, p.file + f, opp_col)
            return float("inf")
        legal_moves = []
        col = p.colour
        opp_col = "white" if col == "black" else "black"

        # forward movement
        for r, f in [(1, 0), (2, 0)]:
            r = r if col == "white" else -r
            if (abs(r) == 2 and p.rank not in [1, 6]) or get_occ(r, f) or \
                self.dc.verify_own_king(king_position, opp_col, p.file, p.rank,
                                        p.file+f, p.rank + r, self.board, checking_pieces):
                break
            else:
                legal_moves.append((p.rank+r, p.file+f))

        # Captures
        for r, f in [(1, -1), (1, 1)]:
            r = r if col == "white" else -r
            if get_occ(r, f) == 1 and not self.dc.verify_own_king(king_position,
                                                                  opp_col, p.file, p.rank, p.file+f, p.rank + r, self.board, checking_pieces):
                legal_moves.append((p.rank+r, p.file+f))

        return legal_moves

    def get_rook_legal_moves(self, r: Rook, king_position: tuple, checking_pieces: dict) -> list:
        pass

    def get_knight_legal_moves(self, kn: Knight, king_position: tuple, checking_pieces: dict) -> list:
        pass

    def get_bishop_legal_moves(self, b: Bishop, king_position: tuple, checking_pieces: dict) -> list:
        pass

    def get_queen_legal_moves(self, q: Queen, king_position: tuple, checking_pieces: dict) -> list:
        pass

    def get_king_legal_moves(self, k: King, king_position: tuple, checking_pieces: dict) -> list:
        pass
