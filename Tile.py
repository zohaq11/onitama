# Import the pygame module
import pygame
from pygame.locals import (
    BLEND_MULT,
)
from Entity import Entity
from OnitamaGame import OnitamaGame
from Pieces import Pieces

from typing import Tuple


class Tile(Entity):
    """
    A board game Tile used in the pygame GUI.
    """
    width: int = 100
    height: int = 100
    row: int
    col: int

    def __init__(self, screen: pygame.Surface, onitama: OnitamaGame, pieces: Pieces, row: int, col: int, offset_x: int = (1000 - 5 * 100) // 2, offset_y: int = (800 - 5 * 100) // 2):
        """
        Initialize this tile.
        """
        super().__init__(screen=screen, onitama=onitama, offset_x=col * self.width + offset_x, offset_y=row *
                         self.height + offset_y)
        self.pieces = pieces
        self.row = row
        self.col = col

    def hover(self, mouse_pos: Tuple[int, int]):
        if self.img_rect and self.img_rect.collidepoint(mouse_pos):
            token = self.onitama.get_token(self.row, self.col).lower()
            color = self.COLOR_VALID if token == self.onitama.whose_turn.player_id.lower(
            ) else self.COLOR_INVALID
            self.img.fill(color, special_flags=BLEND_MULT)
            self.img_rect = self.screen.blit(self.img, self.rect)
            return True
        return False

    def draw(self):
        token = self.onitama.get_token(self.row, self.col)
        self.img = self.pieces.get_image(Pieces.EMPTY, self.row, self.col)

        self.img_rect = self.screen.blit(self.img,
                                         self.rect)
        if token != Pieces.EMPTY:
            # Draw the token image on top of the background
            self.img = self.pieces.get_image(token, self.row, self.col)
            self.img.set_colorkey((0, 0, 0))

        if self.clicked:
            color = self.COLOR_VALID if token.lower() == self.onitama.whose_turn.player_id.lower(
            ) else self.COLOR_INVALID
            self.img.fill(color, special_flags=BLEND_MULT)
            self.img_rect = self.screen.blit(self.img, self.rect)
        elif self.highlighted:
            self.img.fill(self.HIGHLIGHTED_COLOR, special_flags=BLEND_MULT)
            self.img_rect = self.screen.blit(self.img, self.rect)
        self.img_rect = self.screen.blit(self.img, self.rect)
