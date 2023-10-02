# Block Element File
# Version - Alpha 6.5
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
# Player Armory Block
##################################################
BULLET_ORIGIN_X = player.position[0]
BULLET_ORIGIN_Y = player.position[1]
player_armory = Armory()
player_armory.append(name='bullet0',
                     index=0,
                     position=[BULLET_ORIGIN_X, BULLET_ORIGIN_Y],
                     speed=BULLET_SPEED_BASE,
                     exp_range=BULLET_EXPLOSION_RANGE,
                     contact=[[BULLET_ORIGIN_X + 28, BULLET_ORIGIN_Y],
                              [BULLET_ORIGIN_X + 32, BULLET_ORIGIN_Y]],
                     active=True,
                     image=pygame.image.load('resources/player/bullet0.png'),
                     cooldown=[BULLET_COOLDOWN_BASE, BULLET_COOLDOWN_BASE],
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
                     cooldown=[BULLET_COOLDOWN_BASE * 0.5, BULLET_COOLDOWN_BASE * 0.5],
                     damage=20
                     )

##################################################
# Enemy Block
##################################################
# Enemy List
enemies = EnemyList()
for num_enemy in range(ENEMY_NUMBER):
    enemies.append(name='enemy' + str(num_enemy),
                   index=num_enemy,
                   position=[random.randint(BOUNDARY_LEFT, BOUNDARY_RIGHT - ENEMY_SIZE),
                             random.randint(ENEMY_SPAWN[0], ENEMY_SPAWN[1])],
                   speed=random.randint(1, ENEMY_SPEED_MAX) / 1000,
                   active=True,
                   image=pygame.image.load('resources/enemy/enemy' + str(random.randint(0, ENEMY_TYPE - 1)) + '.png'),
                   health=random.randint(ENEMY_BASE_HEALTH[0], ENEMY_BASE_HEALTH[1]),
                   direction=-1 if random.randint(0, 1) == 0 else 1,
                   weapon=random.randint(0, ENEMY_WEAPON_TYPE - 1))


def enemy_reset(enemy_block):
    # Reset Enemy Information
    enemy_block.direction = -1 if random.randint(0, 1) == 0 else 1
    if enemy_block.direction == -1:
        enemy_block.position = [BOUNDARY_RIGHT - ENEMY_SIZE, random.randint(ENEMY_SPAWN[0], ENEMY_SPAWN[1])]
    else:
        enemy_block.position = [BOUNDARY_LEFT, random.randint(ENEMY_SPAWN[0], ENEMY_SPAWN[1])]
    enemy_block.speed = random.randint(1, ENEMY_SPEED_MAX) / 1000
    enemy_block.image = pygame.image.load('resources/enemy/enemy' + str(random.randint(0, ENEMY_TYPE - 1)) + '.png'),
    enemy_block.image = enemy_block.image[0]
    enemy_block.health[1] = enemy_block.health[0]
    enemy_block.weapon = random.randint(0, ENEMY_WEAPON_TYPE - 1)
    enemy_block.active = True
    enemy_block.cooldown = random.randint(0, enemy_armory.index_at(index=enemy_block.weapon).cooldown)
    # Self Start Element Reset
    enemy_block.explode = None
    enemy_block.health_show = True


##################################################
# Enemy Armory Block
##################################################
enemy_armory = Armory()
enemy_armory.append(name='bullet0',
                    index=0,
                    position=[0, 0],
                    speed=ENEMY_BULLET_SPEED_BASE,
                    exp_range=BULLET_EXPLOSION_RANGE,
                    contact=[[24, 45], [26, 45]],
                    active=False,
                    image=pygame.image.load('resources/enemy/bullet0.png'),
                    cooldown=ENEMY_BULLET_COOLDOWN_BASE,
                    damage=10)
enemy_armory.append(name='bullet1',
                    index=1,
                    position=[0, 0],
                    speed=ENEMY_BULLET_SPEED_BASE * 0.1,
                    exp_range=BULLET_EXPLOSION_RANGE * 0.5,
                    contact=[[24, 45], [26, 45]],
                    active=False,
                    image=pygame.image.load('resources/enemy/bullet1.png'),
                    cooldown=ENEMY_BULLET_COOLDOWN_BASE * 3,
                    damage=30)


##################################################
# Boss Block
##################################################
def create_mini_boss():
    global enemies
    for mini_boss_number in range(0, random.randint(0, MINI_BOSS_MAX_AMOUNT)):
        # Create Mini Boss
        enemies.append(name='mini_boss' + str(mini_boss_number),
                       index=ENEMY_NUMBER - 1 + mini_boss_number,
                       position=[random.randint(BOUNDARY_LEFT, BOUNDARY_RIGHT - BOSS_SIZE),
                                 BOSS_SPAWN[0]],
                       speed=random.randint(1, BOSS_SPEED_MAX) / 1000,
                       active=True,
                       image=pygame.image.load('resources/boss' + str(random.randint(0, MINI_BOSS_TYPE)) + '.png'),
                       health=random.randint(BOSS_HEALTH[0], BOSS_HEALTH[1]),
                       direction=-1 if random.randint(0, 1) == 0 else 1,
                       weapon=random.sample([i for i in range(ENEMY_WEAPON_TYPE)], MINI_BOSS_WEAPON_AMOUNT)
                       )
        # Set Mini Boss Center
        current_mini_boss = enemies.index_at(index=ENEMY_NUMBER - 1 + mini_boss_number)
        current_mini_boss.update(size=MINI_BOSS_SIZE)


##################################################
# Boss Armory Block
##################################################

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
