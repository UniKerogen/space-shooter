# Structure File
# Version - Beta 5
# A Modified Linked List for Storage

from settings import *
import multiprocessing
import pygame
import random
import threading
import time
import warnings


##################################################
# Class Prototype - Player
##################################################
class PlayerBlock:
    def __init__(self, name, position, image, speed, health):
        # Input Information
        self.name = name
        self.position = position  # Player Position
        self.image = image  # Player Image
        self.speed = speed  # Player Speed
        self.health = [health, health]  # Player Health
        # Self Start Element
        self.center = [sum(x) for x in zip(position, [PLAYER_SIZE / 2, PLAYER_SIZE / 2])]
        # Background Information
        self.hit_range = round(PLAYER_SIZE / 2 * PLAYER_HIT_RANGE)  # Player Got Hit Range
        self.shield = 0  # Player Shield
        self.shield_image = None  # Player Shield Image
        self.invincible = False  # Player Invincible
        self.invincible_image = None
        self.health_show = True  # Display Player Health
        self.active = True  # Player Active or Not
        self.life = [PLAYER_LIFE, PLAYER_LIFE]  # Player Life
        self.explode_at = None  # Player Exploded or Not
        self.invincible_at = None  # Player Invincible Timer
        self.health_bar = PLAYER_HEALTH_BAR  # Player Health Bar Size
        self.always_invincible = False  # Player Invincible Cheat
        self.size = PLAYER_SIZE  # Player Size
        # Storage Information
        self.x_change = 0  # Player Horizontal Move Value
        self.y_change = 0  # Player Vertical Move Value
        # Weapon System
        self.weapon_amount = (1, 1, 1, 1, 2, 2, 2, 0, 0, 1)
        self.fire_shift = [(0, 0)] * 10
        self.fire_shift[4] = ((0, 0), (24, 0))
        self.fire_shift[5] = ((0, 0), (44, 0))
        self.fire_shift[6] = ((0, 0), (56, 0))
        self.fire_shift = tuple(self.fire_shift)
        # Rocket Storage
        self.rocket = [0, 0]
        self.rocket_cooldown = [0, 0]
        # Save Input Data
        self.data = [name, position, image, speed, health]

    # Update Center
    def update(self):
        # Update Position & Center
        self.position[0] += self.x_change
        self.position[1] += self.y_change
        self.center = [sum(x) for x in zip(self.position, [PLAYER_SIZE / 2, PLAYER_SIZE / 2])]
        # Check Boundary - Horizontal
        if self.position[0] < 0:
            self.position[0] = 0
        elif self.position[0] >= SCREEN_WIDTH - PLAYER_SIZE:
            self.position[0] = SCREEN_WIDTH - PLAYER_SIZE
        # Check Boundary - Vertical
        if self.position[1] < PLAYER_Y_RANGE[0]:
            self.position[1] = PLAYER_Y_RANGE[0]
        elif self.position[1] >= PLAYER_Y_RANGE[1]:
            self.position[1] = PLAYER_Y_RANGE[1]
        # Rocket Cooldown
        for rocket_index in range(0, len(self.rocket_cooldown)):
            if self.rocket_cooldown[rocket_index] > 0:
                self.rocket_cooldown[rocket_index] -= 1

    # Reset Player
    def reset(self):
        self.name = self.data[0]
        self.position = self.data[1]
        self.image = self.data[2]
        self.speed = self.data[3]
        self.health = [self.data[4], self.data[4]]
        self.rocket = [0, 0]
        self.invincible = True
        self.explode_at = None
        self.active = True
        self.health_show = True


##################################################
# Class Prototype - Bullet
##################################################
class BulletBlock:
    def __init__(self, index, position, contact, armory):
        # Linkage
        self.next = None
        # Information
        self.index = index  # Bullet Index
        self.position = position  # Bullet Position
        self.contact = contact  # Bullet Contact Point
        # Self Start Information
        self.speed = armory.index_at(index=index).speed  # Bullet Speed
        self.damage = armory.index_at(index=index).damage  # Bullet Damage
        self.image = armory.index_at(index=index).image  # Bullet Image


class BulletList:
    def __init__(self):
        self.head = None

    # Length of the List
    def __len__(self):
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count

    def append(self, index, position, contact, armory):
        new_node = BulletBlock(index=index, position=position, contact=contact, armory=armory)
        if not self.head:
            self.head = new_node
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node

    def delete(self, current_bullet):
        if not self.head:
            return
        if self.head == current_bullet:
            self.head = self.head.next
            return
        current = self.head
        while current.next:
            if current.next == current_bullet:
                current.next = current.next.next
                return
            current = current.next

    def get_element_at(self, position):
        if position < 0:
            return None  # Invalid position
        current = self.head
        index = 0
        while current:
            if index == position:
                return current  # Return the data at the specified position
            current = current.next
            index += 1
        return None  # Position out of range

    # Delete All Elements
    def delete_list(self):
        self.head = None


##################################################
# Class Prototype - Amory
##################################################
class AmoryBlock:
    def __init__(self, name, index, position, speed, exp_range, contact, active, image, cooldown, damage):
        # Linkage
        self.next = None
        # Format Data
        self.name = name
        self.index = index  # Weapon Index
        self.position = position  # Image Position at Top Left
        self.speed = speed  # Movement Speed
        self.exp_range = exp_range  # Bullet Explosion Range Shift
        self.contact = tuple(tuple(i) for i in contact) if contact is not None else None  # Contact Point - Calculation
        self.active = active  # Bullet Status
        self.image = image  # Bullet Image
        self.cooldown = cooldown  # Bullet CoolDown
        self.damage = damage  # Bullet Damage


class Armory:
    def __init__(self):
        self.armory_dict = {}

    # Add Element at the end
    def append(self, name, index, position, speed, exp_range, contact, active, image, cooldown, damage):
        new_weapon = AmoryBlock(name, index, position, speed, exp_range, contact, active, image, cooldown, damage)
        self.armory_dict[new_weapon.index] = new_weapon

    # Search via Index - Return Bullet Block
    def index_at(self, index):
        if index in self.armory_dict:
            return self.armory_dict.get(index)
        return False

    # Search via Active - Return Bullet Block
    def search_active(self):
        active_list = []
        for armory_index in self.armory_dict:
            if self.armory_dict.get(armory_index).active:
                active_list.append(armory_index)
        return active_list


##################################################
# Class Prototype - Enemy
##################################################
class EnemyBlock:
    def __init__(self, name, index, position, speed, active, image, health, direction, weapon, hit_range):
        self.name = name
        self.index = index  # Enemy Index
        # To Update Element
        self.direction = direction  # Enemy Move Direction
        self.position = position  # Enemy Position
        self.center = [sum(x) for x in zip(position, [ENEMY_SIZE / 2, ENEMY_SIZE / 2])]
        self.speed = speed  # Enemy Speed
        self.active = active  # Enemy Active or Not
        self.image = image  # Enemy Image
        self.health = [health, health]  # Enemy Health
        self.weapon = weapon  # Enemy Weapon
        self.hit_range = round(hit_range)  # Enemy Got Hit Range
        self.size = ENEMY_SIZE
        # Self Start Element
        self.explode_at = None  # Enemy Exploded or not
        self.health_show = True  # Show Enemy Health
        self.fire_cooldown = 0  # Enemy Firing Cooldown
        self.indicator3 = None  # Weapon 3 Indicator
        self.indicator3_shift = None  # Weapon 3 Indicator Shift
        # Connection
        self.next = None
        # Boss Configuration
        self.y_axis = None  # Enemy Target Y Axis
        self.each_weapon_amount = None  # Enemy Each Weapon Amount
        self.fire_shift = None  # Enemy Fire Weapon Shift


class EnemyList:
    def __init__(self):
        self.head = None
        self.hash_index = {}
        self.last_add = None

    def __len__(self):
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count

    def append(self, name, index, position, speed, active, image, health, direction, weapon, hit_range):
        new_node = EnemyBlock(name, index, position, speed, active, image, health, direction, weapon, hit_range)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        # Update Hash Table
        self.hash_index[index] = new_node
        self.last_add = index

    # Search via Index
    def index_at(self, index):
        if index < len(self.hash_index):
            return self.hash_index.get(index)
        return False

    # Delete a Enemy
    def delete(self, enemy_block):
        if not self.head:
            return
        if self.head == enemy_block:
            self.head = self.head.next
            return
        current = self.head
        while current.next:
            if current.next == enemy_block:
                current.next = current.next.next
                return
            current = current.next
        # Delete Hash Table Entry
        del self.hash_index[enemy_block.index]

    def get_last_index(self):
        if len(self.hash_index) == 0:
            return 0
        else:
            return self.last_add

    # Delete All Elements
    def delete_list(self):
        self.head = None
        self.hash_index = {}


##################################################
# Class Prototype - Create
##################################################
class Crate:
    def __init__(self, category, position):
        # Input Element
        self.category = category  # Crate Category
        self.position = position  # Crate Position
        self.next = None
        # Self Start Element
        if self.category == 0:  # Add Life - 10 Chance
            self.info = 1
            self.image = 'resources/crate/life_crate.png'
        elif self.category == 1:  # Invincible - 20 Chance
            self.info = PLAYER_INVINCIBLE_TIME
            self.image = 'resources/crate/invincible_crate.png'
        elif self.category == 2:  # Clear All Enemy Bullet - 30 Chance
            self.info = 0
            self.image = 'resources/crate/clear_bullet_crate.png'
        elif self.category == 3 :  # Rocket Crate - 40 Chance
            self.info = random.randint(0, ROCKET_TYPE)
            self.image = 'resources/crate/rocket' + str(self.info) + '.png'
        elif self.category == 4:  # Weapon Crate - 50 Chance
            self.info = random.randint(0, BULLET_TYPE)
            self.image = 'resources/crate/bullet' + str(self.info) + '.png'
        elif self.category == 5:  # Shield - 60 Chance
            self.info = random.randint(CRATE_SHIELD[0], CRATE_SHIELD[1])
            self.image = 'resources/crate/shield_crate.png'
        elif self.category == 6:  # Health - 70 Chance
            self.info = random.randint(CRATE_HEALTH[0], CRATE_HEALTH[1])
            self.image = 'resources/crate/health_crate.png'
        # Storage
        self.contact = [sum(x) for x in zip(position, [CRATE_SIZE / 2, CRATE_SIZE / 2])]  # Crate Contact Point
        self.direction = 1 if random.randint(0, 1) == 0 else -1  # Crate Move Direction
        self.collect_range = CRATE_COLLECT_RANGE  # Crate Collecting Range


class CrateList:
    def __init__(self):
        self.head = None

    def __len__(self):
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count

    def append(self, category, position):
        new_node = Crate(category, position)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

    # Delete a Crate
    def delete(self, crate_block):
        if not self.head:
            return
        if self.head == crate_block:
            self.head = self.head.next
            return
        current = self.head
        while current.next:
            if current.next == crate_block:
                current.next = current.next.next
                return
            current = current.next


##################################################
# Class Prototype - Button
##################################################
class Button:
    def __init__(self, name):
        self.name = name
        # Image
        self.image = pygame.image.load('resources/button/button_' + str(name) + '.png')
        self.image_hovered = pygame.image.load('resources/button/button_' + str(name) + '_hovered.png')
        # Image Rect
        self.rect = self.image.get_rect()
        # Connect
        self.next = None
        # Self Identifier
        self.hovered = False

    # Show Button
    def draw(self):
        if self.hovered:
            return self.image_hovered
        else:
            return self.image


class ButtonList:
    def __init__(self):
        self.button_set = []
        self.button_names = []

    def append(self, name):
        self.button_set.append(Button(name=name))
        self.button_names.append(name)

    def name(self, name):
        if name in self.button_names:
            return self.button_set[self.button_names.index(name)]
        return False


##################################################
# Image Storage Function
##################################################
class ImageBlock:
    def __init__(self, name, number):
        self.name = name
        self.number = number
        self.image = 'resources/explosion/explosion' + str(number) + ".png"


class ImageList:
    def __init__(self):
        self.image_set = ()

    def append(self, name, number):
        self.image_set += (ImageBlock(name=name, number=number), )

    def get(self):  # Select a random explosion image from list
        return self.image_set[random.randint(0, len(self.image_set) - 1)].image

##################################################
# Class Prototype - Controller
##################################################
class Controller:
    def __init__(self, name, status=False):
        self.name = name
        self.status = status

    def on(self):
        self.status = True

    def off(self):
        self.status = False

class ControllerSet:
    def __init__(self):
        self.controller_set = []
        self.controller_name = []

    def fuse(self, name, status=False):
        self.controller_set.append(Controller(name=name, status=status))
        self.controller_name.append(name)

    def on(self, name):
        if name in self.controller_name:
            # Turn on/off controller
            for controller in self.controller_set:
                if controller.name == name:
                    controller.on()
                else:
                    controller.off()
        else:
            # Turn off all controller
            for controller in self.controller_set:
                controller.off()
            warnings.warn("Unable to find controller with the name " + name)

    def is_on(self, name):
        if name in self.controller_name:
            return self.controller_set[self.controller_name.index(name)].status


##################################################
# Class Prototype - Threading Controller
##################################################
class ThreadController:
    def __init__(self):
        self.threads = []
        self.start_time = None

    def fuse(self, target):
        self.threads.append(threading.Thread(target=target))

    def empty(self):
        self.threads = []
        self.start_time = None

    def initiate(self, empty=True, show_time=False):
        self.start_time = time.time()
        # Start Threads
        for t in self.threads:
            t.start()
        # Wait for Completion
        for t in self.threads:
            t.join()
        # Show Time
        if show_time:
            print("Threading Time: " + str(time.time() - self.start_time))
        # Empty Threads
        if empty:
            self.empty()


##################################################
# Class Prototype - Multi Processing Controller
##################################################
class ProcessingController:
    def __init__(self):
        self.processes = []
        self.start_time = None

    def fuse(self, target, args):
        self.processes.append(multiprocessing.Process(target=target, args=args))

    def empty(self):
        self.processes = []
        self.start_time = None

    def initiate(self, empty=True, show_time=False):
        self.start_time = time.time()
        # Start Process
        for p in self.processes:
            p.start()
        # Wait for Completion
        for p in self.processes:
            p.join()
        # Show Time
        if show_time:
            print("Process Time: " + str(time.time() - self.start_time))
        # Empty Processes
        if empty:
            self.empty()

##################################################
# Main Function
##################################################
def main():
    print("This is a storage for Structures!")


##################################################
# Main Function Runner
##################################################
if __name__ == "__main__":
    main()
