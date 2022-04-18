
from model.discovered_checks import DiscoveredChecks
from model.pieces.piece_interface import Piece
from model.pieces.bishop import Bishop
from model.pieces.rook import Rook
from model.pieces.knight import Knight
from model.pieces.queen import Queen
from model.pieces.pawn import Pawn
from model.square_occ_getter import SquareOccupantGetter
from model.square_validator import SquareValidator


def convert_to_int(square: str):
    return ord(square[0]) - 97, int(square[1]) - 1


class King(Piece):
    """
    Moves 1 pace anywhere as long as it's safe to do so.
    Captures as it moves.
    """

    def __init__(self, colour: str = None) -> None:
        self.dc = DiscoveredChecks()
        self.sog = SquareOccupantGetter()
        self.colour = colour
        self.rank = None
        self.file = None
        self.name = 'king'
        self.can_castle = True
        self.legal_moves = None

    def get_legal_moves(self, kings_positions: list[tuple], checking_pieces: dict,
                        board, flipped=False, king_under_check=None, opp_active_pieces: list[Piece]=None) -> list:
        bad_squares = set()
        idx, opp_col = (0, "white") if self.colour == "black" else (1, "black")
        # print(f"from king: {opp_active_pieces = }")
        rng = list(range(-1, 2))
        pos_squares = set()
        temp_dict = {}
        for i, j in [(i, j) for i in rng for j in rng]:
            if self.rank+i in range(8) and self.file+j in range(8) and not (i == 0 and j == 0) and \
                    self.sog.get_square_occupant(board, self.rank+i, self.file+j, opp_col) != -1:
                pos_squares.add((self.rank+i, self.file+j))
                temp_dict[(self.rank+i, self.file+j)] = board[self.rank+i][self.file+j]
                board[self.rank+i][self.file+j] = 0

        for threat in opp_active_pieces:
            if threat.colour == self.colour:
                raise ValueError(f"Wrong colour active pieces sent. \n{self}, {opp_active_pieces = }")
            if isinstance(threat, King) or isinstance(threat, Pawn):
                continue
            bad_squares |= set(threat.get_legal_moves(kings_positions, checking_pieces, board))

        # pos_squares = set((self.rank+i, self.file+j) for i in rng for j in rng if self.rank+i in range(8) and self.file+j in range(8) and i+j != 0)
        good_squares = pos_squares - bad_squares
        temp = set()
        for r, f in good_squares:
            if not self._king_safe_from_king(f, r, kings_positions, self.colour) or\
                not self._king_safe_from_pawn(f, r, self.colour, board, flipped):
                temp.add((r, f))
                bad_squares.add((r, f))
        good_squares -= temp
        def check_castling(f):
            if self.validate_castling(self.rank, self.file, self.file+f, self.rank, king_under_check, self.colour,\
                    idx, kings_positions, board, flipped, checking_pieces, bad_squares) and \
                    (self.rank, self.file+f) not in bad_squares:
                good_squares.add((self.rank, self.file+f))
        check_castling(2)
        check_castling(-2)
        # print(f"good squares are: {good_squares = }")
        self.legal_moves = list(good_squares)
        # print(f"legal moves: {self.legal_moves = }")
        for pair in temp_dict:
            r, f = pair
            board[r][f] = temp_dict[pair]
        temp_dict.clear()
        return self.legal_moves

    # def get_legal_moves(self, kings_positions: list[tuple], checking_pieces: dict,
    #                     board, flipped=False, king_under_check=None) -> list:
    #     def check(r, f):
    #         if rank + r not in range(8) or file + f not in range(8):
    #             return
    #         occ = self.sog.get_square_occupant(
    #             board,  rank + r, file + f, opp_col)
    #         if occ == -1 or (not r and not f):
    #             return
    #         if not self._is_safe(file+f, rank+r, self.colour, board, kings_positions, flipped):
    #             return
    #         if f not in [2, -2] or (not king_under_check[idx] and
    #                                 self.validate_castling(rank, file, file+f, rank+r, king_under_check,
    #                                 self.colour, idx, kings_positions, board, flipped, checking_pieces)):
    #             self.legal_moves.append((rank + r, file + f))

    #     self.legal_moves = []
    #     opp_col, idx = ("white", 0) if self.colour == "black" else ("black", 1)
    #     rank, file = self.rank, self.file
    #     rng = list(range(-1, 2))
    #     temp = board[rank][file]
    #     board[rank][file] = 0
    #     for r, f in [(i, j) for i in rng for j in rng]:
    #         check(r, f)
    #     check(0, 2)
    #     check(0, -2)
    #     board[rank][file] = temp
    #     return self.legal_moves

    def _king_safe_from_pawn(self, stf_int, str_int, king_colour, board, flipped: bool):
        def check_square(r_dir, opp_colour):
            p1 = board[str_int + r_dir][stf_int - left_f_dir]
            p2 = board[str_int + r_dir][stf_int + right_f_dir]
            return not ((stf_int > 0 and isinstance(p1, Pawn) and p1.colour == opp_colour) or
                        (stf_int < 7 and isinstance(p2, Pawn) and p2.colour == opp_colour))

        left_f_dir = 0 if not stf_int else 1
        right_f_dir = 0 if stf_int == 7 else 1
        if king_colour == 'white' and not flipped and str_int <= 5:
            return check_square(1, 'black')
        elif king_colour == 'black' and flipped and 5 >= str_int:
            return check_square(1, 'white')
        elif king_colour == 'black' and not flipped and 2 <= str_int <= 7:
            return check_square(-1, 'white')
        elif king_colour == 'white' and flipped and 2 <= str_int <= 7:
            return check_square(-1, 'black')

        return True

    def _king_safe_from_king(self, stf_int, str_int, kings_positions, king_colour):
        opp_king = 0 if king_colour == 'white' else 1
        return (abs(kings_positions[opp_king][0]-str_int) > 1 or
                abs(kings_positions[opp_king][1]-stf_int) > 1)

    # def _king_safe_from_knight(self, stf_int, str_int, king_colour, board):
    #     for pair in [((r1, f1), (f1, r1)) for r1 in [-1, 1] for f1 in [-2, 2]]:
    #         for r, f in pair:
    #             r_diff, f_diff = str_int-r, stf_int-f
    #             if r_diff not in range(8) or f_diff not in range(8):
    #                 continue
    #             # if 0 <= r_diff <= 7 and 0 <= f_diff <= 7:
    #             p = board[r_diff][f_diff]
    #             if ((king_colour == 'white' and isinstance(p, Knight) and p.colour == 'black') or
    #                     (king_colour == 'black' and isinstance(p, Knight) and p.colour == 'white')):
    #                 return False
    #     return True

    # def __check(self, str_int, stf_int, board, threat, opp_col, k=1):
    #     """
    #     Utility function for the bishop and rook safety checks.
    #     k is set to 1 for the bishop. However, in order to be 
    #     able to check same file and rank for the rook, we pass
    #     it in as 0.
    #     """
    #     safe1 = safe2 = safe3 = safe4 = None

    #     def check(safe, i, j):
    #         if 0 <= str_int + i <= 7 and 0 <= stf_int + j <= 7 and \
    #                 isinstance(board[str_int + i][stf_int + j], Piece):
    #             p = board[str_int + i][stf_int + j]
    #             # print(f"{type(p)=} {threat=} {opp_col=} {p.colour=}")
    #             if type(p) in threat and p.colour == opp_col:
    #                 safe = False if safe is None else safe
    #             else:
    #                 safe = True if safe is None else safe
    #         return safe

    #     for i in range(1, 8):
    #         safe1 = check(safe1, -i, -i*k)
    #         safe2 = check(safe2, -i*k, i)
    #         safe3 = check(safe3, i*k, -i)
    #         safe4 = check(safe4, i, i*k)
    #         if safe1 == safe2 == safe3 == safe4 == True:
    #             return True
    #     return safe1 != False and safe2 != False and safe3 != False and safe4 != False

    # def _king_safe_from_bishop(self, stf_int, str_int, king_colour, board):
    #     # print("checking king safety from bishop")
    #     threat = [Bishop, Queen]
    #     opp_col = 'black' if king_colour == 'white' else 'white'
    #     return self.__check(str_int, stf_int, board, threat, opp_col)

    # def _king_safe_from_rook(self, stf_int, str_int, king_colour, board):
    #     # print("checking king safety from rook")
    #     threat = [Rook, Queen]
    #     opp_col = 'black' if king_colour == 'white' else 'white'
    #     return self.__check(str_int, stf_int, board, threat, opp_col, k=0)

    # def _king_safe_from_queen(self, stf_int, str_int, king_colour, board):
    #     # print("checking king safety from queen")
    #     return (self._king_safe_from_bishop(stf_int, str_int, king_colour, board) and
    #             self._king_safe_from_rook(stf_int, str_int, king_colour, board))

    # def _is_safe(self, stf_int, str_int, king_colour, board, kings_positions, flipped):
    #     return self._king_safe_from_pawn(stf_int, str_int, king_colour, board, flipped) and \
    #         self._king_safe_from_king(stf_int, str_int, kings_positions, king_colour) and \
    #         self._king_safe_from_knight(stf_int, str_int, king_colour, board) and \
    #         self._king_safe_from_queen(stf_int, str_int, king_colour, board)

    def validate_castling(self, sfr_int, sff_int, stf_int, str_int, king_under_check,
                          king_colour, king_idx, kings_positions, board, flipped, checking_pieces, bad_squares):

        opp_col = 'white' if king_colour == 'black' else 'black'
        # print(f"castling privs: {self.can_castle_kingside=} {self.can_castle_queenside=}, {stf_int=}, {sff_int=}")

        def check(end, f_dir):
            # print(f"{end=}, {f_dir=}, {stf_int=}, {str_int=}, {i=}, {board[str_int][i]=}, {sff_int=}")
            j = 0
            for i in range(sff_int+f_dir, end, f_dir):
                # print(f"{end=}, {f_dir=}, {stf_int=}, {str_int=}, {i=}, {board[str_int][i]=}, {sff_int=}")
                if board[sfr_int][i] != 0:
                    # print(f"************ can't castle cos of occupied square ***************")
                    return False
                if j < 2 and (str_int, i) in bad_squares:
                # if j < 2 and not self._is_safe(i, str_int, king_colour, board, kings_positions, flipped):
                    # print("************ can't castle cos of threatened square ***************")
                    return False
                j += 1
            return True
        file = 0 if stf_int < sff_int else 7
        if board[str_int][file] == 0 or \
                not isinstance(board[str_int][file], Rook) or \
                not board[str_int][file].colour == king_colour or \
                not board[str_int][file].can_castle:
            return False
        # print(f"{board[str_int][file].can_castle=}")
        # print(f"{board[sfr_int][sff_int].can_castle=}")
        # print(f"{self.can_castle=}")
        if stf_int < sff_int:
            chk = check(0, -1)
            if flipped and king_colour == 'black':
                rook_square = (0, 2)
            elif flipped and king_colour == 'white':
                rook_square = (7, 2)
            elif not flipped and king_colour == 'white':
                rook_square = (0, 3)
            else:
                rook_square = (7, 3)
        elif stf_int > sff_int:
            # print(f"{sff_int-stf_int=}")
            chk = check(7, 1)
            if flipped and king_colour == 'black':
                rook_square = (0, 4)
            elif flipped and king_colour == 'white':
                rook_square = (7, 4)
            elif not flipped and king_colour == 'white':
                rook_square = (0, 5)
            else:
                rook_square = (7, 5)
        if self.can_castle and chk:
            # print(f"should castle")
            Rook()._check_opposing_king(kings_positions, kings_positions[king_idx ^ 1], king_under_check, king_idx ^ 1,
                                        rook_square[1], rook_square[0], opp_col, Rook(king_colour), board, checking_pieces)
        return self.can_castle and chk

    def move(self, square_from: str, square_to: str, kings_positions: list[tuple],
             king_under_check: list[bool], board: list[list], sqv: SquareValidator,
             flipped: bool = False, checking_pieces=None, opp_active_pieces: list = None):

        square_from, square_to = square_from.strip(), square_to.strip()

        sff_int, sfr_int = convert_to_int(square_from)
        stf_int, str_int = convert_to_int(square_to)

        king_idx, opp_col = (
            1, 'black') if self.colour == 'white' else (0, 'white')

        # if self.legal_moves is None or flipped:
        self.get_legal_moves(
            kings_positions, checking_pieces, board, flipped, king_under_check, opp_active_pieces)
        move_valid = (str_int, stf_int) in self.legal_moves
        self.legal_moves = None

        if move_valid:
            # Move is valid means the king is now in a safe square.
            king_under_check[king_idx] = False
            checking_pieces[self.colour].clear()

            # Check if this move leads to a discovered check on the other king.
            other_dcb, other_dcr = self.dc.verify_opposing_king(kings_positions[king_idx ^ 1],  self.colour, sff_int,
                                                                sfr_int, stf_int, str_int, board)
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
