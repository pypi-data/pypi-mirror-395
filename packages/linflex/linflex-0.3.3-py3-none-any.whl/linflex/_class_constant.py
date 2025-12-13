from typing import TypeVar, Callable, Generic, Any


T = TypeVar("T")


class class_constant(Generic[T]):
    def __init__(self, method: Callable[[type[T]], T]) -> None:
        self.fget: Callable[[type[T]], T] = method

    def __get__(self, _instance: Any, owner: type[T]) -> T:
        return self.fget(owner)
