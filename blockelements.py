# Block Element File
# Version - Beta 6
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
                     image='resources/player/player.png',
                     speed=PLAYER_SPEED,
                     health=PLAYER_HEALTH)
player.shield_image = 'resources/player/shield.png'
player.invincible_image = 'resources/player/invincible.png'

##################################################
# Player Armory Block
##################################################
player_armory = Armory()
player_armory.append(name='bullet0',
                     index=0,
                     position=[0, 0],
                     speed=BULLET_SPEED_BASE,
                     exp_range=0,
                     contact=[[28, 0], [32, 0]],
                     active=True,
                     image='resources/player/bullet0.png',
                     cooldown=[BULLET_COOLDOWN_BASE, BULLET_COOLDOWN_BASE],
                     damage=50
                     )
player_armory.append(name='bullet1',
                     index=1,
                     position=[0, 0],
                     speed=BULLET_SPEED_BASE * 1.1,
                     exp_range=2,
                     contact=[[26, 0], [34, 0]],
                     active=False,
                     image='resources/player/bullet1.png',
                     cooldown=[BULLET_COOLDOWN_BASE * 0.61, BULLET_COOLDOWN_BASE * 0.61],
                     damage=30
                     )
player_armory.append(name='bullet2',
                     index=2,
                     position=[0, 0],
                     speed=BULLET_SPEED_BASE * 1.5,
                     exp_range=2,
                     contact=[[26, 0], [34, 0]],
                     active=False,
                     image='resources/player/bullet2.png',
                     cooldown=[BULLET_COOLDOWN_BASE * 1.6, BULLET_COOLDOWN_BASE * 1.6],
                     damage=80
                     )
player_armory.append(name='bullet3',
                     index=3,
                     position=[0, 0],
                     speed=BULLET_SPEED_BASE * 0.8,
                     exp_range=5,
                     contact=[[29, 0], [31, 0]],
                     active=False,
                     image='resources/player/bullet3.png',
                     cooldown=[BULLET_COOLDOWN_BASE * 2.4, BULLET_COOLDOWN_BASE * 2.4],
                     damage=120
                     )
player_armory.append(name='bullet4',
                     index=4,
                     position=[0, 0],
                     speed=BULLET_SPEED_BASE * 1.1,
                     exp_range=2,
                     contact=[[17, 16], [19, 16]],
                     active=False,
                     image='resources/player/bullet4.png',
                     cooldown=[BULLET_COOLDOWN_BASE * 1.2, BULLET_COOLDOWN_BASE * 1.2],
                     damage=30
                     )
player_armory.append(name='bullet5',
                     index=5,
                     position=[0, 0],
                     speed=BULLET_SPEED_BASE * 1.3,
                     exp_range=2,
                     contact=[[7, 28], [9, 28]],
                     active=False,
                     image='resources/player/bullet5.png',
                     cooldown=[BULLET_COOLDOWN_BASE * 1.2, BULLET_COOLDOWN_BASE * 1.2],
                     damage=45
                     )
player_armory.append(name='bullet6',
                     index=6,
                     position=[0, 0],
                     speed=BULLET_SPEED_BASE * 1.5,
                     exp_range=2,
                     contact=[[1, 40], [3, 40]],
                     active=False,
                     image='resources/player/bullet6.png',
                     cooldown=[BULLET_COOLDOWN_BASE * 1.2, BULLET_COOLDOWN_BASE * 1.2],
                     damage=55
                     )
player_armory.append(name='bullet9',
                     index=9,
                     position=[0, 0],
                     speed=BULLET_SPEED_BASE * 1.5,
                     exp_range=2,
                     contact=[[26, 0], [34, 0]],
                     active=False,
                     image='resources/player/bullet2.png',
                     cooldown=[BULLET_COOLDOWN_BASE * 0.2, BULLET_COOLDOWN_BASE * 0.2],
                     damage=100
                     )
player_armory.append(name='rocket0',
                     index=10,
                     position=[0, 0],
                     speed=BULLET_SPEED_BASE * 1.25,
                     exp_range=10,
                     contact=[[28, 2], [31, 2]],
                     active=False,
                     image='resources/player/rocket0.png',
                     cooldown=[BULLET_COOLDOWN_BASE * 1.2, BULLET_COOLDOWN_BASE * 1.2],
                     damage=800
                     )
player_armory.append(name='rocket1',
                     index=11,
                     position=[0, 0],
                     speed=BULLET_SPEED_BASE * 1.25,
                     exp_range=15,
                     contact=[[29, 9], [32, 9]],
                     active=False,
                     image='resources/player/rocket1.png',
                     cooldown=[BULLET_COOLDOWN_BASE * 1.2, BULLET_COOLDOWN_BASE * 1.2],
                     damage=1000
                     )

##################################################
# Enemy Block
##################################################
# Enemy List
enemies = EnemyList()


# Enemy Generation - Single
def enemy_generate(index):
    enemies.append(name='enemy' + str(index),
                   index=index,
                   position=[random.randint(BOUNDARY_LEFT, BOUNDARY_RIGHT - ENEMY_SIZE), -ENEMY_SIZE],
                   speed=random.randint(1, ENEMY_SPEED_MAX) / 1000,
                   active=False,
                   image='resources/enemy/enemy' + str(random.randint(0, ENEMY_TYPE - 1)) + '.png',
                   health=random.randint(ENEMY_BASE_HEALTH[0], ENEMY_BASE_HEALTH[1]),
                   direction=-1 if random.randint(0, 1) == 0 else 1,
                   weapon=random.sample([i for i in range(ENEMY_WEAPON_TYPE)], ENEMY_WEAPON_AMOUNT),
                   hit_range=ENEMY_SIZE / 2 * ENEMY_HIT_RANGE)
    current_enemy = enemies.index_at(index=index)
    # Each Weapon Amount
    current_enemy.each_weapon_amount = (1, 1, 1, 1, 1)
    current_enemy.fire_shift = ((0, 0),
                                (0, 0),
                                (0, 0),
                                (0, 0),
                                (0, 0))
    # Set Cooldown
    current_enemy.fire_cooldown = [0] * ENEMY_WEAPON_AMOUNT
    for weapon in current_enemy.weapon:
        index = current_enemy.weapon.index(weapon)
        max_cooldown = enemy_armory.index_at(index=weapon).cooldown
        current_enemy.fire_cooldown[index] = random.randint(BULLET_COOLDOWN_MINIMUM, max_cooldown)
    # Target Y Axis
    current_enemy.y_axis = random.randint(ENEMY_SPAWN[0], ENEMY_SPAWN[1])
    # Load Indicator
    current_enemy.indicator3 = 'resources/enemy/bullet3_indicator.png'
    current_enemy.indicator3_shift = current_enemy.fire_shift[3]


# Enemy Generation - Batch
def batch_enemy_generation(number=ENEMY_NUMBER):
    for num_enemy in range(number):
        enemy_generate(index=num_enemy)


# Enemy Reset
def enemy_reset(enemy_block):
    # Obtain Essential Information
    index = enemy_block.index
    # Delete Current Enemy
    enemies.delete(enemy_block)
    # Create New Enemy
    enemy_generate(index=index)
    del index


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
                    image='resources/enemy/bullet0.png',
                    cooldown=ENEMY_BULLET_COOLDOWN_BASE,
                    damage=20)
enemy_armory.append(name='bullet1',
                    index=1,
                    position=[0, 0],
                    speed=ENEMY_BULLET_SPEED_BASE * 0.1,
                    exp_range=3,
                    contact=[[24, 45], [26, 45]],
                    active=False,
                    image='resources/enemy/bullet1.png',
                    cooldown=ENEMY_BULLET_COOLDOWN_BASE * 3,
                    damage=40)
enemy_armory.append(name='bullet2',
                    index=2,
                    position=[0, 0],
                    speed=ENEMY_BULLET_SPEED_BASE,
                    exp_range=2,
                    contact=[[17, 49], [33, 49]],
                    active=False,
                    image='resources/enemy/bullet2.png',
                    cooldown=ENEMY_BULLET_COOLDOWN_BASE * 0.75,
                    damage=10)
enemy_armory.append(name='bullet3',
                    index=3,
                    position=[0, 0],
                    speed=ENEMY_BULLET_SPEED_BASE * 1.2,
                    exp_range=2,
                    contact=[[22, 40], [28, 40]],
                    active=False,
                    image='resources/enemy/bullet3.png',
                    cooldown=ENEMY_BULLET_COOLDOWN_BASE * 10,
                    damage=100)
enemy_armory.append(name='bullet4',
                    index=4,
                    position=[0, 0],
                    speed=ENEMY_BULLET_SPEED_BASE * 0.8,
                    exp_range=2,
                    contact=[[24, 33], [26, 33]],
                    active=False,
                    image='resources/enemy/bullet4.png',
                    cooldown=ENEMY_BULLET_COOLDOWN_BASE * 2,
                    damage=60)

##################################################
# Mini Boss Block
##################################################
miniboss = EnemyList()


# Miniboss Generation
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
                        image='resources/miniboss/miniboss' + str(miniboss_type) + '.png',
                        health=random.randint(MINI_BOSS_HEALTH[0], MINI_BOSS_HEALTH[1]),
                        direction=-1 if random.randint(0, 1) == 0 else 1,
                        weapon=random.sample([i for i in range(ENEMY_WEAPON_TYPE)], MINI_BOSS_WEAPON_AMOUNT),
                        hit_range=MINI_BOSS_SIZE / 2 * MINI_BOSS_HIT_RANGE
                        )
        # Set Mini Boss Center
        current_miniboss = miniboss.index_at(index=miniboss.get_last_index())
        current_miniboss.size = MINI_BOSS_SIZE
        current_miniboss.center = [sum(x) for x in
                                   zip(current_miniboss.position, [MINI_BOSS_SIZE / 2, MINI_BOSS_SIZE / 2])]
        # Set Mini Boss Weapon Cooldown
        current_miniboss.fire_cooldown = [0] * MINI_BOSS_WEAPON_AMOUNT
        for weapon in current_miniboss.weapon:
            index = current_miniboss.weapon.index(weapon)
            max_cooldown = enemy_armory.index_at(index=weapon).cooldown
            current_miniboss.fire_cooldown[index] = random.randint(BULLET_COOLDOWN_MINIMUM, max_cooldown)
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
        elif miniboss_type == 4: # Type 4 MiniBoss
            current_miniboss.each_weapon_amount = (2, 1, 1, 2, 2)
            current_miniboss.fire_shift = ((contact_point(point=[37, 94], index=0),
                                           contact_point(point=[61, 94], index=0)),
                                           (contact_point(point=[49, 85], index=1)),
                                           (contact_point(point=[42, 100], index=2)),
                                           (contact_point(point=[39, 22], index=3),
                                            contact_point(point=[59, 22], index=3)),
                                           (contact_point(point=[30, 43], index=4),
                                            contact_point(point=[68, 43], index=4))
                                           )
        # Load Indicator
        current_miniboss.indicator3 = 'resources/enemy/bullet3_indicator.png'
        current_miniboss.indicator3_shift = current_miniboss.fire_shift[3]


##################################################
# Boss Block
##################################################
bosses = EnemyList()


# Boss Creation
def boss_create():
    # Create New Big Boss
    num_increase = 0 if len(bosses) == 0 else 1
    boss_type = random.randint(0, BIG_BOSS_TYPE - 1)
    bosses.append(name='big_boss' + str(bosses.get_last_index() + num_increase),
                  index=bosses.get_last_index() + num_increase,
                  position=[random.randint(BOUNDARY_LEFT, BOUNDARY_RIGHT - BIG_BOSS_SIZE), -BIG_BOSS_SIZE],
                  speed=random.randint(1, BIG_BOSS_SPEED_MAX) / 1000,
                  active=False,
                  image='resources/bigboss/bigboss' + str(boss_type) + '.png',
                  health=random.randint(BIG_BOSS_HEALTH[0], BIG_BOSS_HEALTH[1]),
                  direction=-1 if random.randint(0, 1) == 0 else 1,
                  weapon=random.sample([i for i in range(ENEMY_WEAPON_TYPE)], BIG_BOSS_WEAPON_AMOUNT),
                  hit_range=BIG_BOSS_SIZE / 2 * BIG_BOSS_HIT_RANGE)
    # Set Big Boss Center
    current_boss = bosses.index_at(index=bosses.get_last_index())
    current_boss.size = BIG_BOSS_SIZE
    current_boss.center = [sum(x) for x in zip(current_boss.position, [BIG_BOSS_SIZE / 2, BIG_BOSS_SIZE / 2])]
    # Initial Weapon Cooldown
    current_boss.fire_cooldown = [0] * BIG_BOSS_WEAPON_AMOUNT
    for weapon in current_boss.weapon:
        index = current_boss.weapon.index(weapon)
        max_cooldown = enemy_armory.index_at(index=weapon).cooldown
        current_boss.fire_cooldown[index] = random.randint(BULLET_COOLDOWN_MINIMUM, max_cooldown)
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
    # Load Indicator
    current_boss.indicator3 = 'resources/enemy/bullet3_indicator.png'
    current_boss.indicator3_shift = current_boss.fire_shift[3]


##################################################
# Create Block
##################################################
crates = CrateList()


# Crate Generation
def crate_generate(enemy_block, chance=CRATE_CHANCE):
    if random.randint(0, 100) < chance:
        max_chance = CRATE_SUB_CHANCE.copy()  # Calculate Dice Region
        for i in range(1, CRATE_TYPE_AMOUNT):
            max_chance[i] = max_chance[i - 1] + max_chance[i]
        dice = random.randint(0, max(max_chance))  # Roll the Dice
        for crate_type in max_chance:
            if dice < crate_type:
                position = enemy_block.center.copy()
                position[0] += random.randint(-1, 1) * 10  # Shift Crate Horizontal Spawn by 10 Pixel
                position[1] += random.randint(-1, 1) * 10  # Shift Crate Vertical Spawn by 10 Pixel
                crates.append(category=max_chance.index(crate_type), position=position)
                break  # Exit Loop when Crate Created


# Crate Movement
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
button_names = ['endless', 'level', 'help',
                'main_menu', 'quit', 'restart', 'score_board',
                'easy', 'medium', 'hard', 'hell',
                'back', 'exit', 'pause', 'info',
                'resume']
for item in button_names:
    buttons.append(name=item)
# Intro Screen
buttons.name(name='endless').rect.topleft = (220, 460)
buttons.name(name='level').rect.topleft = (85, 460)
buttons.name(name='help').rect.topleft = (360, 643)
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
# On Screen
buttons.name(name='back').rect.topleft = (5, SCREEN_WIDTH - 20 - BUTTON_SIZE_ON_SCREEN[0] * 3)  # 305
buttons.name(name='pause').rect.topleft = (5, SCREEN_WIDTH - 15 - BUTTON_SIZE_ON_SCREEN[0] * 2)  # 335
buttons.name(name='exit').rect.topleft = (5, SCREEN_WIDTH - 10 - BUTTON_SIZE_ON_SCREEN[0])  # 365
buttons.name(name='info').rect.topleft = (5, SCREEN_WIDTH - 5)  # 395
# Pause Screen
buttons.name(name='resume').rect.topleft = (150, 480)


# Mouse Hover Collision
def hover_collide(name, position, position_name=None):
    global buttons
    current_button = buttons.name(name=name)
    if position_name is not None:
        current_button.hovered = buttons.name(name=position_name).rect.collidepoint(position)
    else:
        current_button.hovered = current_button.rect.collidepoint(position)


# Draw Buttons
def button_show(screen, name, position_name=None):
    # Hover Effect
    hover_collide(name=name, position=pygame.mouse.get_pos(), position_name=position_name)
    # Show Buttons on Screen
    if position_name is None:
        screen.blit(buttons.name(name=name).draw(), buttons.name(name=name).rect.topleft)
    else:
        screen.blit(buttons.name(name=name).draw(), buttons.name(name=position_name).rect.topleft)


##################################################
# Explosion Image Block
##################################################
explosion = ImageList()
for number in range(0, EXPLOSION_IMAGE_NUMBER):
    explosion.append(name='explosion' + str(number), number=number)

##################################################
# Controller Block
##################################################
controller = ControllerSet()
controller_names = ("intro", "end", "score_board", "error", "level", "pause", "game")
for screen_name in controller_names:
    controller.fuse(name=screen_name)

difficulty = ControllerSet()
level_names = ("easy", "medium", "hard", "hell", "endless")
for difficulty_level in level_names:
    difficulty.fuse(name=difficulty_level)

##################################################
# Screen Element Storage
##################################################
# On Screen Bullet Storage
player_bullets = BulletList()
enemy_bullets = BulletList()


# Reset Screen to Empty
def reset_screen():
    enemy_bullets.delete_list()
    player_bullets.delete_list()
    miniboss.delete_list()
    enemies.delete_list()


##################################################
# Supplemental Function
##################################################
# Negate Contact Point For Calculation
def negative_contact(index):
    return [-x for x in list(enemy_armory.index_at(index=index).contact[0]).copy()]


# Calculate Contact Point
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


# Block Movement
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
