class SquareOccupantGetter:
    def get_square_occupant(self, board, str_int, stf_int, opp_col):
        try:
            occ = board[str_int][stf_int]
        except IndexError:
            raise
        else:
            if not isinstance(occ, int):
                return 1 if occ.colour == opp_col else -1
            return occ
