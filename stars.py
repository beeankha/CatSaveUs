import pygame
from pygame.sprite import Sprite
from random import randint


class Stars(Sprite):
    """A class to represent stars in the night sky"""

    def __init__(self, ai_game, x=randint(1, 10), y=randint(1, 10)):
        """Initialize the star images."""
        super().__init__()
        self.screen = ai_game.screen

        # Load the star image and set its rect attribute.
        self.image = pygame.image.load('images/star.bmp')
        self.rect = self.image.get_rect()

        self.x = x
        self.y = y
