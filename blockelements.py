# Block Element File
# Version - Alpha 6.6
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
player_armory.append(name='bullet2',
                     index=2,
                     position=[BULLET_ORIGIN_X, BULLET_ORIGIN_Y],
                     speed=BULLET_SPEED_BASE * 1.5,
                     exp_range=BULLET_EXPLOSION_RANGE * 0.5,
                     contact=[[BULLET_ORIGIN_X + 26, BULLET_ORIGIN_Y],
                              [BULLET_ORIGIN_X + 34, BULLET_ORIGIN_Y]],
                     active=False,
                     image=pygame.image.load('resources/player/bullet2.png'),
                     cooldown=[BULLET_COOLDOWN_BASE * 0.1, BULLET_COOLDOWN_BASE * 0.1],
                     damage=80
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


# Enemy Movement
def enemy_move():
    current_enemy = enemies.head
    while current_enemy:
        current_enemy.update(block_size=ENEMY_SIZE, block_spawn=ENEMY_SPAWN)
        current_enemy = current_enemy.next


# Enemy Reset
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
# Mini Boss Block
##################################################
miniboss = EnemyList()


def miniboss_create():
    num_increase = 0 if len(miniboss) == 0 else 1
    for mini_boss_number in range(0, random.randint(0, MINI_BOSS_MAX_AMOUNT)):
        # Create Mini Boss
        miniboss.append(name='mini_boss' + str(mini_boss_number),
                        index=miniboss.get_last_index() + num_increase + mini_boss_number,
                        position=[random.randint(BOUNDARY_LEFT, BOUNDARY_RIGHT - MINI_BOSS_SIZE), -MINI_BOSS_SIZE],
                        speed=random.randint(1, MINI_BOSS_SPEED_MAX) / 1000,
                        active=False,
                        image=pygame.image.load(
                            'resources/miniboss/miniboss' + str(random.randint(0, MINI_BOSS_TYPE - 1)) + '.png'),
                        health=random.randint(MINI_BOSS_HEALTH[0], MINI_BOSS_HEALTH[1]),
                        direction=-1 if random.randint(0, 1) == 0 else 1,
                        weapon=random.sample([i for i in range(ENEMY_WEAPON_TYPE)], MINI_BOSS_WEAPON_AMOUNT)
                        )
        # Set Mini Boss Center
        current_miniboss = miniboss.index_at(index=miniboss.get_last_index())
        current_miniboss.center = [sum(x) for x in
                                   zip(current_miniboss.position, [MINI_BOSS_SIZE / 2, MINI_BOSS_SIZE / 2])]
        current_miniboss.fire_cooldown = [0] * MINI_BOSS_WEAPON_AMOUNT
        current_miniboss.y_axis = random.randint(MINI_BOSS_Y_AXIS[0], MINI_BOSS_Y_AXIS[1])
        # Check
        print("Mini Boss Created")


def miniboss_move():
    current_miniboss = miniboss.head
    while current_miniboss:
        if current_miniboss.position[1] < current_miniboss.y_axis:  # Move Downwards into Screen
            current_miniboss.position[1] += STANDARD_MOVE_SPEED
            if current_miniboss.position[1] < MINI_BOSS_HEALTH_BAR[1]:  # Active when Fully in Screen
                current_miniboss.active = True
        else:  # In Position
            current_miniboss.position[0] += current_miniboss.speed * current_miniboss.direction
            if current_miniboss.position[0] <= BOUNDARY_LEFT:
                current_miniboss.position[0] = BOUNDARY_LEFT
                current_miniboss.direction = - current_miniboss.direction
            elif current_miniboss.position[0] >= BOUNDARY_RIGHT - MINI_BOSS_SIZE:
                current_miniboss.position[0] = BOUNDARY_RIGHT - MINI_BOSS_SIZE
                current_miniboss.direction = - current_miniboss.direction
        # Update Center Information
        current_miniboss.center = [sum(x) for x in
                                   zip(current_miniboss.position, [MINI_BOSS_SIZE / 2, MINI_BOSS_SIZE / 2])]
        # Next Element
        current_miniboss = current_miniboss.next


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
