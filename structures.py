# Structure File
# Version 3.0
# A Modified Linked List for Storage

##################################################
# Libraries
##################################################


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

    # Length of the List
    def length(self):
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count

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
# Class Prototype - CaskList for Amory and Enemy
##################################################
class Node:
    def __init__(self, name, index=None, position=None, speed=None, range=None, contact=None, active=None, image=None,
                 cooldown=None):
        self.name = name
        self.next = None
        # Format Data
        self.index = index
        self.position = position
        self.speed = speed
        self.range = range
        self.contact = tuple(tuple(i) for i in contact) if contact is not None else None
        self.active = active
        self.image = image
        self.cooldown = cooldown


class CaskList:
    def __init__(self):
        self.head = None

    # Add Element at the end
    def append(self, data, index, position, speed, range, contact, active, image, cooldown):
        new_node = Node(name=data, index=index, position=position, speed=speed, range=range, contact=contact,
                        active=active, image=image, cooldown=cooldown)
        if not self.head:
            self.head = new_node
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node

    # Add Element at the head
    def prepend(self, data, index, position, speed, range, contact, active, image, cooldown):
        new_node = Node(name=data, index=index, position=position, speed=speed, range=range, contact=contact,
                        active=active, image=image, cooldown=cooldown)
        new_node.next = self.head
        self.head = new_node

    # Delete Element
    def delete(self, data):
        if not self.head:
            return
        if self.head.name == data:
            self.head = self.head.next
            return
        current = self.head
        while current.next:
            if current.next.name == data:
                current.next = current.next.next
                return
            current = current.next

    # Show Whole List
    def display(self):
        current = self.head
        while current:
            print(current.name, end=" -> ")
            current = current.next
        print("None")

    # Length of the List
    def length(self):
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count

    # Search via Index
    def search_index(self, index):
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
# Function Prototype
##################################################


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
