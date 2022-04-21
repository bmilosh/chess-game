from abc import ABC, abstractmethod
from model.discovered_checks import DiscoveredChecks
from model.square_occ_getter import SquareOccupantGetter
# from model.square_validator import SquareValidator


class PieceInterface(ABC):
    pass


class Piece(PieceInterface):
    dc = DiscoveredChecks()
    sog = SquareOccupantGetter()
    rank: int = None
    file: int = None
    legal_moves: list = None

    def move(self):
        pass

    def get_legal_moves(self):
        pass


class RookInterface(ABC):

    @abstractmethod
    def _check_opposing_king(self):
        pass

    @abstractmethod
    def get_legal_moves(self):
        pass


class BishopInterface(ABC):

    @abstractmethod
    def _check_opposing_king(self):
        pass

    @abstractmethod
    def get_legal_moves(self):
        pass
