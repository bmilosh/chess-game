from abc import ABC, abstractmethod


class Piece(ABC):
    colour: str = None

    @abstractmethod
    def move(self):
        pass

    @abstractmethod
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
