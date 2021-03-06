import ctypes


class DynamicArray:
    """A dynamic array class akin to a simplified Python list."""

    def __init__(self):
        """Create an empty array"""
        self._n = 0
        self._capacity = 1
        self._A = self._make_array(self._capacity)

    def __len__(self):
        """Return number of elements stored in the array."""
        return self._n

    def __getitem__(self, index):
        """Return element at index `index`."""
        if not 0 <= index < self._n:
            raise IndexError("invalid index")
        return self._A[index]

    def append(self, obj):
        """Add object to end of the array."""
        if self._n == self._capacity:
            self._resize(2 * self._capacity)
        self._A[self._n] = obj
        self._n += 1

    def _resize(self, c):
        """Resize internal array to capacity c."""
        b = self._make_array(c)
        for k in range(self._n):
            b[k] = self._A[k]
        self._A = b
        self._capacity = c

    @staticmethod
    def _make_array(c):
        """Return new array with capacity c."""
        return (c * ctypes.py_object)()

    def insert(self, k, value):
        """Insert value at index k, shifting subsequent values rightward."""
        if self._n == self._capacity:
            self._resize(self._capacity * 2)

        for j in range(self._n, k, -1):
            self._A[j] = self._A[j - 1]

        self._A[k] = value
        self._n += 1

    def remove(self, value):
        """Remove first occurrence of value(or raise ValueError)."""
        for k in range(self._n):
            if self._A[k] == value:
                for j in range(k, self._n - 1):
                    self._A[j] = self._A[j + 1]
                self._A[self._n - 1] = None
                self._n -= 1
                return
        raise ValueError("value not found")
