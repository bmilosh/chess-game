from model.pieces.pawn import Pawn
from model.pieces.piece_interface import Piece
from model.pieces.rook import Rook
from model.square_validator import SquareValidator


def convert_to_int(square: str):
    return ord(square[0]) - 97, int(square[1]) - 1


class King(Piece):
    """
    Moves 1 pace anywhere as long as it's safe to do so.
    Captures as it moves.
    """

    def __init__(self, colour: str = None) -> None:
        self.colour = colour
        self.name = "king"
        self.can_castle = True

    def get_legal_moves(
        self, kings_positions: list[tuple], checking_pieces: dict, board, **kwargs
    ) -> list:

        """
        flipped=False,
        king_under_check=None,
        opp_active_pieces: list[Piece] = None,

        """
        flipped = kwargs["flipped"]
        king_under_check = kwargs["king_under_check"]
        opp_active_pieces = kwargs["opp_active_pieces"]

        bad_squares = set()
        idx, opp_col = (0, "white") if self.colour == "black" else (1, "black")
        rng = list(range(-1, 2))
        pos_squares = set()
        temp_dict = {}
        for i, j in [(i1, j1) for i1 in rng for j1 in rng]:
            if (
                self.rank + i in range(8)
                and self.file + j in range(8)
                and not (i == 0 and j == 0)
                and self.sog.get_square_occupant(
                    board, self.rank + i, self.file + j, opp_col
                )
                != -1
            ):
                pos_squares.add((self.rank + i, self.file + j))
                temp_dict[(self.rank + i, self.file + j)] = board[self.rank + i][
                    self.file + j
                ]
                board[self.rank + i][self.file + j] = 0
        board[self.rank][
            self.file
        ] = 0  # set the king pos temporarily to zero as well so we can evaluate threats properly
        for threat in opp_active_pieces:
            if threat.colour == self.colour:
                raise ValueError(
                    f"Wrong colour active pieces sent. \n{self = }, {opp_active_pieces = }"
                )
            if isinstance(threat, King) or isinstance(threat, Pawn):
                continue
            bad_squares |= set(
                threat.get_legal_moves(kings_positions, checking_pieces, board)
            )

        for pair in temp_dict:
            r, f = pair
            board[r][f] = temp_dict[pair]
        temp_dict.clear()
        board[self.rank][self.file] = self  # reset king pos

        good_squares = pos_squares - bad_squares
        temp = set()
        for r, f in good_squares:
            if not self._king_safe_from_king(
                f, r, kings_positions, self.colour
            ) or not self._king_safe_from_pawn(f, r, self.colour, board, flipped):
                temp.add((r, f))
                bad_squares.add((r, f))
        good_squares -= temp

        def check_castling(f):
            if (
                self.validate_castling(
                    self.rank,
                    self.file,
                    self.file + f,
                    self.rank,
                    king_under_check,
                    self.colour,
                    idx,
                    kings_positions,
                    board,
                    flipped,
                    checking_pieces,
                    bad_squares,
                )
                and (self.rank, self.file + f) not in bad_squares
            ):
                good_squares.add((self.rank, self.file + f))

        check_castling(2)
        check_castling(-2)
        # print(f"good squares are: {good_squares = }")
        self.legal_moves = list(good_squares)
        return self.legal_moves

    def _king_safe_from_pawn(self, stf_int, str_int, king_colour, board, flipped: bool):
        def check_square(r_dir, opp_colour):
            p1 = board[str_int + r_dir][stf_int - left_f_dir]
            p2 = board[str_int + r_dir][stf_int + right_f_dir]
            return not (
                (stf_int > 0 and isinstance(p1, Pawn) and p1.colour == opp_colour)
                or (stf_int < 7 and isinstance(p2, Pawn) and p2.colour == opp_colour)
            )

        left_f_dir = 0 if not stf_int else 1
        right_f_dir = 0 if stf_int == 7 else 1
        if king_colour == "white" and not flipped and str_int <= 5:
            return check_square(1, "black")
        elif king_colour == "black" and flipped and 5 >= str_int:
            return check_square(1, "white")
        elif king_colour == "black" and not flipped and 2 <= str_int <= 7:
            return check_square(-1, "white")
        elif king_colour == "white" and flipped and 2 <= str_int <= 7:
            return check_square(-1, "black")

        return True

    def _king_safe_from_king(self, stf_int, str_int, kings_positions, king_colour):
        opp_king = 0 if king_colour == "white" else 1
        return (
            abs(kings_positions[opp_king][0] - str_int) > 1
            or abs(kings_positions[opp_king][1] - stf_int) > 1
        )

    def validate_castling(
        self,
        sfr_int,
        sff_int,
        stf_int,
        str_int,
        king_under_check,
        king_colour,
        king_idx,
        kings_positions,
        board,
        flipped,
        checking_pieces,
        bad_squares,
    ):
        if king_under_check[king_idx]:
            return False

        opp_col = "white" if king_colour == "black" else "black"

        def check(end, f_dir):
            pawn_row = 6 if str_int == 7 else 1
            pos_pawn_files = range(1, 6) if end == 0 else range(3, 8)
            if any(
                isinstance(board[pawn_row][i], Pawn)
                and board[pawn_row][i].colour != king_colour
                for i in pos_pawn_files
            ):
                return False
            j = 0
            for i in range(sff_int + f_dir, end, f_dir):
                if board[sfr_int][i] != 0:
                    return False
                if j < 2 and (str_int, i) in bad_squares:
                    return False
                j += 1
            return True

        file = 0 if stf_int < sff_int else 7
        if (
            board[str_int][file] == 0
            or not isinstance(board[str_int][file], Rook)
            or not board[str_int][file].colour == king_colour
            or not board[str_int][file].can_castle
        ):
            return False
        if stf_int < sff_int:
            chk = check(0, -1)
            if flipped and king_colour == "black":
                rook_square = (0, 2)
            elif flipped and king_colour == "white":
                rook_square = (7, 2)
            elif not flipped and king_colour == "white":
                rook_square = (0, 3)
            else:
                rook_square = (7, 3)
        elif stf_int > sff_int:
            chk = check(7, 1)
            if flipped and king_colour == "black":
                rook_square = (0, 4)
            elif flipped and king_colour == "white":
                rook_square = (7, 4)
            elif not flipped and king_colour == "white":
                rook_square = (0, 5)
            else:
                rook_square = (7, 5)
        if self.can_castle and chk:
            Rook(self.colour)._check_opposing_king(
                kings_positions,
                kings_positions[king_idx ^ 1],
                king_under_check,
                king_idx ^ 1,
                rook_square[1],
                rook_square[0],
                opp_col,
                Rook(king_colour),
                board,
                checking_pieces,
            )
        return self.can_castle and chk

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
        flipped: bool = False,
        checking_pieces=None,
        opp_active_pieces: list = None,
        """

        flipped = kwargs["flipped"]
        checking_pieces = kwargs["checking_pieces"]
        opp_active_pieces = kwargs["opp_active_pieces"]

        square_from, square_to = square_from.strip(), square_to.strip()

        sff_int, sfr_int = convert_to_int(square_from)
        stf_int, str_int = convert_to_int(square_to)

        king_idx, opp_col = (1, "black") if self.colour == "white" else (0, "white")

        self.get_legal_moves(
            kings_positions,
            checking_pieces,
            board,
            flipped=flipped,
            king_under_check=king_under_check,
            opp_active_pieces=opp_active_pieces,
        )
        move_valid = (str_int, stf_int) in self.legal_moves
        self.legal_moves = None

        if move_valid:
            # Move is valid means the king is now in a safe square.
            king_under_check[king_idx] = False
            checking_pieces[self.colour].clear()

            # Check if this move leads to a discovered check on the other king.
            other_dcb, other_dcr = self.dc.verify_opposing_king(
                kings_positions[king_idx ^ 1],
                self.colour,
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

            # Update rank and file
            self.rank, self.file = str_int, stf_int

        return move_valid

    def __repr__(self) -> str:
        return f"{self.colour} {self.name}"
