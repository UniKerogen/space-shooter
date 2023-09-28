# Block Element File
# Version 1.0
# Storage for block elements

##################################################
# Libraries
##################################################
from structures import *
from settings import *
import pygame
import random

##################################################
# Player Block
##################################################
# Player Info Storage
player = PlayerBlock(name='player',
                     position=[SCREEN_WIDTH // 2 - PLAYER_SIZE / 2, SCREEN_HEIGHT - 128],
                     image=pygame.image.load('resources/player/player.png'),
                     speed=PLAYER_SPEED,
                     health=100)

##################################################
# Enemy Block
##################################################
# Enemy Image Storage
enemy_img = []
for i in range(ENEMY_TYPE):
    file = 'resources/enemy/enemy' + str(i) + '.png'
    enemy_img.append(pygame.image.load(file))
# Enemy List
enemies = EnemyList()
for num_enemy in range(ENEMY_NUMBER):
    enemies.append(name='enemy' + str(num_enemy),
                   index=num_enemy,
                   position=[random.randint(BOUNDARY_LEFT, BOUNDARY_RIGHT - ENEMY_SIZE),
                             random.randint(ENEMY_SPAWN[0], ENEMY_SPAWN[1])],
                   speed=random.randint(1, ENEMY_SPEED_MAX) / 1000,
                   active=True,
                   image=enemy_img[random.randint(0, ENEMY_TYPE - 1)],
                   health=random.randint(ENEMY_BASE_HEALTH[0], ENEMY_BASE_HEALTH[1]),
                   direction=-1 if random.randint(0, 1) == 0 else 1)

##################################################
# Armory Block
##################################################
BULLET_ORIGIN_X = player.position[0]
BULLET_ORIGIN_Y = player.position[1]
player_armory = Amory()
player_armory.append(name='bullet0',
                     index=0,
                     position=[BULLET_ORIGIN_X, BULLET_ORIGIN_Y],
                     speed=BULLET_SPEED_BASE,
                     exp_range=BULLET_EXPLOSION_RANGE,
                     contact=[[BULLET_ORIGIN_X + 28, BULLET_ORIGIN_Y + 12],
                              [BULLET_ORIGIN_X + 32, BULLET_ORIGIN_Y + 12]],
                     active=True,
                     image=pygame.image.load('resources/player/bullet0.png'),
                     cooldown=[100, 100],
                     damage=50
                     )
player_armory.append(name='bullet1',
                     index=1,
                     position=[BULLET_ORIGIN_X, BULLET_ORIGIN_Y],
                     speed=BULLET_SPEED_BASE,
                     exp_range=BULLET_EXPLOSION_RANGE * 0.8,
                     contact=[[BULLET_ORIGIN_X + 18, BULLET_ORIGIN_Y + 20],
                              [BULLET_ORIGIN_X + 42, BULLET_ORIGIN_Y + 20]],
                     active=False,
                     image=pygame.image.load('resources/player/bullet1.png'),
                     cooldown=[50, 50],
                     damage=20
                     )


##################################################
# Main Function
##################################################
def main():
    print("This is a storage for Block Elements!")


##################################################
# Main Function Runner
##################################################
if __name__ == "__main__":
    main()
