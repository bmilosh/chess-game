from itertools import zip_longest
from model.square_validator import SquareValidator


def convert_to_int(square: str):
    return ord(square[0]) - 97, int(square[1]) - 1


class UncheckKing:
    """
    Tries to uncheck the king.
    """

    def _uncheck_bishop(self, stf_int, str_int, king_rank, king_file, piece_pos):
        return abs(king_rank - str_int) - abs(king_file - stf_int) == 0 and \
            abs(piece_pos[0] - str_int) - abs(piece_pos[1] - stf_int) == 0

    def _uncheck_rook(self, stf_int, str_int, king_rank, king_file, piece_pos):
        # return abs(king_file - piece_pos[1]) == abs(king_file - stf_int) + abs(stf_int - piece_pos[1]) or \
        #         abs(king_rank - piece_pos[0]) == abs(king_rank - str_int) + abs(str_int - piece_pos[0])
        same_file = (king_file == piece_pos[1] == stf_int) and (abs(
            king_rank - piece_pos[0]) == abs(king_rank - str_int) + abs(str_int - piece_pos[0]))
        same_rank = (king_rank == piece_pos[0] == str_int) and (abs(
            king_file - piece_pos[1]) == abs(king_file - stf_int) + abs(stf_int - piece_pos[1]))
        # return abs(king_file - piece_pos[1]) == abs(king_file - stf_int) + abs(stf_int - piece_pos[1]) or \
        #         abs(king_rank - piece_pos[0]) == abs(king_rank - str_int) + abs(str_int - piece_pos[0])
        print(f"{same_file=}, {same_rank=}")
        return same_file or same_rank

    def uncheck(self, stf_int, str_int, king_pos, checking_piece):
        print(f"{stf_int=}, {str_int=}, {checking_piece=}")
        king_rank, king_file = king_pos
        if checking_piece:
            piece_name, piece_pos = checking_piece[0]
            print(f"{stf_int=}, {str_int=}, {piece_name=}, {piece_pos=}")
            if str_int != piece_pos[0] or stf_int != piece_pos[1]:
                print("we're not capturing the checking piece")
                if piece_name[2:] in ['kn', 'pa']:
                    # Can only uncheck from knight or pawn using another piece if we're capturing the knight
                    return False
                elif piece_name[2:] == 'bi':
                    # Confirm that we're blocking the checking diagonal
                    return self._uncheck_bishop(stf_int, str_int, king_rank, king_file, piece_pos)
                elif piece_name[2:] == 'ro':
                    print("we're here blocking the checking rank/file")
                    # Confirm that we're blocking the checking rank/file
                    return self._uncheck_rook(stf_int, str_int, king_rank, king_file, piece_pos)
                elif piece_name[2:] == 'qu':
                    # Confirm that we're blocking the checking rank/file or diagonal
                    print(
                        "we're here blocking the checking rank/file or diagonal (queen checking)")
                    return self._uncheck_rook(stf_int, str_int, king_rank, king_file, piece_pos) or \
                        self._uncheck_bishop(
                            stf_int, str_int, king_rank, king_file, piece_pos)
                else:
                    print("we seem to be checking with an unknown piece")
            else:
                print("did we capture the checking piece?")
        return True


class DiscoveredChecks:
    """
    Evaluates move to see if it leads to a discovered check on a king.
    """

    def __init__(self) -> None:
        self.unchecker = UncheckKing()

    def verify_own_king(self, king_pos, king_index, king_under_check, opp_col,
                        sff_int, sfr_int, stf_int, str_int, board, checking_pieces):
        temp = board[sfr_int][sff_int]
        board[sfr_int][sff_int] = 0
        col = 'b' if opp_col == 'w' else 'w'
        unchk = self.unchecker.uncheck(
            stf_int, str_int, king_pos, checking_pieces[col])
        dc_b = self.discovered_check_bishop(king_pos, king_index, king_under_check,
                                            opp_col, sff_int, sfr_int, stf_int, str_int, board, checking_pieces)
        dc_r = self.discovered_check_rook(king_pos, king_index, king_under_check,
                                          opp_col, sff_int, sfr_int, stf_int, str_int, board, checking_pieces)
        board[sfr_int][sff_int] = temp
        print(f"{dc_b=}, {dc_r=}, {unchk=}")
        return (dc_b or dc_r) or not unchk

    def verify_opposing_king(self, king_pos, king_index, king_under_check, col,
                             sff_int, sfr_int, stf_int, str_int, board, checking_pieces):
        temp = board[sfr_int][sff_int]
        board[sfr_int][sff_int] = 0
        dc_b = self.discovered_check_bishop(king_pos, king_index, king_under_check,
                                            col, sff_int, sfr_int, stf_int, str_int, board, checking_pieces)
        dc_r = self.discovered_check_rook(king_pos, king_index, king_under_check,
                                          col, sff_int, sfr_int, stf_int, str_int, board, checking_pieces)
        board[sfr_int][sff_int] = temp  # set back to original state
        return dc_b, dc_r

    def discovered_check_bishop(self, king_pos, king_index, king_under_check, col,
                                sff_int, sfr_int, stf_int, str_int, board, checking_pieces):
        """
        Note that when verifying your own king, you must
        pass in your opponent's colour as col. Otherwise,
        pass your own colour"""
        king_rank, king_file = king_pos
        print()
        print(f"{king_pos=}, {king_index=} (sff,sfr)= {sff_int, sfr_int}, (stf,str)= {stf_int,str_int},opp_col={col}")
        print(f"{abs(str_int - king_rank)=}, {abs(stf_int - king_file)=}, {abs(sfr_int - king_rank)=}, {abs(sff_int - king_file)=}")
        # abs(str_int - king_rank) != abs(stf_int - king_file) and
        if abs(sfr_int - king_rank) == abs(sff_int - king_file):
            print("condition above holds true (from dcb)")
            # not sure why i used stf_int initially
            f_dir, end_file = (1, 8) if sff_int > king_file else (-1, -1)
            # not sure why i used str_int initially
            r_dir, end_rank = (1, 8) if sfr_int > king_rank else (-1, -1)
            for r, f in zip(range(king_rank+r_dir, end_rank, r_dir), range(king_file+f_dir, end_file, f_dir)):
                if 0 <= r <= 7 and 0 <= f <= 7:
                    piece = board[r][f]
                    if piece != 0:
                        if piece[0] == col and piece[2:] in ['bi', 'qu']:
                            print("leaving leads to discovered check")
                            return (board[r][f], (r, f))
                        print(f"There's a safe piece there {piece=}")
                        return False
                else:
                    print("out of range")
                    return False
        print("condition above does not hold")
        return False

    def discovered_check_rook(self, king_pos, king_index, king_under_check, col,
                              sff_int, sfr_int, stf_int, str_int, board, checking_pieces):
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

            # print(
            #     f"{file_diff=}, {rank_diff=}, {f_dir=},{r_dir=},{end_file=},{end_rank=},{col=}")
            for r, f in zip_longest(range(king_rank+r_dir, end_rank, r_dir), range(king_file+f_dir, end_file, f_dir), fillvalue=fill_value):
                if 0 <= r <= 7 and 0 <= f <= 7:
                    piece = board[r][f]
                    if piece != 0:
                        if piece[0] == col and piece[2:] in ['ro', 'qu']:
                            return board[r][f], (r, f)
                        return False
                else:
                    return False
            return False


class Pawn:
    """
    Moves 1 pace forward. On its first move, can take 2 paces.
    Captures 1 square in either left or right forward diagonals."""

    def __init__(self) -> None:
        self.dc = DiscoveredChecks()

    def _check(self, file_diff: int, rank_diff: int, square_to_occupant: int,
               square_from: str, square_to: str, col: str, board) -> bool:
        if file_diff == 1:
            # Should make a diagonal movement
            if rank_diff != 1 or square_to_occupant == -1:  # check this later!!!
                return False
            return True
        # Remaining on the same file
        elif file_diff == 0:
            if (rank_diff not in [1, 2] or square_to_occupant != 0 or
                    (rank_diff == 2 and
                     (int(square_from[1]) not in [2, 7] or
                      (board[int(square_to[1])-2][ord(square_to[0])-97] != 0 and col == 'w') or
                      (board[int(square_to[1])][ord(square_to[0])-97] != 0 and col == 'b')))):
                return False
            return True
        return False

    def _check_opposing_king(self, kings_positions: list[tuple], king_under_check: list[bool], sff, sfr, stf, str_int, board):
        col = board[sfr][sff][0]
        king = 0 if col == 'w' else 1
        king_rank, king_file = kings_positions[king]
        # White pawn
        if ((not king and (king_rank-str_int, king_file-stf) in [(1, -1), (1, 1)]) or
                (king and (king_rank-str_int, stf-king_file) in [(-1, -1), (-1, 1)])):
            king_under_check[king] = True

    def move(self, square_from: str, square_to: str, kings_positions: list[tuple],
             king_under_check: list[bool], board: list[list], sqv: SquareValidator, flipped: bool = False, checking_pieces=None):
        square_from, square_to = square_from.strip(), square_to.strip()
        file_diff, rank_diff, square_to_occupant = sqv.check_squares(
            square_from, square_to, board)
        sff_int, sfr_int = convert_to_int(square_from)
        stf_int, str_int = convert_to_int(square_to)

        king = board[sfr_int][sff_int][0]
        king_idx = 0 if king == 'b' else 1
        if king_under_check[king_idx] and checking_pieces is not None and len(checking_pieces[king]) > 1:
            print(f"can't move piece. king under check. {checking_pieces=}")
            return False

        col = king  # board[int(square_from[1])-1][ord(square_from[0])-97][0]
        if (col == 'w' and not flipped) or (col == 'b' and flipped):
            move_valid = self._check(
                file_diff, rank_diff, square_to_occupant, square_from, square_to, 'w', board)
        elif (col == 'b' and not flipped) or (col == 'w' and flipped):
            move_valid = self._check(
                file_diff, -rank_diff, square_to_occupant, square_from, square_to, 'b', board)
        if move_valid:
            opp_col = 'b' if col == 'w' else 'w'
            if self.dc.verify_own_king(kings_positions[king_idx], king_idx, king_under_check,
                                       opp_col, sff_int, sfr_int, stf_int, str_int, board, checking_pieces):
                print("we could not verify our king")
                return False

            # We've unchecked our king by the previous check.
            # Update the king_under_check status as well as
            # checking_piece
            print("we could somehow verify our king")
            print(f"{checking_pieces=} before unchecking using unchecker********")
            king_under_check[king_idx] = False
            checking_pieces[col].clear()
            print(f"{checking_pieces=} after unchecking using unchecker********")

            # Try if this is a checking move on opponent's king
            self._check_opposing_king(
                kings_positions, king_under_check, sff_int, sfr_int, stf_int, str_int, board)

            # Try if a discovered check is possible on opponent's king
            other_dcb, other_dcr = self.dc.verify_opposing_king(kings_positions[king_idx ^ 1], king_idx ^ 1, king_under_check,
                                                                col, sff_int, sfr_int, stf_int, str_int, board, checking_pieces)
            if other_dcb:
                king_under_check[king_idx ^ 1] = True
                print(f"{checking_pieces=} before********")
                # checking_pieces[board[other_dcb[0]][other_dcb[1]][0]].append(other_dcb[2])
                checking_pieces[opp_col].append(other_dcb)
                print(f"{checking_pieces=} after********")
            elif other_dcr:
                king_under_check[king_idx ^ 1] = True
                print(f"{checking_pieces=} before********")
                print(f"{other_dcr=}")
                # checking_pieces[board[other_dcr[0]][other_dcr[1]][0]].append(other_dcr[2])
                checking_pieces[opp_col].append(other_dcr)
                print(f"{checking_pieces=} after********")
        return move_valid


class Rook:
    """
    Moves horizontally and vertically. Not limited to any number of squares but
    can't jump over obstacles in its path.
    Captures as it moves.
    """

    def __init__(self) -> None:
        self.dc = DiscoveredChecks()

    def _check_move(self, low_rank: int, high_rank: int, low_file: int, high_file: int, board) -> bool:
        no_obstacles = True
        for rank in range(low_rank, high_rank):
            for file in range(low_file, high_file):
                if board[rank][file] != 0:
                    no_obstacles = False
        return no_obstacles

    def _check_opposing_king(self, kings_positions: list[tuple], king_under_check: list[bool], sff, sfr, stf, str_int, board, checking_pieces):
        col = board[sfr][sff][0]
        opp_col = 'b' if col == 'w' else 'w'
        king = 0 if col == 'w' else 1
        king_rank, king_file = kings_positions[king]
        not_zero = 0
        if str_int == king_rank:
            f_dir = 1 if king_file > stf else -1
            for f in range(stf+f_dir, king_file+f_dir, f_dir):
                if board[king_rank][f] != 0:
                    not_zero += 1
        elif stf == king_file:
            r_dir = 1 if king_rank > str_int else -1
            for r in range(str_int+r_dir, king_rank+r_dir, r_dir):
                if board[r][king_file] != 0:
                    not_zero += 1
        if not_zero == 1:
            king_under_check[king] = True
            checking_pieces[opp_col].append((board[sfr][sff], (str_int, stf)))

    def move(self, square_from: str, square_to: str, kings_positions: list[tuple],
             king_under_check: list[bool],  board: list[list], sqv: SquareValidator, queen_move=False, checking_pieces=None):
        square_from, square_to = square_from.strip(), square_to.strip()
        file_diff, rank_diff, square_to_occupant = sqv.check_squares(
            square_from, square_to, board)
        sff_int, sfr_int = convert_to_int(square_from)
        stf_int, str_int = convert_to_int(square_to)
        low_rank = min(sfr_int, str_int)
        high_rank = max(sfr_int, str_int)
        low_file = min(stf_int, sff_int)
        high_file = max(stf_int, sff_int)
        # col = board[int(square_from[1])-1][ord(square_from[0])-97][0]

        king = board[sfr_int][sff_int][0]
        col = king
        king_idx = 0 if king == 'b' else 1
        print(
            f"{sff_int=},{sfr_int},{board[sfr_int][sff_int]=},{king=},{col=},{king_idx=}")
        if king_under_check[king_idx] and checking_pieces is not None and len(checking_pieces[king]) > 1:
            print(f"can't move piece. king under check. {checking_pieces=}")
            return False

        # Rook's not moving
        if file_diff == 0 and rank_diff == 0:
            move_valid = False
        # Rook's moving along the same file
        elif file_diff == 0:
            move_valid = (self._check_move(low_rank+1, high_rank, low_file, high_file+1, board)
                          and square_to_occupant != -1)
        # Rook's moving along the same rank
        elif rank_diff == 0:
            move_valid = (self._check_move(low_rank, high_rank+1, low_file+1, high_file, board)
                          and square_to_occupant != -1)
        # Invalid rook movement
        else:
            move_valid = False
        if move_valid:
            opp_col = 'b' if col == 'w' else 'w'
            if self.dc.verify_own_king(kings_positions[king_idx], king_idx, king_under_check,
                                       opp_col, sff_int, sfr_int, stf_int, str_int, board, checking_pieces):
                print("we could not verify our king")
                return False

            # We've unchecked our king by the previous check.
            # Update the king_under_check status as well as
            # checking_piece
            print("we could somehow verify our king")
            print(f"{checking_pieces=} before unchecking using unchecker********")
            king_under_check[king_idx] = False
            checking_pieces[col].clear()
            print(f"{checking_pieces=} after unchecking using unchecker********")

            # Try if this is a checking move on opponent's king
            self._check_opposing_king(
                kings_positions, king_under_check, sff_int, sfr_int, stf_int, str_int, board, checking_pieces)

            # Queen might be checking from the same diagonal as the king
            if queen_move == True:
                Bishop()._check_opposing_king(kings_positions, king_under_check,
                                              sff_int, sfr_int, stf_int, str_int, board, checking_pieces)

            # Try if a discovered check is possible on opponent's king
            other_dcb, other_dcr = self.dc.verify_opposing_king(kings_positions[king_idx ^ 1], king_idx ^ 1, king_under_check,
                                                                col, sff_int, sfr_int, stf_int, str_int, board, checking_pieces)
            if other_dcb:
                king_under_check[king_idx ^ 1] = True
                print(f"{checking_pieces=} before********")
                # checking_pieces[board[other_dcb[0]][other_dcb[1]][0]].append(other_dcb[2])
                checking_pieces[opp_col].append(other_dcb)
                print(f"{checking_pieces=} after********")
            elif other_dcr:
                king_under_check[king_idx ^ 1] = True
                print(f"{checking_pieces=} before********")
                print(f"{other_dcr=}")
                # checking_pieces[board[other_dcr[0]][other_dcr[1]][0]].append(other_dcr[2])
                checking_pieces[opp_col].append(other_dcr)
                print(f"{checking_pieces=} after********")

        return move_valid


class Knight:
    """
    L-shaped movement; only 3 squares at a time but can jump over obstacles.
    Captures as it moves.
    """

    def __init__(self) -> None:
        self.dc = DiscoveredChecks()

    def _check_opposing_king(self, kings_positions: list[tuple], king_under_check: list[bool], sff, sfr, stf, str_int, board, checking_pieces):
        col = board[sfr][sff][0]
        opp_col = 'b' if col == 'w' else 'w'
        king = 0 if col == 'w' else 1
        king_rank, king_file = kings_positions[king]
        f_diff = abs(stf - king_file)
        r_diff = abs(str_int - king_rank)
        if f_diff + r_diff == 3 and f_diff in [1, 2] and r_diff in [1, 2]:
            king_under_check[king] = True
            print(f"{checking_pieces=} before checking with knight********")
            checking_pieces[opp_col].append((board[sfr][sff], (str_int, stf)))
            print(f"{checking_pieces=} after checking with knight********")

    def move(self, square_from: str, square_to: str, kings_positions: list[tuple],
             king_under_check: list[bool], board: list[list], sqv: SquareValidator, checking_pieces=None):
        square_from, square_to = square_from.strip(), square_to.strip()
        file_diff, rank_diff, square_to_occupant = sqv.check_squares(
            square_from, square_to, board)
        file_diff, rank_diff = abs(file_diff), abs(rank_diff)
        sff_int, sfr_int = convert_to_int(square_from)
        stf_int, str_int = convert_to_int(square_to)
        col = board[sfr_int][sff_int][0]

        king = board[sfr_int][sff_int][0]
        king_idx = 0 if king == 'b' else 1
        if king_under_check[king_idx] and checking_pieces is not None and len(checking_pieces[king]) > 1:
            print(f"can't move piece. king under check. {checking_pieces=}")
            return False

        if file_diff not in [1, 2] or rank_diff not in [1, 2] or file_diff + rank_diff != 3 or square_to_occupant == -1:
            move_valid = False
        else:
            move_valid = True
        if move_valid:
            opp_col = 'b' if col == 'w' else 'w'
            if self.dc.verify_own_king(kings_positions[king_idx], king_idx, king_under_check,
                                       opp_col, sff_int, sfr_int, stf_int, str_int, board, checking_pieces):
                return False

            # We've unchecked our king by the previous check.
            # Update the king_under_check status as well as
            # checking_piece
            print(f"{checking_pieces=} before unchecking using unchecker********")
            king_under_check[king_idx] = False
            checking_pieces[col].clear()
            print(f"{checking_pieces=} after unchecking using unchecker********")

            # Try if this is a checking move on opponent's king
            self._check_opposing_king(
                kings_positions, king_under_check, sff_int, sfr_int, stf_int, str_int, board, checking_pieces)

            # Try if a discovered check is possible on opponent's king
            other_dcb, other_dcr = self.dc.verify_opposing_king(kings_positions[king_idx ^ 1], king_idx ^ 1, king_under_check,
                                                                col, sff_int, sfr_int, stf_int, str_int, board, checking_pieces)
            if other_dcb:
                king_under_check[king_idx ^ 1] = True
                print(f"{checking_pieces=} before********")
                # checking_pieces[board[other_dcb[0]][other_dcb[1]][0]].append(other_dcb[2])
                checking_pieces[opp_col].append(other_dcb)
                print(f"{checking_pieces=} after********")
            elif other_dcr:
                king_under_check[king_idx ^ 1] = True
                print(f"{checking_pieces=} before********")
                print(f"{other_dcr=}")
                # checking_pieces[board[other_dcr[0]][other_dcr[1]][0]].append(other_dcr[2])
                checking_pieces[opp_col].append(other_dcr)
                print(f"{checking_pieces=} after********")

        return move_valid


class Bishop:
    """
    Moves diagonally. Not limited to any number of squares but
    can't jump over obstacles in its path.
    Captures as it moves.

    square_type indicates if it's a "light-" or "dark-" square bishop.
    """

    def __init__(self) -> None:
        self.dc = DiscoveredChecks()

    def _check_move(self):
        pass

    def _check_opposing_king(self, kings_positions: list[tuple], king_under_check: list[bool], sff, sfr, stf, str_int, board, checking_pieces):
        col = board[sfr][sff][0]
        opp_col = 'b' if col == 'w' else 'w'
        king = 0 if col == 'w' else 1
        king_rank, king_file = kings_positions[king]
        if abs(str_int - king_rank) == abs(stf - king_file):
            f_dir = 1 if king_file > stf else -1
            r_dir = 1 if king_rank > str_int else -1
            not_zero = 0
            for r, f in zip(range(str_int+r_dir, king_rank+r_dir, r_dir), range(stf+f_dir, king_file+f_dir, f_dir)):
                if board[r][f] != 0:
                    not_zero += 1
            if not_zero == 1:
                print("Detected NOTHING between piece and king")
                king_under_check[king] = True
                checking_pieces[opp_col].append(
                    (board[sfr][sff], (str_int, stf)))
        #     else:
        #         print(f"Detected something between piece and king: {not_zero=}")
        # else:
        #     print("detected bishop and king NOT on same diag")

    def move(self, square_from: str, square_to: str, kings_positions: list[tuple],
             king_under_check: list[bool], board: list[list], sqv: SquareValidator, queen_move=False, checking_pieces=None):
        square_from, square_to = square_from.strip(), square_to.strip()
        file_diff, rank_diff, square_to_occupant = sqv.check_squares(
            square_from, square_to, board)
        file_diff, rank_diff = abs(file_diff), abs(rank_diff)

        sff_int, sfr_int = convert_to_int(square_from)
        stf_int, str_int = convert_to_int(square_to)
        f_dir = 1 if stf_int > sff_int else -1
        r_dir = 1 if str_int > sfr_int else -1

        col = board[sfr_int][sff_int][0]
        king_idx = 0 if col == 'b' else 1
        if king_under_check[king_idx] and checking_pieces is not None and len(checking_pieces[col]) > 1:
            print(f"can't move piece. king under check. {checking_pieces=}")
            return False

        if file_diff != rank_diff or rank_diff not in range(1, 8) or square_to_occupant == -1:
            return False
        move_valid = not any(board[r][f] != 0 for r, f in zip(
            range(sfr_int+r_dir, str_int, r_dir), range(sff_int+f_dir, stf_int, f_dir)))
        if move_valid:
            opp_col = 'b' if col == 'w' else 'w'
            if self.dc.verify_own_king(kings_positions[king_idx], king_idx, king_under_check,
                                       opp_col, sff_int, sfr_int, stf_int, str_int, board, checking_pieces):
                print("we could not verify our king")
                return False

            # We've unchecked our king by the previous check.
            # Update the king_under_check status as well as
            # checking_piece
            print("we could somehow verify our king")
            king_under_check[king_idx] = False
            checking_pieces[col].clear()
            print(f"{checking_pieces=} after unchecking using unchecker********")

            # Try if this is a checking move on opponent's king
            self._check_opposing_king(
                kings_positions, king_under_check, sff_int, sfr_int, stf_int, str_int, board, checking_pieces)

            # Try if a discovered check is possible on opponent's king
            other_dcb, other_dcr = self.dc.verify_opposing_king(kings_positions[king_idx ^ 1], king_idx ^ 1, king_under_check,
                                                                col, sff_int, sfr_int, stf_int, str_int, board, checking_pieces)
            if other_dcb:
                king_under_check[king_idx ^ 1] = True
                print(f"{checking_pieces=} before********")
                checking_pieces[opp_col].append(other_dcb)
                print(f"{checking_pieces=} after********")
            elif other_dcr:
                king_under_check[king_idx ^ 1] = True
                print(f"{checking_pieces=} before********")
                print(f"{other_dcr=}")
                checking_pieces[opp_col].append(other_dcr)
                print(f"{checking_pieces=} after********")

            # self._check_opposing_king(
            #     kings_positions, king_under_check, sff_int, sfr_int, stf_int, str_int, board, checking_pieces)

            # Queen might be checking from the same rank/file as the king
            if queen_move == True:
                Rook()._check_opposing_king(kings_positions, king_under_check,
                                            sff_int, sfr_int, stf_int, str_int, board, checking_pieces)
        return move_valid


class Queen:
    """
    Moves like every other piece except the knight.
    Captures as it moves.
    """

    def __init__(self) -> None:
        self.dc = DiscoveredChecks()

    def move(self, square_from: str, square_to: str, kings_positions: list[tuple],
             king_under_check: list[bool], board: list[list], sqv: SquareValidator, checking_pieces=None):
        bishop = Bishop()
        rook = Rook()
        bish_check = bishop.move(square_from, square_to, kings_positions, king_under_check,
                                 board, sqv, queen_move=True, checking_pieces=checking_pieces)
        rook_check = rook.move(square_from, square_to, kings_positions, king_under_check,
                               board, sqv, queen_move=True, checking_pieces=checking_pieces)
        # move_valid = (bishop.move(square_from, square_to, kings_positions, king_under_check, board, sqv, queen_move=True, checking_pieces=checking_pieces) or
        #               rook.move(square_from, square_to, kings_positions, king_under_check, board, sqv, queen_move=True, checking_pieces=checking_pieces))
        return bish_check or rook_check


class King:
    """
    Moves 1 pace anywhere as long as it's safe to do so.
    Captures as it moves.
    """

    def __init__(self) -> None:
        self.dc = DiscoveredChecks()

    def _king_safe_from_pawn(self, stf_int, str_int, king_colour, board, flipped: bool):
        def check_square(r_dir, opp_colour):
            name = opp_colour + '_pa'
            return not ((stf_int > 0 and board[str_int + r_dir][stf_int - 1] == name) or
                        (stf_int < 7 and board[str_int + r_dir][stf_int + 1] == name))

        if king_colour == 'w' and not flipped and str_int <= 5:
            return check_square(1, 'b')
        elif king_colour == 'b' and flipped and 5 >= str_int:
            return check_square(1, 'w')
        elif king_colour == 'b' and not flipped and 2 <= str_int <= 7:
            return check_square(-1, 'w')
        elif king_colour == 'w' and flipped and 2 <= str_int <= 7:
            return check_square(-1, 'b')

        return True

    def _king_safe_from_king(self, stf_int, str_int, kings_positions, king_colour, board):
        opp_king = 0 if king_colour == 'w' else 1
        return (abs(kings_positions[opp_king][0]-str_int) > 1 or
                abs(kings_positions[opp_king][1]-stf_int) > 1)

    def _king_safe_from_knight(self, stf_int, str_int, king_colour, board):
        for pair in [((r1, f1), (f1, r1)) for r1 in [-1, 1] for f1 in [-2, 2]]:
            for r, f in pair:
                r_diff, f_diff = str_int-r, stf_int-f
                if 0 <= r_diff <= 7 and 0 <= f_diff <= 7:
                    if ((king_colour == 'w' and board[r_diff][f_diff] == 'b_kn') or
                            (king_colour == 'b' and board[r_diff][f_diff] == 'w_kn')):
                        return False
        return True

    def _king_safe_from_bishop(self, stf_int, str_int, king_colour, board):
        for i in range(1, 8):
            if 0 <= str_int - i <= 7 and 0 <= stf_int - i <= 7:
                if isinstance(board[str_int - i][stf_int - i], str):
                    if board[str_int - i][stf_int - i][0] != king_colour and board[str_int - i][stf_int - i][2:] in ['bi', 'qu']:
                        return False
                    break

        for i in range(1, 8):
            if 0 <= str_int - i <= 7 and 0 <= stf_int + i <= 7:
                if isinstance(board[str_int - i][stf_int + i], str):
                    if board[str_int - i][stf_int + i][0] != king_colour and board[str_int - i][stf_int + i][2:] in ['bi', 'qu']:
                        return False
                    break

        for i in range(1, 8):
            if 0 <= str_int + i <= 7 and 0 <= stf_int - i <= 7:
                if isinstance(board[str_int + i][stf_int - i], str):
                    if board[str_int + i][stf_int - i][0] != king_colour and board[str_int + i][stf_int - i][2:] in ['bi', 'qu']:
                        return False
                    break

        for i in range(1, 8):
            if 0 <= str_int + i <= 7 and 0 <= stf_int + i <= 7:
                if isinstance(board[str_int + i][stf_int + i], str):
                    if board[str_int + i][stf_int + i][0] != king_colour and board[str_int + i][stf_int + i][2:] in ['bi', 'qu']:
                        return False
                    break
        return True

    def _king_safe_from_rook(self, stf_int, str_int, king_colour, board):
        for i in range(1, 8):
            if 0 <= str_int - i:
                if isinstance(board[str_int - i][stf_int], str):
                    if board[str_int - i][stf_int][0] != king_colour and board[str_int - i][stf_int][2:] in ['ro', 'qu']:
                        return False
                    break

        for i in range(1, 8):
            if str_int + i <= 7:
                if isinstance(board[str_int + i][stf_int], str):
                    if board[str_int + i][stf_int][0] != king_colour and board[str_int + i][stf_int][2:] in ['ro', 'qu']:
                        return False
                    break

        for i in range(1, 8):
            if 0 <= stf_int - i:
                if isinstance(board[str_int][stf_int - i], str):
                    if board[str_int][stf_int - i][0] != king_colour and board[str_int][stf_int - i][2:] in ['ro', 'qu']:
                        return False
                    break

        for i in range(1, 8):
            if stf_int + i <= 7:
                if isinstance(board[str_int][stf_int + i], str):
                    if board[str_int][stf_int + i][0] != king_colour and board[str_int][stf_int + i][2:] in ['ro', 'qu']:
                        return False
                    break
        return True

    def _king_safe_from_queen(self, stf_int, str_int, king_colour, board):
        return (self._king_safe_from_bishop(stf_int, str_int, king_colour, board) and
                self._king_safe_from_rook(stf_int, str_int, king_colour, board))

    def move(self, square_from: str, square_to: str, kings_positions: list[tuple],
             king_under_check: list[bool], board: list[list], sqv: SquareValidator, flipped: bool = False, checking_pieces=None):
        square_from, square_to = square_from.strip(), square_to.strip()
        file_diff, rank_diff, square_to_occupant = sqv.check_squares(
            square_from, square_to, board)
        sff_int, sfr_int = convert_to_int(square_from)
        stf_int, str_int = convert_to_int(square_to)
        king_colour = board[sfr_int][sff_int][0]
        king = 1 if king_colour == 'w' else 0

        if square_to_occupant == -1 or (not file_diff and not rank_diff) or abs(file_diff) > 1 or abs(rank_diff) > 1:
            move_valid = False
            print("Broke here*****")
        else:
            temp = board[sfr_int][sff_int]
            board[sfr_int][sff_int] = 0
            move_valid = (self._king_safe_from_pawn(stf_int, str_int, king_colour, board, flipped) and
                          self._king_safe_from_king(stf_int, str_int, kings_positions, king_colour, board) and
                          self._king_safe_from_knight(stf_int, str_int, king_colour, board) and
                          self._king_safe_from_queen(stf_int, str_int, king_colour, board))
            board[sfr_int][sff_int] = temp
        if move_valid:
            opp_col = 'b' if temp[0] == 'w' else 'w'
            print("Move was valid from the king's perspective")
            print(f"{checking_pieces=} before unchecking")
            if self.uncheck_king(checking_pieces[king_colour], stf_int, str_int, board):
                print(f"{checking_pieces=} after unchecking")
                king_under_check[king] = False
                temp = board[sfr_int][sff_int]
                board[sfr_int][sff_int] = 0
                other_dcb, other_dcr = self.dc.verify_opposing_king(kings_positions[king ^ 1], king ^ 1, king_under_check, temp[0], sff_int,
                                                                    sfr_int, stf_int, str_int, board, checking_pieces)
                board[sfr_int][sff_int] = temp
                if other_dcb:
                    king_under_check[king ^ 1] = True
                    print(f"{checking_pieces=} before********")
                    checking_pieces[opp_col].append(other_dcb)
                    print(f"{checking_pieces=} after********")
                elif other_dcr:
                    king_under_check[king ^ 1] = True
                    print(f"{checking_pieces=} before********")
                    print(f"{other_dcr=}")
                    checking_pieces[opp_col].append(other_dcr)
                    print(f"{checking_pieces=} after********")

            else:
                print("couldn't uncheck king")
                return False
        else:
            print("Broke at the safe distance phase")
        return move_valid

    def _unckeck_from_pawn(self, pos, stf_int, str_int):
        if (abs(str_int-pos[0]), abs(stf_int-pos[1])) != (1, 1):
            return 1
        return 0

    def _unckeck_from_knight(self, pos, stf_int, str_int):
        if (abs(str_int-pos[0]), abs(stf_int-pos[1])) not in [(1, 2), (2, 1)]:
            return 1
        print("failed here: knight")
        return 0

    def _unckeck_from_rook(self, pos, stf_int, str_int):
        if abs(str_int-pos[0]) != 0 and abs(stf_int-pos[1]) != 0:
            return 1
        return 0

    def _unckeck_from_bishop(self, pos, stf_int, str_int):
        if abs(str_int-pos[0]) != abs(stf_int-pos[1]) or pos == (str_int, stf_int):
            return 1
        return 0

    def _unckeck_from_queen(self, pos, stf_int, str_int, board):
        rank_diff = abs(str_int-pos[0])
        file_diff = abs(stf_int-pos[1])
        next_rank = str_int-1 if str_int > pos[0] else str_int+1
        next_file = stf_int-1 if stf_int > pos[1] else stf_int+1
        if ((file_diff == rank_diff and pos != (str_int, stf_int)) or
                (0 == file_diff != rank_diff and ((next_rank, stf_int) == pos or board[next_rank][stf_int] == 0)) or
                (0 == rank_diff != file_diff and ((str_int, next_file) == pos or board[str_int][next_file] == 0))):
            return 0
        return 1

    def uncheck_king(self, chk_piece: list, stf_int, str_int, board):
        c = 0
        print(f"need to uncheck {len(chk_piece)} pieces: {chk_piece=}")
        for piece_name, pos in chk_piece:
            if piece_name[2:] == 'pa':
                c += self._unckeck_from_pawn(pos, stf_int, str_int)
            elif piece_name[2:] == 'kn':
                c += self._unckeck_from_knight(pos, stf_int, str_int)
            elif piece_name[2:] == 'ro':
                c += self._unckeck_from_rook(pos, stf_int, str_int)
            elif piece_name[2:] == 'bi':
                c += self._unckeck_from_bishop(pos, stf_int, str_int)
            elif piece_name[2:] == 'qu':
                c += self._unckeck_from_queen(pos, stf_int, str_int, board)
            else:
                raise ValueError(f"Checking with unknown piece: {piece_name=}")
        if c == len(chk_piece):
            chk_piece.clear()
            return True
        return False
