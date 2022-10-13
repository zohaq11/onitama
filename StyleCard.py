# Import the pygame module
import pygame
from pygame.locals import (
    BLEND_MULT,
)

from Entity import Entity
from OnitamaGame import OnitamaGame
from Pieces import Pieces
from StyleImages import StyleImages

from typing import Tuple


class StyleCard(Entity):
    """
    A class to represent and display a Style of Onitama.
    """

    def __init__(self, screen: pygame.Surface, onitama: OnitamaGame, player_id: str, style_name: str, style_images: StyleImages, offset_x: int, offset_y: int):
        """
        Initialize this StyleCard.
        """
        super().__init__(screen=screen, onitama=onitama, width=200,
                         height=150, offset_x=offset_x, offset_y=offset_y)
        self.style_name = style_name
        self.style_images = style_images
        self.player_id = player_id

    def hover(self, mouse_pos: Tuple[int, int]):
        if self.img_rect and self.img_rect.collidepoint(mouse_pos):
            color = self.COLOR_VALID if self.player_id == self.onitama.whose_turn.player_id else self.COLOR_INVALID
            self.img.fill(color, special_flags=BLEND_MULT)
            self.img_rect = self.screen.blit(self.img, self.rect[0:2])
            return True
        return False

    def draw(self):
        self.img = self.style_images.get_image(self.style_name)
        # Rotate image if player1.
        if self.player_id == Pieces.G1:
            self.img = pygame.transform.rotate(self.img, 180)

        # If it is not the current player's style, add a grayed out tint
        if self.player_id != self.onitama.whose_turn.player_id:
            self.img.fill(self.COLOR_GRAYED, special_flags=BLEND_MULT)

        # If this style has been clicked, then set a color on it.
        if self.clicked:
            color = self.COLOR_VALID if self.player_id == self.onitama.whose_turn.player_id else self.COLOR_INVALID
            self.img.fill(color, special_flags=BLEND_MULT)

        self.img_rect = self.screen.blit(self.img, self.rect[0:2])
