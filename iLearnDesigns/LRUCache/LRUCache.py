class Node(object):
    def __init__(self, query, results):
        self.query = query  # Hold the key to help with deletion in the cache
        self.results = results
        self.prev = None
        self.next = None

class LinkedList(object):
    def __init__(self):
        self.head = None
        self.tail = None

    def move_to_front(self, node):
        if node.prev:  # If the node is not already the head
            node.prev.next = node.next
            if node.next:  # If the node is not the tail
                node.next.prev = node.prev
            else:
                self.tail = node.prev  # Update the tail if node is tail
            node.prev = None
            node.next = self.head
            self.head.prev = node
            self.head = node

    def append_to_front(self, node):
        if not self.head:
            self.head = self.tail = node
        else:
            node.next = self.head
            self.head.prev = node
            self.head = node

    def remove_from_tail(self):
        if self.tail:
            removed_node = self.tail
            if self.head == self.tail:  # If only one element is present
                self.head = self.tail = None
            else:
                self.tail = self.tail.prev
                self.tail.next = None
            return removed_node
        return None  # If list is empty

class Cache(object):
    def __init__(self, MAX_SIZE):
        self.MAX_SIZE = MAX_SIZE
        self.size = 0
        self.lookup = {}  # key: query, value: node
        self.linked_list = LinkedList()

    def get(self, query):
        node = self.lookup.get(query)
        if node is None:
            return None
        self.linked_list.move_to_front(node)
        return node.results

    def set(self, query, results):
        node = self.lookup.get(query)
        if node is not None:
            node.results = results
            self.linked_list.move_to_front(node)
        else:
            if self.size == self.MAX_SIZE:
                removed_node = self.linked_list.remove_from_tail()
                self.lookup.pop(removed_node.query, None)
                self.size -= 1
            new_node = Node(query, results)
            self.linked_list.append_to_front(new_node)
            self.lookup[query] = new_node
            self.size += 1