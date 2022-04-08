from itertools import zip_longest

from model.uncheck_king import UncheckKing


class DiscoveredChecks:
    """
    Evaluates move to see if it leads to a discovered check on a king.
    """

    def __init__(self) -> None:
        self.unchecker = UncheckKing()

    def verify_own_king(self, king_pos, opp_col,
                        sff_int, sfr_int, stf_int, str_int, board, checking_pieces):
        
        temp = board[sfr_int][sff_int]
        board[sfr_int][sff_int] = 0
        col = 'black' if opp_col == 'white' else 'white'
        
        unchk = self.unchecker.uncheck(
            stf_int, str_int, king_pos, checking_pieces[col])
        
        dc_b = self.discovered_check_bishop(king_pos,
                                            opp_col, sff_int, sfr_int, stf_int, str_int, board)
        
        dc_r = self.discovered_check_rook(king_pos,
                                          opp_col, sff_int, sfr_int, stf_int, str_int, board)
        
        board[sfr_int][sff_int] = temp
        return (dc_b or dc_r) or not unchk

    def verify_opposing_king(self, king_pos, col,
                             sff_int, sfr_int, stf_int, str_int, board):
        
        temp = board[sfr_int][sff_int]
        board[sfr_int][sff_int] = 0
        
        dc_b = self.discovered_check_bishop(king_pos, 
                                            col, sff_int, sfr_int, stf_int, str_int, board)
        dc_r = self.discovered_check_rook(king_pos, 
                                          col, sff_int, sfr_int, stf_int, str_int, board)
        
        board[sfr_int][sff_int] = temp  # set back to original state
        return dc_b, dc_r

    def discovered_check_bishop(self, king_pos, col,
                                sff_int, sfr_int, stf_int, str_int, board):
        """
        Note that when verifying your own king, you must
        pass in your opponent's colour as col. Otherwise,
        pass your own colour"""
        king_rank, king_file = king_pos
        if abs(sfr_int - king_rank) == abs(sff_int - king_file):
            # not sure why i used stf_int initially
            f_dir, end_file = (1, 8) if sff_int > king_file else (-1, -1)
            # not sure why i used str_int initially
            r_dir, end_rank = (1, 8) if sfr_int > king_rank else (-1, -1)
            for r, f in zip(range(king_rank+r_dir, end_rank, r_dir), range(king_file+f_dir, end_file, f_dir)):
                if 0 <= r <= 7 and 0 <= f <= 7:
                    if (r, f) == (str_int, stf_int):
                        return False
                    piece = board[r][f]
                    if piece != 0:
                        if piece in (col + '_bi', col + '_qu'):
                            return piece, (r, f)
                        return False
                else:
                    return False
        return False

    def discovered_check_rook(self, king_pos, col,
                              sff_int, sfr_int, stf_int, str_int, board):
        king_rank, king_file = king_pos
        rank_diff = king_rank - sfr_int
        file_diff = king_file - sff_int
        if file_diff != 0 and rank_diff != 0:
            return False

        else:
            if rank_diff == 0:
                f_dir, end_file = (1, 8) if sff_int > king_file else (-1, -1)
                r_dir, end_rank, king_rank = 1, king_rank+1, king_rank-1
                fill_value = king_rank+1
            else:
                r_dir, end_rank = (1, 8) if sfr_int > king_rank else (-1, -1)
                f_dir, end_file, king_file = 1, king_file+1, king_file-1
                fill_value = king_file+1

            for r, f in zip_longest(range(king_rank+r_dir, end_rank, r_dir), \
                    range(king_file+f_dir, end_file, f_dir), fillvalue=fill_value):
                if 0 <= r <= 7 and 0 <= f <= 7:
                    if (r, f) == (str_int, stf_int):
                        return False
                    piece = board[r][f]
                    if piece != 0:
                        if piece in (col + '_ro', col + '_qu'):
                            return piece, (r, f)
                        return False
                else:
                    return False
            return False
