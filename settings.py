class Settings:
    """ A class to store all the settings of the Alien Invasion."""
    
    def __init__(self):
        """A class to store all settings for Alien Invasion"""

        ### ---- Screen settings ---- 
        self.screen_width = 1000
        self.screen_height = 800
        self.bg_color = (230,230,230)

        ### ---- Ship settings ----
        # On each pass by default speed was 1 pixel, now it is 1.5 pixel
        # Speed can be in decimal
        self.ship_speed = 1.5
        self.ship_limit = 3

        ### ---- Bullet settings ----
        self.bullet_speed = 1.5 #speed lower than the ship speed
        self.bullet_width = 10
        self.bullet_height = 15
        self.bullet_color = (72,61,139)
        self.bullets_allowed = 3

        ### ---- Alien settings ----
        self.alien_speed = 1.0
        # fleet_drop_speed ; controls how quickly the fleet drops down the screen time when an alien reaches either edge
        # fleet move "down" the screen and "left" when it hits the right edge of the screen
        self.fleet_drop_speed = 70
        # fleet_direction of 1 represents righ; -1 represents left
        # using numbers instead of left-right as then if-elif statements would be used
        self.fleet_direction = 1


        # How quickly the game speeds up
        self.speedup_scale = 1.1

        # how quickly the alien point values increase
        self.score_scale = 1.5
        
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed = 1.5
        self.bullet_speed = 3.0
        self.alien_speed = 1.0

        # fleet_direction - +1 represents right; -1 represents left
        self.fleet_direction = 1

        # Scoring
        self.alien_points = 50

    def increase_speed(self):
        """Increase speed settings and alien point values"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        
        self.alien_points = int(self.alien_points * self.score_scale)
        print(self.alien_points)


