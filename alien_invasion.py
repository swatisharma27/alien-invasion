import sys
import pygame

from time import sleep
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien
from pygame.locals import *

# pylint: disable=no-member
class AlienInvasion:
    def __init__(self):
         # initialize the backgroud settings
        pygame.init()
        
        #2 instance of class Settings 
        self.settings = Settings()

        # sets the dimensions of the game window, to draw graphical elements
        # pygame.display.set_mode is a "surface"
        """
        --- Normal Screen ---
                self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height)) #pass a tuple value -- (width, height)

        --- Full Screen ---
                #tells Pygame to figure out window size that will fill the screen
                self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN) 

                # doesn't know the height and width ahead of time, so update the settings after screen is created
                # width and height attritubes of the screen rect's to update settings object
                self.settings.screen_width = self.screen.get_rect().width
                self.settings.screen_height = self.screen.get_rect().height
        """
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height)) #pass a tuple value -- (width, height)

        #10 Instance to store game statistics
        self.stats = GameStats(self)

        #3 instance of class Ship after screen has been created
        """Ship() needs one argument, an instance of AlienInvasion. "self" here refers to the current instance of the class AlienInvasion."""
        self.ship = Ship(self)
        
        #6 create a group to store all live bullets, so we can manage bullets already been fired
        """- The group will be an instance of pygame.spirite.Group class, which behaves as a list with extra functionality
           - Group is used to draw bullets to screen on each pass through the main loop and to update each bullet's position"""
        self.bullets = pygame.sprite.Group()

        #7 
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

        self.play_button = Button(self, "Play")

        # Sets the caption of the game
        pygame.display.set_caption("ALIEN INVASION")

        # Create an instance to store game statistics and create a scoreboard
        self.sb = Scoreboard(self)

    def _check_events(self):
        """ Manage the events in the game.
                # pygame.event.get() returns a list of events that has occured since the last time "run_game()" function has been called
                # event loop - consist of series of events like: 1) moving the mouse 2) pressing a key
        """
        # Main event loop for the game and code 
        for event in pygame.event.get(): 
            # series of if statements to "detect" and "respond" to events
            
            # Event 1: game window close button (detection)
            if event.type == pygame.QUIT:  
                sys.exit() # exit the game (response)
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

            #4 Event 2:  move the ship to right or left - key press release
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)

            #4 Event 3: key release response       
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_play_button(self, mouse_pos):
        """Begin a new game when the player click Play"""

        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Reset the game statistics
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            # Hide the mouse cursor
            pygame.mouse.set_visible(False)

            # Get rid of any remaining aliens and bullets
            self.aliens.empty()

            self.bullets.empty()

            # Create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()
             
            
    def _check_keydown_events(self, event):
        """Respond to keypress."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        #5 Pressing q to quit the game
        elif event.key == pygame.K_q:
            sys.exit()
        #6 Pressing spacebar to fire bullets
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    #6
    def _fire_bullet(self): 
        """Create a new bullet and add to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            # instance of bullet class, using the current instance of AlienInvasion class
            new_bullet = Bullet(self)
            # add the new_bullets to the bullets group, similar to "append" method but "add" is for pygame
            self.bullets.add(new_bullet) 
    
    #7
    def _create_fleet(self):
        """Create the fleet of aliens."""
        alien = Alien(self)
        # Using attribute 'size', contains tuple of width and height of a rect object
        alien_width, alien_height = alien.rect.size
        # Total available space = Screen width - left of 1st alien - right of last alien
        available_space_x = self.settings.screen_width - (2 * alien_width)
        # Number of aliens = Total space// 2*alien_width; 
        # alien width twice as one will be alien and next would be space before next alien is shown
        number_aliens_x = available_space_x // (2 * alien_width)

        # Determine number of rows of aliens that fit on the screen
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        for row_number in range(number_rows):
            for alien_num in range(number_aliens_x):
                self._create_alien(alien_num, row_number)

    #7 
    def _create_alien(self, alien_num, row_number):
        """Create alien and place it in a row."""
        alien = Alien(self)
        # Extracted alien's width from alien's rect attribute and stored in a variable
        alien_width, alien_height = alien.rect.size
        # x- coordinate used to place the aliens in a row
        # Each alien pushed to right one alien width from left margin
        alien.x = alien_width + 2 * alien_width * alien_num
        alien.rect.x = alien.x
        
        alien.y = alien_height + 2 * alien_height * row_number
        alien.rect.y = alien.y
        
        # each new alien gets added to group alien
        self.aliens.add(alien)

    #9 Dropping Fleet and Changing Direction
    def _check_fleet_edges(self):
        """Respond appropriately if any alien have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    #9
    def _change_fleet_direction(self):
        """Drop the entire fleet and change direction.
        
        We loop through all the aliens and drop each one using setting fleet_drop_speed;
        then change value of fleet_directiom by multiplying its current value by -1.
        """
        # aliens dropped to fleet_drop_speed
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        # line to change the fleet direction - we change the fleet direction just once
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        """ Update the screen in the game"""
        #2 Redraw the screen during each pass
        self.screen.fill(self.settings.bg_color)

        #3 After filling the background, we draw the ship on the screen
        self.ship.blitme()

        #6 To make sure each bullet is drawn to the screen before we call flip()
        # bullets.sprites() returns a list of all sprites in the bullets group
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        #7
        self.aliens.draw(self.screen)   

        # Draw the score information
        self.sb.show_score() 

        # Draw the play button if the game is inactive
        if not self.stats.game_active:
            self.play_button.draw_button()

        pygame.display.flip()


    def _update_bullets(self):
        """Updates the position of bullets and get rid of old bullets."""

        #group automatically calls the update() for each sprite in the group.
        self.bullets.update()

        #6 Get rid of bullets that have disappeared at the top
        # we can't remove the items from a list of group within a for loop, so we loop over "copy of the group"
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions, and repopulate the fleet"""

        # check for any bullets that have hit the aliens
        # If so, get rid of the bullet as well as alien
        """ sprite.groupcollide() - compares the rects of each element in one group with the rects of another element;
        - Here, it compares each bullet's rect with each alien's rect and returns a dictionary with keys as bullets and 
        corresponding alien hit will be value in dictionary.
        - Whenever the rects of aliens or bullets overlap, groupcollide() adds a key-value pair to the dictionary it returns.
        - The two "True" argument tell Pygame to delete the bullets and aliens that have collided.
        - High powered bullet, set 1st boolean False and second True, the bullet will only disappear only after it reached the top
        of the screen.
        """
        #Remove any bullets and aliens that have collided.
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)   

        if collisions:
            self.stats.score += self.settings.alien_points
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            # Destroy existing bullets and create new fleet
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Increase level
            self.stats.level += 1
            self.sb.prep_level()

    #10 
    def _ship_hit(self):
        """Acknowledge the ship hit by the alien"""
        
        if self.stats.ships_left > 0:
            # Decrement ships left, and update scoreboard.
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # Clean the screen, remove remaining aliens & bullets
            self.aliens.empty()
            self.bullets.empty()

            # Make the new fleet and place the ship in the center
            self._create_fleet()
            self.ship.center_ship()

            # pause the game
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)
    
    #11
    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    #8
    def _update_aliens(self):  
        """
        Check if the fleet is at edge, Update the positions of all aliens in the fleet.
        """
        #9
        self._check_fleet_edges()
        #8
        self.aliens.update()

        #Look for alien-ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            print("Ship hit!!")
            self._ship_hit()

        # Look for the aliens hitting the bottom of the screen
        self._check_aliens_bottom()

    def run_game(self):
        while True: 
            self._check_events()

            if self.stats.game_active:
                #4 Update ship movement
                self.ship.update()
    
                #6 Update bullet movement
                self._update_bullets()

                #7 Update the aliens movement
                self._update_aliens()

            # Update position to draw a new screenx
            self._update_screen()

            # Makes the most recently drawn screen visible; creates illusion as it closes old windows and shows most recent
            pygame.display.flip() 

if __name__ == '__main__':
    ai = AlienInvasion() 
    ai.run_game()
