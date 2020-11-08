import pygame
import sys

from random import randint
from time import sleep

from alien import Alien
from bullet import Bullet
from cat import Cat
from game_stats import GameStats
from settings import Settings
from stars import Stars


class CatSaveUs:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        # (the pygame method get_rect() returns a Rect object from an image)
        pygame.display.set_caption("Cat Save Us!")

        # Create an instance to store game stats.
        self.stats = GameStats(self)

        self.cat = Cat(self)
        # ^^ The self argument here refers to the current instance of CatSaveUs.

        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.stars = pygame.sprite.Group()

        self._create_starry_sky()
        self._create_fleet()

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            # ^^ The above calls a helper method!

            if self.stats.game_active:
                self.cat.update()
                # ^^ The cat's position will be updated after checking for keyboard events!
                self._update_bullets()
                self._update_aliens()

            self._update_screen()
            # ^^ Same here!

    def _create_starry_sky(self):
        """Instantiate a sky full of stars for the game's background."""

        random_number = randint(1, 10)

        # Make a star.
        star = Stars(self)
        star_width, star_height = star.rect.size
        available_space_stars_x = self.settings.screen_width - (star_width)
        number_stars_x = available_space_stars_x // (star_width)

        # Determine the number of rows of stars that fit on the screen.
        available_space_stars_y = (self.settings.screen_height - (star_height))
        star_number_rows = available_space_stars_y // (star_height)

        # Create the full sky of randomly placed stars.

        for star_row_number in range(star_number_rows):
            for star_number in range(number_stars_x):
                self._create_stars(star_number, star_row_number)

    def _create_stars(self, star_number, star_row_number):
        star = Stars(self)
        random_range = randint(-10, 10)
        random_number = randint(1, 10)

        # star_width, star_height = star.rect.size
        star.rect.x = random_range + random_number * star.rect.width * star_number
        star.rect.y = random_range + random_number * star.rect.height * star_row_number
        self.stars.add(star)

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions.
        self.bullets.update()
        # ^^ Updates the position of the bullets on each pass through

        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        # Remove any bullets and aliens that have collided.
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        # ^^ The sprite.groupcollide() function compares the rects of each element
        # in one group with the rects of each element in another group.

        # To make a high-powered bullet that can travel to the top of the screen,
        # destroying every alien in its path, you could set the first Boolean
        # argument to False and keep the second Boolean argument set to True.
        # The aliens hit would disappear, but all bullets would stay active until
        # they disappeared off the top of the screen.

        if not self.aliens:
            # Destroy existing bullets and create a new fleet.
            self.bullets.empty()
            self._create_fleet()

    def _update_aliens(self):
        """
        Check if the fleet is at an edge, then update the
        positions of all aliens in the fleet.
        """
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien-cat collisions.
        if pygame.sprite.spritecollideany(self.cat, self.aliens):
            self._cat_hit()

        # Look for aliens hitting the bottom of the screen.
        self._check_aliens_bottom()

    def _cat_hit(self):
        """Respond to the cat being hit by an alien ship."""
        if self.stats.cats_left > 0:
            # Decrement cats_left.
            self.stats.cats_left -= 1

            # Get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and center the cat.
            self._create_fleet()
            self.cat.center_cat()

            # Pause.
            sleep(1)
        else:
            self.stats.game_active = False

    def _check_events(self):
        # This is a helper method, for refactoring practice!!
        # Helper methods are indicated via the single starting "_".
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            # pygame.event.get() will access events that Pygame detects.
            # This function returns a list of events that have taken place
            # since the last time this function was called.
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:
            self.cat.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.cat.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        # TODO (implement a superbullet feature!)

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.cat.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.cat.moving_left = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _create_fleet(self):
        """Create the fleet of aliens."""
        # Make an alien.
        alien = Alien(self)

        # Create an alien and find the number of aliens in a row.
        # Spacing between each alien is equal to one alien width.
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # Determine the number of rows of aliens that fit on the screen.
        cat_height = self.cat.rect.height
        available_space_y = (self.settings.screen_height -
                                (3 * alien_height) - cat_height)
        number_rows = available_space_y // (2 * alien_height)

        # Create the full fleet of aliens.
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        # Create an alien and place it in the row.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat this the same as if the cat (player) got hit.
                self._cat_hit()
                break

    def _update_screen(self):
        """Update images on the screen, and flip to a new screen."""
        # Set the background color.
        # Redraw the screen during each pass through the loop.
        self.screen.fill(self.settings.bg_color)
        # ^^ Here we fill the screen with the background color using the fill()
        # method, which acts on a surface and takes only one argument: a color.
        self.stars.draw(self.screen)
        self.cat.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # Make the most recently drawn screen visible.
        pygame.display.flip()
        # ^^ When we move the game elements around, pygame.display.flip() continually
        # updates the display to show the new positions of game elements and hides
        # the old ones, creating the illusion of smooth movement.


if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = CatSaveUs()
    ai.run_game()
    # ^^ Here we create an instance of the game, and then call run_game(). We place run_game()
    # in an if block that only runs if the file is called directly.
