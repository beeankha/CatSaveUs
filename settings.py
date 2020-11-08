class Settings:
    """A class to store all settings for "Cat Save Us!" game."""

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

        # Cat settings
        self.cat_speed = 5
        # (the higher the number, the faster the cat)
        self.cat_limit = 3

        # Bullet settings
        self.bullet_speed = 5.0
        self.bullet_width = 8
        self.bullet_height = 12
        self.bullet_color = (200, 0, 200)
        self.bullets_allowed = 20

        # Alien settings
        self.alien_speed = 2
        self.fleet_drop_speed = 10
        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1
