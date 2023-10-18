# Block Element File
# Version - Alpha 9
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
                     health=PLAYER_HEALTH)
player.shield_image = pygame.image.load('resources/player/shield.png')
player.invincible_image = pygame.image.load('resources/player/invincible.png')

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
                     exp_range=0,
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
                     speed=BULLET_SPEED_BASE * 1.1,
                     exp_range=2,
                     contact=[[BULLET_ORIGIN_X + 18, BULLET_ORIGIN_Y + 20],
                              [BULLET_ORIGIN_X + 42, BULLET_ORIGIN_Y + 20]],
                     active=False,
                     image=pygame.image.load('resources/player/bullet1.png'),
                     cooldown=[BULLET_COOLDOWN_BASE * 0.5, BULLET_COOLDOWN_BASE * 0.5],
                     damage=30
                     )  # TODO Separate Bullet into 2 Elements
player_armory.append(name='bullet2',
                     index=2,
                     position=[BULLET_ORIGIN_X, BULLET_ORIGIN_Y],
                     speed=BULLET_SPEED_BASE * 1.5,
                     exp_range=2,
                     contact=[[BULLET_ORIGIN_X + 26, BULLET_ORIGIN_Y],
                              [BULLET_ORIGIN_X + 34, BULLET_ORIGIN_Y]],
                     active=False,
                     image=pygame.image.load('resources/player/bullet2.png'),
                     cooldown=[BULLET_COOLDOWN_BASE * 1.1, BULLET_COOLDOWN_BASE * 1.1],
                     damage=80
                     )
player_armory.append(name='bullet10',
                     index=10,
                     position=[BULLET_ORIGIN_X, BULLET_ORIGIN_Y],
                     speed=BULLET_SPEED_BASE * 1.5,
                     exp_range=2,
                     contact=[[BULLET_ORIGIN_X + 26, BULLET_ORIGIN_Y],
                              [BULLET_ORIGIN_X + 34, BULLET_ORIGIN_Y]],
                     active=False,
                     image=pygame.image.load('resources/player/bullet2.png'),
                     cooldown=[BULLET_COOLDOWN_BASE * 0.2, BULLET_COOLDOWN_BASE * 0.2],
                     damage=100
                     )

##################################################
# Enemy Block
##################################################
# Enemy List
enemies = EnemyList()


def enemy_generate(number=ENEMY_NUMBER):
    for num_enemy in range(number):
        enemies.append(name='enemy' + str(num_enemy),
                       index=num_enemy,
                       position=[random.randint(BOUNDARY_LEFT, BOUNDARY_RIGHT - ENEMY_SIZE), -ENEMY_SIZE],
                       speed=random.randint(1, ENEMY_SPEED_MAX) / 1000,
                       active=False,
                       image=pygame.image.load(
                           'resources/enemy/enemy' + str(random.randint(0, ENEMY_TYPE - 1)) + '.png'),
                       health=random.randint(ENEMY_BASE_HEALTH[0], ENEMY_BASE_HEALTH[1]),
                       direction=-1 if random.randint(0, 1) == 0 else 1,
                       weapon=random.randint(0, ENEMY_WEAPON_TYPE - 1),
                       hit_range=ENEMY_SIZE / 2 * ENEMY_HIT_RANGE)
        current_enemy = enemies.index_at(index=num_enemy)
        current_enemy.fire_cooldown = random.randint(10,
                                                     enemy_armory.index_at(index=current_enemy.weapon).cooldown * 0.2)
        current_enemy.y_axis = random.randint(ENEMY_SPAWN[0], ENEMY_SPAWN[1])
        current_enemy.indicator = pygame.image.load('resources/enemy/bullet3_indicator.png')


# Enemy Reset
def enemy_reset(enemy_block):
    # Reset Enemy Information
    enemy_block.direction = -1 if random.randint(0, 1) == 0 else 1
    enemy_block.position = [random.randint(BOUNDARY_LEFT, BOUNDARY_RIGHT - ENEMY_SIZE), -ENEMY_SIZE]
    enemy_block.speed = random.randint(1, ENEMY_SPEED_MAX) / 1000
    enemy_block.image = pygame.image.load('resources/enemy/enemy' + str(random.randint(0, ENEMY_TYPE - 1)) + '.png'),
    enemy_block.image = enemy_block.image[0]
    enemy_block.health[1] = enemy_block.health[0]
    enemy_block.weapon = random.randint(0, ENEMY_WEAPON_TYPE - 1)
    enemy_block.active = False
    enemy_block.fire_cooldown = random.randint(0, enemy_armory.index_at(index=enemy_block.weapon).cooldown)
    # Self Start Element Reset
    enemy_block.explode_at = None
    enemy_block.health_show = True
    enemy_block.y_axis = random.randint(ENEMY_SPAWN[0], ENEMY_SPAWN[1])


##################################################
# Enemy Armory Block
##################################################
enemy_armory = Armory()
enemy_armory.append(name='bullet0',
                    index=0,
                    position=[0, 0],
                    speed=ENEMY_BULLET_SPEED_BASE * 0.5,
                    exp_range=3,
                    contact=[[24, 45], [26, 45]],
                    active=False,
                    image=pygame.image.load('resources/enemy/bullet0.png'),
                    cooldown=ENEMY_BULLET_COOLDOWN_BASE,
                    damage=20)
enemy_armory.append(name='bullet1',
                    index=1,
                    position=[0, 0],
                    speed=ENEMY_BULLET_SPEED_BASE * 0.1,
                    exp_range=3,
                    contact=[[24, 45], [26, 45]],
                    active=False,
                    image=pygame.image.load('resources/enemy/bullet1.png'),
                    cooldown=ENEMY_BULLET_COOLDOWN_BASE * 3,
                    damage=40)
enemy_armory.append(name='bullet2',
                    index=2,
                    position=[0, 0],
                    speed=ENEMY_BULLET_SPEED_BASE,
                    exp_range=2,
                    contact=[[17, 49], [33, 49]],
                    active=False,
                    image=pygame.image.load('resources/enemy/bullet2.png'),
                    cooldown=ENEMY_BULLET_COOLDOWN_BASE * 0.75,
                    damage=10)
enemy_armory.append(name='bullet3',
                    index=3,
                    position=[0, 0],
                    speed=ENEMY_BULLET_SPEED_BASE * 1.2,
                    exp_range=2,
                    contact=[[22, 40], [28, 40]],
                    active=False,
                    image=pygame.image.load('resources/enemy/bullet3.png'),
                    cooldown=ENEMY_BULLET_COOLDOWN_BASE * 10,
                    damage=100)
enemy_armory.append(name='bullet4',
                    index=4,
                    position=[0, 0],
                    speed=ENEMY_BULLET_SPEED_BASE * 0.8,
                    exp_range=2,
                    contact=[[24, 33], [26, 33]],
                    active=False,
                    image=pygame.image.load('resources/enemy/bullet4.png'),
                    cooldown=ENEMY_BULLET_COOLDOWN_BASE * 2,
                    damage=60)

##################################################
# Mini Boss Block
##################################################
miniboss = EnemyList()


def miniboss_create():
    num_increase = 0 if len(miniboss) == 0 else 1
    for mini_boss_number in range(0, random.randint(0, MINI_BOSS_MAX_AMOUNT)):
        # Create Mini Boss
        miniboss_type = random.randint(0, MINI_BOSS_TYPE - 1)
        miniboss.append(name='mini_boss' + str(mini_boss_number),
                        index=miniboss.get_last_index() + num_increase + mini_boss_number,
                        position=[random.randint(BOUNDARY_LEFT, BOUNDARY_RIGHT - MINI_BOSS_SIZE), -MINI_BOSS_SIZE],
                        speed=random.randint(1, MINI_BOSS_SPEED_MAX) / 1000,
                        active=False,
                        image=pygame.image.load(
                            'resources/miniboss/miniboss' + str(miniboss_type) + '.png'),
                        health=random.randint(MINI_BOSS_HEALTH[0], MINI_BOSS_HEALTH[1]),
                        direction=-1 if random.randint(0, 1) == 0 else 1,
                        weapon=random.sample([i for i in range(ENEMY_WEAPON_TYPE)], MINI_BOSS_WEAPON_AMOUNT),
                        hit_range=MINI_BOSS_SIZE / 2 * MINI_BOSS_HIT_RANGE
                        )
        # Set Mini Boss Center
        current_miniboss = miniboss.index_at(index=miniboss.get_last_index())
        current_miniboss.center = [sum(x) for x in
                                   zip(current_miniboss.position, [MINI_BOSS_SIZE / 2, MINI_BOSS_SIZE / 2])]
        # Set Mini Boss Weapon Cooldown
        current_miniboss.fire_cooldown = [0] * MINI_BOSS_WEAPON_AMOUNT
        for weapon in current_miniboss.weapon:
            index = current_miniboss.weapon.index(weapon)
            max_cooldown = enemy_armory.index_at(index=weapon).cooldown
            current_miniboss.fire_cooldown[index] = random.randint(0, max_cooldown)
        # Set Mini Boss Y Axis
        current_miniboss.y_axis = random.randint(MINI_BOSS_SPAWN[0], MINI_BOSS_SPAWN[1])
        # Type Specific Adjustment
        if miniboss_type == 0:  # Type 0 MiniBoss
            current_miniboss.each_weapon_amount = (2, 1, 2, 1, 1)
            current_miniboss.fire_shift = (((12, 12), (38, 12)),
                                           (25, 53),
                                           ((-1, 9), (50, 9)),
                                           (28, 56),
                                           (25, 2))
        elif miniboss_type == 1:  # Type 1 MiniBoss
            current_miniboss.each_weapon_amount = (2, 1, 1, 1, 2)
            current_miniboss.fire_shift = (((1, 4), (57, 4)),
                                           (25, 53),
                                           (25, 50),
                                           (28, 56),
                                           ((16, 41), (34, 41)))
        elif miniboss_type == 2:  # Type 2 MiniBoss
            current_miniboss.each_weapon_amount = (2, 2, 2, 1, 2)
            current_miniboss.fire_shift = (((12, 23), (38, 23)),
                                           ((7, 24), (43, 24)),
                                           ((-11, -13), (63, -13)),
                                           (26, 2),
                                           ((-3, -2), (61, -2)))
        elif miniboss_type == 3:  # Type 3 MiniBoss
            current_miniboss.each_weapon_amount = (2, 1, 1, 1, 2)
            current_miniboss.fire_shift = (((13, 21), (37, 21)),
                                           (25, 34),
                                           (25, 49),
                                           (25, 24),
                                           ((11, 7), (39, 7)))


##################################################
# Boss Block
##################################################
bosses = EnemyList()


def boss_create():
    # Create New Big Boss
    num_increase = 0 if len(bosses) == 0 else 1
    boss_type = random.randint(0, BIG_BOSS_TYPE - 1)
    bosses.append(name='big_boss',
                  index=bosses.get_last_index() + num_increase,
                  position=[random.randint(BOUNDARY_LEFT, BOUNDARY_RIGHT - BIG_BOSS_SIZE), -BIG_BOSS_SIZE],
                  speed=random.randint(1, BIG_BOSS_SPEED_MAX) / 1000,
                  active=False,
                  image=pygame.image.load('resources/bigboss/bigboss' + str(boss_type) + '.png'),
                  health=random.randint(BIG_BOSS_HEALTH[0], BIG_BOSS_HEALTH[1]),
                  direction=-1 if random.randint(0, 1) == 0 else 1,
                  weapon=random.sample([i for i in range(ENEMY_WEAPON_TYPE)], BIG_BOSS_WEAPON_AMOUNT),
                  hit_range=BIG_BOSS_SIZE / 2 * BIG_BOSS_HIT_RANGE)
    # Set Big Boss Center
    current_boss = bosses.index_at(index=bosses.get_last_index())
    current_boss.center = [sum(x) for x in zip(current_boss.position, [BIG_BOSS_SIZE / 2, BIG_BOSS_SIZE / 2])]
    # Initial Weapon Cooldown
    current_boss.fire_cooldown = [0] * BIG_BOSS_WEAPON_AMOUNT
    for weapon in current_boss.weapon:
        index = current_boss.weapon.index(weapon)
        max_cooldown = enemy_armory.index_at(index=weapon).cooldown
        current_boss.fire_cooldown[index] = random.randint(0, max_cooldown)
    # Target y_axis
    current_boss.y_axis = random.randint(BIG_BOSS_SPAWN[0], BIG_BOSS_SPAWN[1])
    # Type Specific Adjustment
    if boss_type == 0:  # Type 0 Big Boss
        current_boss.each_weapon_amount = (4, 4, 1, 2, 3)
        current_boss.fire_shift = ((contact_point(point=[36, 156], index=0),
                                    contact_point(point=[93, 86], index=0),
                                    contact_point(point=[105, 86], index=0),
                                    contact_point(point=[162, 156], index=0)),
                                   (contact_point(point=[42, 109], index=1),
                                    contact_point(point=[158, 109], index=1),
                                    contact_point(point=[93, 136], index=1),
                                    contact_point(point=[107, 136], index=1)),
                                   (contact_point(point=[92, 143], index=2)),
                                   (contact_point(point=[88, 67], index=3),
                                    contact_point(point=[106, 67], index=3)),
                                   (contact_point(point=[99, 67], index=4),
                                    contact_point(point=[77, 97], index=4),
                                    contact_point(point=[121, 97], index=4))
                                   )
    elif boss_type == 1:  # Type 1 Big Boss
        current_boss.each_weapon_amount = (4, 4, 2, 1, 4)
        current_boss.fire_shift = ((contact_point(point=[34, 107], index=0),
                                    contact_point(point=[164, 107], index=0),
                                    contact_point(point=[68, 160], index=0),
                                    contact_point(point=[130, 160], index=0)),
                                   (contact_point(point=[82, 129], index=1),
                                    contact_point(point=[117, 129], index=1),
                                    contact_point(point=[60, 77], index=1),
                                    contact_point(point=[139, 77], index=1)),
                                   (contact_point(point=[63, 184], index=2),
                                    contact_point(point=[122, 184], index=2)),
                                   (contact_point(point=[97, 117], index=3)),
                                   (contact_point(point=[51, 150], index=4),
                                    contact_point(point=[147, 150], index=4),
                                    contact_point(point=[99, 117], index=4),
                                    contact_point(point=[99, 78], index=4))
                                   )


##################################################
# Create Block
##################################################
crates = CrateList()


def crate_generate(enemy_block, chance=CRATE_CHANCE):
    if random.randint(0, 100) < chance:
        max_chance = CRATE_SUB_CHANCE.copy()  # Calculate Dice Region
        for i in range(1, CRATE_TYPE_AMOUNT):
            max_chance[i] = max_chance[i - 1] + max_chance[i]
        dice = random.randint(0, max(max_chance))  # Roll the Dice
        for crate_type in max_chance:
            if dice < crate_type:
                crates.append(category=max_chance.index(crate_type), position=enemy_block.center.copy())
                break  # Exit Loop when Crate Created


def crate_movement():
    current_crate = crates.head
    while current_crate:
        current_crate.position[1] += CRATE_SPEED
        current_crate.contact[1] += CRATE_SPEED
        if random.randint(0, 1) == 0:  # x-axis Movement
            current_crate.position[0] += CRATE_SPEED * current_crate.direction
            current_crate.contact[0] += CRATE_SPEED * current_crate.direction
            if current_crate.position[0] <= BOUNDARY_LEFT:
                current_crate.position[0] = BOUNDARY_LEFT
                current_crate.direction = -current_crate.direction
            elif current_crate.position[0] >= BOUNDARY_RIGHT - CRATE_SIZE:
                current_crate.position[0] = BOUNDARY_RIGHT - CRATE_SIZE
                current_crate.direction = -current_crate.direction
        # Out of Boundary - Y Axis
        if current_crate.position[1] >= SCREEN_HEIGHT - CRATE_SIZE:
            crates.delete(crate_block=current_crate)
        # Next Step
        current_crate = current_crate.next


##################################################
# Button Block
##################################################
buttons = ButtonList()
button_names = ['endless', 'level', 'main_menu', 'quit', 'restart', 'score_board',
                'easy', 'medium', 'hard', 'hell']
for item in button_names:
    buttons.append(name=item)
# Intro Screen
buttons.name(name='endless').rect.topleft = (220, 460)
buttons.name(name='level').rect.topleft = (85, 460)
# End Screen - Vertical Stack
buttons.name(name='restart').rect.topleft = (150, 420)
buttons.name(name='main_menu').rect.topleft = (150, 480)
buttons.name(name='score_board').rect.topleft = (150, 540)
buttons.name(name='quit').rect.topleft = (150, 600)
# Level Menu
buttons.name(name='easy').rect.topleft = (150, 240)
buttons.name(name='medium').rect.topleft = (150, 300)
buttons.name(name='hard').rect.topleft = (150, 360)
buttons.name(name='hell').rect.topleft = (150, 420)

##################################################
# Explosion Image Block
##################################################
explosion = ImageList()
for number in range(0, EXPLOSION_IMAGE_NUMBER):
    explosion.append(name='explosion' + str(number), number=number)

##################################################
# Screen Element Storage
##################################################
# On Screen Bullet Storage
player_bullets = BulletList()
enemy_bullets = BulletList()


def reset_screen():
    enemy_bullets.delete_list()
    player_bullets.delete_list()
    miniboss.delete_list()
    enemies.delete_list()


##################################################
# Supplemental Function
##################################################
def negative_contact(index):
    return [-x for x in list(enemy_armory.index_at(index=index).contact[0]).copy()]


def contact_point(point, index):
    return tuple(sum(x) for x in zip(point, negative_contact(index=index)))


# Check if Player Bullet Hit Enemy
def collide_enemy(enemy_block, bullet_block):
    for coordinates in bullet_block.contact:
        distance = ((enemy_block.center[0] - coordinates[0]) ** 2 +
                    (enemy_block.center[1] - coordinates[1]) ** 2
                    ) ** 0.5
        if distance <= enemy_block.hit_range + player_armory.index_at(index=bullet_block.index).exp_range:
            return True  # Return True if within Explosion Range
    return False


# Check if Enemy Bullet Hit Player
def collide_player(player_block, bullet_block):
    for coordinates in bullet_block.contact:
        distance = ((player_block.center[0] - coordinates[0]) ** 2 +
                    (player_block.center[1] - coordinates[1]) ** 2
                    ) ** 0.5
        if distance <= player_block.hit_range + enemy_armory.index_at(index=bullet_block.index).exp_range:
            return True  # Return True if within Explosion Range
    return False


# Check if Player can Collect Create
def collide_crate(player_block, crate_block):
    distance = ((player_block.center[0] - crate_block.contact[0]) ** 2 +
                (player_block.center[1] - crate_block.contact[1]) ** 2
                ) ** 0.5
    if distance <= crate_block.collect_range:
        return True  # Return True if within Collecting Range
    return False


# Movement
def movement(block_list, spawn, size):
    current_block = block_list.head
    while current_block:
        if current_block.explode_at is None:  # No Movement for Exploded Block
            # Initial Vertical Move
            if not current_block.active and current_block.position[1] < current_block.y_axis:
                current_block.position[1] += STANDARD_MOVE_SPEED * 10
                # Active Block
                if spawn == BIG_BOSS_SPAWN:  # Boss Block
                    if current_block.position[1] > spawn[0] - STANDARD_MOVE_SPEED * 10:
                        current_block.active = True
                else:  # Other Block Active at Pixel Y of 25
                    if current_block.position[1] > 25:
                        current_block.active = True
            else:
                # Update Vertical Move
                if current_block.position[1] < current_block.y_axis - STANDARD_MOVE_SPEED:
                    current_block.position[1] += STANDARD_MOVE_SPEED * 2
                # Move to New Y
                elif current_block.position[1] > current_block.y_axis + STANDARD_MOVE_SPEED:
                    current_block.position[1] -= STANDARD_MOVE_SPEED * 2
                # Update Horizontal Move
                else:
                    current_block.position[0] += current_block.speed * current_block.direction
                    if current_block.position[0] <= BOUNDARY_LEFT:
                        current_block.position[0] = BOUNDARY_LEFT
                        current_block.direction = -current_block.direction
                        if random.randint(0, 100) < ENEMY_SHIFT_CHANCE:  # Random Vertical Move
                            current_block.y_axis = random.randint(spawn[0], spawn[1])
                    elif current_block.position[0] >= BOUNDARY_RIGHT - size:
                        current_block.position[0] = BOUNDARY_RIGHT - size
                        current_block.direction = -current_block.direction
                        if random.randint(0, 100) < ENEMY_SHIFT_CHANCE:
                            current_block.y_axis = random.randint(spawn[0], spawn[1])
            # Update Center Information
            current_block.center = [sum(x) for x in zip(current_block.position, [size / 2, size / 2])]
        # Next Block
        current_block = current_block.next


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
