from typing import Any, Optional

# Import the raw C class (renamed to _FastQueue to indicate it's internal)
from .backend.c_queue import FastQueue as _FastQueue


class Queue(_FastQueue):
    """
    A high-performance Queue implemented in C.

    This class wraps the low-level C extension to provide
    type hints and proper documentation.
    """

    def enqueue(self, item: Any) -> None:
        """
        Add an item to the end of the queue.

        Args:
            item: The object to add.
        """
        # We don't need to write 'super().enqueue(item)'
        # because this class INHERITS the C method directly!
        return super().enqueue(item)

    def dequeue(self) -> Any:
        """
        Remove and return the item from the front of the queue.

        Returns:
            The item at the front.

        Raises:
            IndexError: If the queue is empty.
        """
        return super().dequeue()

    def is_empty(self) -> bool:
        """Check if the queue is empty."""
        # Example of adding PURE PYTHON logic on top of the C struct
        # Assuming you haven't implemented __len__ in C yet (though you should!)
        try:
            # This relies on the C implementation raising IndexError on peek/dequeue
            # But ideally, you'd implement __len__ in C.
            return len(self) == 0
        except TypeError:
            # Fallback if __len__ isn't ready in C
            return False
