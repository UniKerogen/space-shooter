# Settings File
# Version 1.0
# Store settings for game

# Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 800
# Player Modification
PLAYER_SPEED = 0.5
PLAYER_SIZE = 60  # Player Image Size 50x50 Pixel
# Bullet Modification
BULLET_SPEED_BASE = 0.8  # Bullet Moving Speed
BULLET_EXPLOSION_RANGE = 30  # Bullet Explosion Range
BULLET_TYPE = 2  # Total Number of Bullet
# Enemy Modification
ENEMY_SIZE = 50  # Enemy Image Size 50x50 Pixel
ENEMY_SPEED_MAX = 100  # /1000 -> Max of 0.1
ENEMY_NUMBER = 5  # On Screen Enemy Number
ENEMY_TYPE = 2  # Total Number of Enemy
ENEMY_SPAWN = (50, 200)
# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

def main():
    print("This is the setting file.")

if __name__ == "__main__":
    main()
