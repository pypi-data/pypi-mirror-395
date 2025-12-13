from __future__ import annotations

from math import isclose, cos, sin

from ._vec2 import Vec2
from ._numerical_tools import sign
from .typing import Radians, Self


class Vec2i(Vec2):
    """`Vector2 integer` data structure.

    Components: `x`, `y`, only type `int`.

    Useful for storing whole numbers in 2D space.
    """

    __slots__ = ("x", "y")

    @classmethod
    def from_angle(cls, angle: Radians, /) -> Self:
        """Create a snapped direction vector of length `1` from given angle.

        Snapping is done by taking the `sign` of each component.
        Formulas used: `x = sign(cos(angle))` and `y = sign(sin(angle))`.

        Args:
            angle (Radians): Angle in radians.

        Returns:
            Self: Snapped direction vector of length `1`.
        """
        x = cos(angle)
        if isclose(x, 0, abs_tol=1e-9):
            x_snapped = 0
        else:
            x_snapped = sign(x)

        y = sin(angle)
        if isclose(y, 0, abs_tol=1e-9):
            y_snapped = 0
        else:
            y_snapped = sign(y)

        return cls(x_snapped, y_snapped)

    def __init__(self, x: int, y: int, /) -> None:
        """Initialize integer vector.

        Args:
            x (int): X component.
            y (int): Y component.
        """
        self.x = x
        self.y = y

    def __add__(self, other: Vec2i | Vec2) -> Vec2i | Vec2:
        """Add two vectors.

        Args:
            other (Vec2i | Vec2): Vector to add.

        Returns:
            Vec2i | Vec2: Result of addition.
        """
        if isinstance(other, Vec2i):
            return Vec2i(int(self.x + other.x), int(self.y + other.y))
        return Vec2(self.x + other.x, self.y + other.y)

    def __iadd__(self, other: Vec2i) -> Vec2i:
        """In-place add two integer vectors.

        Args:
            other (Vec2i): Vector to add.

        Returns:
            Vec2i: Result of addition.
        """
        self.x += other.x
        self.y += other.y
        return self

    def __sub__(self, other: Vec2i | Vec2) -> Vec2i | Vec2:
        """Subtract two vectors.

        Args:
            other (Vec2i | Vec2): Vector to subtract.

        Returns:
            Vec2i | Vec2: Result of subtraction.
        """
        if isinstance(other, Vec2i):
            return Vec2i(int(self.x - other.x), int(self.y - other.y))
        return Vec2(self.x - other.x, self.y - other.y)

    def __isub__(self, other: Vec2i) -> Vec2i:
        """In-place subtract two integer vectors.

        Args:
            other (Vec2i): Vector to subtract.

        Returns:
            Vec2i: Result of subtraction.
        """
        self.x -= other.x
        self.y -= other.y
        return self

    def __mul__(self, other: Vec2i | Vec2 | int | float) -> Vec2i | Vec2:
        """Multiply vector by another vector or scalar.

        Args:
            other (Vec2i | Vec2 | int | float): Value to multiply.

        Returns:
            Vec2i | Vec2: Result of multiplication.
        """
        if isinstance(other, Vec2i):
            return Vec2i(int(self.x * other.x), int(self.y * other.y))
        elif isinstance(other, Vec2):
            return Vec2(self.x * other.x, self.y * other.y)
        return Vec2(self.x * other, self.y * other)

    def __imul__(self, other: Vec2i) -> Vec2i:
        """In-place multiply two integer vectors.

        Args:
            other (Vec2i): Vector to multiply.

        Returns:
            Vec2i: Result of multiplication.
        """
        self.x *= other.x
        self.y *= other.y
        return self

    def __floordiv__(self, other: Vec2i | Vec2 | int | float) -> Vec2i | Vec2:
        """Floor divide vector by another vector or scalar.

        Args:
            other (Vec2i | Vec2 | int | float): Value to divide.

        Returns:
            Vec2i | Vec2: Result of floor division.
        """
        if isinstance(other, Vec2i):
            return Vec2i(
                self.x // other.x,
                self.y // other.y,
            )
        elif isinstance(other, Vec2):
            return Vec2(
                self.x // other.x,
                self.y // other.y,
            )
        elif isinstance(other, int):
            return Vec2i(
                self.x // other,
                self.y // other,
            )
        return Vec2(
            self.x // other,
            self.y // other,
        )

    def __ifloordiv__(self, other: Vec2i) -> Vec2i:
        """In-place floor divide two integer vectors.

        Args:
            other (Vec2i): Vector to divide.

        Returns:
            Vec2i: Result of floor division.
        """
        self.x //= other.x
        self.y //= other.y
        return self

    def __truediv__(self, other: Vec2i | Vec2 | int | float) -> Vec2i | Vec2:
        """Divide vector by another vector or scalar.

        Args:
            other (Vec2i | Vec2 | int | float): Value to divide.

        Returns:
            Vec2i | Vec2: Result of division.
        """
        if isinstance(other, Vec2i):
            return Vec2i(
                int(self.x / other.x),
                int(self.y / other.y),
            )
        elif isinstance(other, Vec2):
            return Vec2(
                self.x / other.x,
                self.y / other.y,
            )
        return Vec2(
            self.x / other,
            self.y / other,
        )

    def __itruediv__(self, other: Vec2i) -> Vec2i:
        """In-place divide two integer vectors.

        Args:
            other (Vec2i): Vector to divide.

        Returns:
            Vec2i: Result of division.
        """
        self.x //= other.x
        self.y //= other.y
        return self

    def __mod__(self, other: Vec2i | Vec2 | int | float) -> Vec2i | Vec2:
        """Modulo vector by another vector or scalar.

        Args:
            other (Vec2i | Vec2 | int | float): Value to modulo.

        Returns:
            Vec2i | Vec2: Result of modulo.
        """
        if isinstance(other, Vec2i):
            return Vec2i(int(self.x % other.x), int(self.y % other.y))
        elif isinstance(other, Vec2):
            return Vec2(self.x % other.x, self.y % other.y)
        return Vec2(self.x % other, self.y % other)

    def __imod__(self, other: Vec2i) -> Vec2i:
        """In-place modulo two integer vectors.

        Args:
            other (Vec2i): Vector to modulo.

        Returns:
            Vec2i: Result of modulo.
        """
        self.x %= other.x
        self.y %= other.y
        return self
