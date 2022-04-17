from abc import ABC, abstractmethod


class Piece(ABC):
    colour: str = None
    @abstractmethod
    def move(self):
        pass

    @abstractmethod
    def get_legal_moves(self):
        pass