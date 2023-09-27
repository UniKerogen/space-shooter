# Cask List File
# Version 1.0
# A Modified Linked List for Storage

##################################################
# Libraries
##################################################


##################################################
# Variable Definition
##################################################
class Node:
    def __init__(self, name, index=None, position=None, speed=None, range=None, contact=None, active=None, image=None):
        self.name = name
        self.next = None
        # Format Data
        self.index = index
        self.position = position
        self.speed = speed
        self.range = range
        self.contact = contact
        self.contact_origin = tuple(tuple(i) for i in contact) if contact is not None else None
        self.active = active
        self.image = image

    def contact_reset(self):
        if self.contact is not None and self.contact_origin is not None:
            for index in range(len(self.contact_origin)):
                self.contact[index] = list(self.contact_origin[index])



class CaskList:
    def __init__(self):
        self.head = None

    def append(self, data, index, position, speed, range, contact, active, image):
        new_node = Node(name=data, index=index, position=position, speed=speed, range=range, contact=contact, active=active, image=image)
        if not self.head:
            self.head = new_node
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node

    def prepend(self, data, index, position, speed, range, contact, active, image):
        new_node = Node(name=data, index=index, position=position, speed=speed, range=range, contact=contact, active=active, image=image)
        new_node.next = self.head
        self.head = new_node

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

    def display(self):
        current = self.head
        while current:
            print(current.name, end=" -> ")
            current = current.next
        print("None")

    def length(self):
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count

    def search_index(self, index):
        current = self.head
        while current:
            if current.index == index:
                return current
            current = current.next
        return False

    def search_active(self):
        current = self.head
        while current:
            if current.active:
                return current
            current = current.next
        return self.head


##################################################
# Class Prototype
##################################################


##################################################
# Function Prototype
##################################################


##################################################
# Main Function
##################################################
def main():
    print("Hello World!")
    my_list = CaskList()
    my_list.append(1)
    my_list.append(2)
    my_list.append(3)
    my_list.prepend(0)
    my_list.display()  # Output: 0 -> 1 -> 2 -> 3 -> None

    my_list.delete(2)
    my_list.display()  # Output: 0 -> 1 -> 3 -> None


##################################################
# Main Function Runner
##################################################
if __name__ == "__main__":
    main()
