import unittest
from opencp import Queue


class TestQueue(unittest.TestCase):
    def test_operations(self):
        q = Queue()

        # Test Enqueue
        q.enqueue(10)
        q.enqueue(20)
        q.enqueue(30)

        # Test Dequeue
        self.assertEqual(q.dequeue(), 10)
        self.assertEqual(q.dequeue(), 20)
        self.assertEqual(q.dequeue(), 30)

    def test_empty_error(self):
        q = Queue()
        with self.assertRaises(IndexError):
            q.dequeue()


if __name__ == "__main__":
    unittest.main()
