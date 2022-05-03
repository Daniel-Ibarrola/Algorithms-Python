from typing import Any


class EmptyListError(ValueError):
    pass


class Node:
    """ Class to implement a node for the LinkedList class"""

    def __init__(self, value: Any) -> None:
        self.value = value
        self.next = None

    def update_next(self, new_next) -> None:
        self.next = new_next

    def update_value(self, new_value) -> None:
        self.value = new_value


class SinglyLinkedList:
    """ Class that implements a singly-linked list with no tail."""

    def __init__(self) -> None:
        self.head = None

    def push_front(self, item: Any) -> None:
        """ Adds item to the front. """
        node = Node(item)
        if self.head is not None:
            node.next = self.head
        self.head = node

    def top_front(self) -> Any:
        """ Returns front item. """
        if self.is_empty():
            raise EmptyListError
        return self.head.value

    def pop_front(self) -> Any:
        """ Removes front item and returns it."""
        if self.is_empty():
            raise EmptyListError
        item = self.head
        self.head = self.head.next
        return item.value

    def push_back(self, item: Any) -> None:
        """ Adds item to the back. """
        if self.is_empty():
            self.head = Node(item)
        else:
            node = self.head
            while node.next is not None:
                node = node.next
            node.next = Node(item)

    def top_back(self) -> Any:
        """ Returns back item. """
        if self.is_empty():
            raise EmptyListError 
        else:
            node = self.head
            while node.next is not None:
                node = node.next
            return node.value

    def pop_back(self) -> Any:
        """ Remove back item and returns it."""
        if self.is_empty():
            raise EmptyListError 
        else:
            node = self.head
            previous = node
            while node.next is not None:
                previous = node
                node = node.next
            previous.next = None
            return node.value

    def find(self, item: Any) -> bool:
        """ Finds an item in the list. """
        if self.is_empty():
            raise EmptyListError 
        else:
            node = self.head
            while node.next is not None:
                if node.value == item:
                    return True
                node = node.next
            return False

    def erase(self, item: Any) -> None:
        """ Erases a specific item. """
        if self.is_empty():
            raise EmptyListError 
        else:
            node = self.head
            previous = node
            while node.next is not None:
                if node.value == item:
                    previous.next = node.next
                    break
                previous = node
                node = node.next

    def is_empty(self) -> bool:
        """ Check whether the list is empty. """
        if self.head is None:
            return True
        return False

    def add_before(self, key, item) -> None:
        """ Adds an item before a certain key or node. """
        if self.is_empty():
            raise EmptyListError
        elif self.head.value == key:
            new_node = Node(item)
            new_node.next = self.head
            self.head = new_node  
        else:
            node = self.head
            previous = node
            while node.next is not None:
                if node.value == key:
                    new_node = Node(item)
                    previous.next = new_node
                    new_node.next = node
                    break
                previous = node
                node = node.next
            
            if node.value == key:
                new_node = Node(item)
                previous.next = new_node
                new_node.next = node

    def add_after(self, key, item) -> None:
        """ Adds an item after a certain key or node. """
        if self.is_empty():
            raise EmptyListError 
        else:
            node = self.head
            previous = node
            while node.next is not None:
                if previous.value == key:
                    new_node = Node(item)
                    new_node.next = node.next
                    node.next = new_node                    
                    break
                previous = node
                node = node.next
            
            # Case when adding a node to the back
            if node.value == key:
                node.next = Node(item)

    def __iter__(self):
        self.n = self.head
        return self

    def __next__(self) -> None:
        if self.n is not None:
            node = self.n
            self.n = self.n.next
            return node.value
        else:
            raise StopIteration

    def __repr__(self) -> str:
        """ String representation of the list. """
        repr_str = "["
        for item in self:
            repr_str += str(item) + ", "
        repr_str = repr_str[:-2] # Delete the last comma
        repr_str += "]"
        return repr_str

    def __len__(self) -> int:
        """ Returns the lenght of the list. O(n) operation."""
        length = 0
        for _ in self:
            length += 1
        return length


class LinkedList(SinglyLinkedList):
    """ Linked List with tail"""
    
    def __init__(self) -> None:
        super().__init__()
        self.head = None
        self.tail = None
    
    def push_front(self, item: Any) -> None:
        """ Push item to front of the list. """
        node = Node(item)
        node.next = self.head
        self.head = node
        if self.tail is None:
            self.tail = self.head

    def pop_front(self) -> Any:
        """ Remove front item and return it. """
        if self.head is None:
            raise EmptyListError
        item = self.head.value
        self.head = self.head.next
        if self.head is None:
            self.tail = None
        return item
    
    def push_back(self, item: Any) -> None:
        """ Push item to the back of the list"""
        node = Node(item)
        if self.tail is None:
            self.head = node
            self.tail = node
        else:
            self.tail.next = node
            self.tail = node
    
    def pop_back(self) -> None:
        """ Remove back item and return it. """
        if self.head is None:
            raise EmptyListError

        if self.head == self.tail:
            item = self.head.value
            self.head = None
            self.tail = None
            return item
        else:
            pointer = self.head
            previous = pointer
            while pointer.next is not None:
                previous = pointer
                pointer = pointer.next                
            
            item = pointer.value
            previous.next = None
            self.tail = previous
            return item


    