from collections.abc import ItemsView, Iterator, KeysView, ValuesView

import pydantic


class ListOf[T](pydantic.RootModel[list[T]]):
    """
    Pydantic RootModel for representing a list of other models.
    """

    def __iter__(self) -> Iterator[T]:  # type:ignore[override]
        """Iterate over the items in the list."""
        return iter(self.root)

    def __getitem__(self, item: int) -> T:
        """Get an item by index."""
        return self.root[item]

    def __len__(self) -> int:
        """Get the length of the list."""
        return len(self.root)


class DictOf[K, V](pydantic.RootModel[dict[K, V]]):
    """
    Pydantic RootModel for representing a dict
    """

    def __getitem__(self, key: K) -> V:
        """Get a value by key."""
        return self.root[key]

    def __setitem__(self, key: K, value: V) -> None:
        """Set a value for a key."""
        self.root[key] = value

    def __delitem__(self, key: K) -> None:
        """Delete a key-value pair."""
        del self.root[key]

    def __contains__(self, key: K) -> bool:
        """Check if a key exists in the dict."""
        return key in self.root

    def __iter__(self) -> Iterator[K]:  # type:ignore[override]
        """Iterate over the keys in the dict."""
        return iter(self.root)

    def __len__(self) -> int:
        """Get the number of key-value pairs."""
        return len(self.root)

    def keys(self) -> KeysView[K]:
        """Get a view of the dict's keys."""
        return self.root.keys()

    def values(self) -> ValuesView[V]:
        """Get a view of the dict's values."""
        return self.root.values()

    def items(self) -> ItemsView[K, V]:
        """Get a view of the dict's key-value pairs."""
        return self.root.items()

    def get(self, key: K, default: V | None = None) -> V | None:
        """Get a value by key with optional default."""
        return self.root.get(key, default)

    def setdefault(self, key: K, default: V) -> V:
        """Get a value by key, setting it to default if not present."""
        return self.root.setdefault(key, default)

    def update(self, other: dict[K, V]) -> None:
        """Update the dict with key-value pairs from another dict."""
        self.root.update(other)

    def pop(self, key: K, default: V | None = None) -> V | None:
        """Remove and return a value by key with optional default."""
        return self.root.pop(key, default)

    def popitem(self) -> tuple[K, V]:
        """Remove and return an arbitrary key-value pair."""
        return self.root.popitem()

    def clear(self) -> None:
        """Remove all key-value pairs from the dict."""
        self.root.clear()
