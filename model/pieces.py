from model.square_validator import SquareValidator


def convert_to_int(square: str):
    return ord(square[0]) - 97, int(square[1]) - 1


class Pawn:
    """
    Moves 1 pace forward. On its first move, can take 2 paces.
    Captures 1 square in either left or right forward diagonals."""

    def __init__(self, colour: str = None) -> None:
        self.name = "pawn"
        self.first_move = True
        self.colour = colour

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
             king_under_check: list[bool], board: list[list], sqv: SquareValidator, flipped: bool=False):
        square_from, square_to = square_from.strip(), square_to.strip()
        file_diff, rank_diff, square_to_occupant = sqv.check_squares(
            square_from, square_to, board)
        sff_int, sfr_int = convert_to_int(square_from)
        stf_int, str_int = convert_to_int(square_to)

        col = board[int(square_from[1])-1][ord(square_from[0])-97][0]
        if (col == 'w' and not flipped) or (col == 'b' and flipped):
            move_valid = self._check(
                file_diff, rank_diff, square_to_occupant, square_from, square_to, 'w', board)
        elif (col == 'b' and not flipped) or (col == 'w' and flipped):
            move_valid = self._check(
                file_diff, -rank_diff, square_to_occupant, square_from, square_to, 'b', board)
        if move_valid:
            self._check_opposing_king(
                kings_positions, king_under_check, sff_int, sfr_int, stf_int, str_int, board)
        return move_valid


class Rook:
    """
    Moves horizontally and vertically. Not limited to any number of squares but
    can't jump over obstacles in its path.
    Captures as it moves.
    """

    def __init__(self, colour: str = None) -> None:
        self.name = "rook"
        self.colour = colour

    def _check_move(self, low_rank: int, high_rank: int, low_file: int, high_file: int, board) -> bool:
        no_obstacles = True
        for rank in range(low_rank, high_rank):
            for file in range(low_file, high_file):
                if board[rank][file] != 0:
                    no_obstacles = False
        return no_obstacles

    def _check_opposing_king(self, kings_positions: list[tuple], king_under_check: list[bool], sff, sfr, stf, str_int, board):
        col = board[sfr][sff][0]
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

    def move(self, square_from: str, square_to: str, kings_positions: list[tuple],
             king_under_check: list[bool],  board: list[list], sqv: SquareValidator, queen_move=False):
        square_from, square_to = square_from.strip(), square_to.strip()
        file_diff, rank_diff, square_to_occupant = sqv.check_squares(
            square_from, square_to, board)
        sff_int, sfr_int = convert_to_int(square_from)
        stf_int, str_int = convert_to_int(square_to)
        low_rank = min(sfr_int, str_int)
        high_rank = max(sfr_int, str_int)
        low_file = min(stf_int, sff_int)
        high_file = max(stf_int, sff_int)

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
            self._check_opposing_king(
                kings_positions, king_under_check, sff_int, sfr_int, stf_int, str_int, board)
            if queen_move:
                Bishop()._check_opposing_king(kings_positions, king_under_check,
                                              sff_int, sfr_int, stf_int, str_int, board)
        return move_valid


class Knight:
    """
    L-shaped movement; only 3 squares at a time but can jump over obstacles.
    Captures as it moves.
    """

    def __init__(self, colour: str = None) -> None:
        self.name = "knight"
        self.colour = colour

    def _check_opposing_king(self, kings_positions: list[tuple], king_under_check: list[bool], sff, sfr, stf, str_int, board):
        col = board[sfr][sff][0]
        king = 0 if col == 'w' else 1
        king_rank, king_file = kings_positions[king]
        f_diff = abs(stf - king_file)
        r_diff = abs(str_int - king_rank)
        if f_diff + r_diff == 3 and f_diff in [1, 2] and r_diff in [1, 2]:
            king_under_check[king] = True

    def move(self, square_from: str, square_to: str, kings_positions: list[tuple],
             king_under_check: list[bool], board: list[list], sqv: SquareValidator):
        square_from, square_to = square_from.strip(), square_to.strip()
        file_diff, rank_diff, square_to_occupant = sqv.check_squares(
            square_from, square_to, board)
        file_diff, rank_diff = abs(file_diff), abs(rank_diff)
        sff_int, sfr_int = convert_to_int(square_from)
        stf_int, str_int = convert_to_int(square_to)

        if file_diff not in [1, 2] or rank_diff not in [1, 2] or file_diff + rank_diff != 3 or square_to_occupant == -1:
            move_valid = False
        else:
            move_valid = True
        if move_valid:
            self._check_opposing_king(
                kings_positions, king_under_check, sff_int, sfr_int, stf_int, str_int, board)
        return move_valid


class Bishop:
    """
    Moves diagonally. Not limited to any number of squares but
    can't jump over obstacles in its path.
    Captures as it moves.

    square_type indicates if it's a "light-" or "dark-" square bishop.
    """

    def __init__(self, colour: str = None, square_type: str = None) -> None:
        self.name = "bishop"
        self.colour = colour
        self.square_type = square_type

    def _check_move(self):
        pass

    def _check_opposing_king(self, kings_positions: list[tuple], king_under_check: list[bool], sff, sfr, stf, str_int, board):
        col = board[sfr][sff][0]
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
                king_under_check[king] = True

    def move(self, square_from: str, square_to: str, kings_positions: list[tuple],
             king_under_check: list[bool], board: list[list], sqv: SquareValidator, queen_move=False):
        square_from, square_to = square_from.strip(), square_to.strip()
        file_diff, rank_diff, square_to_occupant = sqv.check_squares(
            square_from, square_to, board)
        file_diff, rank_diff = abs(file_diff), abs(rank_diff)

        sff_int, sfr_int = convert_to_int(square_from)
        stf_int, str_int = convert_to_int(square_to)
        f_dir = 1 if stf_int > sff_int else -1
        r_dir = 1 if str_int > sfr_int else -1

        if file_diff != rank_diff or rank_diff not in range(1, 8) or square_to_occupant == -1:
            return False
        move_valid = not any(board[r][f] != 0 for r, f in zip(
            range(sfr_int+r_dir, str_int, r_dir), range(sff_int+f_dir, stf_int, f_dir)))
        if move_valid:
            self._check_opposing_king(
                kings_positions, king_under_check, sff_int, sfr_int, stf_int, str_int, board)
            if queen_move:
                Rook()._check_opposing_king(kings_positions, king_under_check,
                                            sff_int, sfr_int, stf_int, str_int, board)
        return move_valid


class Queen:
    """
    Moves like every other piece except the knight.
    Captures as it moves.
    """

    def __init__(self, colour: str = None) -> None:
        self.name = "queen"
        self.colour = colour

    def move(self, square_from: str, square_to: str, kings_positions: list[tuple],
             king_under_check: list[bool], board: list[list], sqv: SquareValidator):
        bishop = Bishop()
        rook = Rook()
        move_valid = (bishop.move(square_from, square_to, kings_positions, king_under_check, board, sqv, True) or
                      rook.move(square_from, square_to, kings_positions, king_under_check, board, sqv, True))
        return move_valid


class King:
    """
    Moves 1 pace anywhere as long as it's safe to do so.
    Captures as it moves.
    """

    def __init__(self, colour: str = None) -> None:
        self.name = "king"
        self.colour = colour

    def _king_safe_from_pawn(self, stf_int, str_int, king_colour, board):
        def check_square(r_dir, opp_colour):
            name = opp_colour + '_pa'
            return not ((stf_int > 0 and board[str_int + r_dir][stf_int - 1] == name) or
                        (stf_int < 7 and board[str_int + r_dir][stf_int + 1] == name))
        if king_colour == 'w' and str_int <= 5:
            return check_square(1, 'b')
        elif king_colour == 'b' and str_int >= 2:
            return check_square(-1, 'w')
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

    def _king_safe_from_bishop(self, square_to: str, board: list[list]):
        pass

    def _king_safe_from_rook(self, square_from: str, square_to: str, board: list[list]):
        pass

    def _king_safe_from_queen(self, square_from: str, square_to: str, board: list[list]):
        return self._king_safe_from_bishop() and self._king_safe_from_rook()

    def _discovered_check_bishop(self, king_pos, king_index, king_under_check, col, sff_int, sfr_int, stf_int, str_int, board):
        king_rank, king_file = king_pos
        if abs(sfr_int - king_rank) == abs(sff_int - king_file):
            f_dir, end_file = (1, 8) if stf_int > king_file else (-1, -1)
            r_dir, end_rank = (1, 8) if str_int > king_rank else (-1, -1)
            # if stf_int > king_file:
            #     f_dir, end_file = 1, 8
            # else:
            #     f_dir, end_file = -1, -1
            # if str_int > king_rank:
            #     r_dir, end_rank = 1, 8
            # else:
            #     r_dir, end_rank = -1, -1
            for r, f in zip(range(king_rank+r_dir, end_rank, r_dir), range(king_file+f_dir, end_file, f_dir)):
                if 0 <= r <= 7 and 0 <= f <= 7:
                    piece = board[r][f]
                    if piece != 0:
                        if piece[0] == col and piece[2:] in ['bi', 'qu']:
                            king_under_check[king_index] = True
                        return
                else:
                    return

    def _check_opposing_king(self, kings_positions: list[tuple], king_under_check: list[bool], sff, sfr, stf, str_int, board):
        col = board[sfr][sff][0]
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
                king_under_check[king] = True

    def move(self, square_from: str, square_to: str, kings_positions: list[tuple],
             king_under_check: list[bool], board: list[list], sqv: SquareValidator, checking_pieces=None):
        square_from, square_to = square_from.strip(), square_to.strip()
        file_diff, rank_diff, square_to_occupant = sqv.check_squares(
            square_from, square_to, board)
        sff_int, sfr_int = convert_to_int(square_from)
        stf_int, str_int = convert_to_int(square_to)
        king_colour = board[sfr_int][sff_int][0]
        king = 1 if king_colour == 'w' else 0

        if square_to_occupant == -1 or (not file_diff and not rank_diff) or abs(file_diff) > 1 or abs(rank_diff) > 1:
            move_valid = False
        else:
            move_valid = (True and
                          self._king_safe_from_pawn(stf_int, str_int, king_colour, board) and
                          self._king_safe_from_king(stf_int, str_int, kings_positions, king_colour, board) and
                          self._king_safe_from_knight(stf_int, str_int, king_colour, board))
        if move_valid:
            king_under_check[king] = False
            temp = board[sfr_int][sff_int]
            board[sfr_int][sff_int] = 0
            self._discovered_check_bishop(kings_positions[king ^ 1], king ^ 1, king_under_check, temp[0], sff_int,
                                          sfr_int, stf_int, str_int, board)
            board[sfr_int][sff_int] = temp
        return move_valid
        # return (self._king_safe_from_bishop() and
        #         self._king_safe_from_knight() and
        #         self._king_safe_from_rook() and
        #         self._king_safe_from_queen())
