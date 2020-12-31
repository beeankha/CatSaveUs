import pygame
import sys

from random import randint
from time import sleep

from alien import Alien
from bullet import Bullet, ShockWave
from button import Button
from cat import Cat
from game_stats import GameStats
from scoreboard import Scoreboard
from settings import Settings
from stars import Stars


class CatSaveUs:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.settings = Settings()

        (width, height) = (self.settings.screen_width, self.settings.screen_height)
        self.screen = pygame.display.set_mode((width, height))
        # (the pygame method get_rect() returns a Rect object from an image)
        pygame.display.set_caption("Cat Save Us!")

        # Create an instance to store game stats and create a scoreboard.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.cat = Cat(self)
        # ^^ The self argument here refers to the current instance of CatSaveUs.
        self.cat_face = Cat(self)

        self.bullets = pygame.sprite.Group()
        self.shock_waves = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.stars = pygame.sprite.Group()

        self._create_starry_sky()
        self._create_fleet()

        # Make the Play button.
        self.play_button = Button(self, "Double Click to Play")

        bg_music = 'sounds/BuzzsawsOnMercury.wav'
        pygame.mixer.init()
        pygame.mixer.music.load(bg_music)
        pygame.mixer.music.play(-1)  # the loop of -1 means this song will repeate indefinitely


    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()  # ??????
            # ^^ The above calls a helper method!

            if self.stats.game_active:
                self.cat.update()
                # ^^ The cat's position will be updated after checking for keyboard events!
                self._update_bullets()
                self._update_shock_waves()
                self._update_aliens()

            self._update_screen()
            # ^^ Same here!

    def _create_starry_sky(self):
        """Instantiate a sky full of stars for the game's background."""

        # Make a star.
        star = Stars(self)
        star_width, star_height = star.rect.size
        available_space_stars_x = self.settings.screen_width - (star_width)
        number_stars_x = available_space_stars_x // (star_width)

        # Determine the number of rows of stars that fit on the screen.
        available_space_stars_y = (self.settings.screen_height - (star_height))
        star_number_rows = available_space_stars_y // (star_height)

        # Create the full sky of stars.
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

    def _update_shock_waves(self):
        """Update position of the shockwave and get rid of old shockwaves."""
        # Update shockwave positions.
        self.shock_waves.update()
        # ^^ Updates the position of the bullets on each pass through

        # Get rid of shockwaves that have disappeared.
        for shock_wave in self.shock_waves.copy():
            if shock_wave.rect.bottom <= 0:
                self.shock_waves.remove(shock_wave)

        self._check_shock_wave_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        # Remove any bullets and aliens that have collided.
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        # ^^ The sprite.groupcollide() function compares the rects of each element
        # in one group with the rects of each element in another group.
        collision_sound = pygame.mixer.Sound('sounds/AlienShipCrash.wav')
        collision_sound.set_volume(0.3)

        if collisions:
            pygame.mixer.Sound.play(collision_sound)
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            # Destroy existing bullets and create a new fleet.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Increase level.
            self.stats.level += 1
            self.sb.prep_level()

    def _check_shock_wave_alien_collisions(self):
        """Respond to shockwave-alien collisions."""
        # Remove any bullets and aliens that have collided.
        shock_wave_collisions = pygame.sprite.groupcollide(self.shock_waves, self.aliens, False, True)
        # ^^ The sprite.groupcollide() function compares the rects of each element
        # in one group with the rects of each element in another group.
        shockwave_sound = pygame.mixer.Sound('sounds/ShockWaveHit.wav')
        shockwave_sound.set_volume(0.4)

        if shock_wave_collisions:
            pygame.mixer.Sound.play(shockwave_sound)
            for aliens in shock_wave_collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

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
        cat_hit_sound = pygame.mixer.Sound('sounds/CatHit.wav')
        game_over_sound = pygame.mixer.Sound('sounds/GameOver.wav')
        last_cat_sound = pygame.mixer.Sound('sounds/CatMeow.wav')

        if self.stats.cats_left > 0:
            pygame.mixer.Sound.play(cat_hit_sound)

            # Decrement cats_left, and update scoreboard.
            self.stats.cats_left -= 1
            self.sb.prep_cats()

            # Get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()
            self.shock_waves.empty()

            # Create a new fleet and center the cat.
            self._create_fleet()
            self.cat.center_cat()

            # Pause.
            sleep(1)
        else:
            pygame.mixer.Sound.play(game_over_sound)
            pygame.mixer.Sound.play(last_cat_sound)
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

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
                self._check_keydown_events(event)  # ??????
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.stats.game_active is True:
                    pass
                else:
                    mouse_pos = pygame.mouse.get_pos()
                    self._check_play_button(mouse_pos)

    def pause(self):
        paused = True
        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        paused = False
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        quit()

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Reset the game settings.
            self.settings.initialize_dynamic_settings()
            # Reset the game statistics.
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_cats()

            # Hide the mouse cursor.
            pygame.mouse.set_visible(False)

        # Get rid of any remaining aliens and bullets.
        self.aliens.empty()
        self.bullets.empty()
        self.shock_waves.empty()

        # Create a new fleet and center the cat.
        self._create_fleet()
        self.cat.center_cat()

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:
            self.cat.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.cat.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_p:
            self.pause()
            self.pause_button = Button(self, "Paused\nPress C to continue or Q to quit.")
            pygame.display.update()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_LSHIFT:
            self._fire_shock_wave()

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.cat.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.cat.moving_left = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        cat_bullet_sound = pygame.mixer.Sound('sounds/CatBullet.wav')
        cat_bullet_sound.set_volume(0.5)

        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            pygame.mixer.Sound.play(cat_bullet_sound)
            self.bullets.add(new_bullet)

    def _fire_shock_wave(self):
        """Create a new shockwave and add it to the shockwaves group."""
        cat_shockwave_sound = pygame.mixer.Sound('sounds/EmitShockwave.wav')
        cat_shockwave_sound.set_volume(0.5)

        if len(self.shock_waves) < self.settings.shock_waves_allowed:
            new_shock_wave = ShockWave(self)
            pygame.mixer.Sound.play(cat_shockwave_sound)
            self.shock_waves.add(new_shock_wave)

    def _create_fleet(self):
        """Create the fleet of aliens."""
        # Make an alien.
        alien = Alien(self)

        # Create an alien and find the number of aliens in a row.
        # Spacing between each alien is equal to one alien width.
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # Determine the number of rows of aliens that fit on the screen.
        cat_height = self.cat.rect.height
        available_space_y = (self.settings.screen_height -
                                (2 * alien_height) - cat_height)
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
        for shock_wave in self.shock_waves.sprites():
            shock_wave.draw_shock_wave()
        self.aliens.draw(self.screen)

        # Draw the score information.
        self.sb.show_score()
        self.sb.prep_high_score()
        # Draw the play button if the game is inactive.
        if not self.stats.game_active:
            self.play_button.draw_button()

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
