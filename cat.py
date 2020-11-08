import pygame

class Cat:
    """A class to manage the feline savior."""

    def __init__(self, ai_game):
        """Initialize the cat and set its starting position."""
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()
        # In Pygame, "rect" = rectangles.

        # Load the cat image and get its rect.
        self.image = pygame.image.load('images/cat.png')
        self.rect = self.image.get_rect()

        # Start each new cat at the bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom
        # "midbottom" is one of the shortcut properties you can use to place game
        # elements; alternatively you can use x- and y-coordinates.
        # In Pygame, the origin (0, 0) is at the top-left corner of the screen,
        # and coordinates increase as you go down and to the right.

        # Store a decimal value for the cat's horizontal position.
        self.x = float(self.rect.x)

        # Movement flags
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Update the cat's position based on the movement flags."""
        # Update the cat's x value, not the rect.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.cat_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.cat_speed

        # Update rect object from self.x.
        self.rect.x = self.x

    def blitme(self):
        """Draw the cat at its current location."""
        self.screen.blit(self.image, self.rect)
        # The position is specified by self.rect.

    def center_cat(self):
        """Center the cat on the screen."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
