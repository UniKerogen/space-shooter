# Top Down Shooter Game
# A Simple Top Down Shooter for Raiden Mockup
# Version 6.2.1


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

##################################################
# Structures Setting
##################################################
# On Screen Bullet Storage
bullets = BulletList()


####################################################################################################
# Function Prototype
####################################################################################################
def show_player(player_block):
    global screen
    screen.blit(player_block.image, (player_block.position[0], player_block.position[1]))


def show_enemy(enemy_block):
    global screen
    screen.blit(enemy_block.image, (enemy_block.position[0], enemy_block.position[1]))


def fire_bullet(bullet_block):
    global screen, armory
    screen.blit(armory.search_index(index=bullet_block.index).image,
                (bullet_block.position[0], bullet_block.position[1]))


def collide(enemy_block, bullet_block):
    global armory
    for coordinates in bullet_block.contact:
        distance = (((enemy_block.position[0] + ENEMY_SIZE / 2) - coordinates[0]) ** 2 +
                    ((enemy_block.position[1] + ENEMY_SIZE / 2) - coordinates[1]) ** 2
                    ) ** 0.5
        if distance < armory.search_index(index=bullet_block.index).exp_range:
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
    global armory, bullets, BULLET_FIRE
    global score
    # Running Game
    running = True
    while running:
        # Display Background
        screen.blit(background, (0, 0))
        # Find Active Bullet
        bullet = armory.search_active()
        ################################################################################
        ################################################################################
        # Obtain Single Keyboard Event
        for event in pygame.event.get():
            # Event of Quiting
            if event.type == pygame.QUIT:
                running = False
            # Event of Key Press
            if event.type == pygame.KEYDOWN:
                # Player Movement
                if event.key == pygame.K_LEFT:
                    player.x_change = -player.speed
                elif event.key == pygame.K_RIGHT:
                    player.x_change = player.speed
                # Fire Bullet
                elif event.key == pygame.K_SPACE:
                    BULLET_FIRE = True
                # Weapon Switch
                elif event.key == pygame.K_1:
                    armory.search_active().active = False
                    armory.search_index(index=0).active = True
                elif event.key == pygame.K_2:
                    armory.search_active().active = False
                    armory.search_index(index=1).active = True
            # Event of Key Release
            if event.type == pygame.KEYUP:
                # Stop Player Movement
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player.x_change = 0
                if event.key == pygame.K_SPACE:
                    BULLET_FIRE = False
        # Continuous Shooting
        if BULLET_FIRE:
            if bullet.cooldown[1] == 0:
                # Bullet Fire at Current Player x position
                bullets.append(index=bullet.index,
                               position=[player.position[0], BULLET_ORIGIN_Y],
                               contact=[list(item) for item in bullet.contact])
                # Reset CoolDown
                bullet.cooldown[1] = bullet.cooldown[0]
                # Bullet contact set
                new_bullet = bullets.get_last_element()
                for item in new_bullet.contact:
                    item[0] = player.position[0] + item[0] - BULLET_ORIGIN_X
        # Cool Down for Bullet
        if bullet.cooldown[1] > 0:
            bullet.cooldown[1] -= 1
        ################################################################################
        ################################################################################
        # Player Movement
        player.position[0] += player.x_change
        # Check Boundary
        if player.position[0] < 0:
            player.position[0] = 0
        elif player.position[0] >= SCREEN_WIDTH - PLAYER_SIZE:
            player.position[0] = SCREEN_WIDTH - PLAYER_SIZE
        # Movement of Each Enemy
        for enemy_index in range(len(enemies)):
            current_enemy = enemies.search_index(index=enemy_index)
            current_enemy.position[0] += current_enemy.speed * current_enemy.direction
            # Far Left Side
            if current_enemy.position[0] <= BOUNDARY_LEFT:
                current_enemy.position[0] = BOUNDARY_RIGHT - ENEMY_SIZE
                current_enemy.position[1] = random.randint(ENEMY_SPAWN[0], ENEMY_SPAWN[1])
            # Far Right Side
            elif current_enemy.position[0] >= BOUNDARY_RIGHT - ENEMY_SIZE:
                current_enemy.position[0] = BOUNDARY_LEFT
                current_enemy.position[1] = random.randint(ENEMY_SPAWN[0], ENEMY_SPAWN[1])
        # Bullet movement
        if len(bullets) > 0:
            for bullet_index in range(0, len(bullets)):
                bullet0 = bullets.get_element_at(bullet_index)
                if bullet0 is not None:
                    # Bullet Position
                    bullet0.position[1] -= bullet.speed
                    for item in bullet0.contact:
                        item[1] -= bullet.speed
                    # Reset Bullet
                    if bullet0.position[1] <= 0:
                        bullets.delete(current_bullet=bullet0)
        ################################################################################
        ################################################################################
        # Collision
        for enemy_index in range(len(enemies)):
            current_enemy = enemies.search_index(enemy_index)
            # Collide only when enemy is active and there is a bullet
            if len(bullets) > 0 and current_enemy.active:
                for bullet_index in range(len(bullets)):
                    bullet0 = bullets.get_element_at(bullet_index)
                    if bullet0 is not None:
                        if collide(enemy_block=current_enemy, bullet_block=bullet0):
                            if current_enemy.active:  # Active Enemy Explode
                                current_enemy.speed = 0  # Stop Moving
                                current_enemy.image = explosion_img
                                current_enemy.explode_at = time.time()
                                current_enemy.active = False
                                score += 1  # Update Score
                            bullets.delete(bullet0)  # Bullet Reset after Collision
            # Reset enemy to active after some time
            if not current_enemy.active and current_enemy.explode_at is not None:
                # Reset Enemy after Explosion of EXPLOSION_TIME
                if time.time() - current_enemy.explode_at >= EXPLOSION_TIME:
                    current_enemy.direction = -1 if random.randint(0, 1) == 0 else 1
                    if current_enemy.direction == -1:
                        current_enemy.position = [BOUNDARY_RIGHT - ENEMY_SIZE,
                                                  random.randint(ENEMY_SPAWN[0], ENEMY_SPAWN[1])]
                    else:
                        current_enemy.position = [BOUNDARY_LEFT,
                                                  random.randint(ENEMY_SPAWN[0], ENEMY_SPAWN[1])]
                    current_enemy.speed = random.randint(1, ENEMY_SPEED_MAX) / 1000
                    current_enemy.image = enemy_img[random.randint(0, ENEMY_TYPE - 1)]
                    current_enemy.active = True
                    current_enemy.explode = None

        ########################################
        ########################################
        # Update Player
        show_player(player_block=player)
        # Update Enemy
        for enemy_index in range(len(enemies)):
            show_enemy(enemy_block=enemies.search_index(index=enemy_index))
        # Update Bullet when Available
        if len(bullets) > 0:
            for bullet_index in range(0, len(bullets)):
                bullet0 = bullets.get_element_at(bullet_index)
                fire_bullet(bullet_block=bullet0)
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
