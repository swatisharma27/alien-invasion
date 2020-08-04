import pygame
from pygame.sprite import Sprite


# Bullet class inherits from Sprite class
class Bullet(Sprite): 

    # current instance of AlienInvasion needed to create bullet instance
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # create bullet rect attribute; bullet not based on image so need to build it
        # pygame.Rect() class used, which requires x- and y-coordinates of the top-left corner of rect, the width and the height of the rect.
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        # bullet initialized at (0,0) and then position the bullet's position w.r.t the ship's position
        self.rect.midtop = ai_game.ship.rect.midtop

        # Store the bullet's position as a decimal value
        self.y = float(self.rect.y)

    
    def update(self):
        """Manage the bullet's position."""
        # decreasing y-coordinate
        self.y -= self.settings.bullet_speed

        # speed updated in decimal pixels, but we will use only integer value for controlling bullet value
        # only integer value of updated "self.y" will be stored in bullet's self.rect.y
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw the bullet to the screen."""
        # screen, bullet color, bullet rect attribute
        pygame.draw.rect(self.screen, self.color, self.rect)
