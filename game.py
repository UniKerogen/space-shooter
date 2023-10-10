# Top Down Shooter Game
# A Simple Top Down Shooter for Raiden Mockup
# Version - Alpha 7


####################################################################################################
# Libraries
####################################################################################################
import pygame
import random
import time

from structures import *
from settings import *
from blockelements import *

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
# Explosion
explosion_img = pygame.image.load('resources/explosion.png')
# Background
background = pygame.image.load('resources/background.png')
background_rect1 = background.get_rect()
background_rect2 = background.get_rect()
background_rect3 = background.get_rect()
background_rect1.topleft = (0, 0)
background_rect2.topleft = (0, -SCREEN_HEIGHT)
background_rect3.topleft = (0, -SCREEN_HEIGHT * 2)
# Shield
shield_image = pygame.image.load('resources/player/shield.png')
# Invincible
invincible_image = pygame.image.load('resources/player/invincible.png')
##################################################
# Structures Setting
##################################################
# On Screen Bullet Storage
player_bullets = BulletList()
enemy_bullets = BulletList()


####################################################################################################
# Function Prototype
####################################################################################################
def show_player(player_block):
    global screen
    # Invincible Coat
    if player_block.invincible:
        screen.blit(invincible_image, (player_block.position[0], player_block.position[1]))
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
            screen.blit(shield_image, (player_block.position[0], player_block.position[1] - 5))


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
    screen.blit(player_armory.index_at(index=bullet_block.index).image,
                (bullet_block.position[0], bullet_block.position[1]))


# Enemy Fire Bullet
def fire_bullet_enemy(bullet_block):
    # noinspection PyGlobalUndefined
    global screen, enemy_armory
    screen.blit(enemy_armory.index_at(index=bullet_block.index).image,
                (bullet_block.position[0], bullet_block.position[1]))


# Check if Player Bullet Hit Enemy
def collide_enemy(enemy_block, bullet_block):
    # noinspection PyGlobalUndefined
    global player_armory
    for coordinates in bullet_block.contact:
        distance = ((enemy_block.center[0] - coordinates[0]) ** 2 +
                    (enemy_block.center[1] - coordinates[1]) ** 2
                    ) ** 0.5
        if distance < player_armory.index_at(index=bullet_block.index).exp_range:
            return True  # Return True if within Explosion Range
    return False


# Check if Enemy Bullet Hit Player
def collide_player(player_block, bullet_block):
    global enemy_armory
    for coordinates in bullet_block.contact:
        distance = ((player_block.center[0] - coordinates[0]) ** 2 +
                    (player_block.center[1] - coordinates[1]) ** 2
                    ) ** 0.5
        if distance < enemy_armory.index_at(index=bullet_block.index).exp_range:
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


####################################################################################################
# Main Function
####################################################################################################
def main():
    # Global Variable
    global screen, score, crates
    global player
    global enemies, miniboss, boss
    global player_armory, player_bullets, enemy_bullets
    global BULLET_FIRE, end_screen
    ################################################################################
    ################################################################################
    # Mini Boss Spawn
    if score > 0 and score % 100 % 30 == 0 and len(miniboss) == 0:
        miniboss_create()
    # Boss Spawn
    ################################################################################
    ################################################################################
    # Find Active Bullet
    active_bullet = player_armory.search_active()
    ################################################################################
    ################################################################################
    # Continuous Shooting - Player
    if BULLET_FIRE and player.active:
        if active_bullet.cooldown[1] == 0:
            # Bullet Fire at Current Player x position
            player_bullets.append(index=active_bullet.index,
                                  position=[player.position[0], BULLET_ORIGIN_Y],
                                  contact=[list(item) for item in active_bullet.contact])
            # Reset CoolDown
            active_bullet.cooldown[1] = active_bullet.cooldown[0]
            # Bullet contact set
            new_bullet = player_bullets.get_last_element()
            for item in new_bullet.contact:
                item[0] = player.position[0] + item[0] - BULLET_ORIGIN_X
    # Cool Down for Bullet
    if active_bullet.cooldown[1] > 0:
        active_bullet.cooldown[1] -= 1
    ################################################################################
    ################################################################################
    # Continuous Shooting - Enemy
    current_enemy = enemies.head
    while current_enemy:
        if current_enemy.active and current_enemy.fire_cooldown <= 0:  # When Able to Fire
            # Fire Bullet at Current Enemy Position
            enemy_bullets.append(index=current_enemy.weapon,
                                 position=current_enemy.position.copy(),
                                 contact=[list(item) for item in
                                          enemy_armory.index_at(index=current_enemy.weapon).contact])
            # Reset CoolDown
            current_enemy.fire_cooldown = enemy_armory.index_at(index=current_enemy.weapon).cooldown
            # Set Bullet Contact
            new_bullet = enemy_bullets.get_last_element()
            for item in new_bullet.contact:
                item[0] = new_bullet.position[0] + item[0]
                item[1] = new_bullet.position[1] + item[1]
        else:  # When Already fired  - in cooldown
            current_enemy.fire_cooldown -= 1
        # Next Enemy
        current_enemy = current_enemy.next
    ################################################################################
    ################################################################################
    # Continuous Shooting - Miniboss
    current_miniboss = miniboss.head
    while current_miniboss:
        if current_miniboss.active:
            # Fire Bullet at current miniboss position
            for current_weapon in current_miniboss.weapon:
                if current_weapon == 0 and current_miniboss.fire_cooldown[current_weapon] <= 0:  # Bullet0
                    # First Shot
                    fire_position = [sum(x) for x in zip(current_miniboss.position, [0, 10])]
                    contact_point = [list(item) for item in
                                     enemy_armory.index_at(index=current_weapon).contact]
                    contact_point = [[sum(x) for x in zip(item, fire_position)] for item in contact_point]
                    enemy_bullets.append(index=current_weapon, position=fire_position, contact=contact_point)
                    # Second Shot
                    fire_position = [sum(x) for x in zip(current_miniboss.position, [50, 10])]
                    contact_point = [list(item) for item in
                                     enemy_armory.index_at(index=current_weapon).contact]
                    contact_point = [[sum(x) for x in zip(item, fire_position)] for item in contact_point]
                    enemy_bullets.append(index=current_weapon, position=fire_position, contact=contact_point)
                    # Reset Cooldown
                    current_miniboss.fire_cooldown[current_weapon] = enemy_armory.index_at(
                        index=current_weapon).cooldown
                elif current_weapon == 1 and current_miniboss.fire_cooldown[current_weapon] <= 0:  # Bullet1
                    fire_position = [sum(x) for x in zip(current_miniboss.position, [25, 53])]
                    contact_point = [list(item) for item in
                                     enemy_armory.index_at(index=current_weapon).contact]
                    contact_point = [[sum(x) for x in zip(item, fire_position)] for item in contact_point]
                    enemy_bullets.append(index=current_weapon, position=fire_position, contact=contact_point)
                    # Reset Cooldown
                    current_miniboss.fire_cooldown[current_weapon] = enemy_armory.index_at(
                        index=current_weapon).cooldown
                else:
                    current_miniboss.fire_cooldown = [sum(x) for x in zip(current_miniboss.fire_cooldown, [-1, -1])]
        # Next Miniboss
        current_miniboss = current_miniboss.next
    ################################################################################
    ################################################################################
    # Continuous Shooting - Big Boss
    ################################################################################
    ################################################################################
    # Player Movement
    player.update()
    # Movement of Each Enemy
    enemy_move()
    # Movement of Mini Boss
    miniboss_move()
    # Movement of Boss

    # Create Movement
    crate_movement()
    # Player Bullet Movement
    current_bullet = player_bullets.head
    while current_bullet:
        current_bullet.position[1] -= active_bullet.speed  # Update Position
        for item in current_bullet.contact:  # Update Contact Point
            item[1] -= active_bullet.speed
        # Reset Bullet
        if current_bullet.position[1] <= 0:  # Delete Bullet After Moves Off Screen
            player_bullets.delete(current_bullet=current_bullet)
        current_bullet = current_bullet.next
    # Enemy Bullet Movement
    current_bullet = enemy_bullets.head
    while current_bullet:
        current_bullet.position[1] += enemy_armory.index_at(index=current_bullet.index).speed  # Update Position
        for item in current_bullet.contact:  # Update Contact
            item[1] += enemy_armory.index_at(index=current_bullet.index).speed
        if current_bullet.position[1] >= SCREEN_HEIGHT:  # Remove After Off-Screen
            enemy_bullets.delete(current_bullet=current_bullet)
        current_bullet = current_bullet.next
    ################################################################################
    ################################################################################
    # Collision of Enemy & Player Bullet
    current_enemy = enemies.head
    while current_enemy:  # Iteration of Enemy
        if len(player_bullets) > 0 and current_enemy.active:
            current_bullet = player_bullets.head
            # Iteration of Player Bullet with Active Zone
            while current_bullet and current_enemy.position[1] <= ENEMY_SPAWN[1]:
                if collide_enemy(enemy_block=current_enemy, bullet_block=current_bullet):  # Check Collision
                    # Enemy Health Decrease
                    current_enemy.health[1] -= player_armory.index_at(index=current_bullet.index).damage
                    # Enemy Health Check
                    if current_enemy.health[1] <= 0:  # Explode at Health of 0
                        current_enemy.speed = 0  # Stop Moving
                        current_enemy.image = explosion_img  # Set Explosion Image
                        current_enemy.explode_at = time.time()  # Set Explosion Time
                        current_enemy.active = False  # De-active Enemy
                        current_enemy.health_show = False  # Disable Health Bar Element
                        score += 1  # Update Score
                        crate_generate(enemy_block=current_enemy, chance=CRATE_CHANCE)  # Generate Create
                    player_bullets.delete(current_bullet=current_bullet)  # Bullet Reset after Collision
                current_bullet = current_bullet.next  # Next Bullet
        # Reset enemy to active after some time
        if not current_enemy.active and current_enemy.explode_at is not None:
            # Reset Enemy after Explosion of EXPLOSION_TIME
            if time.time() - current_enemy.explode_at >= EXPLOSION_TIME:
                # Reset Enemy Reset
                enemy_reset(enemy_block=current_enemy)
        # Next Enemy
        current_enemy = current_enemy.next
    ################################################################################
    ################################################################################
    # Collision of Mini Boss & Player Bullet
    current_miniboss = miniboss.head
    while current_miniboss:  # Iteration of MiniBoss
        if len(player_bullets) > 0 and current_miniboss.active:
            current_bullet = player_bullets.head
            # Iteration of Bullet with Active Zone
            while current_bullet and current_miniboss.position[1] <= MINI_BOSS_Y_AXIS[1]:
                if collide_enemy(enemy_block=current_miniboss, bullet_block=current_bullet):  # Check Collision
                    # Miniboss Health Decrease
                    current_miniboss.health[1] -= player_armory.index_at(index=current_bullet.index).damage
                    # Health Check
                    if current_miniboss.health[1] <= 0:
                        current_miniboss.speed = 0  # Stop Moving
                        current_miniboss.image = explosion_img  # Explosion Image
                        current_miniboss.explode_at = time.time()  # Explosion Time
                        current_miniboss.active = False  # De-active Mini Boss
                        current_miniboss.health_show = False  # Hide Health Bar
                        score += 5  # Update Score
                        crate_generate(enemy_block=current_miniboss, chance=100)  # Guarantee a Create
                        crate_generate(enemy_block=current_miniboss, chance=CRATE_CHANCE)  # Generate Second Create
                    player_bullets.delete(current_bullet=current_bullet)  # Bullet Reset after Collision
                current_bullet = current_bullet.next  # Next Bullet
        # Reset enemy to active after some time
        if not current_miniboss.active and current_miniboss.explode_at is not None:
            # Reset Enemy after Explosion of EXPLOSION_TIME
            if time.time() - current_miniboss.explode_at >= EXPLOSION_TIME:
                miniboss.delete(enemy_block=current_miniboss)  # Delete Destroyed Miniboss
        current_miniboss = current_miniboss.next  # Next Element
    ################################################################################
    ################################################################################
    # Collision of Boss & Player Bullet
    ################################################################################
    ################################################################################
    # Collision of Player & Enemy Bullet
    current_bullet = enemy_bullets.head
    while current_bullet and player.active and not player.invincible:
        explosion_range = enemy_armory.index_at(index=current_bullet.index).exp_range
        # Set Danger Zone
        danger_range = [player.position[1] - explosion_range * 2, player.position[1] + PLAYER_SIZE]
        if danger_range[0] < current_bullet.position[1] < danger_range[1]:
            if collide_player(player_block=player, bullet_block=current_bullet):  # Check Collision
                # Decrease Player Shield and Health
                shield = player.shield - enemy_armory.index_at(index=current_bullet.index).damage
                if shield >= 0:  # Has Shield Remaining
                    player.shield = shield
                else:  # Decrease Health after Shield Consumption
                    player.shield = 0
                    player.health[1] += shield
                # Player Health Check
                if player.health[1] <= 0:  # Explode when No Health
                    player.image = explosion_img  # Set Explosion Image
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
                end_screen = True
    # Reset Invincibility
    if player.invincible:
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
            elif current_crate.category == 3:  # Weapon Create
                player_armory.search_active().active = False
                player_armory.index_at(index=current_crate.info).active = True
            elif current_crate.category == 4:  # Shield
                player.shield += current_crate.info
                player.shield = player.shield if player.shield <= PLAYER_SHIELD_MAX else PLAYER_SHIELD_MAX
            elif current_crate.category == 5:  # Collect Health
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
    score_text = font24.render("Score: " + str(score), True, WHITE)
    screen.blit(score_text, (10, 10))
    life_text = font18.render("Life X " + str(player.life[1]), True, WHITE)
    screen.blit(life_text, (10, SCREEN_HEIGHT - 5 - 18))


####################################################################################################
# Main Function Runner
####################################################################################################
if __name__ == "__main__":
    # Variable
    RUNNING, BULLET_FIRE = True, False
    intro_screen, end_screen, score_board, error_screen = True, False, False, False
    background_timer = time.time()
    # Running Loop
    while RUNNING:
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
                RUNNING = False
            # Event of Mouse Click
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Intro Screen
                if intro_screen and buttons.name('level').rect.collidepoint(event.pos):
                    intro_screen = False
                    error_screen = True
                elif intro_screen and buttons.name('endless').rect.collidepoint(event.pos):
                    intro_screen = False
                # End Screen
                elif end_screen and buttons.name('restart').rect.collidepoint(event.pos):
                    end_screen = False
                    score = 0
                    player.life[1] = player.life[0]
                    player.reset()
                    player.invincible_at = time.time()

                elif end_screen and buttons.name('main_menu').rect.collidepoint(event.pos):
                    end_screen = False
                    intro_screen = True
                elif end_screen and buttons.name('score_board').rect.collidepoint(event.pos):
                    score_board = True
                elif end_screen and buttons.name('quit').rect.collidepoint(event.pos):
                    RUNNING = False
                # Pause Screen
                elif score_board and buttons.name('main_menu').rect.collidepoint(event.pos):
                    score_board = False
                    intro_screen = True
                elif score_board and buttons.name('quit').rect.collidepoint(event.pos):
                    RUNNING = False
                # Error Screen
                elif error_screen and buttons.name('main_menu').rect.collidepoint(event.pos):
                    error_screen = False
                    intro_screen = True
                elif error_screen and buttons.name('score_board').rect.collidepoint(event.pos):
                    RUNNING = False
            # Event of Key Press
            if event.type == pygame.KEYDOWN and not intro_screen and not end_screen:
                # Player Movement
                if event.key == pygame.K_LEFT:
                    if player.active:
                        player.x_change = -player.speed
                elif event.key == pygame.K_RIGHT:
                    if player.active:
                        player.x_change = player.speed
                # Fire Bullet
                elif event.key == pygame.K_SPACE:
                    if player.active:
                        BULLET_FIRE = True
                # Weapon Switch -- TO BE DISABLED
                elif event.key == pygame.K_1 and not intro_screen:
                    player_armory.search_active().active = False
                    player_armory.index_at(index=0).active = True
                elif event.key == pygame.K_2 and not intro_screen:
                    player_armory.search_active().active = False
                    player_armory.index_at(index=1).active = True
                elif event.key == pygame.K_3 and not intro_screen:
                    player_armory.search_active().active = False
                    player_armory.index_at(index=2).active = True
            # Event of Key Release
            if event.type == pygame.KEYUP and not intro_screen:
                # Stop Player Movement
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player.x_change = 0
                if event.key == pygame.K_SPACE:
                    BULLET_FIRE = False
        ################################################################################
        ################################################################################
        if intro_screen:
            # Intro Texts and Locations
            intro_text = font36.render("Space Shooter", True, WHITE)
            intro_text_rect = intro_text.get_rect()
            intro_text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)
            # Show Texts
            screen.blit(intro_text, intro_text_rect)
            # Intro Screen Button
            screen.blit(buttons.name('level').image, buttons.name('level').rect.topleft)
            screen.blit(buttons.name('endless').image, buttons.name('endless').rect.topleft)
        ################################################################################
        ################################################################################
        elif end_screen:
            # Show Score
            score_text_end = font36.render("Score :" + str(score), True, WHITE)
            score_text_end_rect = score_text_end.get_rect()
            score_text_end_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)
            screen.blit(score_text_end, score_text_end_rect)
            # Render Button
            screen.blit(buttons.name('restart').image, buttons.name('restart').rect.topleft)
            screen.blit(buttons.name('main_menu').image, buttons.name('main_menu').rect.topleft)
            screen.blit(buttons.name('score_board').image, buttons.name('score_board').rect.topleft)
            screen.blit(buttons.name('quit').image, buttons.name('quit').rect.topleft)
        ################################################################################
        ################################################################################
        elif score_board:
            # Show Button
            screen.blit(buttons.name('main_menu').image, buttons.name('main_menu').rect.topleft)
            screen.blit(buttons.name('quit').image, buttons.name('score_board').rect.topleft)
        ################################################################################
        ################################################################################
        elif error_screen:
            # Show Text
            error_text = font36.render("Oops! Something went Wrong!", True, WHITE)
            error_text_rect = error_text.get_rect()
            error_text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)
            screen.blit(error_text, error_text_rect)
            # Show Button
            screen.blit(buttons.name('main_menu').image, buttons.name('main_menu').rect.topleft)
            screen.blit(buttons.name('quit').image, buttons.name('score_board').rect.topleft)
        ################################################################################
        ################################################################################
        else:  # Normal Game
            main()  # Main Game Function - Endless Run
        # Update Pygame Screen
        pygame.display.update()
    pygame.quit()  # Exit Game
