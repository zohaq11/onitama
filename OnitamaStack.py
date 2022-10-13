from typing import Any, List, Tuple


class OnitamaStack:
    """A last-in-first-out (LIFO) stack of tuples.

    Stores data in a last-in, first-out order. When removing an item from the
    stack, the most recently-added item is the one that is removed.
    """
    # === Private Attributes ===
    # _items:
    #     The items stored in this stack. The end of the list represents
    #     the top of the stack.
    _items: List[Tuple]

    def __init__(self) -> None:
        """Initialize a new empty stack."""
        self._items = []

    def empty(self) -> bool:
        """Return whether this stack contains no items.

        >>> s = OnitamaStack()
        >>> s.empty()
        True
        >>> s.push('hi', 'hello')
        >>> s.empty()
        False
        """
        return self._items == []

    def push(self, item: Any, item2: Any) -> None:
        """Adds two new elements to the top of this stack."""
        self._items.append((item, item2))

    def pop(self) -> Any:
        """Remove and return the elements at the top of this stack.

        Raise an EmptyStackError if this stack is empty.

        >>> s = OnitamaStack()
        >>> s.push('hi', 'hello')
        >>> s.pop()
        ('hi', 'hello')
        """
        if self.empty():
            raise EmptyStackError
        else:
            return self._items.pop()


class EmptyStackError(Exception):
    """Exception raised when an error occurs."""
    pass
