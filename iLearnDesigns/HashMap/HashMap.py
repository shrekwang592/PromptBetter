class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None

class HashMap:
    def __init__(self, capacity=1000):
        self.capacity = capacity
        self.map = [None] * self.capacity

    def hash_function(self, key):
        return key % self.capacity

    def put(self, key, value):
        index = self.hash_function(key)
        if self.map[index] is None:
            self.map[index] = Node(key, value)
        else:
            current = self.map[index]
            while True:
                if current.key == key:
                    current.value = value
                    return
                if current.next is None:
                    break
                current = current.next
            current.next = Node(key, value)

    def get(self, key):
        index = self.hash_function(key)
        current = self.map[index]
        while current is not None:
            if current.key == key:
                return current.value
            current = current.next
        return None

    def remove(self, key):
        index = self.hash_function(key)
        current = self.map[index]
        prev = None
        while current is not None:
            if current.key == key:
                if prev is None:
                    self.map[index] = current.next
                else:
                    prev.next = current.next
                return True
            prev = current
            current = current.next
        return False
    
# Define the test cases
def test_hashmap():
    print("Starting HashMap tests...")

    # Create a hashmap instance
    hashmap = HashMap()

    # Test case 1: Insert key-value pairs
    hashmap.put(10, 'Value for 10')
    hashmap.put(20, 'Value for 20')
    hashmap.put(10, 'New Value for 10')  # This should update the value for key 10

    # Test case 2: Retrieve values
    if hashmap.get(10) == 'New Value for 10':
        print("Test case 2 passed: Value for key 10 retrieved successfully.")
    else:
        print("Test case 2 failed: Failed to retrieve the updated value for key 10.")

    if hashmap.get(20) == 'Value for 20':
        print("Test case 2 passed: Value for key 20 retrieved successfully.")
    else:
        print("Test case 2 failed: Failed to retrieve the value for key 20.")

    # Testing non-existent key
    if hashmap.get(30) is None:
        print("Test case 2 passed: Correctly returns None for non-existent key.")
    else:
        print("Test case 2 failed: Incorrect value returned for non-existent key.")

    # Test case 3: Remove key
    if hashmap.remove(10):
        if hashmap.get(10) is None:
            print("Test case 3 passed: Key 10 removed successfully.")
        else:
            print("Test case 3 failed: Key 10 still exists after removal.")
    else:
        print("Test case 3 failed: Failed to remove key 10.")

    # Inserting keys that should collide
    hashmap.put(10, 'Colliding Value for 10')
    hashmap.put(1010, 'Colliding Value for 1010')

    if hashmap.get(1010) == 'Colliding Value for 1010':
        print("Test case 4 passed: Colliding key-value pair handled correctly.")
    else:
        print("Test case 4 failed: Failed to handle colliding key-value pair correctly.")

    print("HashMap tests completed.")

# Run the tests
test_hashmap()