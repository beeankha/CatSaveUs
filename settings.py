import pygame

class Settings:
    """A class to store all settings for "Cat Save Us!" game."""

    def __init__(self):
        """Initialize the game's static settings."""
        # Screen settings
        self.screen_width = 1350
        self.screen_height = 800
        # ^^ (1200, 800) is a tuple that defines dimensions of game window, in pixels.
        # The object we assigned to self.screen is called a "surface". Each element
        # the game is its own surface.
        self.bg_color = (0, 0, 0)
        # self.bg_color = (104, 130, 158) (greyish blue, aka "Daytime Mode")

        # Cat settings
        self.cat_limit = 3

        # Bullet settings
        self.bullet_width = 8
        self.bullet_height = 20
        self.bullet_color = (200, 0, 200)
        self.bullets_allowed = 20

        # Shockwave settings
        self.shock_wave_width = 300
        self.shock_wave_height = 12
        self.shock_wave_color = (255, 0, 0)
        self.shock_waves_allowed = 1

        # Alien settings
        self.fleet_drop_speed = 10

        # How quickly the game speeds up
        self.speedup_scale = 1.2

        # How quickly the alien point values increase
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.cat_speed = 5
        # (the higher the number, the faster the cat)
        self.bullet_speed = 5.0
        self.shock_wave_speed = 1.5
        self.alien_speed = 2

        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1

        # Scoring
        self.alien_points = 50

    def increase_speed(self):
        """Increase speed settings and alien point values."""
        self.cat_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
