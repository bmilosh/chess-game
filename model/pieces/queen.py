from model.discovered_checks import DiscoveredChecks
from model.pieces.bishop import Bishop
from model.pieces.piece_interface import BishopInterface, Piece
from model.pieces.rook import Rook
from model.square_validator import SquareValidator


def convert_to_int(square: str):
    return ord(square[0]) - 97, int(square[1]) - 1


class Queen(Piece):
    """
    Moves like every other piece except the knight.
    Captures as it moves.
    """

    def __init__(self, colour: str = None) -> None:
        self.dc = DiscoveredChecks()
        self.colour = colour
        self.rank = None
        self.file = None
        self.name = 'queen'
        self.legal_moves = None
        self.bishop = Bishop(self.colour)
        self.rook = Rook(self.colour)
        self.bishop.rank, self.bishop.file = self.rank, self.file
        self.rook.rank, self.rook.file = self.rank, self.file

    def get_legal_moves(self, kings_positions: list[tuple], checking_pieces: dict, board, flipped=False, king_under_check=None):
        self.bishop.rank, self.bishop.file = self.rank, self.file
        self.rook.rank, self.rook.file = self.rank, self.file
        self.legal_moves = self.bishop.get_legal_moves(kings_positions, checking_pieces, board) +\
            self.rook.get_legal_moves(kings_positions, checking_pieces, board)
        return self.legal_moves

    def move(self, square_from: str, square_to: str, kings_positions: list[tuple],
             king_under_check: list[bool], board: list[list], sqv: SquareValidator,
             flipped: bool = False, checking_pieces=None):

        king_idx, opp_col = (
            0, 'white') if self.colour == 'black' else (1, 'black')
        if king_under_check[king_idx] and checking_pieces is not None and len(checking_pieces[self.colour]) > 1:
            return False

        stf_int, str_int = convert_to_int(square_to)
        # if self.legal_moves is None or flipped:
        self.get_legal_moves(kings_positions, checking_pieces, board)
        move_valid = (str_int, stf_int) in self.legal_moves
        # print(f"queen legal moves: {self.legal_moves}")
        # print(f"{move_valid=} {str_int=} {stf_int=}")
        self.legal_moves = None
        if move_valid:
            # print(f"checking pieces from queen: {checking_pieces=} (before checking)")
            king_under_check[king_idx] = False
            checking_pieces[self.colour].clear()
            self.bishop._check_opposing_king(kings_positions, kings_positions[king_idx ^ 1], king_under_check, king_idx ^ 1,
                                             stf_int, str_int, opp_col, self, board, checking_pieces)
            self.rook._check_opposing_king(kings_positions, kings_positions[king_idx ^ 1], king_under_check, king_idx ^ 1,
                                           stf_int, str_int, opp_col, self, board, checking_pieces)  # board[self.rank][self.file]
            # print(f"checking pieces from queen: {checking_pieces=} (after checking)")
            # print()
            self.rank, self.file = str_int, stf_int
        return move_valid

    def __repr__(self) -> str:
        return f"{self.colour} {self.name}"
