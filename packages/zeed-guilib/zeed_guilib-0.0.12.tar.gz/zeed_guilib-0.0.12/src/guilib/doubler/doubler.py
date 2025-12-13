from typing import Any


class Doubler[T]:
    def __init__(self, left: T, right: T) -> None:
        self._left = left
        self._right = right

    def __getattr__(self, name: str) -> 'Doubler[Any]':
        return Doubler(getattr(self._left, name), getattr(self._right, name))

    def __call__(self, *args: Any, **kwargs: Any) -> 'Doubler[Any]':
        if not callable(self._left) or not callable(self._right):
            raise TypeError

        return Doubler(
            self._left(*args, **kwargs), self._right(*args, **kwargs)
        )
