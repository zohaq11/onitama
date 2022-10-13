import pygame
import pygame.freetype
from pygame.locals import (
    BLEND_ADD,
)

from OnitamaGame import OnitamaGame
from Entity import Entity

from typing import Tuple


class Button(Entity):
    """
    A class to represent a button in Pygame.
    """

    def __init__(self, screen: pygame.Surface, onitama: OnitamaGame, offset_x: int, offset_y: int, text: str):
        """
        Initialize this Button.
        """
        super().__init__(screen=screen, onitama=onitama,
                         width=200, height=50,
                         offset_x=offset_x, offset_y=offset_y)
        font = pygame.freetype.SysFont(
            pygame.freetype.get_default_font(), 32)
        self.text = text
        self.text_rect, _ = font.render(
            text, fgcolor=(0, 0, 0))
        self.size = self.text_rect.get_size()
        self.color = (255, 255, 255, 100)
        self.highlighted = False

    def draw_text(self, color: Tuple[int, int, int, int]) -> None:
        """
        Draw the text on the surface of the button.
        """
        self.img = pygame.Surface((self.width, self.height))
        self.img.fill(color, special_flags=BLEND_ADD)
        self.img.blit(self.text_rect, ((self.width -
                                        self.size[0]) // 2, (self.height - self.size[1]) // 2))

        self.img_rect = self.screen.blit(self.img, self.rect)

    def hover(self, mouse_pos: Tuple[int, int]):
        if self.img_rect and self.img_rect.collidepoint(mouse_pos):
            self.draw_text(self.HIGHLIGHTED_COLOR)
            return True
        return False

    def draw(self):
        # Highlight the button green if it iss selected.
        if self.highlighted:
            self.draw_text(self.COLOR_VALID)
        else:
            self.draw_text(self.color)
