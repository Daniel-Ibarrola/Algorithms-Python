from linkedlist import SinglyLinkedList, LinkedList


def test_create_linked_list():

    llist = SinglyLinkedList()
    assert llist.is_empty()


def test_push_and_pop_front():

    llist = SinglyLinkedList()
    llist.push_front(5)
    llist.push_front(6)
    llist.push_front(7)
    
    assert not llist.is_empty()
    assert len(llist) == 3

    assert llist.pop_front() == 7
    assert llist.pop_front() == 6
    assert llist.pop_front() == 5
    assert llist.is_empty()

    # Test linked list with tail
    llist = LinkedList()
    llist.push_front(5)
    llist.push_front(6)
    llist.push_front(7)
    
    assert not llist.is_empty()
    assert len(llist) == 3

    assert llist.pop_front() == 7
    assert llist.pop_front() == 6
    assert llist.pop_front() == 5
    assert llist.is_empty()


def test_push_and_pop_back():
    
    llist = SinglyLinkedList()
    for ii in range(4, 8):
        llist.push_front(ii)

    llist.push_back(10)
    llist.push_back(12)
    assert len(llist) == 6

    assert llist.pop_back() == 12
    assert llist.pop_back() == 10
    assert len(llist) == 4

    # Test linked list with tail
    llist = LinkedList()
    for ii in range(4, 8):
        llist.push_front(ii)

    llist.push_back(10)
    llist.push_back(12)
    assert len(llist) == 6

    assert llist.pop_back() == 12
    assert llist.pop_back() == 10
    assert len(llist) == 4


def test_find():
    
    llist = SinglyLinkedList()
    llist.push_front(5)
    llist.push_front(6)
    llist.push_front(7)

    assert llist.find(7)
    assert not llist.find(15)


def test_erase():
    
    llist = SinglyLinkedList()
    llist.push_front(5)
    llist.push_front(6)
    llist.push_front(7)

    llist.erase(6)
    assert llist.pop_front() == 7
    assert llist.pop_front() == 5
    assert llist.is_empty()


def test_add_before():

    llist = SinglyLinkedList()
    llist.push_front(5)
    llist.push_front(6)
    llist.push_front(7)

    llist.add_before(7, 5)
    assert len(llist) == 4
    assert repr(llist) == "[5, 7, 6, 5]"


def test_add_after():

    llist = SinglyLinkedList()
    llist.push_front(5)
    llist.push_front(6)
    llist.push_front(7)

    llist.add_after(5, 4)
    assert len(llist) == 4
    assert repr(llist) == "[7, 6, 5, 4]"

