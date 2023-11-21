# Settings File
# Version - Beta 5
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
STANDARD_MOVE_SPEED = 0.1  # Standard Movement Speed
BOUNDARY_MARGIN = 3  # Pixel of Margin for calculation
SPEED_MULTIPLIER = 2  # Speed Adjustment
COOLDOWN_MULTIPLIER = 0.8 # Cooldown Adjustment

# Create
CRATE_SIZE = 40  # Pixel
CRATE_CHANCE = 10  # % of Chance generating crate
CRATE_SUB_CHANCE = [10, 20, 30, 40, 50, 60, 70]  # Each Crate Chance
CRATE_SPEED = 0.1 * SPEED_MULTIPLIER  # Crate Movement Speed
CRATE_HEALTH = (10, 50)  # Crate Health Range
CRATE_SHIELD = (25, 75)  # Crate Shield Range
CRATE_TYPE_AMOUNT = len(CRATE_SUB_CHANCE)  # Total Types of Crate
CRATE_COLLECT_RANGE = 30  # pixel of range for crate collection

# Player Modification
PLAYER_SPEED = 0.5 * SPEED_MULTIPLIER # Player Movement Speed
PLAYER_SIZE = 60  # Player Image Size 50x50 Pixel
PLAYER_HEALTH_BAR = (PLAYER_SIZE, 5, PLAYER_SIZE + 5)  # Width x Height x Shift
PLAYER_INVINCIBLE_TIME = 5  # Player Invincible Time
PLAYER_LIFE = 5  # Player Life Amount
PLAYER_HEALTH = 150  # Player Health
PLAYER_SHIELD_MAX = 300  # Player Max Shield
PLAYER_HIT_RANGE = 0.83  # Player Got Hit Range Multiplier
PLAYER_Y_RANGE = (SCREEN_HEIGHT - 128 - 150, SCREEN_HEIGHT - 128)  # Player Vertical Move Range
WEAPON_TYPE_1_AMOUNT = 4  # Number of Type 1 Weapon for Player
WEAPON_TYPE_2_AMOUNT = 3  # Number of Type 2 Weapon for Player

# Bullet Modification
BULLET_SPEED_BASE = 2 * SPEED_MULTIPLIER  # Bullet Moving Speed
BULLET_TYPE = 6  # Total Number of Player Bullet
BULLET_COOLDOWN_BASE = 100 * COOLDOWN_MULTIPLIER  # Base for bullet cooldown
BULLET_COOLDOWN_MINIMUM = 10 * COOLDOWN_MULTIPLIER # Minimum Cooldown for Bullet
BULLET_SIZE = 50  # Bullet Image Size - Enemy

# Rocket Information
ROCKET_TYPE = 1  # Types of Rocket

# Explosion
EXPLOSION_TIME = 0.5  # second
EXPLOSION_IMAGE_NUMBER = 5  # Number of explosion images

# Enemy Modification
ENEMY_SIZE = 50  # Enemy Image Size 50x50 Pixel
ENEMY_SPEED_MAX = 100 * SPEED_MULTIPLIER  # /1000 -> Max of 0.1
ENEMY_NUMBER = 4  # On Screen Enemy Number
ENEMY_TYPE = 8  # Total Number of Enemy
ENEMY_SPAWN = (200 - ENEMY_SIZE, 300 - ENEMY_SIZE)  # Enemy Spawn Range
ENEMY_BASE_HEALTH = (100, 200)  # Enemy Base Health Range
ENEMY_HEALTH_BAR = (ENEMY_SIZE, 5, -10)  # Enemy Health Bar Width x Height x Shift
ENEMY_HEALTH_BAR_SHIFT = -10  # Distance Between Enemy and Health Bar Display
ENEMY_WEAPON_AMOUNT = 1  # Amount of Weapon Each Enemy Has
ENEMY_WEAPON_TYPE = 5  # Type of Weapon Enemy can use
ENEMY_BULLET_SPEED_BASE = 0.5 * SPEED_MULTIPLIER # Base speed of enemy bullet
ENEMY_BULLET_COOLDOWN_BASE = 2000 * COOLDOWN_MULTIPLIER # Bullet Cooldown for Enemy
ENEMY_HIT_RANGE = 0.8  # Enemy Got Hit Range Multiplier
ENEMY_SHIFT_CHANCE = 35  # % of Chance of Get New Y

# Mini Boss Modification
MINI_BOSS_SIZE = 100  # Pixel
MINI_BOSS_SPEED_MAX = 50 * SPEED_MULTIPLIER  # /100 -> Max of 0.05
MINI_BOSS_SPAWN = (180 - MINI_BOSS_SIZE, 230 - MINI_BOSS_SIZE)  # Mini Boss Spawn Range
MINI_BOSS_TYPE = 4  # Total Number of Types of MiniBoss
MINI_BOSS_HEALTH = (500, 800)  # MiniBoss Health Range
MINI_BOSS_MAX_AMOUNT = 2  # MiniBoss On Screen Amount
MINI_BOSS_WEAPON_AMOUNT = 2  # Amount of Weapon MiniBoss Carry
MINI_BOSS_HEALTH_BAR = (MINI_BOSS_SIZE, 5, -10)  # MiniBoss Health Bar Region WxHxShift
MINI_BOSS_HIT_RANGE = 0.68  # MiniBoss Got Hit Range Multiplier

# Big Boss Modification
BIG_BOSS_SIZE = 200
BIG_BOSS_SPEED_MAX = 20 * SPEED_MULTIPLIER  # /100 -> Max of 0.02
BIG_BOSS_SPAWN = (150 - BIG_BOSS_SIZE, 170 - BIG_BOSS_SIZE)  # Big Boss Spawn Location
BIG_BOSS_TYPE = 2  # Big Boss Type Amount
BIG_BOSS_HEALTH = (1300, 1500)  # Big Boss Health Region
BIG_BOSS_WEAPON_AMOUNT = 3  # Big Boss Weapon Amount
BIG_BOSS_HEALTH_BAR = (BIG_BOSS_SIZE, 5, 50)  # Big Boss Health Bar Region WxHxShift
BIG_BOSS_HIT_RANGE = 0.9  # Big Boss Got Hit Range Multiplier

# Colors
WHITE = (255, 255, 255)  # RGB Value for Color White
RED = (255, 0, 0)  # RGB Value for Color Red
GREEN = (0, 255, 0)  # RGB Value for Color Green
GREY = (213, 213, 213)  # RGB Value for Color Grey
BLACK = (0, 0, 0)  # RGB Value for Color Black

# Button Size
BUTTON_SIZE_INTRO = (100, 50)
BUTTON_SIZE_END = (150, 50)
BUTTON_SIZE_ON_SCREEN = (25, 25)


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
