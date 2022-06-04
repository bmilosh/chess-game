class UncheckKing:
    """
    Removes the king from check when possible.
    """

    def _uncheck_from_bishop(self, stf_int, str_int, king_rank, king_file, piece_pos):
        return (
            abs(king_rank - str_int) - abs(king_file - stf_int) == 0
            and abs(piece_pos[0] - str_int) - abs(piece_pos[1] - stf_int) == 0
            and abs(king_rank - piece_pos[0])
            == abs(king_rank - str_int) + abs(str_int - piece_pos[0])
            and abs(king_file - piece_pos[1])
            == abs(king_file - stf_int) + abs(stf_int - piece_pos[1])
        )

    def _uncheck_from_rook(self, stf_int, str_int, king_rank, king_file, piece_pos):
        same_file = (king_file == piece_pos[1] == stf_int) and (
            abs(king_rank - piece_pos[0])
            == abs(king_rank - str_int) + abs(str_int - piece_pos[0])
        )
        same_rank = (king_rank == piece_pos[0] == str_int) and (
            abs(king_file - piece_pos[1])
            == abs(king_file - stf_int) + abs(stf_int - piece_pos[1])
        )
        return same_file or same_rank

    def uncheck(self, stf_int, str_int, king_pos: tuple, checking_piece: tuple) -> bool:
        """
        The main unchecking method.
        king_pos is something like: (7,4)
        checking_piece for example: ('w_qu', (2,3))
        Returns boolean indicating ability to uncheck king.
        """
        king_rank, king_file = king_pos
        if checking_piece:
            piece_, piece_pos = checking_piece[0]
            piece_name = piece_.name
            if str_int != piece_pos[0] or stf_int != piece_pos[1]:
                if piece_name in ["knight", "pawn"]:
                    # Can only uncheck from knight or pawn using another piece if we're capturing the knight
                    return False
                elif piece_name == "bishop":
                    # Confirm that we're blocking the checking diagonal
                    return self._uncheck_from_bishop(
                        stf_int, str_int, king_rank, king_file, piece_pos
                    )
                elif piece_name == "rook":
                    # Confirm that we're blocking the checking rank/file
                    return self._uncheck_from_rook(
                        stf_int, str_int, king_rank, king_file, piece_pos
                    )
                elif piece_name == "queen":
                    # Confirm that we're blocking the checking rank/file or diagonal
                    return self._uncheck_from_rook(
                        stf_int, str_int, king_rank, king_file, piece_pos
                    ) or self._uncheck_from_bishop(
                        stf_int, str_int, king_rank, king_file, piece_pos
                    )
        return True
