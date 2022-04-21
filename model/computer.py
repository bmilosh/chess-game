from model.pieces.piece_interface import Piece
from random import shuffle

class Computer:
    """
    Used in a single-player setting.
    Makes random legal moves.
    """

    def __init__(self, colour: str, active_pieces: list[Piece]) -> None:
        self.colour = colour
        self.ap = active_pieces

    def make_move(self, kings_positions: list[tuple], checking_pieces: dict, board, \
                flipped=False, king_under_check=None,opp_active_pieces: list[Piece]=None):
        shuffle(self.ap)
        idx = 0 if self.colour == "black" else 1
        for piece in self.ap:
            if piece.name == 'king':
                moves = piece.get_legal_moves(kings_positions, checking_pieces, board, flipped, king_under_check, opp_active_pieces)
            else:
                moves = piece.get_legal_moves(kings_positions, checking_pieces, board, flipped, king_under_check)
            
            if len(moves):
                shuffle(moves)
                move = moves[0]
                ### Need to verify opponent's king (i.e., see if we've checked their king) ###
                if move in [(0, 0), (0, 7), (7, 0), (7, 7)] and \
                        hasattr(board[move[0]][move[1]], 'can_castle') and \
                        board[move[0]][move[1]].colour != self.colour:
                    board[move[0]][move[1]].can_castle = False
                # piece.rank, piece.file = move
                king_under_check[idx] = False
                checking_pieces[self.colour].clear()
                return piece, move
        print("************** There's a stalemate on the board!!! ************")
        return None