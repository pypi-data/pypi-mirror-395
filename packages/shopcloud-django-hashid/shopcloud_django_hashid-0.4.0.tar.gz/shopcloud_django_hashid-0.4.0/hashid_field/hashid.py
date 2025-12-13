"""Hashid wrapper class.

Provides a wrapper around hashid values that supports integer operations,
comparison, hashing, and pickling.
"""

from __future__ import annotations

from typing import Any

from hashids import Hashids


class Hashid:
    """Wrapper class for hashid values.

    Stores both the integer value and its hashid representation.
    Supports comparison with integers and strings, arithmetic operations,
    and can be used as dictionary keys.

    Args:
        value: The integer ID or hashid string to wrap
        salt: Salt for encoding (default: "")
        min_length: Minimum length of the hashid (default: 0)
        alphabet: Character set for encoding (default: Hashids.ALPHABET)
        prefix: Prefix to add to the hashid string (default: "")
        hashids: Pre-built Hashids encoder instance (optional)

    Raises:
        ValueError: If value is negative or an invalid hashid string
    """

    __slots__ = ("_id", "_hashid", "_prefix", "_hashids", "_salt", "_min_length", "_alphabet")

    def __init__(
        self,
        value: int | str,
        salt: str = "",
        min_length: int = 0,
        alphabet: str = Hashids.ALPHABET,
        prefix: str = "",
        hashids: Hashids | None = None,
    ) -> None:
        self._prefix = prefix
        self._salt = salt
        self._min_length = min_length
        self._alphabet = alphabet
        self._hashids = hashids or Hashids(salt=salt, min_length=min_length, alphabet=alphabet)

        if isinstance(value, int):
            if value < 0:
                raise ValueError(f"Hashid value must be non-negative, got {value}")
            self._id = value
            self._hashid = self._prefix + self._hashids.encode(value)
        elif isinstance(value, str):
            # Handle prefixed hashids
            hashid_str = value
            if prefix and hashid_str.startswith(prefix):
                hashid_str = hashid_str[len(prefix) :]

            decoded = self._hashids.decode(hashid_str)
            if not decoded:
                raise ValueError(f"Invalid hashid string: {value}")
            self._id = decoded[0]
            self._hashid = self._prefix + hashid_str
        elif isinstance(value, Hashid):
            self._id = value._id
            self._hashid = value._hashid
        else:
            raise TypeError(f"Hashid value must be int or str, got {type(value).__name__}")

    @property
    def id(self) -> int:
        """Get the underlying integer value."""
        return self._id

    @property
    def hashid(self) -> str:
        """Get the hashid string representation (with prefix if any)."""
        return self._hashid

    @property
    def prefix(self) -> str:
        """Get the prefix."""
        return self._prefix

    @property
    def hashids(self) -> Hashids:
        """Get the Hashids encoder instance."""
        return self._hashids

    # Comparison operators - compare by underlying id
    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Hashid):
            return self._id == other._id
        if isinstance(other, int):
            return self._id == other
        if isinstance(other, str):
            return self._hashid == other
        return NotImplemented

    def __ne__(self, other: Any) -> bool:
        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        return not result

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, Hashid):
            return self._id < other._id
        if isinstance(other, int):
            return self._id < other
        return NotImplemented

    def __le__(self, other: Any) -> bool:
        if isinstance(other, Hashid):
            return self._id <= other._id
        if isinstance(other, int):
            return self._id <= other
        return NotImplemented

    def __gt__(self, other: Any) -> bool:
        if isinstance(other, Hashid):
            return self._id > other._id
        if isinstance(other, int):
            return self._id > other
        return NotImplemented

    def __ge__(self, other: Any) -> bool:
        if isinstance(other, Hashid):
            return self._id >= other._id
        if isinstance(other, int):
            return self._id >= other
        return NotImplemented

    # Arithmetic operators - delegate to underlying id
    def __add__(self, other: Any) -> int:
        if isinstance(other, (int, Hashid)):
            return self._id + int(other)
        return NotImplemented

    def __radd__(self, other: Any) -> int:
        if isinstance(other, int):
            return other + self._id
        return NotImplemented

    def __sub__(self, other: Any) -> int:
        if isinstance(other, (int, Hashid)):
            return self._id - int(other)
        return NotImplemented

    def __rsub__(self, other: Any) -> int:
        if isinstance(other, int):
            return other - self._id
        return NotImplemented

    def __mul__(self, other: Any) -> int:
        if isinstance(other, (int, Hashid)):
            return self._id * int(other)
        return NotImplemented

    def __rmul__(self, other: Any) -> int:
        if isinstance(other, int):
            return other * self._id
        return NotImplemented

    def __truediv__(self, other: Any) -> float:
        if isinstance(other, (int, Hashid)):
            return self._id / int(other)
        return NotImplemented

    def __rtruediv__(self, other: Any) -> float:
        if isinstance(other, int):
            return other / self._id
        return NotImplemented

    def __floordiv__(self, other: Any) -> int:
        if isinstance(other, (int, Hashid)):
            return self._id // int(other)
        return NotImplemented

    def __rfloordiv__(self, other: Any) -> int:
        if isinstance(other, int):
            return other // self._id
        return NotImplemented

    def __mod__(self, other: Any) -> int:
        if isinstance(other, (int, Hashid)):
            return self._id % int(other)
        return NotImplemented

    def __rmod__(self, other: Any) -> int:
        if isinstance(other, int):
            return other % self._id
        return NotImplemented

    def __pow__(self, other: Any) -> int:
        if isinstance(other, (int, Hashid)):
            return self._id ** int(other)
        return NotImplemented

    def __rpow__(self, other: Any) -> int:
        if isinstance(other, int):
            return other**self._id
        return NotImplemented

    # Bitwise operators
    def __and__(self, other: Any) -> int:
        if isinstance(other, (int, Hashid)):
            return self._id & int(other)
        return NotImplemented

    def __rand__(self, other: Any) -> int:
        if isinstance(other, int):
            return other & self._id
        return NotImplemented

    def __or__(self, other: Any) -> int:
        if isinstance(other, (int, Hashid)):
            return self._id | int(other)
        return NotImplemented

    def __ror__(self, other: Any) -> int:
        if isinstance(other, int):
            return other | self._id
        return NotImplemented

    def __xor__(self, other: Any) -> int:
        if isinstance(other, (int, Hashid)):
            return self._id ^ int(other)
        return NotImplemented

    def __rxor__(self, other: Any) -> int:
        if isinstance(other, int):
            return other ^ self._id
        return NotImplemented

    def __lshift__(self, other: Any) -> int:
        if isinstance(other, (int, Hashid)):
            return self._id << int(other)
        return NotImplemented

    def __rlshift__(self, other: Any) -> int:
        if isinstance(other, int):
            return other << self._id
        return NotImplemented

    def __rshift__(self, other: Any) -> int:
        if isinstance(other, (int, Hashid)):
            return self._id >> int(other)
        return NotImplemented

    def __rrshift__(self, other: Any) -> int:
        if isinstance(other, int):
            return other >> self._id
        return NotImplemented

    # Conversion methods
    def __int__(self) -> int:
        return self._id

    def __str__(self) -> str:
        return self._hashid

    def __repr__(self) -> str:
        return f"Hashid({self._id!r}): {self._hashid}"

    def __hash__(self) -> int:
        return hash(self._id)

    def __len__(self) -> int:
        return len(self._hashid)

    def __bool__(self) -> bool:
        return True  # Hashid is always truthy (even for id=0)

    # Pickling support
    def __getstate__(self) -> dict[str, Any]:
        """Return state for pickling."""
        return {
            "_id": self._id,
            "_hashid": self._hashid,
            "_prefix": self._prefix,
            "_salt": self._salt,
            "_min_length": self._min_length,
            "_alphabet": self._alphabet,
        }

    def __setstate__(self, state: dict[str, Any]) -> None:
        """Restore state from pickle."""
        self._id = state["_id"]
        self._hashid = state["_hashid"]
        self._prefix = state["_prefix"]
        self._hashids = Hashids(
            salt=state["_salt"],
            min_length=state["_min_length"],
            alphabet=state["_alphabet"],
        )

    # For JSON serialization
    def __json__(self) -> str:
        return self._hashid
