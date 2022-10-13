import pygame

from ImageGenerator import ImageGenerator


class Pieces(ImageGenerator):
    """
    A class which contains constants for piece representations.
    Also returns images to represent each piece.

    === Attributes ===
    M1: Characters is an identifier for monk for player 1
    M2: Characters is an identifier for monk for player 2
    G1: Characters is an identifier for grandmaster for player 1
    G2: Characters is an identifier for grandmaster for player 2

    === Private Attributes ===
    _BLACK: DON'T WORRY ABOUT IT! (ITALIAN ACCENT)
    _WHITE: DON'T WORRY ABOUT IT! (ITALIAN ACCENT)

    """
    _BLACK: str = 'black'
    _WHITE: str = 'white'
    M1: str = 'x'
    M2: str = 'y'
    G1: str = 'X'
    G2: str = 'Y'
    EMPTY: str = ' '

    def __init__(self, pygame: pygame, width: int, height: int) -> None:
        """
        Initialize all of the pygame images based on the images in the assets folder.
        """
        super().__init__(pygame)
        images = {
            self._BLACK:  'black',
            self._WHITE:  'white',
            self.M1: 'b_monk',
            self.M2: 'w_monk',
            self.G1: 'michael_gm',
            self.G2: 'ilir_gm'
        }
        self.add_images(images)
        self.scale_images(width, height)

    def get_image(self, piece: str, i: int = -1, j: int = -1) -> pygame.Surface:
        """
        Returns the pygame image based on the piece and coordinate of the piece.
        """
        if piece == self.EMPTY:
            # Black
            if i % 2 == j % 2:
                piece = self._BLACK
            else:
                piece = self._WHITE
        return self.images.get(piece, self._WHITE).copy()
