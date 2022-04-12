from model.discovered_checks import DiscoveredChecks
from model.pieces import *

class LegalMovesGetter:
    """
    Given a piece, it returns a list of all
    its available legal moves."""

    def __init__(self, board: list[list]) -> None:
        self.board = board
        self.dc = DiscoveredChecks()

    def _bishop_and_rook_moves(self, sfr_int, sff_int, king_position, checking_pieces, opp_col, k=1):
        """
        Utility function for the bishop and rook moves.
        k is set to 1 for the bishop. However, in order to be 
        able to check same file and rank for the rook, we pass
        it in as 0.
        """
        safe1 = safe2 = safe3 = safe4 = None
        cap1 = cap2 = cap3 = cap4 = False
        moves = []

        def check(safe, captured, i, j):
            if captured or safe == False or \
                    sfr_int + i not in range(8) or sff_int + j not in range(8):
                return False, captured
            occ = self.get_square_occupant(sfr_int + i, sff_int + j, opp_col)
            if occ == -1:
                return False, captured
            disc_check = self.dc.verify_own_king(king_position, opp_col, sff_int, sfr_int,
                                                 sff_int + j, sfr_int + i, self.board, checking_pieces)
            if disc_check:
                return False, captured
            if occ == 1:
                captured = True
            return True, captured

        for i in range(1, 8):
            safe1, cap1 = check(safe1, cap1, -i, -i*k)
            safe2, cap2 = check(safe2, cap2, -i*k, i)
            safe3, cap3 = check(safe3, cap3, i*k, -i)
            safe4, cap4 = check(safe4, cap4, i, i*k)
            if safe1:
                moves.append((sfr_int - i, sff_int - (i*k)))
            if safe2:
                moves.append((sfr_int - (i*k), sff_int + i))
            if safe3:
                moves.append((sfr_int + (i*k), sff_int - i))
            if safe4:
                moves.append((sfr_int + i, sff_int + (i*k)))
        return moves

    def get_square_occupant(self, str_int, stf_int, opp_col):
        try:
            occ = self.board[str_int][stf_int]
        except IndexError:
            raise
        else:
            if occ:
                return 1 if occ.colour == opp_col else -1
            return 0

    def get_pawn_legal_moves(self, p: Pawn, kings_positions: list[tuple], checking_pieces: dict, flipped=False) -> list:
        def get_occ(r, f):
            # r = r if col == "white" else -r
            if 0 <= p.rank + r <= 7 and 0 <= p.file + f <= 7:
                return self.get_square_occupant(p.rank + r, p.file + f, opp_col)
            return float("inf")
        legal_moves = []
        col = p.colour
        opp_col = "white" if col == "black" else "black"
        king_position = kings_positions[0] if col == "black" else kings_positions[1]

        # forward movement
        for r, f in [(1, 0), (2, 0)]:
            r = r if col == "white" else -r
            if (abs(r) == 2 and p.rank not in [1, 6]) or get_occ(r, f):
                break
            if self.dc.verify_own_king(king_position, opp_col, p.file, p.rank,
                                        p.file+f, p.rank + r, self.board, checking_pieces):
                continue
            else:
                legal_moves.append((p.rank+r, p.file+f))

        # Captures
        for r, f in [(1, -1), (1, 1)]:
            r = r if col == "white" else -r
            if get_occ(r, f) == 1 and not self.dc.verify_own_king(king_position,
                                                                  opp_col, p.file, p.rank, p.file+f, p.rank + r, self.board, checking_pieces):
                legal_moves.append((p.rank+r, p.file+f))

        return legal_moves

    def get_rook_legal_moves(self, r: Rook, kings_positions: list[tuple], checking_pieces: dict) -> list:
        col = r.colour
        opp_col = "white" if col == "black" else "black"
        king_position = kings_positions[0] if col == "black" else kings_positions[1]
        legal_moves = self._bishop_and_rook_moves(
            r.rank, r.file, king_position, checking_pieces, opp_col, k=0)
        return legal_moves

    def get_knight_legal_moves(self, kn: Knight, kings_positions: list[tuple], checking_pieces: dict) -> list:
        legal_moves = []
        col = kn.colour
        opp_col = "white" if col == "black" else "black"
        king_position = kings_positions[0] if col == "black" else kings_positions[1]
        rank, file = kn.rank, kn.file
        for pair in [((r1, f1), (f1, r1)) for r1 in [-1, 1] for f1 in [-2, 2]]:
            for r, f in pair:
                r_diff, f_diff = rank - r, file - f
                if r_diff not in range(8) or f_diff not in range(8):
                    continue
                occ = self.get_square_occupant(r_diff, f_diff, opp_col)
                if occ == -1:
                    continue
                if self.dc.verify_own_king(king_position, opp_col, file, rank,
                                           f_diff, r_diff, self.board, checking_pieces):
                    continue
                legal_moves.append((r_diff, f_diff))
        return legal_moves

    def get_bishop_legal_moves(self, b: Bishop, kings_positions: list[tuple], checking_pieces: dict) -> list:
        col = b.colour
        opp_col = "white" if col == "black" else "black"
        king_position = kings_positions[0] if col == "black" else kings_positions[1]
        legal_moves = self._bishop_and_rook_moves(
            b.rank, b.file, king_position, checking_pieces, opp_col)
        return legal_moves

    def get_queen_legal_moves(self, q: Queen, kings_positions: list[tuple], checking_pieces: dict) -> list:
        return self.get_bishop_legal_moves(q, kings_positions, checking_pieces) + \
            self.get_rook_legal_moves(q, kings_positions, checking_pieces)

    def get_king_legal_moves(self, k: King, kings_positions: list[tuple], checking_pieces: dict,
                             king_under_check, flipped=False) -> list:
        def check(r, f):
            if rank + r not in range(8) or file + f not in range(8):
                return
            occ = self.get_square_occupant(rank + r, file + f, opp_col)
            if occ == -1 or (not r and not f):
                return
            if k._is_safe(file+f, rank+r, col, self.board, kings_positions, flipped):
                if f not in [2, -2] or k.validate_castling(rank, file, file+f, rank+r, king_under_check,
                                                           col, idx, kings_positions, self.board, flipped, checking_pieces):
                    legal_moves.append((rank + r, file + f))
        legal_moves = []
        col = k.colour
        opp_col, idx = ("white", 0) if col == "black" else ("black", 1)
        rank, file = k.rank, k.file
        rng = list(range(-1, 2))
        self.board[rank][file] = 0
        for r, f in [(i, j) for i in rng for j in rng]:
            check(r, f)
        check(0, 2)
        check(0, -2)
        self.board[rank][file] = k
        return legal_moves
