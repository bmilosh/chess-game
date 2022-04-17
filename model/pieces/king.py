
from model.discovered_checks import DiscoveredChecks
from model.pieces.piece_interface import Piece
from model.pieces.bishop import Bishop
from model.pieces.rook import Rook
from model.pieces_old import Pawn
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

    # def get_legal_moves(self):
    def get_legal_moves(self, kings_positions: list[tuple], checking_pieces: dict,
                             board, flipped=False, king_under_check=None) -> list:
        def check(r, f):
            if rank + r not in range(8) or file + f not in range(8):
                return
            occ = self.sog.get_square_occupant(board,  rank + r, file + f, opp_col)
            if occ == -1 or (not r and not f):
                return
            if self._is_safe(file+f, rank+r, col, board, kings_positions, flipped):
                if f not in [2, -2] or (not king_under_check[idx] and\
                        self.validate_castling(rank, file, file+f, rank+r, king_under_check,
                                        col, idx, kings_positions, board, flipped, checking_pieces)):
                    self.legal_moves.append((rank + r, file + f))
        self.legal_moves = []
        col = self.colour
        opp_col, idx = ("white", 0) if self.colour == "black" else ("black", 1)
        rank, file = self.rank, self.file
        rng = list(range(-1, 2))
        temp = board[rank][file]
        board[rank][file] = 0
        for r, f in [(i, j) for i in rng for j in rng]:
            check(r, f)
        check(0, 2)
        check(0, -2)
        board[rank][file] = temp
        return self.legal_moves

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

    def _king_safe_from_knight(self, stf_int, str_int, king_colour, board):
        for pair in [((r1, f1), (f1, r1)) for r1 in [-1, 1] for f1 in [-2, 2]]:
            for r, f in pair:
                r_diff, f_diff = str_int-r, stf_int-f
                if r_diff not in range(8) or f_diff not in range(8):
                    continue
                # if 0 <= r_diff <= 7 and 0 <= f_diff <= 7:
                p = board[r_diff][f_diff]
                if ((king_colour == 'white' and isinstance(p, Knight) and p.colour == 'black') or
                        (king_colour == 'black' and isinstance(p, Knight) and p.colour == 'white')):
                    return False
        return True

    def __check(self, str_int, stf_int, board, threat, opp_col, k=1):
        """
        Utility function for the bishop and rook safety checks.
        k is set to 1 for the bishop. However, in order to be 
        able to check same file and rank for the rook, we pass
        it in as 0.
        """
        safe1 = safe2 = safe3 = safe4 = None

        def check(safe, i, j):
            if 0 <= str_int + i <= 7 and 0 <= stf_int + j <= 7 and \
                    isinstance(board[str_int + i][stf_int + j], Piece):
                p = board[str_int + i][stf_int + j]
                # print(f"{type(p)=} {threat=} {opp_col=} {p.colour=}")
                if type(p) in threat and p.colour == opp_col:
                    safe = False if safe is None else safe
                else:
                    safe = True if safe is None else safe
            return safe

        for i in range(1, 8):
            safe1 = check(safe1, -i, -i*k)
            safe2 = check(safe2, -i*k, i)
            safe3 = check(safe3, i*k, -i)
            safe4 = check(safe4, i, i*k)
            if safe1 == safe2 == safe3 == safe4 == True:
                return True
        return safe1 != False and safe2 != False and safe3 != False and safe4 != False

    def _king_safe_from_bishop(self, stf_int, str_int, king_colour, board):
        # print("checking king safety from bishop")
        threat = [Bishop, Queen]
        opp_col = 'black' if king_colour == 'white' else 'white'
        return self.__check(str_int, stf_int, board, threat, opp_col)

    def _king_safe_from_rook(self, stf_int, str_int, king_colour, board):
        # print("checking king safety from rook")
        threat = [Rook, Queen]
        opp_col = 'black' if king_colour == 'white' else 'white'
        return self.__check(str_int, stf_int, board, threat, opp_col, k=0)

    def _king_safe_from_queen(self, stf_int, str_int, king_colour, board):
        # print("checking king safety from queen")
        return (self._king_safe_from_bishop(stf_int, str_int, king_colour, board) and
                self._king_safe_from_rook(stf_int, str_int, king_colour, board))

    def _is_safe(self, stf_int, str_int, king_colour, board, kings_positions, flipped):
        return self._king_safe_from_pawn(stf_int, str_int, king_colour, board, flipped) and \
            self._king_safe_from_king(stf_int, str_int, kings_positions, king_colour) and \
            self._king_safe_from_knight(stf_int, str_int, king_colour, board) and \
            self._king_safe_from_queen(stf_int, str_int, king_colour, board)

    def validate_castling(self, sfr_int, sff_int, stf_int, str_int, king_under_check,
                    king_colour, king_idx, kings_positions, board, flipped, checking_pieces):
        
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
                if j < 2 and not self._is_safe(i, str_int, king_colour, board, kings_positions, flipped):
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
            Rook()._check_opposing_king(kings_positions[king_idx^1], king_under_check, king_idx^1, 
                rook_square[1], rook_square[0], opp_col, Rook(king_colour), board, checking_pieces)
        return self.can_castle and chk


    def _move_is_valid(self, rank_diff, file_diff, square_to_occupant, sfr_int, sff_int,
                       stf_int, str_int, king_colour, board, kings_positions,
                       king_under_check, king_idx, flipped, checking_pieces):
        if square_to_occupant == -1 or (not file_diff and not rank_diff) or file_diff > 2 or abs(rank_diff) > 1:
            return False
        elif file_diff == 2:
            return not king_under_check[king_idx] and \
                 self.validate_castling(sfr_int, sff_int, stf_int, str_int, king_under_check,
                        king_colour, king_idx, kings_positions, board, flipped, checking_pieces)
        else:
            # print("checking king safety")
            temp = board[sfr_int][sff_int]
            board[sfr_int][sff_int] = 0
            move_valid = self._is_safe(
                stf_int, str_int, king_colour, board, kings_positions, flipped)
            board[sfr_int][sff_int] = temp
            return move_valid

    def move(self, square_from: str, square_to: str, kings_positions: list[tuple],
             king_under_check: list[bool], board: list[list], sqv: SquareValidator, 
             flipped: bool = False, checking_pieces=None):
        square_from, square_to = square_from.strip(), square_to.strip()
        # file_diff, rank_diff, square_to_occupant = sqv.check_squares(
        #     square_from, square_to, board)
        sff_int, sfr_int = convert_to_int(square_from)
        stf_int, str_int = convert_to_int(square_to)
        # king_colour = board[sfr_int][sff_int].colour
        king_idx, opp_col = (1, 'black') if self.colour == 'white' else (0, 'white')
        # print(board[str_int][stf_int], square_to_occupant)
        # if hasattr(board[str_int][stf_int], 'colour'):
        #     print(board[str_int][stf_int].colour)

        if self.legal_moves is None or flipped:
            self.get_legal_moves(kings_positions, checking_pieces, board, flipped, king_under_check)
        move_valid = (str_int, stf_int) in self.legal_moves
        self.legal_moves = None

        # move_valid = self._move_is_valid(rank_diff, file_diff, square_to_occupant, sfr_int, sff_int,
        #                                  stf_int, str_int, king_colour, board, kings_positions,
        #                                  king_under_check, king_idx, flipped, checking_pieces)
        if move_valid:
            # opp_col = 'black' if king_colour == 'white' else 'white'
            if self.uncheck_king(checking_pieces[self.colour], stf_int, str_int, board):
                king_under_check[king_idx] = False
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

            else:
                return False
        return move_valid

    def _uncheck_from_pawn(self, pos, stf_int, str_int):
        if (abs(str_int-pos[0]), abs(stf_int-pos[1])) != (1, 1):
            return 1
        return 0

    def _uncheck_from_knight(self, pos, stf_int, str_int):
        if (abs(str_int-pos[0]), abs(stf_int-pos[1])) not in [(1, 2), (2, 1)]:
            return 1
        return 0

    def _uncheck_from_rook(self, pos, stf_int, str_int):
        if (abs(str_int-pos[0]) != 0 and abs(stf_int-pos[1]) != 0) or \
                (abs(str_int-pos[0]) == 0 and abs(stf_int-pos[1]) == 0):
            return 1
        return 0

    def _uncheck_from_bishop(self, pos, stf_int, str_int):
        if abs(str_int-pos[0]) != abs(stf_int-pos[1]) or pos == (str_int, stf_int):
            return 1
        return 0

    def _uncheck_from_queen(self, pos, stf_int, str_int, board):
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
        for piece_name, pos in chk_piece:
            if piece_name.name == 'pawn':
                c += self._uncheck_from_pawn(pos, stf_int, str_int)
            elif piece_name.name == 'knight':
                c += self._uncheck_from_knight(pos, stf_int, str_int)
            elif piece_name.name == 'rook':
                c += self._uncheck_from_rook(pos, stf_int, str_int)
            elif piece_name.name == 'bishop':
                c += self._uncheck_from_bishop(pos, stf_int, str_int)
            elif piece_name.name == 'queen':
                c += self._uncheck_from_queen(pos, stf_int, str_int, board)
            else:
                raise ValueError(f"Checking with unknown piece: {piece_name=}")
        if c == len(chk_piece):
            chk_piece.clear()
            return True
        return False

    def __repr__(self) -> str:
        return f"{self.colour} {self.name}"