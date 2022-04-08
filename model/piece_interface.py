from abc import ABC, abstractmethod


class Piece(ABC):
    colour: str = None
    @abstractmethod
    def move(self):
        pass