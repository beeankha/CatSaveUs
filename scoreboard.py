import pygame.font

from pygame.sprite import Group
from cat import CatFace


class Scoreboard:
    """A class to report scoring information."""

    def __init__(self, ai_game):
        """Initialize scorekeeping attributes."""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # We give __init__() the ai_game parameter here so that it can access
        # the settings, screen, and stats objects, which it will need to report
        # the values we’re tracking

        # Font settings for scoring information.
        self.text_color = (0, 200, 100)
        self.font = pygame.font.SysFont(None, 48)

        # Prepare the initial score images.
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_cats()

    def prep_score(self):
        """Turn the score into a rendered image."""
        rounded_score = round(self.stats.score, -1)
        # ^^ The above rounds the score to multiples of 10
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)

        # Display the score at the top right of the screen.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20
        # ^^ To make sure the score always lines up with the right side of the screen,
        # there is a rect called score_rect and its right edge is set 20 pixels from
        # the right edge of the screen. We then place the top edge 20 pixels down
        # from the top of the screen.

    def prep_high_score(self):
        """Turn the high score into a rendered image."""
        high_score = round(self.stats.high_score, -1)

        f = open('high_score.txt', 'r')
        file = f.readlines()
        all_time_high_score = int(file[0])

        high_score_str = "High Score: {:,}".format(all_time_high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.settings.bg_color)

        # Center the all-time high score at the top of the screen.
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

        if all_time_high_score < int(high_score):
            f.close()
            file = open('high_score.txt', 'w')
            file.write(str(high_score))
            file.close()
            return high_score
        return all_time_high_score

    def show_score(self):
        """Draw scores, level, and cats to the screen."""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.cats.draw(self.screen)

    def check_high_score(self):
        """Check to see if there's a new high score."""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def prep_level(self):
        """Turn the level into a rendered image."""
        level_str = str(self.stats.level)
        current_level = "Level: {}".format(level_str)
        self.level_image = self.font.render(current_level, True, self.text_color, self.settings.bg_color)

        # Position the level below the score.
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_cats(self):
        """Show how many cat lives are left."""
        self.cats = Group()
        for cat_number in range(self.stats.cats_left):
            cat = CatFace(self.ai_game)
            cat.rect.x = 10 + cat_number * cat.rect.width
            cat.rect.y = 10
            self.cats.add(cat)
