import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    """A class to manage the ship."""

    def __init__(self, ai_game):
        """Initialize the ship and set its starting position"""
        super().__init__()

        # Assign screen to a Ship attribute , so we can access in all the methods in the class
        self.screen = ai_game.screen

        # create settings attribute to use it in ship_update()
        self.settings = ai_game.settings

        # screen converted to a rectangle using "get_rect()"
        self.screen_rect = ai_game.screen.get_rect()

        # loads the ship.bmp image
        self.image = pygame.image.load("images/ship.bmp")
        # converts the image to rectangle
        self.rect = self.image.get_rect()

        """
        ## center - center, centerx, centery
        ## edges - top, bottom, left, right
        ## combine center and edges - midtop, midbottom, midleft, midright
        Origin- (0,0) ; top-center 
        Bottom-right (1200,800) 
        image range --> (0,0) to ((1200, 800) --> variable screen size)
        """
        # Positions the image to bottom center of the screen
        self.rect.midbottom = self.screen_rect.midbottom

        """
        - Adjusting the position of ship by fraction of a pixel, so we assign position to a variable that can store decimal value
        - rect attributes such as x or y are only integer values
        - self.x can hold decimal values
        """
        self.x = float(self.rect.x)

        # Movement Flag of ship
        self.moving_right = False
        self.moving_left = False
    
    def update(self):
        """ Update ship's position based on the movement flag status. """
        if self.moving_right and self.rect.right < self.screen_rect.right:
            # speed adjusted to updated ship speed settings in settings.py
            self.x += self.settings.ship_speed

        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        # speed updated in decimal pixels, but we will use only integer value for controlling ship value
        # only integer value of updated "self.x" will be stored in self.image_rect.x
        self.rect.x = self.x

    def blitme(self):
        """Draw ship at the current location"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Center the ship on the screen"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        