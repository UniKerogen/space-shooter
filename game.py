# Top Down Shooter Game
# A Simple Top Down Shooter for Raiden Mockup
# Version 5.0
# Add Weapon Switch


##################################################
# Libraries
##################################################
import pygame
import random
import time

from structures import *
from settings import *

##################################################
# Variable Definition
##################################################
# Settings
# Initialize Pygame
pygame.init()
# Create Screen
screen = pygame.display.set_mode(size=(SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Top-Down Shooter")
# Score System
font = pygame.font.Font(None, 24)
score = 0
# Player Value
player_img = pygame.image.load('resources/player.png')
player_x = SCREEN_WIDTH // 2 - PLAYER_SIZE / 2  # Middle of Screen
player_y = SCREEN_HEIGHT - 128  # Manually Set
player_x_change = 0
# Explosion
EXPLOSION_TIME = 0.5  # second
explosion_img = pygame.image.load('resources/explosion.png')
# Enemy
enemy_img = []
for i in range(ENEMY_TYPE):
    file = 'resources/enemy' + str(i) + '.png'
    enemy_img.append(pygame.image.load(file))
# Enemy Cask - [x, y, type, speed]
enemy_list = CaskList()
for num_enemy in range(ENEMY_NUMBER):
    enemy_list.append(data='enemy' + str(num_enemy), index=num_enemy,
                      position=[random.randint(0, SCREEN_WIDTH - ENEMY_SIZE),
                                random.randint(ENEMY_SPAWN[0], ENEMY_SPAWN[1])],
                      speed=random.randint(1, ENEMY_SPEED_MAX) / 1000,
                      active=True,
                      image=enemy_img[random.randint(0, ENEMY_TYPE - 1)],
                      range=None,
                      contact=None)
# Bullet
BULLET_ORIGIN_X = player_x
BULLET_ORIGIN_Y = player_y
bullet_state = 'ready'
# Bullet Cask
bullet_list = CaskList()
bullet_list.append(data='bullet0', index=0, position=[BULLET_ORIGIN_X, BULLET_ORIGIN_Y],
                   speed=BULLET_SPEED_BASE,
                   range=BULLET_EXPLOSION_RANGE,
                   contact=[[BULLET_ORIGIN_X + 28, BULLET_ORIGIN_Y + 30], [BULLET_ORIGIN_X + 32, BULLET_ORIGIN_Y + 30]],
                   active=True,
                   image=pygame.image.load('resources/bullet0.png'))
bullet_list.append(data='bullet1', index=1, position=[BULLET_ORIGIN_X, BULLET_ORIGIN_Y],
                   speed=BULLET_SPEED_BASE,
                   range=BULLET_EXPLOSION_RANGE * 0.8,
                   contact=[[BULLET_ORIGIN_X + 18, BULLET_ORIGIN_Y + 23], [BULLET_ORIGIN_X + 42, BULLET_ORIGIN_Y + 23]],
                   active=False,
                   image=pygame.image.load('resources/bullet1.png'))
# Background
background = pygame.image.load('resources/background.png')

##################################################
# Class Prototype
##################################################


##################################################
# Function Prototype
##################################################
def player(x, y):
    global screen, player_img
    screen.blit(player_img, (x, y))


def enemy(enemy_node):
    global screen
    screen.blit(enemy_node.image, (enemy_node.position[0], enemy_node.position[1]))


def fire_bullet(bullet):
    global bullet_state, screen
    bullet_state = 'fire'
    screen.blit(bullet.image, (bullet.position[0], bullet.position[1]))


def collide(enemy_x, enemy_y, bullet_x, bullet_y, explosion_range):
    distance = (((enemy_x + ENEMY_SIZE / 2) - (bullet_x)) ** 2 +
                ((enemy_y + ENEMY_SIZE / 2) - (bullet_y)) ** 2
                ) ** 0.5
    return distance < explosion_range


##################################################
# Main Function
##################################################
def main():
    # Global Variable
    global screen
    global player_x, player_y, player_x_change
    global enemy_list
    global bullet_list, bullet_state
    global score
    # Running Game
    running = True
    while running:
        # Display Background
        screen.blit(background, (0, 0))
        # FInd Active Bullet
        bullet = bullet_list.search_active()
        # Obtain Keyboard Event
        for event in pygame.event.get():
            # Event of Quiting
            if event.type == pygame.QUIT:
                running = False
            # Event of Key Press
            if event.type == pygame.KEYDOWN:
                # Player Movement
                if event.key == pygame.K_LEFT:
                    player_x_change = -PLAYER_SPEED
                elif event.key == pygame.K_RIGHT:
                    player_x_change = PLAYER_SPEED
                # Fire Bullet
                elif event.key == pygame.K_SPACE and bullet_state == 'ready':
                    # Bullet Fire at Current Player_X
                    bullet.position[0] = player_x
                    # Bullet contact set
                    for item in bullet.contact:
                        item[0] = player_x + item[0] - BULLET_ORIGIN_X
                    fire_bullet(bullet=bullet)
                # Weapon Switch
                elif event.key == pygame.K_1:
                    bullet_list.search_active().active = False
                    bullet_list.search_index(index=0).active = True
                elif event.key == pygame.K_2:
                    bullet_list.search_active().active = False
                    bullet_list.search_index(index=1).active = True
            # Event of Key Release
            if event.type == pygame.KEYUP:
                # Stop Player Movement
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player_x_change = 0
        # Player Movement
        player_x += player_x_change
        # Check Boundary
        if player_x < 0:
            player_x = 0
        elif player_x >= SCREEN_WIDTH - 64:
            player_x = SCREEN_WIDTH - 64
        # Movement of Each Enemy
        for enemy_index in range(enemy_list.length()):
            current_enemy = enemy_list.search_index(index=enemy_index)
            current_enemy.position[0] += current_enemy.speed
            if current_enemy.position[0] >= SCREEN_WIDTH - ENEMY_SIZE:
                current_enemy.position[0] = 0
                current_enemy.position[1] = random.randint(ENEMY_SPAWN[0], ENEMY_SPAWN[1])
        # Bullet movement
        if bullet_state == "fire":
            # Bullet Position
            bullet.position[1] -= bullet.speed
            for item in bullet.contact:
                item[1] -= bullet.speed
            fire_bullet(bullet=bullet)
            # Reset Bullet
            if bullet.position[1] <= 0:
                bullet_state = "ready"
                bullet.position[1] = player_y
                bullet.contact_reset()
        # Collision
        for enemy_index in range(enemy_list.length()):
            current_enemy = enemy_list.search_index(enemy_index)
            for contact_point in bullet.contact:
                collided = collide(enemy_x=current_enemy.position[0], enemy_y=current_enemy.position[1],
                                   bullet_x=contact_point[0], bullet_y=contact_point[1],
                                   explosion_range=bullet.range)
                if collided:
                    # Explosion
                    if current_enemy.active:
                        current_enemy.speed = 0  # Stop Moving
                        current_enemy.image = explosion_img
                        current_enemy.range = time.time()
                        current_enemy.active = False
                        # Update Score
                        score += 1
                    # Bullet Reset after Collision
                    bullet.position[1] = SCREEN_HEIGHT - 64
                    bullet_state = 'ready'
                    bullet.contact_reset()
                if current_enemy.range is not None:
                    # Reset Enemy after Explosion of EXPLOSION_TIME
                    if time.time() - current_enemy.range >= EXPLOSION_TIME:
                        current_enemy.position = [0, random.randint(ENEMY_SPAWN[0], ENEMY_SPAWN[1])]
                        current_enemy.speed = random.randint(1, ENEMY_SPEED_MAX) / 1000
                        current_enemy.image = enemy_img[random.randint(0, ENEMY_TYPE - 1)]
                        current_enemy.active = True
                        current_enemy.range = None
        # Update New Location
        player(player_x, player_y)
        for enemy_index in range(enemy_list.length()):
            enemy(enemy_node=enemy_list.search_index(index=enemy_index))
        # Update Display Element
        score_text = font.render("Score: " + str(score), True, WHITE)
        screen.blit(score_text, (10, 10))
        # Update Pygame Screen
        pygame.display.update()
        # Break Point
    # Quit
    pygame.quit()


##################################################
# Main Function Runner
##################################################
if __name__ == "__main__":
    main()
