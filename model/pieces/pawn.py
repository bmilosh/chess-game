from model.discovered_checks import DiscoveredChecks
from model.pieces.piece_interface import Piece, RookInterface
from model.square_occ_getter import SquareOccupantGetter
from model.square_validator import SquareValidator


def convert_to_int(square: str):
    return ord(square[0]) - 97, int(square[1]) - 1


class Pawn(Piece):
    """
    Moves 1 pace forward. On its first move, can take 2 paces.
    Captures 1 square in either left or right forward diagonals.
    """

    def __init__(self, colour: str = None) -> None:
        self.dc = DiscoveredChecks()
        self.sog = SquareOccupantGetter()
        self.colour = colour
        self.rank = None
        self.file = None
        self.name = 'pawn'
        self.legal_moves = None

    def get_legal_moves(self, kings_positions: list[tuple], checking_pieces: dict, board, flipped=False, king_under_check=None) -> list:
        def get_occ(r, f):
            # r = r if col == "white" else -r
            if 0 <= self.rank + r <= 7 and 0 <= self.file + f <= 7:
                return self.sog.get_square_occupant(board, self.rank + r, self.file + f, opp_col)
            return float("inf")
        self.legal_moves = []
        col = self.colour
        opp_col = "white" if self.colour == "black" else "black"
        king_position = kings_positions[0] if self.colour == "black" else kings_positions[1]

        # forward movement
        for r, f in [(1, 0), (2, 0)]:
            r = r if self.colour == "white" else -r
            if (abs(r) == 2 and self.rank not in [1, 6]) or get_occ(r, f):
                break
            if self.dc.verify_own_king(king_position, opp_col, self.file, self.rank,
                                       self.file+f, self.rank + r, board, checking_pieces):
                continue
            else:
                self.legal_moves.append((self.rank+r, self.file+f))

        # Captures
        for r, f in [(1, -1), (1, 1)]:
            r = r if self.colour == "white" else -r
            if get_occ(r, f) == 1 and \
                    not self.dc.verify_own_king(king_position,
                                                opp_col, self.file, self.rank, self.file+f, self.rank + r, board, checking_pieces):
                self.legal_moves.append((self.rank+r, self.file+f))

        return self.legal_moves

    def _check(self, file_diff: int, rank_diff: int, square_to_occupant: int,
               square_from: str, square_to: str, col: str, board) -> bool:
        if file_diff == 1:
            # Should make a diagonal movement
            if rank_diff != 1 or square_to_occupant != 1:  # check this later!!!
                # print(f"can't make diagonal move: {rank_diff=}, {square_to_occupant=}")
                return False
            # print(f"******CAN make diagonal move: {rank_diff=}, {square_to_occupant=}")
            return True
        # Remaining on the same file
        elif file_diff == 0:
            if (rank_diff not in [1, 2] or square_to_occupant != 0 or
                    (rank_diff == 2 and
                     (int(square_from[1]) not in [2, 7] or
                      (board[int(square_to[1])-2][ord(square_to[0])-97] != 0 and col == 'white') or
                      (board[int(square_to[1])][ord(square_to[0])-97] != 0 and col == 'black')))):
                return False
            return True
        return False

    def _check_opposing_king(self, king_position: tuple, king_under_check: list[bool], king_idx,
                             stf_int, str_int, opp_col, entry, board, checking_pieces):
        king_rank, king_file = king_position
        # entry = board[sfr_int][sff_int]
        temp = board[str_int][stf_int]
        board[str_int][stf_int] = entry
        if ((not king_idx and (king_rank-str_int, king_file-stf_int) in [(1, -1), (1, 1)]) or
                (king_idx and (king_rank-str_int, stf_int-king_file) in [(-1, -1), (-1, 1)])):
            king_under_check[king_idx] = True
            checking_pieces[opp_col].append((entry, (str_int, stf_int)))
        board[str_int][stf_int] = temp

    def move(self, square_from: str, square_to: str, kings_positions: list[tuple],
             king_under_check: list[bool], board: list[Piece], sqv: SquareValidator,
             flipped: bool = False, checking_pieces=None):

        square_from, square_to = square_from.strip(), square_to.strip()
        # file_diff, rank_diff, square_to_occupant = sqv.check_squares(
        #     square_from, square_to, board)
        sff_int, sfr_int = convert_to_int(square_from)
        stf_int, str_int = convert_to_int(square_to)

        king_idx = 0 if self.colour == 'black' else 1
        if king_under_check[king_idx] and checking_pieces is not None and len(checking_pieces[self.colour]) > 1:
            return False

        # if (col == 'white' and not flipped) or (col == 'black' and flipped):
        #     move_valid = self._check(
        #         file_diff, rank_diff, square_to_occupant, square_from, square_to, 'white', board)
        # elif (col == 'black' and not flipped) or (col == 'white' and flipped):
        #     move_valid = self._check(
        #         file_diff, -rank_diff, square_to_occupant, square_from, square_to, 'black', board)

        if self.legal_moves is None or flipped:
            self.get_legal_moves(
                kings_positions, checking_pieces, board, flipped)
        move_valid = (str_int, stf_int) in self.legal_moves
        self.legal_moves = None

        if move_valid:
            opp_col = 'black' if self.colour == 'white' else 'white'
            # if self.dc.verify_own_king(kings_positions[king_idx],
            #                            opp_col, sff_int, sfr_int, stf_int, str_int, board, checking_pieces):
            #     return False

            # We've unchecked our king by the previous check.
            # Update the king_under_check status as well as
            # checking_piece
            king_under_check[king_idx] = False
            checking_pieces[self.colour].clear()

            # Try if this is a checking move on opponent's king
            self._check_opposing_king(kings_positions[king_idx ^ 1], king_under_check, king_idx ^ 1,
                                      stf_int, str_int, opp_col, board[sfr_int][sff_int], board, checking_pieces)

            # Try if a discovered check is possible on opponent's king
            other_dcb, other_dcr = self.dc.verify_opposing_king(kings_positions[king_idx ^ 1],
                                                                self.colour, sff_int, sfr_int, stf_int, str_int, board)
            if other_dcb:
                king_under_check[king_idx ^ 1] = True
                checking_pieces[opp_col].append(other_dcb)
            elif other_dcr:
                king_under_check[king_idx ^ 1] = True
                checking_pieces[opp_col].append(other_dcr)

            # If it's a corner move, update castling options
            if (str_int, stf_int) in [(0, 0), (0, 7), (7, 0), (7, 7)] and \
                    hasattr(board[str_int][stf_int], 'can_castle') and \
                    board[str_int][stf_int].colour == opp_col:
                board[str_int][stf_int].can_castle = False

            # Update rank and file
            self.rank, self.file = str_int, stf_int

        return move_valid

    def __repr__(self) -> str:
        return f"{self.colour} {self.name}"
