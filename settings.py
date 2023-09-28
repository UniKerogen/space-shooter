# Settings File
# Version 3.0
# Store settings for game

##################################################
# Variable Definition
##################################################
# Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 800
BOUNDARY_LEFT = 5
BOUNDARY_RIGHT = SCREEN_WIDTH - BOUNDARY_LEFT
# Player Modification
PLAYER_SPEED = 0.5
PLAYER_SIZE = 60  # Player Image Size 50x50 Pixel
# Bullet Modification
AUTO_FIRE = False
BULLET_FIRE = False
BULLET_SPEED_BASE = 1  # Bullet Moving Speed
BULLET_EXPLOSION_RANGE = 25  # Bullet Explosion Range
BULLET_TYPE = 2  # Total Number of Bullet
# Explosion
EXPLOSION_TIME = 0.5  # second
# Enemy Modification
ENEMY_SIZE = 50  # Enemy Image Size 50x50 Pixel
ENEMY_SPEED_MAX = 100  # /1000 -> Max of 0.1
ENEMY_NUMBER = 5  # On Screen Enemy Number
ENEMY_TYPE = 3  # Total Number of Enemy
ENEMY_SPAWN = (50, 250)  # Enemy Spawn Range
# Boss Modification
BOSS_SIZE = 100
BOSS_SPEED_MAX = 50  # /100 -> Max of 0.05
BOSS_SPAWN = (30, 50)  # Boss Spawn Range
# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)


##################################################
# Main Function
##################################################
def main():
    print("This is the setting file.")


##################################################
# Main Function Runner
##################################################
if __name__ == "__main__":
    main()
