import pygame
from pygame.locals import (
    BLEND_MULT,
)

from OnitamaGame import OnitamaGame
from typing import Tuple, Union


class Entity:
    """
    An entity to be drawn upon the pygame Screen and rendered onto the GUI.
    """
    # Color constants
    COLOR_INVALID: Tuple[int, int, int, int] = (200, 0, 0, 100)
    COLOR_VALID: Tuple[int, int, int, int] = (0, 200, 0, 100)
    COLOR_GRAYED: Tuple[int, int, int, int] = (100, 100, 100, 100)
    CLICKED_COLOR: Tuple[int, int, int, int] = (0, 200, 0, 100)
    HIGHLIGHTED_COLOR: Tuple[int, int, int, int] = (0, 0, 200, 100)
    width: int
    height: int
    rect: Tuple[int, int]
    onitama: OnitamaGame
    img_rect: Union[None, pygame.Surface]
    img: Union[None, pygame.Surface]
    clicked: bool
    highlighted: bool

    def __init__(self, screen: pygame.Surface, onitama: OnitamaGame, width: int = 100, height: int = 100, offset_x: int = 0, offset_y: int = 0):
        """
        Initialize an entity to be placed on the screen.
        """
        self.screen = screen
        self.onitama = onitama
        self.width = width
        self.height = height
        self.rect = (offset_x,
                     offset_y)
        self.img_rect = None
        self.img = None
        self.clicked = False
        self.highlighted = False

    def hover(self, mouse_pos: Tuple[int, int]):
        """
        Check if the mouse position is hovering over this entity.
        """
        if self.img_rect and self.img_rect.collidepoint(mouse_pos):
            color = self.COLOR_VALID
            self.img.fill(color, special_flags=BLEND_MULT)
            self.img_rect = self.screen.blit(self.img, self.rect)
            return True
        return False

    def set_highlight(self, highlighted):
        """
        Set's this entity as highlighted.
        """
        self.highlighted = highlighted

    def click(self, mouse_pos: Tuple[int, int]):
        """
        Check if this entity has been clicked.
        The clicked attribute will serve as a toggle. 
        Hence, if it is clicked once and then clicked again, 
        then it will untoggle and clicked will be set to false.

        Returns whether it is currently clicked or not.
        """
        self.clicked = self.img_rect and self.img_rect.collidepoint(
            mouse_pos) and not self.clicked
        return self.clicked

    def draw(self):
        """
        Draw this entity on the screen.
        """
        raise NotImplementedError
