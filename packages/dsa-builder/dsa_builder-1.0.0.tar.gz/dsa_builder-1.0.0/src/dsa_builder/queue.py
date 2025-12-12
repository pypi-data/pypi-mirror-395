from __future__ import annotations
from collections import deque
from typing import Generic, Iterable, Iterator, Optional, TypeVar

T = TypeVar("T")

class DequeQueue(Generic[T]):
    def __init__(self, iterable: Optional[Iterable[T]]= None)-> None:
        self.dq = deque(iterable) if iterable else deque()

    def enqueue(self, item: T)-> None:
        self.dq.append(item)

    def dequeue(self)-> T:
        if not self.dq:
            raise IndexError("dequeue from empty queue")
        return self.dq.popleft()
    
    def peek(self) -> Optional[T]:
        return self.dq[0] if self.dq else None

    def is_empty(self) -> bool:
        return not self.dq

    def __len__(self) -> int:
        return len(self.dq)

    def __iter__(self) -> Iterator[T]:
        return iter(self.dq)

    def __repr__(self) -> str:
        return f"DequeQueue({list(self.dq)})"

    # Clear all items from the queue
    def clear(self) -> None:
        self.dq.clear()

    # Check if a value exists in the queue
    def contains(self, item: T) -> bool:
        return item in self.dq

    # Convert queue to a Python list
    def to_list(self) -> list[T]:
        return list(self.dq)

    # Make a copy of the queue
    def copy(self) -> DequeQueue[T]:
        return DequeQueue(self.dq)

    # Reverse the queue in-place
    def reverse_in_place(self) -> None:
        self.dq.reverse()

    # Return a new reversed queue (does not modify original)
    def reversed_queue(self) -> DequeQueue[T]:
        return DequeQueue(reversed(self.dq))

    # Truthiness: allows "if queue:"
    def __bool__(self) -> bool:
        return not self.is_empty()

    # Compare two DequeQueues using ==
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DequeQueue):
            return False
        return list(self.dq) == list(other.dq)

    # Return the last element (rear of queue)
    def rear(self) -> Optional[T]:
        return self.dq[-1] if self.dq else None

    
class Node(Generic[T]):
    __slots__ = ("value", "next")
    def __init__(self, value: T) -> None:
        self.value = value
        self.next: Optional[Node[T]] = None

    def __repr__(self) -> str:
        return f"Node({self.value})"
    
class LinkedQueue(Generic[T]):
    def __init__(self, iterable: Optional[Iterable[T]] = None) -> None:
        self.head: Optional[Node[T]] = None
        self.tail: Optional[Node[T]] = None
        self._size = 0
        if iterable:
            for item in iterable:
                self.enqueue(item)

    def enqueue(self, item: T) -> None:
        node = Node(item)
        if self.tail:
            self.tail.next = node
            self.tail = node
        else:
            self.head = self.tail = node
        self._size += 1

    def dequeue(self) -> T:
        if self.head is None:
            raise IndexError("dequeue from empty queue")
        node = self.head
        self.head = node.next
        if self.head is None:
            self.tail = None
        self._size -= 1
        return node.value

    def peek(self) -> Optional[T]:
        return self.head.value if self.head else None

    def is_empty(self) -> bool:
        return self.head is None

    def __len__(self) -> int:
        return self._size

    def __iter__(self) -> Iterator[T]:
        curr = self.head
        while curr:
            yield curr.value
            curr = curr.next

    def __repr__(self) -> str:
        return f"LinkedQueue(size={self._size})"

    # Clear all elements from the queue
    def clear(self) -> None:
        self.head = None
        self.tail = None
        self._size = 0

    # Check if a value exists in the queue
    def contains(self, item: T) -> bool:
        return any(value == item for value in self)

    # Convert the linked queue to a Python list (front → rear)
    def to_list(self) -> list[T]:
        return list(self)

    # Make a copy of the linked queue
    def copy(self) -> LinkedQueue[T]:
        return LinkedQueue(self.to_list())

    # Reverse the queue in-place
    def reverse_in_place(self) -> None:
        prev = None
        curr = self.head
        self.tail = self.head  # old head becomes new tail
        while curr:
            nxt = curr.next
            curr.next = prev
            prev = curr
            curr = nxt
        self.head = prev

    # Return a new reversed queue (does not modify original)
    def reversed_queue(self) -> LinkedQueue[T]:
        new_queue = LinkedQueue()
        nodes = list(self)
        for item in reversed(nodes):
            new_queue.enqueue(item)
        return new_queue

    # Truthiness: allows "if queue:"
    def __bool__(self) -> bool:
        return not self.is_empty()

    # Compare two LinkedQueues using ==
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, LinkedQueue):
            return False
        return self.to_list() == other.to_list()

    # Return the last element (rear of queue)
    def rear(self) -> Optional[T]:
        return self.tail.value if self.tail else None

    # Return the size explicitly (alternative to len())
    def size_of(self) -> int:
        return self._size
