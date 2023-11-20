# Top Down Shooter Game
# A Simple Top Down Shooter for Raiden Mockup
# Version - Beta 5
import pygame.mouse

####################################################################################################
# Libraries
####################################################################################################
from blockelements import *
import time

####################################################################################################
# Settings
####################################################################################################
# Initialize Pygame
pygame.init()
# Create Screen
screen = pygame.display.set_mode(size=(SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Shooter")
# Display System
score = 0
font18 = pygame.font.Font(None, 18)
font24 = pygame.font.Font(None, 24)
font30 = pygame.font.Font(None, 30)
font36 = pygame.font.Font(None, 36)
font42 = pygame.font.Font(None, 42)
font48 = pygame.font.Font(None, 48)
# Background
background = pygame.image.load('resources/images/background.png')
background_rect1 = background.get_rect()
background_rect2 = background.get_rect()
background_rect3 = background.get_rect()
background_rect1.topleft = (0, 0)
background_rect2.topleft = (0, -SCREEN_HEIGHT)
background_rect3.topleft = (0, -SCREEN_HEIGHT * 2)

##################################################
# Structures Variable
##################################################
create_boss, create_miniboss = True, True


####################################################################################################
# Function Prototype
####################################################################################################
# Show Player
def show_player(player_block):
    global screen
    # Invincible Coat
    if player_block.invincible:
        screen.blit(player.invincible_image, (player_block.position[0], player_block.position[1]))
    # Player Self
    screen.blit(player_block.image, (player_block.position[0], player_block.position[1]))
    # Shield
    if player_block.health_show:
        pygame.draw.rect(screen,
                         color=RED,
                         rect=(player_block.position[0], player_block.position[1] + player_block.health_bar[2],
                               player_block.health_bar[0], player_block.health_bar[1]))
        pygame.draw.rect(screen,
                         color=GREEN,
                         rect=(player_block.position[0], player_block.position[1] + player_block.health_bar[2],
                               player_block.health[1] / player_block.health[0] * player_block.health_bar[0],
                               player_block.health_bar[1]))
        if player_block.shield > 0:
            pygame.draw.rect(screen,
                             color=GREY,
                             rect=(player_block.position[0], player_block.position[1] + player_block.health_bar[2],
                                   player_block.shield / PLAYER_SHIELD_MAX * player_block.health_bar[0],
                                   player_block.health_bar[1]))
            screen.blit(player.shield_image, (player_block.position[0], player_block.position[1] - 5))


# Show Each Create
def show_crate(crate_list):
    global screen
    current_crate = crate_list.head
    while current_crate:
        screen.blit(current_crate.image, (current_crate.position[0], current_crate.position[1]))
        current_crate = current_crate.next  # Next Element


# Show Each Enemy
def show_enemy(enemy_list, health_bar=ENEMY_HEALTH_BAR):
    global screen
    enemy_block = enemy_list.head
    while enemy_block:
        screen.blit(enemy_block.image, (enemy_block.position[0], enemy_block.position[1]))
        # Type 3 Weapon Indicator - Regular Enemy
        if 3 in enemy_block.weapon and enemy_block.explode_at is None:
            if enemy_block.each_weapon_amount[3] > 1:
                for position in enemy_block.indicator3_shift:
                    screen.blit(enemy_block.indicator3, [sum(x) for x in zip(position, enemy_block.position)])
            else:
                screen.blit(enemy_block.indicator3,
                            [sum(x) for x in zip(enemy_block.indicator3_shift, enemy_block.position)])
        # Show Health
        if enemy_block.health_show:
            pygame.draw.rect(screen,
                             color=RED,
                             rect=(enemy_block.position[0], enemy_block.position[1] + health_bar[2],
                                   health_bar[0], health_bar[1]))
            pygame.draw.rect(screen,
                             color=GREEN,
                             rect=(enemy_block.position[0], enemy_block.position[1] + health_bar[2],
                                   enemy_block.health[1] / enemy_block.health[0] * health_bar[0],
                                   health_bar[1]))
        enemy_block = enemy_block.next  # Next Element


# Player Fire Bullet
def fire_bullet_player(bullet_block):
    # noinspection PyGlobalUndefined
    global screen, player_armory
    screen.blit(bullet_block.image, (bullet_block.position[0], bullet_block.position[1]))


# Player Fire Rocket
def rocket_fire(type):
    global player, player_armory, player_bullets
    firing_rocket = player_armory.index_at(index=10 + type)  # Obtain Rocket
    if player.active and player.rocket_cooldown[1] <= 0:
        fire_position = player.position.copy()  # Set Fire Position
        # Set Rocket Contact Position
        rocket_contact = [list(item7) for item7 in firing_rocket.contact]
        rocket_contact = [[sum(x) for x in zip(fire_position, item8)] for item8 in rocket_contact]
        # Add to Bullet List
        player_bullets.append(index=firing_rocket.index,
                              position=fire_position,
                              contact=rocket_contact,
                              armory=player_armory)
        # Reset Cooldown
        player.rocket_cooldown[type] = firing_rocket.cooldown[0]


# Enemy Fire Bullet
def fire_bullet_enemy(bullet_block):
    # noinspection PyGlobalUndefined
    global screen, enemy_armory
    screen.blit(bullet_block.image, (bullet_block.position[0], bullet_block.position[1]))


# Bullet Collision
def bullet_collision(block_list, bullet_list, spawn):
    global score
    current_block = block_list.head
    while current_block:  # Iteration of Block List
        if len(bullet_list) > 0 and current_block.active:
            current_bullet = bullet_list.head
            while current_bullet and current_block.position[1] < spawn[1] + BOUNDARY_MARGIN:
                if collide_enemy(enemy_block=current_block, bullet_block=current_bullet):  # Check Collision
                    # Health Decrease
                    current_block.health[1] -= current_bullet.damage
                    # Health Check
                    if current_block.health[1] <= 0:
                        current_block.speed = 0  # Stop Moving
                        current_block.explode_at = time.time()  # Set Explosion Time
                        current_block.active = False  # De-active block
                        current_block.health_show = False  # Hide Health Bar
                        # Update Score and Crate
                        if spawn == ENEMY_SPAWN:
                            score += 1
                            current_block.image = pygame.transform.scale(explosion.get(), (
                                ENEMY_SIZE, ENEMY_SIZE))  # Set Explosion Image
                        elif spawn == MINI_BOSS_SPAWN:
                            score += 5
                            current_block.image = pygame.transform.scale(explosion.get(),
                                                                         (MINI_BOSS_SIZE, MINI_BOSS_SIZE))
                            crate_generate(enemy_block=current_block, chance=100)  # Additional Crate
                        elif spawn == BIG_BOSS_SPAWN:
                            score += 15
                            current_block.image = pygame.transform.scale(explosion.get(),
                                                                         (BIG_BOSS_SIZE, BIG_BOSS_SIZE))
                            crate_generate(enemy_block=current_block, chance=100)  # Additional Crate
                            crate_generate(enemy_block=current_block, chance=100)  # Additional Crate
                            crate_generate(enemy_block=current_block, chance=50)  # 50% Chance of Additional Crate
                        crate_generate(enemy_block=current_block, chance=CRATE_CHANCE)  # Regular Crate
                    # Delete Bullets
                    bullet_list.delete(current_bullet=current_bullet)
                current_bullet = current_bullet.next  # Next Bullet
        # Reset block to active after some time
        if not current_block.active and current_block.explode_at is not None:
            if time.time() - current_block.explode_at >= EXPLOSION_TIME:
                if spawn == ENEMY_SPAWN:  # Enemy List
                    enemy_reset(enemy_block=current_block)
                else:  # Boss and Mini Boss
                    block_list.delete(enemy_block=current_block)
        current_block = current_block.next  # Next Block


# Continuous Shooting
def enemy_shooting(block_list):
    # noinspection PyGlobalUndefined
    global enemy_bullets
    current_enemy = block_list.head
    while current_enemy:
        if current_enemy.active:
            # Fire Bullet at current position
            for current_weapon in current_enemy.weapon:
                weapon_index = current_enemy.weapon.index(current_weapon)
                if current_enemy.fire_cooldown[weapon_index] <= 0:
                    # Fire Bullet
                    for shot_number in range(current_enemy.each_weapon_amount[current_weapon]):
                        if current_enemy.each_weapon_amount[current_weapon] > 1:
                            fire_shift = current_enemy.fire_shift[current_weapon][shot_number]
                        else:
                            fire_shift = current_enemy.fire_shift[current_weapon]
                        fire_position = [sum(x) for x in zip(current_enemy.position, fire_shift)]
                        contact = [list(item0) for item0 in enemy_armory.index_at(index=current_weapon).contact]
                        contact = [[sum(x) for x in zip(item1, fire_position)] for item1 in contact]
                        # Add to Enemy Bullet
                        enemy_bullets.append(index=current_weapon,
                                             position=fire_position,
                                             contact=contact,
                                             armory=enemy_armory)
                    # Set Cooldown
                    current_enemy.fire_cooldown[current_enemy.weapon.index(current_weapon)] = enemy_armory.index_at(
                        index=current_weapon).cooldown
                else:
                    # Decrease Cooldown
                    current_enemy.fire_cooldown[weapon_index] -= 1
        # Next Block
        current_enemy = current_enemy.next


####################################################################################################
# Main Function
####################################################################################################
# noinspection PyGlobalUndefined
def main():
    # Global Variable
    global screen, score, crates
    global player
    global enemies, miniboss, bosses
    global player_armory, player_bullets, enemy_bullets
    global bullet_fire
    global create_boss, create_miniboss
    ################################################################################
    ################################################################################
    # Boss Creation - Big Boss
    if score > 10 and 0 <= score % 100 <= 5 and create_boss:
        boss_create()
        create_boss = False
    elif score > 10 > score % 100 > 5:
        create_boss = True
    # Boss Creation - Mini Boss - TODO Generation Error
    if score > 10 and 5 >= score % 25 >= 0 != score % 100 and create_miniboss:
        miniboss_create()
        create_miniboss = False
    elif score > 10 > score % 25 > 5:
        create_miniboss = True
    ################################################################################
    ################################################################################
    # Find Active Bullet
    active_bullet_list = player_armory.search_active()
    if 9 in active_bullet_list:
        active_bullet_list = [9]
    ################################################################################
    ################################################################################
    # Continuous Shooting - Player
    for active_bullet_index in active_bullet_list:
        active_bullet = player_armory.index_at(index=active_bullet_index)
        if bullet_fire.status and player.active and player.weapon_amount[active_bullet.index] > 0:
            if active_bullet.cooldown[1] <= 0:
                for fire_amount in range(0, player.weapon_amount[active_bullet.index]):
                    if player.weapon_amount[active_bullet.index] > 1:
                        fire_shift = player.fire_shift[active_bullet.index][fire_amount]
                    else:
                        fire_shift = player.fire_shift[active_bullet.index]
                    fire_position = [sum(x) for x in zip(player.position, fire_shift)]
                    # Bullet contact set
                    bullet_contact = [list(item2) for item2 in active_bullet.contact]
                    bullet_contact = [[sum(x) for x in zip(fire_position, item6)] for item6 in bullet_contact]
                    # Bullet Fire at Current Player
                    player_bullets.append(index=active_bullet.index,
                                          position=fire_position,
                                          contact=bullet_contact,
                                          armory=player_armory)
                # Reset CoolDown
                active_bullet.cooldown[1] = active_bullet.cooldown[0]
        # Cool Down for Bullet
        if active_bullet.cooldown[1] > 0:
            active_bullet.cooldown[1] -= 1
    ################################################################################
    ################################################################################
    # Continuous Shooting - Enemy
    enemy_shooting(block_list=enemies)
    ################################################################################
    ################################################################################
    # Continuous Shooting - Miniboss
    enemy_shooting(block_list=miniboss)
    ################################################################################
    ################################################################################
    # Continuous Shooting - Big Boss
    enemy_shooting(block_list=bosses)
    ################################################################################
    ################################################################################
    # Player Movement
    player.update()
    # Movement of Enemy
    movement(block_list=enemies, spawn=ENEMY_SPAWN, size=ENEMY_SIZE)
    # Movement of Mini Boss
    movement(block_list=miniboss, spawn=MINI_BOSS_SPAWN, size=MINI_BOSS_SIZE)
    # Movement of Boss
    movement(block_list=bosses, spawn=BIG_BOSS_SPAWN, size=BIG_BOSS_SIZE)
    # Create Movement
    crate_movement()
    # Player Bullet Movement
    current_bullet = player_bullets.head
    while current_bullet:
        current_bullet.position[1] -= current_bullet.speed  # Update Position
        for item4 in current_bullet.contact:  # Update Contact Point
            item4[1] -= current_bullet.speed
        # Reset Bullet
        if current_bullet.position[1] <= 0:  # Delete Bullet After Moves Off Screen
            player_bullets.delete(current_bullet=current_bullet)
        current_bullet = current_bullet.next
    # Enemy Bullet Movement
    current_bullet = enemy_bullets.head
    while current_bullet:
        current_bullet.position[1] += current_bullet.speed  # Update Position
        for item5 in current_bullet.contact:  # Update Contact
            if current_bullet.index == 3 and current_bullet.position[1] < player.position[1] + PLAYER_SIZE:
                # Special Case of Type 3 Weapon
                item5[1] = player.center[1]
            else:
                item5[1] += current_bullet.speed
        if current_bullet.position[1] >= SCREEN_HEIGHT:  # Remove After Off-Screen
            enemy_bullets.delete(current_bullet=current_bullet)
        current_bullet = current_bullet.next
    ################################################################################
    ################################################################################
    # Collision of Enemy & Player Bullet
    bullet_collision(block_list=enemies, bullet_list=player_bullets, spawn=ENEMY_SPAWN)
    ################################################################################
    ################################################################################
    # Collision of Mini Boss & Player Bullet
    bullet_collision(block_list=miniboss, bullet_list=player_bullets, spawn=MINI_BOSS_SPAWN)
    ################################################################################
    ################################################################################
    # Collision of Boss & Player Bullet
    bullet_collision(block_list=bosses, bullet_list=player_bullets, spawn=BIG_BOSS_SPAWN)
    ################################################################################
    ################################################################################
    # Collision of Player & Enemy Bullet
    current_bullet = enemy_bullets.head
    while current_bullet and player.active and not player.invincible:
        explosion_range = enemy_armory.index_at(index=current_bullet.index).exp_range
        # Set Danger Zone - Vertical - To Active Collision Calculation
        if current_bullet.index == 3:
            danger_range_y = [0, SCREEN_HEIGHT - ENEMY_SIZE]
        else:
            danger_range_y = [player.position[1] - explosion_range * 2, player.position[1] + PLAYER_SIZE]
        # Set Danger Zone - Horizontal - To Active Collision Calculation
        danger_range_x = [player.position[0] - BULLET_SIZE, player.position[0] + PLAYER_SIZE + BULLET_SIZE]
        if (danger_range_x[0] < current_bullet.position[0] < danger_range_x[1] and
                danger_range_y[0] < current_bullet.position[1] < danger_range_y[1]):
            if collide_player(player_block=player, bullet_block=current_bullet):  # Check Collision
                # Decrease Player Shield and Health
                shield = player.shield - current_bullet.damage
                if shield >= 0:  # Has Shield Remaining
                    player.shield = shield
                else:  # Decrease Health after Shield Consumption
                    player.shield = 0
                    player.health[1] += shield
                # Player Health Check
                if player.health[1] <= 0:  # Explode when No Health
                    player.image = pygame.transform.scale(explosion.get(), (PLAYER_SIZE, PLAYER_SIZE))
                    player.explode_at = time.time()  # Set Explosion Time
                    player.active = False  # De-active Player
                    player.health_show = False  # Hide Health Bar
                enemy_bullets.delete(current_bullet=current_bullet)  # Delete Collided Bullet
        # Next Element
        current_bullet = current_bullet.next
    # Reset Player After a certain time of Explosion
    if not player.active and player.explode_at is not None:
        if time.time() - player.explode_at >= EXPLOSION_TIME:
            player.life[1] -= 1  # Decrease Player Life
            if player.life[1] > 0:  # With Lives Left
                player.reset()
                player.invincible_at = time.time()
            else:  # With No Life Left
                controller.on(name="end")
    # Reset Invincibility
    if player.invincible and not player.always_invincible:
        if time.time() - player.invincible_at > PLAYER_INVINCIBLE_TIME:
            player.invincible = False
    ################################################################################
    ################################################################################
    # Create Collection
    current_crate = crates.head
    while current_crate:  # Iteration of Create
        if collide_crate(player_block=player, crate_block=current_crate):
            if current_crate.category == 0:  # Add a Life
                player.life[1] += 1
            elif current_crate.category == 1:  # Collect Invincible
                player.invincible_at = time.time()
                player.invincible = True
            elif current_crate.category == 2:  # Clear Enemy Bullet
                enemy_bullets = BulletList()
            elif current_crate.category == 3:  # Rocket Crate
                if player.rocket[current_crate.info] < 3:
                    player.rocket[current_crate.info] += 1
            elif current_crate.category == 4:  # Weapon Create
                for active_bullet_index in player_armory.search_active():
                    if active_bullet_index < WEAPON_TYPE_1_AMOUNT and current_crate.info < WEAPON_TYPE_1_AMOUNT:
                        player_armory.index_at(index=active_bullet_index).active = False
                    elif WEAPON_TYPE_1_AMOUNT - 1 < active_bullet_index < WEAPON_TYPE_1_AMOUNT + WEAPON_TYPE_2_AMOUNT and WEAPON_TYPE_1_AMOUNT - 1 < current_crate.info < WEAPON_TYPE_1_AMOUNT + WEAPON_TYPE_2_AMOUNT:
                        player_armory.index_at(index=active_bullet_index).active = False
                player_armory.index_at(index=current_crate.info).active = True
            elif current_crate.category == 5:  # Shield
                player.shield += current_crate.info
                player.shield = player.shield if player.shield <= PLAYER_SHIELD_MAX else PLAYER_SHIELD_MAX
            elif current_crate.category == 6:  # Collect Health
                player.health[1] += current_crate.info
                player.health[1] = player.health[1] if player.health[1] < player.health[0] else player.health[0]
            crates.delete(crate_block=current_crate)  # Delete Collected Crate
        current_crate = current_crate.next  # Next Element
    ################################################################################
    ################################################################################
    # Update Player
    show_player(player_block=player)
    # Update Enemy
    show_enemy(enemy_list=enemies, health_bar=ENEMY_HEALTH_BAR)
    # Update Mini Boss
    show_enemy(enemy_list=miniboss, health_bar=MINI_BOSS_HEALTH_BAR)
    # Update Boss
    show_enemy(enemy_list=bosses, health_bar=BIG_BOSS_HEALTH_BAR)
    # Update Create
    show_crate(crate_list=crates)
    # Update Bullet when Available
    if len(player_bullets) > 0:
        for bullet_index in range(0, len(player_bullets)):
            fire_bullet_player(bullet_block=player_bullets.get_element_at(position=bullet_index))
    if len(enemy_bullets) > 0:
        for bullet_index in range(0, len(enemy_bullets)):
            fire_bullet_enemy(bullet_block=enemy_bullets.get_element_at(position=bullet_index))
    # Update Display Element
    current_score = font24.render("Score: " + str(score), True, WHITE)
    screen.blit(current_score, (10, 10))
    life_text = font18.render("Life X " + str(player.life[1]), True, WHITE)
    screen.blit(life_text, (10, SCREEN_HEIGHT - 5 - 18))
    rocket_indicator = font18.render("Rocket: [ " + str(player.rocket[0]) + " , " + str(player.rocket[1]) + " ]", True, WHITE)
    screen.blit(rocket_indicator, (SCREEN_WIDTH - 95, SCREEN_HEIGHT - (5 + 18)))


####################################################################################################
# Main Function Runner
####################################################################################################
if __name__ == "__main__":
    # Variable
    global player_bullets
    program_run = Controller(name="program_run", status=True)
    bullet_fire = Controller(name="bullet_fire")
    enemy_exist = False
    controller.on(name="intro")
    background_timer = time.time()
    # Storage
    highest_score = 0
    # Running Loop
    while program_run.status:
        ################################################################################
        ################################################################################
        # Background Infinite Scroll Settings
        if time.time() - background_timer > BACKGROUND_REFRESH_TIME:
            background_timer = time.time()
            background_rect1.y += BACKGROUND_SCROLL_SPEED
            background_rect2.y += BACKGROUND_SCROLL_SPEED
            background_rect3.y += BACKGROUND_SCROLL_SPEED
            if background_rect1.y >= SCREEN_HEIGHT:
                background_rect1.topleft = (0, -SCREEN_HEIGHT * 2)
            if background_rect2.y >= SCREEN_HEIGHT:
                background_rect2.topleft = (0, -SCREEN_HEIGHT * 2)
            if background_rect3.y >= SCREEN_HEIGHT:
                background_rect3.topleft = (0, -SCREEN_HEIGHT * 2)
        # Draw the background
        screen.blit(background, background_rect1)
        screen.blit(background, background_rect2)
        screen.blit(background, background_rect3)
        ################################################################################
        ################################################################################
        # Obtain Single Keyboard Event
        for event in pygame.event.get():
            # Event of Quiting
            if event.type == pygame.QUIT:
                program_run.off()
            # Event of Mouse Click
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Intro Screen
                if controller.is_on(name="intro"):
                    if buttons.name('level').rect.collidepoint(event.pos):
                        controller.on(name="level")
                    elif buttons.name('endless').rect.collidepoint(event.pos):
                        difficulty.on(name="endless")
                        controller.on(name="game")
                # End Screen
                elif controller.is_on(name="end"):
                    if buttons.name('restart').rect.collidepoint(event.pos):
                        # Restart Endless Run
                        controller.on(name="game")
                        # Reset Player
                        score = 0
                        player.life[1] = player.life[0]
                        player.reset()
                        player.invincible_at = time.time()
                        # Reset Enemy and Bullets
                        reset_screen()
                        enemy_exist = False
                    elif buttons.name('main_menu').rect.collidepoint(event.pos):
                        # Back to Main Menu/Intro Menu
                        controller.on(name="intro")
                    elif buttons.name('score_board').rect.collidepoint(event.pos):
                        # Show Score Board
                        controller.on(name="score_board")
                    elif buttons.name('quit').rect.collidepoint(event.pos):
                        # Quit Game
                        program_run.off()
                # Score Board Screen
                elif controller.is_on(name="score_board"):
                    if buttons.name('main_menu').rect.collidepoint(event.pos):
                        controller.on(name="intro")
                    elif buttons.name('quit').rect.collidepoint(event.pos):
                        program_run.off()
                # Error Screen
                elif controller.is_on(name="error"):
                    if buttons.name('main_menu').rect.collidepoint(event.pos):
                        controller.on(name="intro")
                    elif buttons.name('score_board').rect.collidepoint(event.pos):
                        program_run.off()
                # Level Screen
                elif controller.is_on(name="level"):
                    if buttons.name('easy').rect.collidepoint(event.pos):
                        difficulty.on(name="easy")
                        controller.on(name="game")
                    elif buttons.name('medium').rect.collidepoint(event.pos):
                        difficulty.on(name="medium")
                        controller.on(name="game")
                    elif buttons.name('hard').rect.collidepoint(event.pos):
                        difficulty.on(name="hard")
                        controller.on(name="game")
                    elif buttons.name('hell').rect.collidepoint(event.pos):
                        difficulty.on(name="hell")
                        controller.on(name="game")
                    elif buttons.name('score_board').rect.collidepoint(event.pos):
                        controller.on(name="intro")
                    elif buttons.name('quit').rect.collidepoint(event.pos):
                        program_run.off()
                # Pause Screen
                elif controller.is_on(name="pause"):
                    if buttons.name('score_board').rect.collidepoint(event.pos):
                        program_run.off()
                    elif buttons.name('resume').rect.collidepoint(event.pos):
                        controller.on(name="game")
                # Game Screen
                elif controller.is_on(name="game"):
                    if buttons.name('back').rect.collidepoint(event.pos):
                        controller.on(name="intro")
                        reset_screen()
                        enemy_exist = False
                    elif buttons.name('pause').rect.collidepoint(event.pos):
                        controller.on(name="pause")
                    elif buttons.name('exit').rect.collidepoint(event.pos):
                        program_run.off()
            # Event of Key Press
            if event.type == pygame.KEYDOWN and controller.is_on(name="game"):
                # Player Movement
                if event.key == pygame.K_LEFT:
                    if player.active:
                        player.x_change = -player.speed
                elif event.key == pygame.K_RIGHT:
                    if player.active:
                        player.x_change = player.speed
                elif event.key == pygame.K_UP:
                    if player.active:
                        player.y_change = -player.speed
                elif event.key == pygame.K_DOWN:
                    if player.active:
                        player.y_change = player.speed
                # Fire Bullet
                elif event.key == pygame.K_SPACE:
                    if player.active:
                        bullet_fire.on()
                # Fire Rocket
                elif event.key == pygame.K_z and player.rocket[0] > 0 and player.rocket_cooldown[0] <= 0:
                    rocket_fire(type=0)
                    player.rocket[0] -= 1
                elif event.key == pygame.K_x and player.rocket[1] > 0 and player.rocket_cooldown[1] <= 0:
                    rocket_fire(type=1)
                    player.rocket[1] -= 1
                #################################################################
                # Weapon Switch -- TO BE DISABLED
                elif event.key == pygame.K_0:
                    player_armory.index_at(index=9).active = not player_armory.index_at(index=9).active
                # Always Invincible
                elif event.key == pygame.K_9:
                    player.always_invincible = not player.always_invincible
                    player.invincible = not player.invincible
                # Add Rocket
                elif event.key == pygame.K_8:
                    player.rocket[1] += 1
                ################################################################
            # Event of Key Release
            if event.type == pygame.KEYUP and controller.is_on(name="game"):
                # Stop Player Movement
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player.x_change = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    player.y_change = 0
                # Fire Bullet
                if event.key == pygame.K_SPACE:
                    bullet_fire.off()
        ################################################################################
        ################################################################################
        if controller.is_on(name="intro"):
            # Intro Texts and Locations
            intro_text = font48.render("Space Shooter", True, WHITE)
            intro_text_rect = intro_text.get_rect()
            intro_text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80)
            # Show Texts
            screen.blit(intro_text, intro_text_rect)
            # Show Tutorial Block if Hover over Help Button
            if buttons.name(name='help').rect.collidepoint(pygame.mouse.get_pos()):
                screen.blit(pygame.image.load('resources/images/tutorial_block.png'), (0, 0))
            # Intro Screen Button
            button_show(screen=screen, name='level')
            button_show(screen=screen, name='endless')
            button_show(screen=screen, name='help')
        ################################################################################
        ################################################################################
        elif controller.is_on(name="end"):
            # Show Score
            score_text_end = font42.render("Score : " + str(score), True, WHITE)
            score_text_end_rect = score_text_end.get_rect()
            score_text_end_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)
            screen.blit(score_text_end, score_text_end_rect)
            # End Screen Button
            button_show(screen=screen, name='restart')
            button_show(screen=screen, name='main_menu')
            button_show(screen=screen, name='score_board')
            button_show(screen=screen, name='quit')
        ################################################################################
        ################################################################################
        elif controller.is_on(name="score_board"):
            # Show Score Board - TODO Show Multiple High Scores
            highest_score = score if highest_score < score else highest_score
            score_board_text = font36.render("Current High Score : " + str(highest_score), True, WHITE)
            score_board_text_rect = score_board_text.get_rect()
            score_board_text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)
            screen.blit(score_board_text, score_board_text_rect)
            # Show Button
            button_show(screen=screen, name='main_menu')
            button_show(screen=screen, name='quit', position_name='score_board')
        ################################################################################
        ################################################################################
        elif controller.is_on(name="error"):
            # Show Text
            error_text = font36.render("Oops! Something went Wrong!", True, WHITE)
            error_text_rect = error_text.get_rect()
            error_text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)
            screen.blit(error_text, error_text_rect)
            # Show Button
            button_show(screen=screen, name='main_menu')
            button_show(screen=screen, name='quit', position_name='score_board')
        ################################################################################
        ################################################################################
        elif controller.is_on(name="level"):  # Level Selection
            # Show Title
            level_title = font42.render("Select Game Difficulty", True, WHITE)
            level_title_rect = level_title.get_rect()
            level_title_rect.center = (200, 150)
            screen.blit(level_title, level_title_rect)
            # Show Button
            button_show(screen=screen, name='easy')
            button_show(screen=screen, name='medium')
            button_show(screen=screen, name='hard')
            button_show(screen=screen, name='hell')
            button_show(screen=screen, name='main_menu', position_name='score_board')
            button_show(screen=screen, name='quit')
        ################################################################################
        ################################################################################
        elif controller.is_on(name="pause"):
            # Show Score
            score_text = font42.render("Current Score : " + str(score), True, WHITE)
            score_text_rect = score_text.get_rect()
            score_text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)
            screen.blit(score_text, score_text_rect)
            # Button
            button_show(screen=screen, name='resume')
            button_show(screen=screen, name='quit', position_name='score_board')
        ################################################################################
        ################################################################################
        elif controller.is_on(name="game"):  # Game
            # Generate Enemy - Level Selection
            if not enemy_exist:
                if difficulty.is_on(name="easy"):  # Easy Mode
                    batch_enemy_generation(number=2)
                elif difficulty.is_on(name="medium"):  # Medium Mode
                    batch_enemy_generation(number=5)
                elif difficulty.is_on(name="hard"):  # Hard Mode
                    batch_enemy_generation(number=8)
                elif difficulty.is_on(name="hell"):  # Death Mode
                    batch_enemy_generation(number=12)
                elif difficulty.is_on(name="endless"):  # Default Mode
                    batch_enemy_generation(number=ENEMY_NUMBER)
                enemy_exist = True
            # Endless Run
            button_show(screen=screen, name='back')
            button_show(screen=screen, name='exit')
            button_show(screen=screen, name='pause')
            button_show(screen=screen, name='info')
            # Show Tutorial Block if Hover over Help Button
            if buttons.name(name='info').rect.collidepoint(pygame.mouse.get_pos()):
                screen.blit(pygame.image.load('resources/images/info_block.png'), (0, 0))
            main()  # Main Game Function - Endless Run
            # Screen Element Rendering

        # Update Pygame Screen
        pygame.display.update()
    # Store and Update Scores - TODO Update and store highest scores

    # Exit Game
    pygame.quit()
