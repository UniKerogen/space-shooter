# Settings File
# Version - Alpha 6.6
# Store settings for game

##################################################
# Variable Definition
##################################################
# Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 800
BOUNDARY_LEFT = 5
BOUNDARY_RIGHT = SCREEN_WIDTH - BOUNDARY_LEFT
BACKGROUND_SCROLL_SPEED = 1  # Pixel
BACKGROUND_REFRESH_TIME = 0.1  # Second
STANDARD_MOVE_SPEED = 0.5
# Player Modification
PLAYER_SPEED = 0.5
PLAYER_SIZE = 60  # Player Image Size 50x50 Pixel
PLAYER_HEALTH_BAR = (PLAYER_SIZE, 5)
PLAYER_HEALTH_BAR_SHIFT = PLAYER_SIZE + 5
PLAYER_INVINCIBLE_TIME = 5
# Bullet Modification
BULLET_SPEED_BASE = 2  # Bullet Moving Speed
BULLET_EXPLOSION_RANGE = 25  # Bullet Explosion Range
BULLET_TYPE = 2  # Total Number of Bullet
BULLET_COOLDOWN_BASE = 100  # Base for bullet cooldown
# Explosion
EXPLOSION_TIME = 0.5  # second
EXPLOSION_IMAGE_NUMBER = 1  # Number of explosion images
# Enemy Modification
ENEMY_SIZE = 50  # Enemy Image Size 50x50 Pixel
ENEMY_SPEED_MAX = 100  # /1000 -> Max of 0.1
ENEMY_NUMBER = 3  # On Screen Enemy Number
ENEMY_TYPE = 3  # Total Number of Enemy
ENEMY_SPAWN = (125 - ENEMY_SIZE, 300 - ENEMY_SIZE)  # Enemy Spawn Range
ENEMY_BASE_HEALTH = (80, 150)  # Enemy Base Health Range
ENEMY_HEALTH_BAR = (ENEMY_SIZE, 5, -10)  # Enemy Health Bar Width x Height x Shift
ENEMY_HEALTH_BAR_SHIFT = -10  # Distance Between Enemy and Health Bar Display
ENEMY_WEAPON_TYPE = 2  # Type of Weapon Enemy can use
ENEMY_BULLET_SPEED_BASE = 0.5  # Base speed of enemy bullet
ENEMY_BULLET_COOLDOWN_BASE = 1500  # Bullet Cooldown for Enemy
# Mini Boss Modification
MINI_BOSS_SIZE = 100
MINI_BOSS_SPEED_MAX = 50  # /100 -> Max of 0.05
MINI_BOSS_Y_AXIS = (150 - MINI_BOSS_SIZE, 200 - MINI_BOSS_SIZE)  # Mini Boss Spawn Range
MINI_BOSS_TYPE = 1
MINI_BOSS_HEALTH = (350, 500)
MINI_BOSS_MAX_AMOUNT = 2
MINI_BOSS_WEAPON_AMOUNT = 2
MINI_BOSS_HEALTH_BAR = (MINI_BOSS_SIZE, 5, -10)
# Big Boss Modification
BIG_BOSS_SIZE = 200
BIG_BOSS_SPEED_MAX = 20  #/100 -> Max of 0.02
BIG_BOSS_SPAWN = (0 - BIG_BOSS_SIZE, 50 - BIG_BOSS_SIZE)
BIG_BOSS_TYPE = 1
BIG_BOSS_HEALTH = (800, 1000)
BIG_BOSS_WEAPON_AMOUNT = 3

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)


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