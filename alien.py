import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """A class to represent a single alien in the fleet."""

    def __init__(self, ai_game):
        """Initialize the alien and set its starting position"""
        super().__init__()

        # Assign screen to a Alien class attribute , so we can access in all the methods in the class
        self.screen = ai_game.screen
        # create settings attribute to use it in alien_update()
        self.settings = ai_game.settings

        self.image = pygame.image.load("images/alien.bmp")
        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen
        # Add a space to left of it that's equal to the alien's width and a space  above it equal to its height
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact horizontal position - as we are mainly concerned about horizontal position
        self.x = float(self.rect.x)

    def check_edges(self):
        """Return True if the alien is at the edge of the screen
        - Alien at right edge : when the right attribute of the alien is greater or equal to right attribute of screen
        - Alien at left edge : when the left attribute of the alien is greater than or equal to zero 
        """
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True


    def update(self):
        """
        Move the alien to the right or left
        
        fleet_direction = 1; value of alien_speed will be added to the alien's current position - moving right
        fleet_direction = -1; value of alien_speed will be subtarcted from the aliens's position - moving left
        """
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x
