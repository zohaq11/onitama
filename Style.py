from __future__ import annotations
from typing import List, Tuple, Union
from Pieces import Pieces


class Style:
    """
    A Style class
    """

    pairs: List[Tuple[int, int]]
    name: str
    owner: str

    def __init__(self, pairs: List[Tuple[int, int]], name: str, owner=Pieces.EMPTY) -> None:
        """
        Initializes a new Style object
        """
        self.name = name
        self._moves = pairs.copy()
        self.owner = owner

    def get_moves(self) -> List[Tuple[int, int]]:
        """
        Returns a copy of _moves of the Style object
        """
        return self._moves.copy()

    def __eq__(self, other: Style) -> bool:
        """
        Returns if the two Style objects are equal
        """
        return self.name == other.name and self.owner == other.owner

    def __copy__(self) -> Style:
        """
        Returns a copy of Style object
        """
        return Style(self._moves.copy(), self.name, self.owner)
