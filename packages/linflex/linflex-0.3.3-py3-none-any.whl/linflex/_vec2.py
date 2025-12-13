from __future__ import annotations

from math import sqrt, floor, ceil, cos, sin, atan2, inf as INF
from typing import Iterator, Literal, Any

from ._numerical_tools import lerp, sign, clamp, move_toward
from ._class_constant import class_constant
from .typing import Radians, Self


class Vec2:
    """`Vector2` data structure.

    Components: `x`, `y`.

    Useful for storing position or direction in 2D space.
    """

    __slots__ = ("x", "y")

    @class_constant
    def ZERO(cls: type[Self]) -> Self:  # type: ignore
        """Vector with all components set to `0`."""
        return cls(0, 0)

    @class_constant
    def ONE(cls: type[Self]) -> Self:  # type: ignore
        """Vector with all components set to `1`."""
        return cls(1, 1)

    @class_constant
    def INF(cls: type[Self]) -> Self:  # type: ignore
        """Vector with all components set to `math.inf`."""
        return cls(INF, INF)

    @class_constant
    def LEFT(cls: type[Self]) -> Self:  # type: ignore
        """Left unit vector.

        Represents the `left direction`.
        """
        return cls(-1, 0)

    @class_constant
    def RIGHT(cls: type[Self]) -> Self:  # type: ignore
        """Right unit vector.

        Represents the `right direction`.
        """
        return cls(1, 0)

    @class_constant
    def UP(cls: type[Self]) -> Self:  # type: ignore
        """Up unit vector.

        Represents the `up direction`.

        `NOTE`
        Since `positive Y` points `downward` in this 2D coordinate system,
        the `up direction` is represented by `-Y`.
        """
        return cls(0, -1)

    @class_constant
    def DOWN(cls: type[Self]) -> Self:  # type: ignore
        """Down unit vector.

        Represents the `down direction`.

        `NOTE`
        Since `positive Y` points `downward` in this 2D coordinate system,
        the `down direction` is represented by `+Y`.
        """
        return cls(0, 1)

    @classmethod
    def from_angle(cls, angle: Radians, /) -> Self:
        """Create a direction vector of length 1 from given angle.

        Args:
            angle (Radians): Angle in radians.

        Returns:
            Self: Direction vector of length 1.
        """
        x = cos(angle)
        y = sin(angle)
        return cls(x, y)

    def __init__(self, x: float, y: float, /) -> None:
        """Initialize vector.

        Args:
            x (float): X component.
            y (float): Y component.
        """
        self.x = x
        self.y = y

    def __reduce__(self) -> tuple[type[Self], tuple[float, float]]:
        """Helper for pickling support."""
        return (self.__class__, (self.x, self.y))

    def __len__(self) -> Literal[2]:
        """Return the number of components in the vector.

        Returns:
            int: Number of components (always `2`).
        """
        return 2

    def __iter__(self) -> Iterator[float]:
        """Iterate over the components of the vector.

        Returns:
            Iterator[float]: Iterator over `x` and `y`.
        """
        return iter((self.x, self.y))

    def __getitem__(self, axis_index: Literal[0, 1]) -> float:
        """Get a component by index.

        Args:
            axis_index (int): Axis index, `0` for `x` and `1` for `y`.

        Returns:
            float: Value of the component.

        Raises:
            ValueError: Invalid axis index.
        """
        if axis_index == 0:
            return self.x
        elif axis_index == 1:
            return self.y
        raise IndexError(
            f"axis index '{axis_index}' does not correspond to x or y axis."
        )

    def __setitem__(self, axis_index: Literal[0, 1], value: float) -> None:
        """Set a component by axis index.

        Args:
            axis_index (int): Axis index, `0` for `x` and `1` for `y`.
            value (float): New axis value.

        Raises:
            ValueError: Invalid axis index.
        """
        if axis_index == 0:
            self.x = value
        elif axis_index == 1:
            self.y = value
        raise IndexError(
            f"axis index '{axis_index}' does not correspond to x or y axis."
        )

    def __abs__(self) -> Self:
        """Return a vector with absolute values of each component.

        Returns:
            Self: Vector with absolute values.
        """
        return self.__class__(
            abs(self.x),
            abs(self.y),
        )

    def __round__(self, ndigits: int = 0) -> Self:
        """Return a vector with each component rounded.

        Args:
            ndigits (int): Number of digits to round to.

        Returns:
            Self: Rounded vector.
        """
        return self.__class__(
            round(self.x, ndigits),
            round(self.y, ndigits),
        )

    def __floor__(self) -> Self:
        """Return a vector with each component floored.

        Returns:
            Self: Floored vector.
        """
        return self.__class__(
            floor(self.x),
            floor(self.y),
        )

    def __ceil__(self) -> Self:
        """Return a vector with each component ceiled.

        Returns:
            Self: Ceiled vector.
        """
        return self.__class__(
            ceil(self.x),
            ceil(self.y),
        )

    def __neg__(self) -> Vec2:
        """Return a vector with each component negated.

        Returns:
            Vec2: Negated vector.
        """
        return Vec2(-self.x, -self.y)

    def __add__(self, other: Vec2) -> Vec2:
        """Add two vectors.

        Args:
            other (Vec2): Vector to add.

        Returns:
            Vec2: Result of addition.
        """
        return Vec2(self.x + other.x, self.y + other.y)

    def __radd__(self, other: Vec2 | int | float) -> Vec2:
        """Right-hand addition.

        Adds this vector to another vector or scalar, when this vector is on the right side of the `+` operator.

        Args:
            other (Vec2 | int | float): Value to add.

        Returns:
            Vec2: Result of addition.
        """
        if isinstance(other, Vec2):
            return Vec2(other.x + self.x, other.y + self.y)
        return Vec2(other + self.x, other + self.y)

    def __iadd__(self, other: Vec2) -> Vec2:
        """In-place add two vectors.

        Args:
            other (Vec2): Vector to add.

        Returns:
            Vec2: Result of addition.
        """
        self.x += other.x
        self.y += other.y
        return self

    def __sub__(self, other: Vec2) -> Vec2:
        """Subtract two vectors.

        Args:
            other (Vec2): Vector to subtract.

        Returns:
            Vec2: Result of subtraction.
        """
        return Vec2(self.x - other.x, self.y - other.y)

    def __rsub__(self, other: Vec2 | int | float) -> Vec2:
        """Right-hand subtraction.

        Subtracts this vector from another vector or scalar, when this vector is on the right side of the `-` operator.

        Args:
            other (Vec2 | int | float): Value to subtract from.

        Returns:
            Vec2: Result of subtraction.
        """
        if isinstance(other, Vec2):
            return Vec2(other.x - self.x, other.y - self.y)
        return Vec2(other - self.x, other - self.y)

    def __isub__(self, other: Vec2) -> Vec2:
        """In-place subtract two vectors.

        Args:
            other (Vec2): Vector to subtract.

        Returns:
            Vec2: Result of subtraction.
        """
        self.x -= other.x
        self.y -= other.y
        return self

    def __mul__(self, other: Vec2 | int | float) -> Vec2:
        """Multiply vector by another vector or scalar.

        Args:
            other (Vec2 | int | float): Value to multiply.

        Returns:
            Vec2: Result of multiplication.
        """
        if isinstance(other, Vec2):
            return Vec2(
                self.x * other.x,
                self.y * other.y,
            )
        return Vec2(
            self.x * other,
            self.y * other,
        )

    def __rmul__(self, other: Vec2 | int | float) -> Vec2:
        """Right-hand multiplication.

        Multiplies another vector or scalar by this vector, when this vector is on the right side of the `*` operator.

        Args:
            other (Vec2 | int | float): Value to multiply.

        Returns:
            Vec2: Result of multiplication.
        """
        if isinstance(other, Vec2):
            return Vec2(other.x * self.x, other.y * self.y)
        return Vec2(other * self.x, other * self.y)

    def __imul__(self, other: Vec2 | int | float) -> Vec2:
        """In-place multiply vector by another vector or scalar.

        Args:
            other (Vec2 | int | float): Value to multiply.

        Returns:
            Vec2: Result of multiplication.
        """
        if isinstance(other, Vec2):
            self.x *= other.x
            self.y *= other.y
        else:
            self.x *= other
            self.y *= other
        return self

    def __floordiv__(self, other: Vec2 | int | float) -> Vec2:
        """Floor divide vector by another vector or scalar.

        Args:
            other (Vec2 | int | float): Value to divide.

        Returns:
            Vec2: Result of floor division.
        """
        if isinstance(other, Vec2):
            return Vec2(
                self.x // other.x,
                self.y // other.y,
            )
        return Vec2(
            self.x // other,
            self.y // other,
        )

    def __rfloordiv__(self, other: Vec2 | int | float) -> Vec2:
        """Right-hand floor division.

        Floor divides another vector or scalar by this vector, when this vector is on the right side of the `//` operator.

        Args:
            other (Vec2 | int | float): Value to divide.

        Returns:
            Vec2: Result of floor division.
        """
        if isinstance(other, Vec2):
            return Vec2(other.x // self.x, other.y // self.y)
        return Vec2(other // self.x, other // self.y)

    def __ifloordiv__(self, other: Vec2 | int | float) -> Vec2:
        """In-place floor divide vector by another vector or scalar.

        Args:
            other (Vec2 | int | float): Value to divide.

        Returns:
            Vec2: Result of floor division.
        """
        if isinstance(other, Vec2):
            self.x //= other.x
            self.y //= other.y
        else:
            self.x //= other
            self.y //= other
        return self

    def __truediv__(self, other: Vec2 | int | float) -> Vec2:
        """Divide vector by another vector or scalar.

        Args:
            other (Vec2 | int | float): Value to divide.

        Returns:
            Vec2: Result of division.
        """
        if isinstance(other, Vec2):
            return Vec2(
                self.x / other.x,
                self.y / other.y,
            )
        return Vec2(
            self.x / other,
            self.y / other,
        )

    def __rtruediv__(self, other: Vec2 | int | float) -> Vec2:
        """Right-hand true division.

        Divides another vector or scalar by this vector, when this vector is on the right side of the `/` operator.

        Args:
            other (Vec2 | int | float): Value to divide.

        Returns:
            Vec2: Result of division.
        """
        if isinstance(other, Vec2):
            return Vec2(other.x / self.x, other.y / self.y)
        return Vec2(other / self.x, other / self.y)

    def __itruediv__(self, other: Vec2 | int | float) -> Vec2:
        """In-place divide vector by another vector or scalar.

        Args:
            other (Vec2 | int | float): Value to divide.

        Returns:
            Vec2: Result of division.
        """
        if isinstance(other, Vec2):
            self.x /= other.x
            self.y /= other.y
        else:
            self.x /= other
            self.y /= other
        return self

    def __mod__(self, other: Vec2 | int | float) -> Vec2:
        """Modulo vector by another vector or scalar.

        Args:
            other (Vec2 | int | float): Value to modulo.

        Returns:
            Vec2: Result of modulo.
        """
        if isinstance(other, Vec2):
            return Vec2(
                self.x % other.x,
                self.y % other.y,
            )
        return Vec2(
            self.x % other,
            self.y % other,
        )

    def __rmod__(self, other: Vec2 | int | float) -> Vec2:
        """Right-hand modulo.

        Computes the modulo of another vector or scalar by this vector, when this vector is on the right side of the `%` operator.

        Args:
            other (Vec2 | int | float): Value to modulo.

        Returns:
            Vec2: Result of modulo.
        """
        if isinstance(other, Vec2):
            return Vec2(other.x % self.x, other.y % self.y)
        return Vec2(other % self.x, other % self.y)

    def __imod__(self, other: Vec2 | int | float) -> Vec2:
        """In-place modulo vector by another vector or scalar.

        Args:
            other (Vec2 | int | float): Value to modulo.

        Returns:
            Vec2: Result of modulo.
        """
        if isinstance(other, Vec2):
            self.x %= other.x
            self.y %= other.y
        else:
            self.x %= other
            self.y %= other
        return self

    def __eq__(self, other: Vec2) -> bool:
        """Check if two vectors are equal.

        Args:
            other (Vec2): Vector to compare.

        Returns:
            bool: True if equal, False otherwise.
        """
        return (self.x == other.x) and (self.y == other.y)

    def __ne__(self, other: Vec2) -> bool:
        """Check if two vectors are not equal.

        Args:
            other (Vec2): Vector to compare.

        Returns:
            bool: True if not equal, False otherwise.
        """
        return (self.x != other.x) or (self.y != other.y)

    def __gt__(self, other: Vec2) -> bool:
        """Check if this vector is greater than another.

        Args:
            other (Vec2): Vector to compare.

        Returns:
            bool: True if greater, False otherwise.
        """
        return (self.x > other.x) and (self.y > other.y)

    def __lt__(self, other: Vec2) -> bool:
        """Check if this vector is less than another.

        Args:
            other (Vec2): Vector to compare.

        Returns:
            bool: True if less, False otherwise.
        """
        return (self.x < other.x) and (self.y < other.y)

    def __ge__(self, other: Vec2) -> bool:
        """Check if this vector is greater than or equal to another.

        Args:
            other (Vec2): Vector to compare.

        Returns:
            bool: True if greater or equal, False otherwise.
        """
        return (self.x >= other.x) and (self.y >= other.y)

    def __le__(self, other: Vec2) -> bool:
        """Check if this vector is less than or equal to another.

        Args:
            other (Vec2): Vector to compare.

        Returns:
            bool: True if less or equal, False otherwise.
        """
        return (self.x <= other.x) and (self.y <= other.y)

    def __copy__(self) -> Self:
        """Return a copy of the vector.

        Returns:
            Self: A new copy.
        """
        return self.__class__(self.x, self.y)

    def __deepcopy__(self, _memo: dict[int, Any]) -> Self:
        """Return a deep copy of the vector.

        Args:
            _memo (dict): Memoization dictionary.

        Returns:
            Self: A new deep copy.
        """
        return self.__class__(self.x, self.y)

    def copy(self) -> Self:
        """Return a vector copy.

        Returns:
            Self: A new copy.
        """
        return self.__copy__()

    def length(self) -> float:
        """Return the length of the vector.

        Returns:
            float: Length.
        """
        if self.x == 0 and self.y == 0:
            return 0
        return sqrt(self.x * self.x + self.y * self.y)

    def length_squared(self) -> float:
        """Return the length of the vector squared.

        Returns:
            float: Length squared.
        """
        if self.x == 0 and self.y == 0:
            return 0
        return self.x * self.x + self.y * self.y

    def distance_to(self, other: Vec2, /) -> float:
        """Return the relative distance to the other point.

        Args:
            other (Vec2): Other point.

        Returns:
            float: Distance.
        """
        return (other - self).length()

    def distance_squared_to(self, other: Vec2, /) -> float:
        """Return the relative distance to the other point, squared.

        Args:
            other (Vec2): Other point.

        Returns:
            float: Distance squared.
        """
        return (other - self).length_squared()

    def normalized(self) -> Vec2:
        """Return a vector with length of 1, still with same direction.

        Returns:
            Vec2: Normalized vector.
        """
        length = self.length()
        if length == 0:
            return Vec2(0, 0)
        return self / self.length()

    def dot(self, other: Vec2, /) -> float:
        """Return the dot product between two 2D vectors.

        Args:
            other (Vec2): Other vector.

        Returns:
            float: Dot product.
        """
        return self.x * other.x + self.y * other.y

    def cross(self, other: Vec2, /) -> float:
        """Cross product interpreted in 2D space, like defined in the `Godot Game Engine`.

        Args:
            other (Vec2): Other vector.

        Returns:
            float: Cross product.
        """
        return self.x * other.y - self.y * other.x

    def direction_to(self, other: Vec2, /) -> Vec2:
        """Return the direction to the other point.

        Args:
            other (Vec2): Other point.

        Returns:
            Vec2: Direction.
        """
        return (other - self).normalized()

    def angle(self, /) -> float:
        """Return the angle (measured in radians), using `atan2`.

        Returns:
            float: Angle given in radians.
        """
        return atan2(self.y, self.x)

    def angle_to(self, other: Vec2, /) -> float:
        """Return the angle (measured in radians) to the other point.

        Args:
            other (Vec2): Other point.

        Returns:
            float: Angle given in radians.
        """
        return (other - self).angle()

    def lerp(self, target: Vec2, /, weight: float) -> Vec2:
        """Lerp towards vector `target` with `weight` ranging from 0 to 1.

        Args:
            target (Vec2): Target to lerp towards.
            weight (float): Percentage to lerp.

        Returns:
            Vec2: Vector after performing interpolation.
        """
        return Vec2(
            lerp(self.x, target.x, weight),
            lerp(self.y, target.y, weight),
        )

    def sign(self) -> Vec2:
        """Return a Vec2 with each component being the sign of the vector.

        Returns:
            Vec2: Vector with signed components.
        """
        return Vec2(
            sign(self.x),
            sign(self.y),
        )

    def clamp(self, smallest: Vec2, largest: Vec2, /) -> Vec2:
        """Return a new clamped vector.

        Args:
            smallest (Vec2): Lower bound for x and y.
            largest (Vec2): Upper bound for x and y.

        Returns:
            Vec2: Vector clamped.
        """
        return Vec2(
            clamp(self.x, smallest.x, largest.x),
            clamp(self.y, smallest.y, largest.y),
        )

    def move_toward(self, stop: Vec2, /, change: int | float) -> Vec2:
        """Move toward a vector, from a vector, with given change.

        Args:
            stop (Vec2): Target vector.
            change (int | float): Max distance to move.

        Returns:
            Vec2: New vector moved.
        """
        return Vec2(
            move_toward(self.x, stop.x, change),
            move_toward(self.y, stop.y, change),
        )

    def rotated(self, angle: float, /) -> Vec2:
        """Return a vector rotated clockwise by `angle` given in radians.

        Args:
            angle (float): Radians to rotate with.

        Returns:
            Vec2: Rotated vector.
        """
        cos_rad = cos(angle)
        sin_rad = sin(angle)
        x = cos_rad * self.x + sin_rad * self.y
        y = -sin_rad * self.x + cos_rad * self.y
        return Vec2(x, y)

    def rotated_around(self, angle: float, point: Vec2) -> Vec2:
        """Return a vector rotated by `angle` given in radians, around `point`.

        Args:
            angle (float): Radians to rotate with.
            point (Vec2): Point to rotate around.

        Returns:
            Vec2: Vector rotated around `point`.
        """
        diff = self - point
        cos_rad = cos(angle)
        sin_rad = sin(angle)
        x = point.x + cos_rad * diff.x + sin_rad * diff.y
        y = point.y + -sin_rad * diff.x + cos_rad * diff.y
        return Vec2(x, y)
