import pygame

from ImageGenerator import ImageGenerator


class StyleImages(ImageGenerator):
    """
    A class which contains constants for style images.
    """
    CRAB: str = 'crab'
    DRAGON: str = 'dragon'
    HORSE: str = 'horse'
    MANTIS: str = 'mantis'
    ROOSTER: str = 'rooster'

    def __init__(self, pygame: pygame, width: int, height: int) -> None:
        """
        Initialize all of the pygame images based on the images in the assets folder.
        """
        super().__init__(pygame)
        images = {
            self.CRAB:  'crab',
            self.DRAGON: 'dragon',
            self.HORSE: 'horse',
            self.MANTIS: 'mantis',
            self.ROOSTER: 'rooster'
        }
        self.add_images(images)
        self.scale_images(width, height)
