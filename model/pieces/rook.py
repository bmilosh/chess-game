from itertools import zip_longest

from model.bishop_and_rook_move_getter import BishopAndRookMovesGetter
from model.discovered_checks import DiscoveredChecks
from model.pieces.piece_interface import BishopInterface, Piece
from model.square_occ_getter import SquareOccupantGetter
from model.square_validator import SquareValidator


def convert_to_int(square: str):
    return ord(square[0]) - 97, int(square[1]) - 1


class Rook(Piece):
    """
    Moves horizontally and vertically. Not limited to any number of squares but
    can't jump over obstacles in its path.
    Captures as it moves.
    """

    def __init__(self, colour: str = None) -> None:
        self.dc = DiscoveredChecks()
        self.bandr_mgtr = BishopAndRookMovesGetter()
        self.colour = colour
        self.rank = None
        self.file = None
        self.name = 'rook'
        self.can_castle = True
        self.legal_moves = None

    # def get_legal_moves(self):
    #     pass

    def get_legal_moves(self, kings_positions: list[tuple], checking_pieces: dict, board, flipped=False, king_under_check=None) -> list:
        opp_col = "white" if self.colour == "black" else "black"
        king_position = kings_positions[0] if self.colour == "black" else kings_positions[1]
        self.legal_moves = self.bandr_mgtr.bishop_and_rook_moves(
            self.rank, self.file, king_position, checking_pieces, board, self.dc, opp_col, k=0)
        return self.legal_moves

    def _check_move(self, low_rank: int, high_rank: int, low_file: int, high_file: int, board) -> bool:
        no_obstacles = True
        for rank in range(low_rank, high_rank):
            for file in range(low_file, high_file):
                if board[rank][file] != 0:
                    no_obstacles = False
        return no_obstacles

    def _check_opposing_king(self, kings_positions, king_position: tuple, king_under_check: list[bool], king_idx,
                             stf_int, str_int, opp_col, entry, board, checking_pieces):
        self.rank, self.file = str_int, stf_int
        self.get_legal_moves(kings_positions, checking_pieces, board)
        # king_rank, king_file = king_position
        if king_position in self.legal_moves:
            king_under_check[king_idx] = True
            checking_pieces[opp_col].append(
                (entry, (str_int, stf_int)))
        self.legal_moves = None

    # def _check_opposing_king(self, king_position: tuple, king_under_check: list[bool], king_idx,
    #                          stf_int, str_int, opp_col, entry, board, checking_pieces):

    #     king_rank, king_file = king_position
    #     not_zero = 0
    #     temp = board[str_int][stf_int]
    #     board[str_int][stf_int] = entry
    #     if str_int == king_rank or stf_int == king_file:
    #         r_dir, f_dir, fill_value = (
    #             1, 0, str_int) if str_int == king_rank else (0, 1, stf_int)

    #         min1, max1 = min(str_int, king_rank), max(str_int, king_rank)
    #         min2, max2 = min(stf_int, king_file), max(stf_int, king_file)
    #         for r, f in zip_longest(range(min1, max1 + r_dir), range(min2, max2 + f_dir), fillvalue=fill_value):
    #             if 0 <= r <= 7 and 0 <= f <= 7:
    #                 if board[r][f] != 0:
    #                     not_zero += 1
    #     if not_zero == 1:
    #         king_under_check[king_idx] = True
    #         checking_pieces[opp_col].append((entry, (str_int, stf_int)))
    #     board[str_int][stf_int] = temp

    def move(self, square_from: str, square_to: str, kings_positions: list[tuple],
             king_under_check: list[bool],  board: list[list], sqv: SquareValidator,
             flipped: bool = False, queen_move: BishopInterface = None, checking_pieces=None):

        square_from, square_to = square_from.strip(), square_to.strip()

        # file_diff, rank_diff, square_to_occupant = sqv.check_squares(
        #     square_from, square_to, board)

        sff_int, sfr_int = convert_to_int(square_from)
        stf_int, str_int = convert_to_int(square_to)
        # low_rank = min(sfr_int, str_int)
        # high_rank = max(sfr_int, str_int)
        # low_file = min(stf_int, sff_int)
        # high_file = max(stf_int, sff_int)

        col = king = board[sfr_int][sff_int].colour
        king_idx = 0 if king == 'black' else 1
        if king_under_check[king_idx] and checking_pieces is not None and len(checking_pieces[king]) > 1:
            return False

        # # Rook's not moving
        # if file_diff == 0 and rank_diff == 0:
        #     move_valid = False
        # # Rook's moving along the same file
        # elif file_diff == 0:
        #     move_valid = (self._check_move(low_rank+1, high_rank, low_file, high_file+1, board)
        #                   and square_to_occupant != -1)
        # # Rook's moving along the same rank
        # elif rank_diff == 0:
        #     move_valid = (self._check_move(low_rank, high_rank+1, low_file+1, high_file, board)
        #                   and square_to_occupant != -1)
        # # Invalid rook movement
        # else:
        #     move_valid = False
        # if self.legal_moves is None:
        self.get_legal_moves(kings_positions, checking_pieces, board)
        move_valid = (str_int, stf_int) in self.legal_moves
        # print(f"rook legal moves: {self.legal_moves=}")
        # print(f"Valid rook move = {move_valid}")
        # print(f"{str_int=} {stf_int=}")
        self.legal_moves = None
        if move_valid:
            opp_col = 'black' if col == 'white' else 'white'
            # if self.dc.verify_own_king(kings_positions[king_idx],
            #                            opp_col, sff_int, sfr_int, stf_int, str_int, board, checking_pieces):
            #     return False

            # We've unchecked our king by the previous check.
            # Update the king_under_check status as well as
            # checking_piece
            king_under_check[king_idx] = False
            checking_pieces[col].clear()

            # Try if this is a checking move on opponent's king
            self._check_opposing_king(kings_positions, kings_positions[king_idx ^ 1], king_under_check,
                                      king_idx ^ 1, stf_int, str_int, opp_col, board[sfr_int][sff_int], board, checking_pieces)

            # Queen might be checking from the same diagonal as the king
            if queen_move is not None:
                queen_move._check_opposing_king(kings_positions, kings_positions[king_idx ^ 1], king_under_check, king_idx ^ 1,
                                                stf_int, str_int, opp_col, board[sfr_int][sff_int], board, checking_pieces)

            # Try if a discovered check is possible on opponent's king
            other_dcb, other_dcr = self.dc.verify_opposing_king(kings_positions[king_idx ^ 1],
                                                                col, sff_int, sfr_int, stf_int, str_int, board)
            if other_dcb:
                king_under_check[king_idx ^ 1] = True
                checking_pieces[opp_col].append(other_dcb)
            elif other_dcr:
                king_under_check[king_idx ^ 1] = True
                checking_pieces[opp_col].append(other_dcr)

            # update castling options
            if not queen_move:
                self.can_castle = False

            # Update rank and file
            self.rank, self.file = str_int, stf_int

        return move_valid

    def __repr__(self) -> str:
        return f"{self.colour} {self.name}"
