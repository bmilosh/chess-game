from model.pieces.piece_interface import PieceInterface

class SquareValidator:
    def single_square_validator(self, square: str) -> tuple[bool,str]:
        return (len(square) == 2 and square[0] in 'abcdefgh' and 
                square[1].isdecimal() and int(square[1]) in range(1,9))

    def validate_both_squares(self, square_from: str, square_to: str):
        return (self.single_square_validator(square_from) and 
                self.single_square_validator(square_to))

    def check_squares(self, square_from: str, square_to: str, board: list[list]):
        if not self.validate_both_squares(square_from, square_to):
            raise ValueError("Invalid square given")
        file_diff = abs(ord(square_from[0]) - ord(square_to[0]))
        rank_diff = int(square_to[1]) - int(square_from[1])
        square_from_occupant = board[int(square_from[1])-1][ord(square_from[0])-97]
        square_to_occupant = board[int(square_to[1])-1][ord(square_to[0])-97]
        # # print(f"{square_from_occupant=} {square_to_occupant=} {square_from=} {square_to=}")
        # print(f"{isinstance(square_to_occupant, Piece)=}")
        # print(f"{isinstance(square_from_occupant, Piece)=}")
        # print(f"{square_to_occupant=}")
        # # print(f"same colour = {square_from_occupant.colour == square_to_occupant.colour}")
        
        if isinstance(square_from_occupant, PieceInterface) and isinstance(square_to_occupant, PieceInterface):
            # print(f"same colour = {square_from_occupant.colour == square_to_occupant.colour}")
            if square_from_occupant.colour == square_to_occupant.colour:
                square_to_occupant = -1
            else:
                square_to_occupant = 1
        # if square_to_occupant and isinstance(square_from_occupant, str) and isinstance(square_to_occupant, str):
        #     # print(square_from_occupant[0], square_to_occupant[0])
        #     if square_from_occupant[0] == square_to_occupant[0]:
        #         square_to_occupant = -1
        #     else:
        #         square_to_occupant = 1
        return file_diff, rank_diff, square_to_occupant