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
        self.bandr_mgtr = BishopAndRookMovesGetter()
        self.colour = colour
        self.name = "rook"
        self.can_castle = True

    def get_legal_moves(
        self, kings_positions: list[tuple], checking_pieces: dict, board, **kwargs
    ) -> list:
        opp_col = "white" if self.colour == "black" else "black"
        king_position = (
            kings_positions[0] if self.colour == "black" else kings_positions[1]
        )
        self.legal_moves = self.bandr_mgtr.bishop_and_rook_moves(
            self.rank,
            self.file,
            king_position,
            checking_pieces,
            board,
            self.dc,
            opp_col,
            k=0,
        )
        return self.legal_moves

    def _check_move(
        self, low_rank: int, high_rank: int, low_file: int, high_file: int, board
    ) -> bool:
        no_obstacles = True
        for rank in range(low_rank, high_rank):
            for file in range(low_file, high_file):
                if board[rank][file] != 0:
                    no_obstacles = False
        return no_obstacles

    def _check_opposing_king(
        self,
        kings_positions,
        king_position: tuple,
        king_under_check: list[bool],
        king_idx,
        stf_int,
        str_int,
        opp_col,
        entry,
        board,
        checking_pieces,
    ):
        self.rank, self.file = str_int, stf_int
        self.get_legal_moves(kings_positions, checking_pieces, board)
        if king_position in self.legal_moves:
            king_under_check[king_idx] = True
            checking_pieces[opp_col].append((entry, (str_int, stf_int)))
        self.legal_moves = None

    def move(
        self,
        square_from: str,
        square_to: str,
        kings_positions: list[tuple],
        king_under_check: list[bool],
        board: list[list],
        sqv: SquareValidator,
        **kwargs,
    ):

        """
        **kwargs
        flipped: bool = False,
        queen_move: BishopInterface = None,
        checking_pieces=None
        """
        queen_move = kwargs["queen_move"]
        checking_pieces = kwargs["checking_pieces"]

        square_from, square_to = square_from.strip(), square_to.strip()

        sff_int, sfr_int = convert_to_int(square_from)
        stf_int, str_int = convert_to_int(square_to)

        col = king = board[sfr_int][sff_int].colour
        king_idx = 0 if king == "black" else 1
        if (
            king_under_check[king_idx]
            and checking_pieces is not None
            and len(checking_pieces[king]) > 1
        ):
            return False

        self.get_legal_moves(kings_positions, checking_pieces, board)
        move_valid = (str_int, stf_int) in self.legal_moves
        self.legal_moves = None

        if move_valid:
            opp_col = "black" if col == "white" else "white"

            # We've unchecked our king by the previous check.
            # Update the king_under_check status as well as
            # checking_piece
            king_under_check[king_idx] = False
            checking_pieces[col].clear()

            # Try if this is a checking move on opponent's king
            self._check_opposing_king(
                kings_positions,
                kings_positions[king_idx ^ 1],
                king_under_check,
                king_idx ^ 1,
                stf_int,
                str_int,
                opp_col,
                board[sfr_int][sff_int],
                board,
                checking_pieces,
            )

            # Queen might be checking from the same diagonal as the king
            if queen_move is not None:
                queen_move._check_opposing_king(
                    kings_positions,
                    kings_positions[king_idx ^ 1],
                    king_under_check,
                    king_idx ^ 1,
                    stf_int,
                    str_int,
                    opp_col,
                    board[sfr_int][sff_int],
                    board,
                    checking_pieces,
                )

            # Try if a discovered check is possible on opponent's king
            other_dcb, other_dcr = self.dc.verify_opposing_king(
                kings_positions[king_idx ^ 1],
                col,
                sff_int,
                sfr_int,
                stf_int,
                str_int,
                board,
            )
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
