import pygame
from typing import Dict


class ImageGenerator:
    """
    A class which is responsible for generating pygame images. 
    """
    EMPTY: str = ' '
    img_dir = './assets/img'
    # Contains the image mapping for each piece
    images: Dict[str, pygame.Surface]

    def __init__(self, pygame: pygame) -> None:
        """
        Initialize the pygame image for EMPTY which is the default return value for get_image.
        """
        self.images = {
            self.EMPTY:  pygame.image.load(f'{self.img_dir}/space.png').convert(),
        }

    def add_images(self, images: Dict[str, str]) -> None:
        """
        Generate and add images based on their key and filenames.
        """
        for key, filename in images.items():
            self.images[key] = pygame.image.load(
                f'{self.img_dir}/{filename}.png').convert()

    def scale_images(self, width: int, height: int) -> None:
        """
        Scale all of the images with the given width and height.
        """
        # Scale the images
        for key in self.images:
            self.images[key] = pygame.transform.smoothscale(
                self.images[key], (width, height))

    def get_image(self, key: str) -> pygame.Surface:
        """
        Returns the pygame image based on the key.
        """
        return self.images.get(key, self.EMPTY).copy()
