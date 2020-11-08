class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        # ^^ (1200, 800) is a tuple that defines dimensions of game window, in pixels.
        # The object we assigned to self.screen is called a "surface". Each element
        # the game is its own surface.
        self.bg_color = (0, 0, 0)
        # self.bg_color = (104, 130, 158) (greyish blue, aka "Daytime Mode")

        # Ship settings
        self.ship_speed = 3.5

        # Bullet settings
        self.bullet_speed = 5.0
        self.bullet_width = 3
        self.bullet_height = 10
        self.bullet_color = (200, 0, 200)
        self.bullets_allowed = 20