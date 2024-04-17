import unittest

from LRUCache import Cache

class TestLRUCache(unittest.TestCase):
    def test_get_set_item(self):
        cache = Cache(MAX_SIZE=2)
        # Setting items
        cache.set('a', 1)
        cache.set('b', 2)
        self.assertEqual(cache.get('a'), 1)
        self.assertEqual(cache.get('b'), 2)

    def test_move_to_front_on_access(self):
        cache = Cache(MAX_SIZE=2)
        cache.set('a', 1)
        cache.set('b', 2)
        # Access 'a' to ensure it moves to the front
        cache.get('a')
        cache.set('c', 3)  # This should evict 'b'
        self.assertIsNone(cache.get('b'))
        self.assertEqual(cache.get('a'), 1)
        self.assertEqual(cache.get('c'), 3)

    def test_append_to_front(self):
        cache = Cache(MAX_SIZE=2)
        cache.set('a', 1)
        self.assertEqual(cache.linked_list.head.results, 1)
        self.assertEqual(cache.linked_list.tail.results, 1)

    def test_remove_from_tail(self):
        cache = Cache(MAX_SIZE=2)
        cache.set('a', 1)
        cache.set('b', 2)
        self.assertEqual(cache.linked_list.tail.results, 1)
        cache.set('c', 3)  # 'a' should be removed as it's the LRU item
        self.assertIsNone(cache.get('a'))
        self.assertEqual(cache.linked_list.tail.results, 2)

    def test_lru_cache_max_size_limit(self):
        cache = Cache(MAX_SIZE=3)
        cache.set('a', 1)
        cache.set('b', 2)
        cache.set('c', 3)
        # With next insertion, 'a' should be removed
        cache.set('d', 4)
        self.assertIsNone(cache.get('a'))
        self.assertEqual(cache.get('b'), 2)
        self.assertEqual(cache.get('c'), 3)
        self.assertEqual(cache.get('d'), 4)

# This runs the test cases defined above
if __name__ == '__main__':
    unittest.main()