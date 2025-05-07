from dataclasses import dataclass, field
import unittest

@dataclass
class CircularQueue:
    capacity: int
    values: list[int] = field(default_factory=list)
    front: int = 0
    rear: int = -1
    size: int = 0

    def enqueue(self, value: int):
        if self.is_full():
            return None
        self.rear = (self.rear + 1) % self.capacity
        self.values[self.rear] = value
        self.size += 1
        return True

    def dequeue(self) -> Optional[int]:
        if self.is_empty():
            return None
        value = self.values[self.front]
        self.values[self.front] = -1
        self.front = (self.front + 1) % self.capacity
        self.size -= 1
        return value

    def is_empty(self) -> bool:
        return self.size == 0

    def is_full(self) -> bool:
        return self.size == self.capacity

class TestQueue(unittest.TestCase):
    def test_one_empty(self):
        cq = CircularQueue(10)
        cq.values = [-1] * cq.capacity
        cq.enqueue(5)
        self.assertEqual(cq.values[0], 5)
        self.assertEqual(cq.front, 0)
        self.assertEqual(cq.rear, 0)

    def test_enqueue_full(self):
        cq = CircularQueue(3)
        cq.values = [-1] * cq.capacity
        cq.enqueue(1)
        cq.enqueue(2)
        cq.enqueue(3)
        result = cq.enqueue(4)
        self.assertTrue(cq.is_full())
        self.assertEqual(result, None)
        self.assertEqual(cq.values, [1, 2, 3])

    def test_dequeue(self):
        cq = CircularQueue(3)
        cq.values = [-1] * cq.capacity
        cq.enqueue(10)
        cq.enqueue(20)
        value = cq.dequeue()
        self.assertEqual(value, 10)
        self.assertEqual(cq.size, 1)
        self.assertEqual(cq.values[(cq.front - 1) % cq.capacity], -1)

    def test_dequeue_empty(self):
        cq = CircularQueue(2)
        cq.values = [-1] * cq.capacity
        result = cq.dequeue()
        self.assertEqual(result, None)
        self.assertTrue(cq.is_empty())

    def test_circle(self):
        cq = CircularQueue(3)
        cq.values = [-1] * cq.capacity
        cq.enqueue(1)
        cq.enqueue(2)
        cq.enqueue(3)
        cq.dequeue()
        cq.enqueue(4)

        self.assertEqual(cq.values, [4, 2, 3])
        self.assertEqual(cq.rear, 0)

    def test_is_full(self):
        cq = CircularQueue(2)
        cq.values = [-1] * cq.capacity
        self.assertTrue(cq.is_empty())
        cq.enqueue(1)
        self.assertFalse(cq.is_full())
        cq.enqueue(2)
        self.assertTrue(cq.is_full())

if __name__ == "__main__":
    unittest.main()
