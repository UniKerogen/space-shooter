# Structure File
# Version - Alpha 9
# A Modified Linked List for Storage

from settings import *
import random
import pygame


##################################################
# Class Prototype - Player
##################################################
class PlayerBlock:
    def __init__(self, name, position, image, speed, health):
        # Input Information
        self.name = name
        self.position = position
        self.image = image
        self.speed = speed
        self.health = [health, health]
        # Self Start Element
        self.center = [sum(x) for x in zip(position, [PLAYER_SIZE / 2, PLAYER_SIZE / 2])]
        # Background Information
        self.hit_range = round(PLAYER_SIZE / 2 * PLAYER_HIT_RANGE)
        self.shield = 0
        self.shield_image = None
        self.invincible = False
        self.invincible_image = None
        self.health_show = True
        self.active = True
        self.life = [3, 3]
        self.explode_at = None
        self.invincible_at = None
        self.health_bar = PLAYER_HEALTH_BAR
        self.always_invincible = False
        # Storage Information
        self.x_change = 0
        # Save Input Data
        self.data = [name, position, image, speed, health]

    # Update Center
    def update(self):
        self.position[0] += self.x_change
        self.center = [sum(x) for x in zip(self.position, [PLAYER_SIZE / 2, PLAYER_SIZE / 2])]
        # Check Boundary
        if self.position[0] < 0:
            self.position[0] = 0
        elif self.position[0] >= SCREEN_WIDTH - PLAYER_SIZE:
            self.position[0] = SCREEN_WIDTH - PLAYER_SIZE

    # Reset Player
    def reset(self):
        self.name = self.data[0]
        self.position = self.data[1]
        self.image = self.data[2]
        self.speed = self.data[3]
        self.health = [self.data[4], self.data[4]]
        self.invincible = True
        self.explode_at = None
        self.active = True
        self.health_show = True


##################################################
# Class Prototype - Bullet
##################################################
class BulletBlock:
    def __init__(self, index, position, contact):
        # Linkage
        self.next = None
        # Information
        self.index = index
        self.position = position
        self.contact = contact


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

    def append(self, index, position, contact):
        new_node = BulletBlock(index=index, position=position, contact=contact)
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

    def get_last_element(self):
        if not self.head:
            return None  # The list is empty
        current = self.head
        while current.next:
            current = current.next
        return current

    # Delete All Elements
    def delete_list(self):
        current = self.head
        while current:
            previous = current.next
            del current.index
            del current.position
            del current.contact
            del current.next
            current = previous
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
        self.head = None

    # Length of the List
    def __len__(self):
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count

    # Add Element at the end
    def append(self, name, index, position, speed, exp_range, contact, active, image, cooldown, damage):
        new_node = AmoryBlock(name, index, position, speed, exp_range, contact, active, image, cooldown, damage)
        if not self.head:
            self.head = new_node
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node

    # Search via Index
    def index_at(self, index):
        current = self.head
        while current:
            if current.index == index:
                return current
            current = current.next
        return False

    # Search via Active
    def search_active(self):
        current = self.head
        while current:
            if current.active:
                return current
            current = current.next
        return self.head


##################################################
# Class Prototype - Enemy
##################################################
class EnemyBlock:
    def __init__(self, name, index, position, speed, active, image, health, direction, weapon, hit_range):
        self.name = name
        self.index = index
        # To Update Element
        self.direction = direction
        self.position = position
        self.center = [sum(x) for x in zip(position, [ENEMY_SIZE / 2, ENEMY_SIZE / 2])]
        self.speed = speed
        self.active = active
        self.image = image
        self.health = [health, health]
        self.weapon = weapon
        self.hit_range = round(hit_range)
        # Self Start Element
        self.explode_at = None
        self.health_show = True
        self.fire_cooldown = 0
        self.indicator = None
        # Connection
        self.next = None
        # Boss Configuration
        self.y_axis = None
        self.each_weapon_amount = None
        self.fire_shift = None


class EnemyList:
    def __init__(self):
        self.head = None

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

    # Search via Index
    def index_at(self, index):
        current = self.head
        while current:
            if current.index == index:
                return current
            current = current.next
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

    def get_last_index(self):
        if not self.head:
            return 0  # The list is empty
        current = self.head
        while current.next:
            current = current.next
        return current.index

        # Delete All Elements

    def delete_list(self):
        current = self.head
        while current:
            previous = current.next
            del current.name, current.index
            del current.direction, current.position, current.center, current.speed
            del current.active, current.image, current.health
            del current.weapon, current.hit_range
            del current.explode_at, current.health_show, current.fire_cooldown
            del current.next
            del current.y_axis, current.each_weapon_amount, current.fire_shift
            current = previous
        self.head = None


##################################################
# Class Prototype - Create
##################################################
class Crate:
    def __init__(self, category, position):
        # Input Element
        self.category = category
        self.position = position
        self.next = None
        # Self Start Element
        if self.category == 0:  # Add Life - 10 Chance
            self.info = 1
            self.image = pygame.image.load('resources/create/life_create.png')
        elif self.category == 1:  # Invincible - 20 Chance
            self.info = PLAYER_INVINCIBLE_TIME
            self.image = pygame.image.load('resources/create/invincible_create.png')
        elif self.category == 2:  # Clear All Enemy Bullet - 30 Chance
            self.info = 0
            self.image = pygame.image.load('resources/create/clear_bullet_create.png')
        elif self.category == 3:  # Weapon Create - 40 Chance
            self.info = random.randint(0, BULLET_TYPE)
            self.image = pygame.image.load('resources/create/bullet' + str(self.info) + '.png')
        elif self.category == 4:  # Shield - 50 Chance
            self.info = random.randint(CRATE_SHIELD[0], CRATE_SHIELD[1])
            self.image = pygame.image.load('resources/create/shield_create.png')
        elif self.category == 5:  # Health - 60 Chance
            self.info = random.randint(CRATE_HEALTH[0], CRATE_HEALTH[1])
            self.image = pygame.image.load('resources/create/health_create.png')
        # Storage
        self.contact = [sum(x) for x in zip(position, [CRATE_SIZE / 2, CRATE_SIZE / 2])]
        self.direction = 1 if random.randint(0, 1) == 0 else -1
        self.collect_range = CRATE_COLLECT_RANGE


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
        self.image = pygame.image.load('resources/button/button_' + str(name) + '.png')
        self.rect = self.image.get_rect()
        # Connect
        self.next = None


class ButtonList:
    def __init__(self):
        self.head = None

    def append(self, name):
        new_node = Button(name=name)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

    def name(self, name):
        current = self.head
        while current:
            if current.name == name:
                return current
            current = current.next
        return False


##################################################
# Image Storage Function
##################################################
class ImageBlock:
    def __init__(self, name, number):
        self.name = name
        self.number = number
        self.image = pygame.image.load('resources/explosion/explosion' + str(number) + ".png")
        # Linkage
        self.next = None


class ImageList:
    def __init__(self):
        self.head = None

    def append(self, name, number):
        new_node = ImageBlock(name=name, number=number)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

    def get(self):  # Select a random explosion image from list
        number = random.randint(0, EXPLOSION_IMAGE_NUMBER - 1)
        current = self.head
        while current:
            if current.number == number:
                return current.image
            current = current.next
        return False


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
