# Top Down Shooter Game
# A Simple Top Down Shooter for Raiden Mockup
# Version - Alpha 9


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
# Background
background = pygame.image.load('resources/background.png')
background_rect1 = background.get_rect()
background_rect2 = background.get_rect()
background_rect3 = background.get_rect()
background_rect1.topleft = (0, 0)
background_rect2.topleft = (0, -SCREEN_HEIGHT)
background_rect3.topleft = (0, -SCREEN_HEIGHT * 2)


##################################################
# Structures Setting
##################################################


####################################################################################################
# Function Prototype
####################################################################################################
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
        if enemy_block.weapon == 3 and enemy_block.explode_at is None:
            screen.blit(enemy_block.indicator, (enemy_block.position[0], enemy_block.position[1]))
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
    screen.blit(player_armory.index_at(index=bullet_block.index).image,
                (bullet_block.position[0], bullet_block.position[1]))


# Enemy Fire Bullet
def fire_bullet_enemy(bullet_block):
    # noinspection PyGlobalUndefined
    global screen, enemy_armory
    screen.blit(enemy_armory.index_at(index=bullet_block.index).image,
                (bullet_block.position[0], bullet_block.position[1]))


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
                    current_block.health[1] -= player_armory.index_at(index=current_bullet.index).damage
                    # Health Check
                    if current_block.health[1] <= 0:
                        current_block.speed = 0  # Stop Moving
                        current_block.explode_at = time.time()  # Set Explosion Time
                        current_block.active = False  # De-active block
                        current_block.health_show = False  # Hide Health Bar
                        # Update Score and Crate
                        if spawn == ENEMY_SPAWN:
                            score += 1
                            current_block.image = pygame.transform.scale(explosion.get(), (ENEMY_SIZE, ENEMY_SIZE))  # Set Explosion Image
                        elif spawn == MINI_BOSS_SPAWN:
                            score += 5
                            current_block.image = pygame.transform.scale(explosion.get(), (MINI_BOSS_SIZE, MINI_BOSS_SIZE))
                            crate_generate(enemy_block=current_block, chance=100)  # Additional Crate
                        elif spawn == BIG_BOSS_SPAWN:
                            score += 15
                            current_block.image = pygame.transform.scale(explosion.get(), (BIG_BOSS_SIZE, BIG_BOSS_SIZE))
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


# Continuous Shooting - TODO Continuous Shooting General Function
def enemy_shooting(block_list):
    print("Here")


####################################################################################################
# Main Function
####################################################################################################
def main():
    # Global Variable
    global screen, score, crates
    global player
    global enemies, miniboss, bosses
    global player_armory, player_bullets, enemy_bullets
    global BULLET_FIRE, end_screen
    ################################################################################
    ################################################################################
    # Mini Boss Spawn
    if score > 0 and score % 100 % 30 == 0 and len(miniboss) == 0:
        miniboss_create()
    # Boss Spawn - TODO Boss not spawn with score jump i.e. 98 -> 103
    if score > 0 and score % 100 == 0 and len(bosses) == 0:
        boss_create()
    ################################################################################
    ################################################################################
    # Find Active Bullet
    active_bullet = player_armory.search_active()
    ################################################################################
    ################################################################################
    # Continuous Shooting - Player
    if BULLET_FIRE and player.active:
        if active_bullet.cooldown[1] <= 0:
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
                weapon_index = current_miniboss.weapon.index(current_weapon)
                if current_miniboss.fire_cooldown[weapon_index] <= 0:
                    for shot_number in range(current_miniboss.each_weapon_amount[current_weapon]):
                        if current_miniboss.each_weapon_amount[current_weapon] > 1:
                            fire_shift = current_miniboss.fire_shift[current_weapon][shot_number]
                            fire_position = [sum(x) for x in zip(current_miniboss.position, fire_shift)]
                        else:
                            fire_shift = current_miniboss.fire_shift[current_weapon]
                            fire_position = [sum(x) for x in zip(current_miniboss.position, fire_shift)]
                        contact_point = [list(item) for item in enemy_armory.index_at(index=current_weapon).contact]
                        contact_point = [[sum(x) for x in zip(item, fire_position)] for item in contact_point]
                        # Add Enemy Bullet
                        enemy_bullets.append(index=current_weapon, position=fire_position, contact=contact_point)
                    # Reset Cooldown
                    current_miniboss.fire_cooldown[
                        current_miniboss.weapon.index(current_weapon)] = enemy_armory.index_at(
                        index=current_weapon).cooldown
                else:
                    current_miniboss.fire_cooldown[weapon_index] -= 1
        # Next Miniboss
        current_miniboss = current_miniboss.next
    ################################################################################
    ################################################################################
    # Continuous Shooting - Big Boss
    current_boss = bosses.head
    while current_boss:
        if current_boss.active:
            # Fire Bullet at current big boss position
            for current_weapon in current_boss.weapon:
                weapon_index = current_boss.weapon.index(current_weapon)
                if current_boss.fire_cooldown[weapon_index] <= 0:
                    for shot_number in range(current_boss.each_weapon_amount[current_weapon]):
                        if current_boss.each_weapon_amount[current_weapon] > 1:
                            fire_shift = current_boss.fire_shift[current_weapon][shot_number]
                        else:
                            fire_shift = current_boss.fire_shift[current_weapon]
                        fire_position = [sum(x) for x in zip(current_boss.position, fire_shift)]
                        contact_point = [list(item) for item in enemy_armory.index_at(index=current_weapon).contact]
                        contact_point = [[sum(x) for x in zip(item, fire_position)] for item in contact_point]
                        # Add Enemy Bullet
                        enemy_bullets.append(index=current_weapon, position=fire_position, contact=contact_point)
                    # Reset Cooldown
                    current_boss.fire_cooldown[current_boss.weapon.index(current_weapon)] = enemy_armory.index_at(
                        index=current_weapon).cooldown
                else:
                    current_boss.fire_cooldown[weapon_index] -= 1
        # Next Big Boss
        current_boss = current_boss.next
    ################################################################################
    ################################################################################
    # Player Movement
    player.update()
    # Movement of Each Enemy
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
            if current_bullet.index == 3:  # Special Case of Type 3 Weapon
                item[1] = player.center[1]
            else:
                item[1] += enemy_armory.index_at(index=current_bullet.index).speed
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
        # Set Danger Zone
        if current_bullet.index == 3:
            danger_range = [0, SCREEN_HEIGHT - ENEMY_SIZE]
        else:
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
                end_screen = True
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
    enemy_exist = False
    intro_screen, end_screen, score_board, error_screen, level_screen = True, False, False, False, False
    background_timer = time.time()
    # Storage
    highest_score = 0
    level_set = 0
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
                    level_screen = True
                elif intro_screen and buttons.name('endless').rect.collidepoint(event.pos):
                    intro_screen = False
                # End Screen
                elif end_screen and buttons.name('restart').rect.collidepoint(event.pos):
                    # Restart Endless Run
                    end_screen = False
                    # Reset Player
                    score = 0
                    player.life[1] = player.life[0]
                    player.reset()
                    player.invincible_at = time.time()
                    # Reset Enemy and Bullets
                    reset_screen()
                    enemy_exist = False
                elif end_screen and buttons.name('main_menu').rect.collidepoint(event.pos):
                    # Back to Main Menu/Intro Menu
                    end_screen = False
                    intro_screen = True
                elif end_screen and buttons.name('score_board').rect.collidepoint(event.pos):
                    # Show Score Board
                    end_screen = False
                    score_board = True
                elif end_screen and buttons.name('quit').rect.collidepoint(event.pos):
                    # Quit Game
                    RUNNING = False
                # Score Board Screen
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
                # Level Screen
                elif level_screen:
                    if buttons.name('easy').rect.collidepoint(event.pos):
                        level_set = 1
                        level_screen = False
                    elif buttons.name('medium').rect.collidepoint(event.pos):
                        level_set = 2
                        level_screen = False
                    elif buttons.name('hard').rect.collidepoint(event.pos):
                        level_set = 3
                        level_screen = False
                    elif buttons.name('hell').rect.collidepoint(event.pos):
                        level_set = 4
                        level_screen = False
                    elif buttons.name('score_board').rect.collidepoint(event.pos):
                        level_screen = False
                        intro_screen = True
                    elif buttons.name('quit').rect.collidepoint(event.pos):
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
                elif event.key == pygame.K_0 and not intro_screen:
                    player_armory.search_active().active = False
                    player_armory.index_at(index=10).active = True
                # Always Invincible
                elif event.key == pygame.K_9 and not intro_screen:
                    player.always_invincible = not player.always_invincible
                    player.invincible = not player.invincible
            # Event of Key Release
            if event.type == pygame.KEYUP and not intro_screen and not end_screen:
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
            score_text_end = font36.render("Score : " + str(score), True, WHITE)
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
            # Show Score Board - TODO Show Multiple High Scores
            highest_score = score if highest_score < score else highest_score
            score_board_text = font36.render("Current High Score : " + str(highest_score), True, WHITE)
            score_board_text_rect = score_board_text.get_rect()
            score_board_text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)
            screen.blit(score_board_text, score_board_text_rect)
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
        elif level_screen:  # Level Selection - TODO Create Level Selection Screen
            # Show Title
            level_title = font36.render("Select Level", True, WHITE)
            level_title_rect = level_title.get_rect()
            level_title_rect.center = (200, 150)
            screen.blit(level_title, level_title_rect)
            # Show Button
            screen.blit(buttons.name('easy').image, buttons.name('easy').rect.topleft)
            screen.blit(buttons.name('medium').image, buttons.name('medium').rect.topleft)
            screen.blit(buttons.name('hard').image, buttons.name('hard').rect.topleft)
            screen.blit(buttons.name('hell').image, buttons.name('hell').rect.topleft)
            screen.blit(buttons.name('main_menu').image, buttons.name('score_board').rect.topleft)
            screen.blit(buttons.name('quit').image, buttons.name('quit').rect.topleft)
        ################################################################################
        ################################################################################
        else:  # Normal Game
            # Generate Enemy - Level Selection
            if not enemy_exist:
                if level_set == 1:  # Easy Mode
                    enemy_generate(number=2)
                elif level_set == 2:  # Medium Mode
                    enemy_generate(number=5)
                elif level_set == 3:  # Hard Mode
                    enemy_generate(number=8)
                elif level_set == 4:  # Death Mode
                    enemy_generate(number=12)
                else:  # Default Mode
                    enemy_generate(number=ENEMY_NUMBER)
                enemy_exist = True
            # Endless Run
            main()  # Main Game Function - Endless Run
        # Update Pygame Screen
        pygame.display.update()
    # Store and Update Scores - TODO Update and store highest scores

    # Exit Game
    pygame.quit()
