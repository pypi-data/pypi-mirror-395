from __future__ import annotations
from typing import Generic, Iterable, Iterator, Optional, TypeVar

T = TypeVar('T')

class Stack(Generic[T]):
    def __init__(self, iterable: Optional[Iterable[T]]= None)-> None:
        self.items: list[T] = list(iterable) if iterable else []

    def push(self, item: T)-> None:
        self.items.append(item)

    def pop(self)-> T:
        if not self.items:
            raise IndexError("pop empty stack")
        return self.items.pop()
    
    def peek(self)-> Optional[T]:
        return self.items[-1] if self.items else None
    
    def is_empty(self)-> bool:
        return not self.items
    
    def __len__(self)-> int:
        return len(self.items)
    
    def __iter__(self)-> Iterator[T]:
        for i in range(len(self.items)-1, -1, -1):
            yield self.items[i]

    def __repr__(self):
        return f"Stack({self.items}!)"
    
    def reverse_stack(self)-> Stack[T]:
        reversed_stack = Stack[T]()
        for item in self:
            reversed_stack.push(item)
        return reversed_stack

    # Clears all elements from the stack
    def clear(self) -> None:
        self.items.clear()

    # Check if an item exists in the stack
    def contains(self, item: T) -> bool:
        return item in self.items

    # Convert stack to Python list (bottom → top)
    def to_list(self) -> list[T]:
        return list(self.items)

    # Copy this stack
    def copy(self) -> Stack[T]:
        return Stack(self.items)

    # Reverse the stack IN PLACE (no new stack created)
    def reverse_in_place(self) -> None:
        self.items.reverse()

    # Stack truthiness: allows "if stack:" 
    def __bool__(self) -> bool:
        return not self.is_empty()

    # Compare stacks using "=="
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Stack):
            return False
        return self.items == other.items

    # Return size explicitly (alternative to len())
    def size(self) -> int:
        return len(self.items)

    # View bottom item (optional educational method)
    def bottom(self) -> Optional[T]:
        return self.items[0] if self.items else None

    
class Node(Generic[T]):
    __slots__ = ('value', 'next')
    def __init__(self, value: T, next: Optional[Node[T]]= None)-> None:
        self.value = value
        self.next = next

    def __repr__(self)-> str:
        return f"Node({self.value})"
    
class LinkedStack(Generic[T]):
    def __init__(self, iterable: Optional[Iterable[T]]= None)-> None:
        self.head: Optional[Node[T]]= None
        self.size = 0
        if iterable:
            for item in iterable:
                self.push(item)

    def push(self, item: T)-> None:
        node = Node(item, self.head)
        self.head = node
        self.size += 1

    def pop(self)-> T:
        if self.head is None:
            raise IndexError("pop empty stack")
        node = self.head
        self.head = node.next
        self.size -= 1
        return node.value
    
    def peek(self)-> Optional[T]:
        return self.head.value if self.head else None
    
    def is_empty(self)-> bool:
        return self.head is None
    
    def __len__(self)-> int:
        return self.size
    
    def __iter__(self)-> Iterator[T]:
        curr = self.head 
        while curr:
            yield curr.value
            curr = curr.next

    def __repr__(self)-> str:
        return f"LinkedStack(size={self.size})"

    # Remove all elements from the stack
    def clear(self) -> None:
        self.head = None
        self.size = 0

    # Check if a value exists in the stack
    def contains(self, item: T) -> bool:
        return any(value == item for value in self)

    # Convert the linked stack to a Python list (top → bottom)
    def to_list(self) -> list[T]:
        return list(self)

    # Makes a deep copy of the stack
    def copy(self) -> LinkedStack[T]:
        return LinkedStack(self.to_list())

    # Reverse the stack IN PLACE using pointer reversal
    def reverse_in_place(self) -> None:
        prev = None
        curr = self.head
        while curr:
            nxt = curr.next
            curr.next = prev
            prev = curr
            curr = nxt
        self.head = prev

    # Return a new reversed stack (not in-place)
    def reverse_stack(self) -> LinkedStack[T]:
        new_stack = LinkedStack[T]()
        for value in self:
            new_stack.push(value)
        return new_stack

    # Truthiness: allows "if stack:"
    def __bool__(self) -> bool:
        return not self.is_empty()

    # Compare two LinkedStacks using ==
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, LinkedStack):
            return False
        return self.to_list() == other.to_list()

    # Return the bottom-most value
    def bottom(self) -> Optional[T]:
        if not self.head:
            return None
        curr = self.head
        while curr.next:
            curr = curr.next
        return curr.value

    # Return the size explicitly (alternative to len())
    def size_of(self) -> int:
        return self.size
