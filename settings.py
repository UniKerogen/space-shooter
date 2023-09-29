# Settings File
# Version - Alpha 6.5
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
# Enemy Modification
ENEMY_SIZE = 50  # Enemy Image Size 50x50 Pixel
ENEMY_SPEED_MAX = 100  # /1000 -> Max of 0.1
ENEMY_NUMBER = 3  # On Screen Enemy Number
ENEMY_TYPE = 3  # Total Number of Enemy
ENEMY_SPAWN = (50, 250)  # Enemy Spawn Range
ENEMY_BASE_HEALTH = (80, 150)  # Enemy Base Health Range
ENEMY_HEALTH_BAR = (ENEMY_SIZE, 5)  # Enemy Health Bar Width x Height
ENEMY_HEALTH_BAR_SHIFT = -10  # Distance Between Enemy and Health Bar Display
ENEMY_WEAPON_TYPE = 2  # Type of Weapon Enemy can use
ENEMY_BULLET_SPEED_BASE = 0.5  # Base speed of enemy bullet
ENEMY_BULLET_COOLDOWN_BASE = 1500  # Bullet Cooldown for Enemy
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
