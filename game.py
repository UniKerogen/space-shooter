# Top Down Shooter Game
# A Simple Top Down Shooter for Raiden Mockup
# Version - Alpha 6.5


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
pygame.display.set_caption("Top-Down Shooter")
# Score System
font = pygame.font.Font(None, 24)
score = 0
# Explosion
explosion_img = pygame.image.load('resources/explosion.png')
# Background
background = pygame.image.load('resources/background.png')
background_rect1 = background.get_rect()
background_rect2 = background.get_rect()
background_rect1.topleft = (0, 0)
background_rect2.topleft = (0, -SCREEN_HEIGHT)
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
    screen.blit(player_block.image, (player_block.position[0], player_block.position[1]))
    if player_block.health_show:
        pygame.draw.rect(screen,
                         color=RED,
                         rect=(player_block.position[0], player_block.position[1] + PLAYER_HEALTH_BAR_SHIFT,
                               PLAYER_HEALTH_BAR[0], PLAYER_HEALTH_BAR[1]))
        pygame.draw.rect(screen,
                         color=GREEN,
                         rect=(player_block.position[0], player_block.position[1] + PLAYER_HEALTH_BAR_SHIFT,
                               player_block.health[1] / player_block.health[0] * PLAYER_HEALTH_BAR[0],
                               PLAYER_HEALTH_BAR[1]))


def show_enemy(enemy_block):
    global screen
    screen.blit(enemy_block.image, (enemy_block.position[0], enemy_block.position[1]))
    if enemy_block.health_show:
        pygame.draw.rect(screen,
                         color=RED,
                         rect=(enemy_block.position[0], enemy_block.position[1] + ENEMY_HEALTH_BAR_SHIFT,
                               ENEMY_HEALTH_BAR[0], ENEMY_HEALTH_BAR[1]))
        pygame.draw.rect(screen,
                         color=GREEN,
                         rect=(enemy_block.position[0], enemy_block.position[1] + ENEMY_HEALTH_BAR_SHIFT,
                               enemy_block.health[1] / enemy_block.health[0] * ENEMY_HEALTH_BAR[0],
                               ENEMY_HEALTH_BAR[1]))


def fire_bullet_player(bullet_block):
    global screen, player_armory
    screen.blit(player_armory.index_at(index=bullet_block.index).image,
                (bullet_block.position[0], bullet_block.position[1]))


def fire_bullet_enemy(bullet_block):
    global screen, enemy_armory
    screen.blit(enemy_armory.index_at(index=bullet_block.index).image,
                (bullet_block.position[0], bullet_block.position[1]))


def collide_enemy(enemy_block, bullet_block):
    global player_armory
    for coordinates in bullet_block.contact:
        distance = ((enemy_block.center[0] - coordinates[0]) ** 2 +
                    (enemy_block.center[1] - coordinates[1]) ** 2
                    ) ** 0.5
        if distance < player_armory.index_at(index=bullet_block.index).exp_range:
            return True
    return False


def collide_player(player_block, bullet_block):
    global enemy_armory
    for coordinates in bullet_block.contact:
        distance = ((player_block.center[0] - coordinates[0]) ** 2 +
                    (player_block.center[1] - coordinates[1]) ** 2
                    ) ** 0.5
        if distance < enemy_armory.index_at(index=bullet_block.index).exp_range:
            return True
    return False


####################################################################################################
# Main Function
####################################################################################################
def main():
    # Global Variable
    global screen
    global player
    global enemies
    global player_armory, player_bullets
    global score
    # Running Game
    RUNNING = True
    BULLET_FIRE = False
    background_timer = time.time()
    while RUNNING:
        ################################################################################
        ################################################################################
        if time.time() - background_timer > BACKGROUND_REFRESH_TIME:
            background_timer = time.time()
            # Scroll the background
            background_rect1.y += BACKGROUND_SCROLL_SPEED
            background_rect2.y += BACKGROUND_SCROLL_SPEED
            if background_rect1.y >= SCREEN_HEIGHT:
                background_rect1.topleft = (0, 0)
            if background_rect2.y >= SCREEN_HEIGHT:
                background_rect2.topleft = (0, -SCREEN_HEIGHT)
        # Draw the background
        screen.blit(background, background_rect1)
        screen.blit(background, background_rect2)
        ################################################################################
        ################################################################################
        # Find Active Bullet
        active_bullet = player_armory.search_active()
        ################################################################################
        ################################################################################
        # Obtain Single Keyboard Event
        for event in pygame.event.get():
            # Event of Quiting
            if event.type == pygame.QUIT:
                RUNNING = False
            # Event of Key Press
            if event.type == pygame.KEYDOWN:
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
                # Weapon Switch
                elif event.key == pygame.K_1:
                    player_armory.search_active().active = False
                    player_armory.index_at(index=0).active = True
                elif event.key == pygame.K_2:
                    player_armory.search_active().active = False
                    player_armory.index_at(index=1).active = True
            # Event of Key Release
            if event.type == pygame.KEYUP:
                # Stop Player Movement
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player.x_change = 0
                if event.key == pygame.K_SPACE:
                    BULLET_FIRE = False
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
        for enemy_index in range(len(enemies)):
            current_enemy = enemies.index_at(index=enemy_index)
            if current_enemy.fire_bullet and current_enemy.active:  # When Able to Fire
                current_enemy.fire_bullet = False
                # Fire Bullet at Current Enemy Position
                enemy_bullets.append(index=current_enemy.weapon,
                                     position=current_enemy.position.copy(),
                                     contact=[list(item) for item in
                                              enemy_armory.index_at(index=current_enemy.weapon).contact])
                # Reset CoolDown
                current_enemy.cooldown = enemy_armory.index_at(index=current_enemy.weapon).cooldown
                # Set Bullet Contact
                new_bullet = enemy_bullets.get_last_element()
                for item in new_bullet.contact:
                    item[0] = new_bullet.position[0] + item[0]
                    item[1] = new_bullet.position[1] + item[1]
            else:  # When Already fired  - in cooldown
                current_enemy.cooldown -= 1
                if current_enemy.cooldown <= 0:
                    current_enemy.fire_bullet = True
        ################################################################################
        ################################################################################
        # Player Movement
        player.update()
        # Movement of Each Enemy
        for enemy_index in range(len(enemies)):
            current_enemy = enemies.index_at(index=enemy_index)
            # Enemy Self Movement
            current_enemy.update(block_size=ENEMY_SIZE)
        # Player Bullet Movement
        if len(player_bullets) > 0:
            for bullet_index in range(0, len(player_bullets)):
                bullet0 = player_bullets.get_element_at(position=bullet_index)
                if bullet0 is not None:
                    # Bullet Position
                    bullet0.position[1] -= active_bullet.speed
                    for item in bullet0.contact:
                        item[1] -= active_bullet.speed
                    # Reset Bullet
                    if bullet0.position[1] <= 0:
                        player_bullets.delete(current_bullet=bullet0)
        # Enemy Bullet Movement
        if len(enemy_bullets) > 0:
            for bullet_index in range(0, len(enemy_bullets)):
                bullet0 = enemy_bullets.get_element_at(position=bullet_index)
                if bullet0 is not None:
                    bullet0.position[1] += enemy_armory.index_at(index=bullet0.index).speed
                    for item in bullet0.contact:
                        item[1] += enemy_armory.index_at(index=bullet0.index).speed
                    if bullet0.position[1] >= SCREEN_HEIGHT:
                        enemy_bullets.delete(current_bullet=bullet0)
        ################################################################################
        ################################################################################
        # Collision of Enemy & Player Bullet
        for enemy_index in range(len(enemies)):
            current_enemy = enemies.index_at(index=enemy_index)
            # Collide only when enemy is active and there is a bullet
            if len(player_bullets) > 0 and current_enemy.active:
                for bullet_index in range(len(player_bullets)):
                    bullet0 = player_bullets.get_element_at(bullet_index)
                    if bullet0 is not None and bullet0.position[1] <= ENEMY_SPAWN[1]:
                        if collide_enemy(enemy_block=current_enemy, bullet_block=bullet0):
                            # Enemy Health Decrease
                            current_enemy.health[1] -= player_armory.index_at(index=bullet0.index).damage
                            # Enemy Health Check
                            if current_enemy.health[1] <= 0:  # Explode at Health of 0
                                current_enemy.speed = 0  # Stop Moving
                                current_enemy.image = explosion_img
                                current_enemy.explode_at = time.time()
                                current_enemy.active = False
                                current_enemy.health_show = False
                                score += 1  # Update Score
                            player_bullets.delete(current_bullet=bullet0)  # Bullet Reset after Collision
            # Reset enemy to active after some time
            if not current_enemy.active and current_enemy.explode_at is not None:
                # Reset Enemy after Explosion of EXPLOSION_TIME
                if time.time() - current_enemy.explode_at >= EXPLOSION_TIME:
                    # Reset Enemy Reset
                    enemy_reset(enemy_block=current_enemy)
        ################################################################################
        ################################################################################
        # Collision of Player & Enemy Bullet
        if len(enemy_bullets) > 0 and player.active and not player.invincible:
            for bullet_index in range(0, len(enemy_bullets)):
                bullet0 = enemy_bullets.get_element_at(position=bullet_index)
                if bullet0 is not None:
                    explosion_range = enemy_armory.index_at(index=bullet0.index).exp_range
                    danger_range = [player.position[1] - explosion_range * 2, player.position[1] + PLAYER_SIZE]
                    if danger_range[0] < bullet0.position[1] < danger_range[1]:
                        if collide_player(player_block=player, bullet_block=bullet0):
                            # Decrease Player Health
                            player.health[1] -= enemy_armory.index_at(index=bullet0.index).damage
                            # Player Health Check
                            if player.health[1] <= 0:
                                # Explode
                                player.image = explosion_img
                                player.explode_at = time.time()
                                player.active = False
                                player.health_show = False
                            enemy_bullets.delete(current_bullet=bullet0)
        # Reset After a certain time
        if not player.active and player.explode_at is not None:
            if time.time() - player.explode_at >= EXPLOSION_TIME:
                player.life[1] -= 1
                # With Lives Left
                if player.life[1] > 0:
                    player.reset()
                    player.invincible_at = time.time()
                # With No Life Left
                else:
                    RUNNING = False
        # Reset Invincibility
        if player.invincible:
            if time.time() - player.invincible_at > PLAYER_INVINCIBLE_TIME:
                player.invincible = False
        ################################################################################
        ################################################################################
        # Update Player
        show_player(player_block=player)
        # Update Enemy
        for enemy_index in range(len(enemies)):
            show_enemy(enemy_block=enemies.index_at(index=enemy_index))
        # Update Bullet when Available
        if len(player_bullets) > 0:
            for bullet_index in range(0, len(player_bullets)):
                fire_bullet_player(bullet_block=player_bullets.get_element_at(position=bullet_index))
        if len(enemy_bullets) > 0:
            for bullet_index in range(0, len(enemy_bullets)):
                fire_bullet_enemy(bullet_block=enemy_bullets.get_element_at(position=bullet_index))
        # Update Display Element
        score_text = font.render("Score: " + str(score), True, WHITE)
        screen.blit(score_text, (10, 10))
        # Update Pygame Screen
        pygame.display.update()
    # Quit
    pygame.quit()


####################################################################################################
# Main Function Runner
####################################################################################################
if __name__ == "__main__":
    main()