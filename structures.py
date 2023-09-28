# Structure File
# Version - Alpha 6.4
# A Modified Linked List for Storage

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
        # Background Information
        self.shield = None
        self.invincible = False
        self.health_show = True
        # Storage Information
        self.x_change = 0


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


##################################################
# Class Prototype - Amory
##################################################
class AmoryBlock:
    def __init__(self, name, index, position, speed, exp_range, contact, active, image, cooldown, damage):
        # Linkage
        self.next = None
        # Format Data
        self.name = name
        self.index = index
        self.position = position
        self.speed = speed
        self.exp_range = exp_range
        self.contact = tuple(tuple(i) for i in contact) if contact is not None else None
        self.active = active
        self.image = image
        self.cooldown = cooldown
        self.damage = damage


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
    def __init__(self, name, index, position, speed, active, image, health, direction, weapon):
        self.name = name
        self.index = index
        # To Update Element
        self.direction = direction
        self.position = position
        self.speed = speed
        self.active = active
        self.image = image
        self.health = [health, health]
        self.weapon = weapon
        # Self Start Element
        self.explode_at = None
        self.health_show = True
        # Connection
        self.next = None


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

    def append(self, name, index, position, speed, active, image, health, direction, weapon):
        new_node = EnemyBlock(name, index, position, speed, active, image, health, direction, weapon)
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


##################################################
# Main Function
##################################################
def main():
    print("Hello World!")


##################################################
# Main Function Runner
##################################################
if __name__ == "__main__":
    main()
