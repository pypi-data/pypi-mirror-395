from __future__ import annotations
from typing import Generic, Iterable, Iterator, Optional, TypeVar

T = TypeVar("T")

# ============================================================
#   Singly Linked List Node
# ============================================================
class SLLNode(Generic[T]):
    __slots__ = ("value", "next")

    def __init__(self, value: T, next: Optional[SLLNode[T]] = None) -> None:
        self.value = value
        self.next = next

    def __repr__(self):
        return f"SLLNode({self.value})"


# ============================================================
#   Singly Linked List
# ============================================================
class SinglyLL(Generic[T]):
    """A simple singly linked list implementation with extra teaching tools."""

    def __init__(self, iterable: Optional[Iterable[T]] = None) -> None:
        self.head: Optional[SLLNode[T]] = None
        self.size = 0

        if iterable:
            for item in iterable:
                self.append(item)

    # -------------------- Basic ops --------------------
    def is_empty(self) -> bool:
        return self.size == 0

    def prepend(self, value: T) -> None:
        self.head = SLLNode(value, self.head)
        self.size += 1

    def append(self, value: T) -> None:
        node = SLLNode(value)
        if not self.head:
            self.head = node
        else:
            cur = self.head
            while cur.next:
                cur = cur.next
            cur.next = node
        self.size += 1

    def clear(self) -> None:
        self.head = None
        self.size = 0

    # -------------------- Searching --------------------
    def find(self, value: T) -> Optional[SLLNode[T]]:
        cur = self.head
        while cur:
            if cur.value == value:
                return cur
            cur = cur.next
        return None

    def __contains__(self, value: T) -> bool:
        return self.find(value) is not None

    # -------------------- Index operations --------------------
    def get(self, index: int) -> T:
        if index < 0 or index >= self.size:
            raise IndexError("Index out of bounds")
        cur = self.head
        for _ in range(index):
            cur = cur.next
        return cur.value

    def set(self, index: int, value: T) -> None:
        if index < 0 or index >= self.size:
            raise IndexError("Index out of bounds")
        cur = self.head
        for _ in range(index):
            cur = cur.next
        cur.value = value

    def insert(self, index: int, value: T) -> None:
        if index < 0 or index > self.size:
            raise IndexError("Index out of bounds")
        if index == 0:
            self.prepend(value)
            return
        cur = self.head
        for _ in range(index - 1):
            cur = cur.next
        cur.next = SLLNode(value, cur.next)
        self.size += 1

    def pop(self, index: int) -> T:
        if index < 0 or index >= self.size:
            raise IndexError("Index out of bounds")
        if index == 0:
            val = self.head.value
            self.head = self.head.next
            self.size -= 1
            return val
        prev = self.head
        for _ in range(index - 1):
            prev = prev.next
        val = prev.next.value
        prev.next = prev.next.next
        self.size -= 1
        return val

    # -------------------- Deletion --------------------
    def delete(self, value: T) -> bool:
        if not self.head:
            return False
        if self.head.value == value:
            self.head = self.head.next
            self.size -= 1
            return True

        prev = self.head
        cur = self.head.next
        while cur:
            if cur.value == value:
                prev.next = cur.next
                self.size -= 1
                return True
            prev, cur = cur, cur.next
        return False

    # -------------------- Advanced ops --------------------
    def reverse(self) -> None:
        prev = None
        cur = self.head
        while cur:
            nxt = cur.next
            cur.next = prev
            prev = cur
            cur = nxt
        self.head = prev

    def reverse_recursive(self) -> None:
        def helper(node, prev=None):
            if not node:
                return prev
            nxt = node.next
            node.next = prev
            return helper(nxt, node)
        self.head = helper(self.head)

    def middle(self) -> Optional[T]:
        """Return middle element (slow-fast pointer)."""
        slow = fast = self.head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        return slow.value if slow else None

    def detect_cycle(self) -> bool:
        """Floyd’s cycle detection."""
        slow = fast = self.head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow == fast:
                return True
        return False

    def remove_duplicates(self) -> None:
        seen = set()
        cur = self.head
        prev = None
        while cur:
            if cur.value in seen:
                prev.next = cur.next
                self.size -= 1
            else:
                seen.add(cur.value)
                prev = cur
            cur = cur.next

    # -------------------- Helpers --------------------
    def to_list(self) -> list[T]:
        return list(iter(self))

    @classmethod
    def from_list(cls, lst: list[T]) -> "SinglyLL[T]":
        return cls(lst)

    # -------------------- Magic --------------------
    def __len__(self): return self.size

    def __iter__(self) -> Iterator[T]:
        cur = self.head
        while cur:
            yield cur.value
            cur = cur.next

    def __repr__(self):
        return f"SinglyLL([{', '.join(str(x) for x in self)}])"



# ============================================================
#   Doubly Linked List Node
# ============================================================
class DLLNode(Generic[T]):
    __slots__ = ("value", "prev", "next")

    def __init__(self, value: T):
        self.value = value
        self.prev: Optional[DLLNode[T]] = None
        self.next: Optional[DLLNode[T]] = None

    def __repr__(self):
        return f"DLLNode({self.value})"



# ============================================================
#   Doubly Linked List
# ============================================================
class DoublyLinkedList(Generic[T]):

    def __init__(self, iterable: Optional[Iterable[T]] = None):
        self.head: Optional[DLLNode[T]] = None
        self.tail: Optional[DLLNode[T]] = None
        self._size = 0
        if iterable:
            for item in iterable:
                self.append(item)

    # -------------------- Basic ops --------------------
    def is_empty(self):
        return self._size == 0

    def append(self, value: T) -> None:
        node = DLLNode(value)
        if not self.head:
            self.head = self.tail = node
        else:
            node.prev = self.tail
            self.tail.next = node
            self.tail = node
        self._size += 1

    def prepend(self, value: T) -> None:
        node = DLLNode(value)
        if not self.head:
            self.head = self.tail = node
        else:
            self.head.prev = node
            node.next = self.head
            self.head = node
        self._size += 1

    def clear(self):
        self.head = self.tail = None
        self._size = 0

    # -------------------- Extra insert ops --------------------
    def insert_after(self, target: T, value: T) -> bool:
        cur = self.head
        while cur:
            if cur.value == target:
                node = DLLNode(value)
                node.prev, node.next = cur, cur.next
                if cur.next:
                    cur.next.prev = node
                else:
                    self.tail = node
                cur.next = node
                self._size += 1
                return True
            cur = cur.next
        return False

    def insert_before(self, target: T, value: T) -> bool:
        if not self.head:
            return False
        if self.head.value == target:
            self.prepend(value)
            return True

        cur = self.head.next
        while cur:
            if cur.value == target:
                node = DLLNode(value)
                prev = cur.prev
                node.prev, node.next = prev, cur
                prev.next = node
                cur.prev = node
                self._size += 1
                return True
            cur = cur.next
        return False

    # -------------------- Delete --------------------
    def delete(self, value: T) -> bool:
        cur = self.head
        while cur:
            if cur.value == value:
                if cur.prev:
                    cur.prev.next = cur.next
                else:
                    self.head = cur.next
                if cur.next:
                    cur.next.prev = cur.prev
                else:
                    self.tail = cur.prev
                self._size -= 1
                return True
            cur = cur.next
        return False

    # -------------------- Reverse --------------------
    def reverse(self):
        cur = self.head
        while cur:
            cur.prev, cur.next = cur.next, cur.prev
            cur = cur.prev
        self.head, self.tail = self.tail, self.head

    # -------------------- Helpers --------------------
    def to_list(self) -> list[T]:
        return list(iter(self))

    @classmethod
    def from_list(cls, lst: list[T]):
        return cls(lst)

    # -------------------- Magic --------------------
    def __len__(self): return self._size

    def __iter__(self) -> Iterator[T]:
        cur = self.head
        while cur:
            yield cur.value
            cur = cur.next

    def iter_reverse(self) -> Iterator[T]:
        cur = self.tail
        while cur:
            yield cur.value
            cur = cur.prev

    def __repr__(self):
        return f"DoublyLinkedList([{', '.join(str(x) for x in self)}])"



# ============================================================
#   Circular Linked List
# ============================================================
class CircularLinkedList(Generic[T]):
    """Circular Linked List: last node points to head."""

    def __init__(self):
        self.head: Optional[SLLNode[T]] = None
        self._size = 0

    # -------------------- Basic ops --------------------
    def append(self, value: T) -> None:
        node = SLLNode(value)
        if not self.head:
            self.head = node
            node.next = node
        else:
            cur = self.head
            while cur.next != self.head:
                cur = cur.next
            cur.next = node
            node.next = self.head
        self._size += 1

    def is_empty(self):
        return self._size == 0

    def __contains__(self, value: T) -> bool:
        return self.find(value) is not None

    # -------------------- Searching --------------------
    def find(self, value: T) -> Optional[SLLNode[T]]:
        if not self.head:
            return None
        cur = self.head
        for _ in range(self._size):
            if cur.value == value:
                return cur
            cur = cur.next
        return None

    # -------------------- Delete --------------------
    def delete(self, value: T) -> bool:
        if not self.head:
            return False
        cur = self.head
        prev = None

        for _ in range(self._size):
            if cur.value == value:
                if prev is None:  # deleting head
                    # find last node
                    last = self.head
                    while last.next != self.head:
                        last = last.next
                    if self._size == 1:
                        self.head = None
                    else:
                        last.next = cur.next
                        self.head = cur.next
                else:
                    prev.next = cur.next
                self._size -= 1
                return True
            prev, cur = cur, cur.next
        return False

    # -------------------- Split circular list --------------------
    def split(self):
        """Split into two halves."""
        slow = fast = self.head
        if not self.head or self._size < 2:
            return None, None

        while fast.next != self.head and fast.next.next != self.head:
            fast = fast.next.next
            slow = slow.next

        head1 = self.head
        head2 = slow.next
        slow.next = head1

        cur = head2
        while cur.next != self.head:
            cur = cur.next
        cur.next = head2

        first = CircularLinkedList()
        second = CircularLinkedList()
        first.head = head1
        second.head = head2
        first._size = (self._size + 1) // 2
        second._size = self._size // 2
        return first, second

    # -------------------- Josephus Problem --------------------
    def josephus(self, k: int) -> T:
        """Solve Josephus problem, return survivor."""
        if self._size == 0:
            return None
        cur = self.head
        while self._size > 1:
            for _ in range(k - 2):
                cur = cur.next
            self.delete(cur.next.value)
            cur = cur.next
        return cur.value

    # -------------------- Magic --------------------
    def __len__(self): return self._size

    def __iter__(self):
        if not self.head:
            return
        cur = self.head
        for _ in range(self._size):
            yield cur.value
            cur = cur.next

    def __repr__(self):
        return f"CircularLinkedList([{', '.join(str(x) for x in self)}])"