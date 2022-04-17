from model.discovered_checks import DiscoveredChecks
from model.square_occ_getter import SquareOccupantGetter


class BishopAndRookMovesGetter:
    """
    Used by the bishop and rook pieces to
    get their legal moves.
    """

    def __init__(self) -> None:
        self.sog = SquareOccupantGetter()

    def bishop_and_rook_moves(self, sfr_int, sff_int, king_position, checking_pieces, board, dc, opp_col, k=1):
        """
        Utility function for the bishop and rook moves.
        k is set to 1 for the bishop. However, in order to be 
        able to check same file and rank for the rook, we pass
        it in as 0.
        """
        safe1 = safe2 = safe3 = safe4 = None
        cap1 = cap2 = cap3 = cap4 = False
        disc1 = disc2 = disc3 = disc4 = None
        moves = []

        def check(safe, captured, disc, i, j):
            if captured or safe == False or \
                    sfr_int + i not in range(8) or sff_int + j not in range(8):
                return False, captured, disc
            occ = self.sog.get_square_occupant(
                board, sfr_int + i, sff_int + j, opp_col)
            if occ == -1:
                return False, captured, disc
            disc_check = dc.verify_own_king(king_position, opp_col, sff_int, sfr_int,
                                            sff_int + j, sfr_int + i, board, checking_pieces)
            if disc_check:
                # Leaves the king in check. Invalid move.
                safe = safe if disc is None else False
            elif not disc_check:
                # Valid move. If it's the first good move,
                # update safe and disc.
                safe = True if disc is None else safe
                disc = False if disc is None else disc
            if occ == 1:
                captured = True
            return safe, captured, disc

        for i in range(1, 8):
            safe1, cap1, disc1 = check(safe1, cap1, disc1, -i, -i*k)
            safe2, cap2, disc2 = check(safe2, cap2, disc2, -i*k, i)
            safe3, cap3, disc3 = check(safe3, cap3, disc3, i*k, -i)
            safe4, cap4, disc4 = check(safe4, cap4, disc4, i, i*k)
            if safe1:
                moves.append((sfr_int - i, sff_int - (i*k)))
            if safe2:
                moves.append((sfr_int - (i*k), sff_int + i))
            if safe3:
                moves.append((sfr_int + (i*k), sff_int - i))
            if safe4:
                moves.append((sfr_int + i, sff_int + (i*k)))
        return moves
