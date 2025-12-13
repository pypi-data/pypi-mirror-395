from __future__ import annotations

from math import sqrt, floor, ceil, cos, sin, atan2, inf as INF
from typing import Iterator, Literal, Any

from ._numerical_tools import lerp, sign, clamp, move_toward
from ._class_constant import class_constant
from .typing import Self


class Vec3:
    """`Vector3` data structure.

    Components: `x`, `y`, `z`.

    Useful for storing position or direction in 3D space.
    """

    __slots__ = ("x", "y", "z")

    @class_constant
    def ZERO(cls: type[Self]) -> Self:  # type: ignore
        """Vector with all components set to `0`."""
        return cls(0, 0, 0)

    @class_constant
    def ONE(cls: type[Self]) -> Self:  # type: ignore
        """Vector with all components set to `1`."""
        return cls(1, 1, 1)

    @class_constant
    def INF(cls: type[Self]) -> Self:  # type: ignore
        """Vector with all components set to `math.inf`."""
        return cls(INF, INF, INF)

    @class_constant
    def LEFT(cls: type[Self]) -> Self:  # type: ignore
        """Left unit vector.

        Represents both local direction left, and the global direction west.
        """
        return cls(-1, 0, 0)

    @class_constant
    def RIGHT(cls: type[Self]) -> Self:  # type: ignore
        """Right unit vector.

        Represents both local direction right, and global direction east.
        """
        return cls(1, 0, 0)

    @class_constant
    def UP(cls: type[Self]) -> Self:  # type: ignore
        """Up unit vector.

        Represents up direction.
        """
        return cls(0, 1, 0)

    @class_constant
    def DOWN(cls: type[Self]) -> Self:  # type: ignore
        """Down unit vector.

        Represents down direction.
        """
        return cls(0, -1, 0)

    @class_constant
    def FORWARD(cls: type[Self]) -> Self:  # type: ignore
        """Forward unit vector.

        Represents both local direction forward, and global direction north.
        """
        return cls(0, 0, 1)

    @class_constant
    def BACK(cls: type[Self]) -> Self:  # type: ignore
        """Back/backward unit vector.

        Represents local direction back/backwards, and global direction south.
        """
        return cls(0, 0, -1)

    @classmethod
    def from_angles(cls, angles: Vec3, /) -> Self:
        """Create a direction vector of length `1` from given angles.

        Args:
            angles (Vec3): Vector representing rotation around each axis (`x`, `y`, `z`).

        Returns:
            Self: Direction vector of length `1`.
        """
        x_cos = cos(angles.x)
        y_cos = cos(angles.y)
        z_cos = cos(angles.z)

        x_sin = sin(angles.x)
        y_sin = sin(angles.y)
        z_sin = sin(angles.z)

        x = y_cos * z_cos
        y = x_sin * y_sin * z_cos + x_cos * z_sin
        z = x_cos * y_sin * z_cos - x_sin * z_sin

        return cls(x, y, z)

    def __init__(self, x: float, y: float, z: float, /) -> None:
        """Initialize vector.

        Args:
            x (float): X component.
            y (float): Y component.
            z (float): Z component.
        """
        self.x = x
        self.y = y
        self.z = z

    def __reduce__(self) -> tuple[type[Self], tuple[float, float]]:
        """Helper for pickling support."""
        return (self.__class__, (self.x, self.y))

    def __len__(self) -> Literal[3]:
        """Return the number of components in the vector.

        Returns:
            int: Number of components (always `3`).
        """
        return 3

    def __iter__(self) -> Iterator[float]:
        """Iterate over the components of the vector.

        Returns:
            Iterator[float]: Iterator over `x`, `y`, and `z`.
        """
        return iter((self.x, self.y, self.z))

    def __getitem__(self, axis_index: Literal[0, 1, 2]) -> float:
        """Get a component by axis index.

        Args:
            axis_index (int): Axis index, `0` for `x`, `1` for `y` and `2` for `z`.

        Returns:
            float: Value of the component.

        Raises:
            ValueError: Invalid axis index.
        """
        if axis_index == 0:
            return self.x
        elif axis_index == 1:
            return self.y
        elif axis_index == 2:
            return self.z
        raise IndexError(
            f"axis index '{axis_index}' does not correspond to x or y or z axis."
        )

    def __setitem__(self, axis_index: Literal[0, 1], value: float) -> None:
        """Set a component by axis index.

        Args:
            axis_index (int): Axis index, `0` for `x`, `1` for `y` and `2` for `z`.
            value (float): New axis value.

        Raises:
            ValueError: Invalid axis index.
        """
        if axis_index == 0:
            self.x = value
        elif axis_index == 1:
            self.y = value
        elif axis_index == 2:
            self.z = value
        raise IndexError(
            f"axis index '{axis_index}' does not correspond to x, y or z axis."
        )

    def __repr__(self) -> str:
        """Create representation.

        Returns:
            str: Representation containing the `x`, `y`, and `z` components.
        """
        return f"{self.__class__.__name__}({self.x}, {self.y}, {self.z})"

    def __str__(self) -> str:
        """Create string representation.

        Returns:
            str: Representation containing the `x`, `y`, and `z` components.
        """
        return f"{self.__class__.__name__}({self.x}, {self.y}, {self.z})"

    def __bool__(self) -> bool:
        """Return whether `x`, `y`, or `z` is not zero.

        Returns:
            bool: Truthiness.
        """
        return bool(self.x or self.y or self.z)

    def __abs__(self) -> Self:
        """Return a vector with absolute values of each component.

        Returns:
            Self: Vector with absolute values.
        """
        return self.__class__(abs(self.x), abs(self.y), abs(self.z))

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
            round(self.z, ndigits),
        )

    def __floor__(self) -> Self:
        """Return a vector with each component floored.

        Returns:
            Self: Floored vector.
        """
        return self.__class__(
            floor(self.x),
            floor(self.y),
            floor(self.z),
        )

    def __ceil__(self) -> Self:
        """Return a vector with each component ceiled.

        Returns:
            Self: Ceiled vector.
        """
        return self.__class__(
            ceil(self.x),
            ceil(self.y),
            ceil(self.z),
        )

    def __add__(self, other: Vec3) -> Vec3:
        """Add two vectors.

        Args:
            other (Vec3): Vector to add.

        Returns:
            Vec3: Result of addition.
        """
        return Vec3(
            self.x + other.x,
            self.y + other.y,
            self.z + other.z,
        )

    def __radd__(self, other: Vec3 | int | float) -> Vec3:
        """Right-hand addition.

        Adds this vector to another vector or scalar, when this vector is on the right side of the `+` operator.

        Args:
            other (Vec3 | int | float): Value to add.

        Returns:
            Vec3: Result of addition.
        """
        if isinstance(other, Vec3):
            return Vec3(other.x + self.x, other.y + self.y, other.z + self.z)
        return Vec3(other + self.x, other + self.y, other + self.z)

    def __iadd__(self, other: Vec3) -> Vec3:
        """In-place add two vectors.

        Args:
            other (Vec3): Vector to add.

        Returns:
            Vec3: Result of addition.
        """
        self.x += other.x
        self.y += other.y
        self.z += other.z
        return self

    def __sub__(self, other: Vec3) -> Vec3:
        """Subtract two vectors.

        Args:
            other (Vec3): Vector to subtract.

        Returns:
            Vec3: Result of subtraction.
        """
        return Vec3(
            self.x - other.x,
            self.y - other.y,
            self.z - other.z,
        )

    def __rsub__(self, other: Vec3 | int | float) -> Vec3:
        """Right-hand subtraction.

        Subtracts this vector from another vector or scalar, when this vector is on the right side of the `-` operator.

        Args:
            other (Vec3 | int | float): Value to subtract from.

        Returns:
            Vec3: Result of subtraction.
        """
        if isinstance(other, Vec3):
            return Vec3(other.x - self.x, other.y - self.y, other.z - self.z)
        return Vec3(other - self.x, other - self.y, other - self.z)

    def __isub__(self, other: Vec3) -> Vec3:
        """In-place subtract two vectors.

        Args:
            other (Vec3): Vector to subtract.

        Returns:
            Vec3: Result of subtraction.
        """
        self.x -= other.x
        self.y -= other.y
        self.z -= other.z
        return self

    def __mul__(self, other: Vec3 | int | float) -> Vec3:
        """Multiply vector by another vector or scalar.

        Args:
            other (Vec3 | int | float): Value to multiply.

        Returns:
            Vec3: Result of multiplication.
        """
        if isinstance(other, Vec3):
            return Vec3(
                self.x * other.x,
                self.y * other.y,
                self.z * other.z,
            )
        return Vec3(
            self.x * other,
            self.y * other,
            self.z * other,
        )

    def __rmul__(self, other: Vec3 | int | float) -> Vec3:
        """Right-hand multiplication.

        Multiplies another vector or scalar by this vector, when this vector is on the right side of the `*` operator.

        Args:
            other (Vec3 | int | float): Value to multiply.

        Returns:
            Vec3: Result of multiplication.
        """
        if isinstance(other, Vec3):
            return Vec3(other.x * self.x, other.y * self.y, other.z * self.z)
        return Vec3(other * self.x, other * self.y, other * self.z)

    def __imul__(self, other: Vec3 | int | float) -> Vec3:
        """In-place multiply vector by another vector or scalar.

        Args:
            other (Vec3 | int | float): Value to multiply.

        Returns:
            Vec3: Result of multiplication.
        """
        if isinstance(other, Vec3):
            self.x *= other.x
            self.y *= other.y
            self.z *= other.z
        else:
            self.x *= other
            self.y *= other
            self.z *= other
        return self

    def __floordiv__(self, other: Vec3 | int | float) -> Vec3:
        """Floor divide vector by another vector or scalar.

        Args:
            other (Vec3 | int | float): Value to divide.

        Returns:
            Vec3: Result of floor division.
        """
        if isinstance(other, Vec3):
            if not other.x or not other.y or not other.z:
                return Vec3.ZERO
            return Vec3(
                self.x // other.x,
                self.y // other.y,
                self.z // other.z,
            )
        return Vec3(
            self.x // other,
            self.y // other,
            self.z // other,
        )

    def __rfloordiv__(self, other: Vec3 | int | float) -> Vec3:
        """Right-hand floor division.

        Floor divides another vector or scalar by this vector, when this vector is on the right side of the `//` operator.

        Args:
            other (Vec3 | int | float): Value to divide.

        Returns:
            Vec3: Result of floor division.
        """
        if isinstance(other, Vec3):
            if not self.x or not self.y or not self.z:
                return Vec3.ZERO
            return Vec3(other.x // self.x, other.y // self.y, other.z // self.z)
        return Vec3(other // self.x, other // self.y, other // self.z)

    def __ifloordiv__(self, other: Vec3 | int | float) -> Vec3:
        """In-place floor divide vector by another vector or scalar.

        Args:
            other (Vec3 | int | float): Value to divide.

        Returns:
            Vec3: Result of floor division.
        """
        if isinstance(other, Vec3):
            if not other.x or not other.y or not other.z:
                return Vec3.ZERO
            self.x //= other.x
            self.y //= other.y
            self.z //= other.z
        else:
            self.x //= other
            self.y //= other
            self.z //= other
        return self

    def __truediv__(self, other: Vec3 | int | float) -> Vec3:
        """Divide vector by another vector or scalar.

        Args:
            other (Vec3 | int | float): Value to divide.

        Returns:
            Vec3: Result of division.
        """
        if isinstance(other, Vec3):
            if not other.x or not other.y or not other.z:
                return Vec3.ZERO
            return Vec3(
                self.x / other.x,
                self.y / other.y,
                self.z / other.z,
            )
        return Vec3(
            self.x / other,
            self.y / other,
            self.z / other,
        )

    def __rtruediv__(self, other: Vec3 | int | float) -> Vec3:
        """Right-hand true division.

        Divides another vector or scalar by this vector, when this vector is on the right side of the `/` operator.

        Args:
            other (Vec3 | int | float): Value to divide.

        Returns:
            Vec3: Result of division.
        """
        if isinstance(other, Vec3):
            if not self.x or not self.y or not self.z:
                return Vec3.ZERO
            return Vec3(other.x / self.x, other.y / self.y, other.z / self.z)
        return Vec3(other / self.x, other / self.y, other / self.z)

    def __itruediv__(self, other: Vec3 | int | float) -> Vec3:
        """In-place divide vector by another vector or scalar.

        Args:
            other (Vec3 | int | float): Value to divide.

        Returns:
            Vec3: Result of division.
        """
        if isinstance(other, Vec3):
            if not other.x or not other.y or not other.z:
                return Vec3(0, 0, 0)
            self.x /= other.x
            self.y /= other.y
            self.z /= other.z
        else:
            self.x /= other
            self.y /= other
            self.z /= other
        return self

    def __mod__(self, other: Vec3 | int | float) -> Vec3:
        """Modulo vector by another vector or scalar.

        Args:
            other (Vec3 | int | float): Value to modulo.

        Returns:
            Vec3: Result of modulo.
        """
        if isinstance(other, Vec3):
            return Vec3(
                self.x % other.x,
                self.y % other.y,
                self.z % other.z,
            )
        return Vec3(
            self.x % other,
            self.y % other,
            self.z % other,
        )

    def __rmod__(self, other: Vec3 | int | float) -> Vec3:
        """Right-hand modulo.

        Computes the modulo of another vector or scalar by this vector, when this vector is on the right side of the `%` operator.

        Args:
            other (Vec3 | int | float): Value to modulo.

        Returns:
            Vec3: Result of modulo.
        """
        if isinstance(other, Vec3):
            return Vec3(other.x % self.x, other.y % self.y, other.z % self.z)
        return Vec3(other % self.x, other % self.y, other % self.z)

    def __imod__(self, other: Vec3 | int | float) -> Vec3:
        """In-place modulo vector by another vector or scalar.

        Args:
            other (Vec3 | int | float): Value to modulo.

        Returns:
            Vec3: Result of modulo.
        """
        if isinstance(other, Vec3):
            self.x %= other.x
            self.y %= other.y
            self.z %= other.z
        else:
            self.x %= other
            self.y %= other
            self.z %= other
        return self

    def __eq__(self, other: Vec3) -> bool:
        """Check if two vectors are equal.

        Args:
            other (Vec3): Vector to compare.

        Returns:
            bool: True if equal, False otherwise.
        """
        return (self.x == other.x) and (self.y == other.y) and (self.z == other.z)

    def __ne__(self, other: Vec3) -> bool:
        """Check if two vectors are not equal.

        Args:
            other (Vec3): Vector to compare.

        Returns:
            bool: True if not equal, False otherwise.
        """
        return (self.x != other.x) or (self.y != other.y) or (self.z != other.z)

    def __gt__(self, other: Vec3) -> bool:
        """Check if this vector is greater than another.

        Args:
            other (Vec3): Vector to compare.

        Returns:
            bool: True if greater, False otherwise.
        """
        return (self.x > other.x) and (self.y > other.y) and (self.z > other.z)

    def __lt__(self, other: Vec3) -> bool:
        """Check if this vector is less than another.

        Args:
            other (Vec3): Vector to compare.

        Returns:
            bool: True if less, False otherwise.
        """
        return (self.x < other.x) and (self.y < other.y) and (self.z < other.z)

    def __ge__(self, other: Vec3) -> bool:
        """Check if this vector is greater than or equal to another.

        Args:
            other (Vec3): Vector to compare.

        Returns:
            bool: True if greater or equal, False otherwise.
        """
        return (self.x >= other.x) and (self.y >= other.y) and (self.z >= other.z)

    def __le__(self, other: Vec3) -> bool:
        """Check if this vector is less than or equal to another.

        Args:
            other (Vec3): Vector to compare.

        Returns:
            bool: True if less or equal, False otherwise.
        """
        return (self.x <= other.x) and (self.y <= other.y) and (self.z <= other.z)

    def __copy__(self) -> Self:
        """Return a copy of the vector.

        Returns:
            Self: A new copy.
        """
        return self.__class__(self.x, self.y, self.z)

    def __deepcopy__(self, _memo: dict[int, Any]) -> Self:
        """Return a deep copy of the vector.

        Args:
            _memo (dict): Memoization dictionary.

        Returns:
            Self: A new deep copy.
        """
        return self.__class__(self.x, self.y, self.z)

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
        return sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def length_squared(self) -> float:
        """Return the length of the vector squared.

        Returns:
            float: Length squared.
        """
        return self.x * self.x + self.y * self.y + self.z * self.z

    def normalized(self) -> Vec3:
        """Return a vector with length of `1`, still with same direction.

        Returns:
            Vec3: Normalized vector.
        """
        length = self.length()
        if length == 0:
            return Vec3.ZERO
        return Vec3(
            self.x / length,
            self.y / length,
            self.z / length,
        )

    def lerp(self, target: Vec3, /, weight: float) -> Vec3:
        """Lerp towards vector `target` with `weight` ranging from `0` to `1`.

        Args:
            target (Vec3): Target to lerp towards.
            weight (float): Percentage to lerp.

        Returns:
            Vec3: Vector after performing interpolation.
        """
        return Vec3(
            lerp(self.x, target.x, weight),
            lerp(self.y, target.y, weight),
            lerp(self.z, target.z, weight),
        )

    def sign(self) -> Vec3:
        """Return a Vec3 with each component being the sign of the vector.

        Returns:
            Vec3: Vector with signed components.
        """
        return Vec3(
            sign(self.x),
            sign(self.y),
            sign(self.z),
        )

    def clamp(self, smallest: Vec3, largest: Vec3, /) -> Vec3:
        """Return a new clamped vector.

        Args:
            smallest (Vec3): Lower bound for `x`, `y`, and `z`.
            largest (Vec3): Upper bound for `x`, `y`, and `z`.

        Returns:
            Vec3: Vector clamped.
        """
        return Vec3(
            clamp(self.x, smallest.x, largest.x),
            clamp(self.y, smallest.y, largest.y),
            clamp(self.z, smallest.z, largest.z),
        )

    def move_toward(self, stop: Vec3, /, change: int | float) -> Vec3:
        """Move toward a vector, from a vector, with given change.

        Args:
            stop (Vec3): Target vector.
            change (int | float): Max distance to move.

        Returns:
            Vec3: New vector moved.
        """
        return Vec3(
            move_toward(self.x, stop.x, change),
            move_toward(self.y, stop.y, change),
            move_toward(self.z, stop.z, change),
        )

    def distance_to(self, target: Vec3, /) -> float:
        """Return the relative distance to the target point.

        Args:
            target (Vec3): Target point.

        Returns:
            float: Distance.
        """
        return (target - self).length()

    def distance_squared_to(self, target: Vec3, /) -> float:
        """Return the relative distance to the target point, squared.

        Args:
            target (Vec3): Target point.

        Returns:
            float: Distance squared.
        """
        return (target - self).length_squared()

    def direction_to(self, target: Vec3, /) -> Vec3:
        """Return the direction to the target point.

        Args:
            target (Vec3): Target point.

        Returns:
            Vec3: Direction.
        """
        return (target - self).normalized()

    def dot(self, other: Vec3, /) -> float:
        """Return the dot product between two 3D vectors.

        Args:
            other (Vec3): Other vector.

        Returns:
            float: Dot product.
        """
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other: Vec3, /) -> Vec3:
        """Return the cross product between two 3D vectors.

        Args:
            other (Vec3): Other vector.

        Returns:
            Vec3: Cross product.
        """
        x = self.y * other.z - self.z * other.y
        y = self.z * other.x - self.x * other.z
        z = self.x * other.y - self.y * other.x
        return Vec3(x, y, z)

    def angles(self) -> Vec3:
        """Return the angles (pitch, yaw, roll) of the vector.

        Returns:
            Vec3: Angles in radians.
        """
        xy_length = sqrt(self.x * self.x + self.y * self.y)
        pitch = atan2(self.z, xy_length)
        yaw = atan2(self.y, self.x)
        return Vec3(pitch, yaw, 0)

    def angles_to(self, target: Vec3, /) -> Vec3:
        """Return the angles to the target point.

        Args:
            target (Vec3): Target point.

        Returns:
            Vec3: Angles in radians.
        """
        return (target - self).angles()

    def rotated_around_x(self, angle: float, /) -> Vec3:
        """Return a vector rotated around the `X` axis by `angle` radians.

        Args:
            angle (float): Radians to rotate with.

        Returns:
            Vec3: Rotated vector.
        """
        new_y = self.y * cos(angle) - self.z * sin(angle)
        new_z = self.y * sin(angle) + self.z * cos(angle)
        return Vec3(self.x, new_y, new_z)

    def rotated_around_y(self, angle: float, /) -> Vec3:
        """Return a vector rotated around the `Y` axis by `angle` radians.

        Args:
            angle (float): Radians to rotate with.

        Returns:
            Vec3: Rotated vector.
        """
        new_x = self.x * cos(angle) + self.z * sin(angle)
        new_z = -self.x * sin(angle) + self.z * cos(angle)
        return Vec3(new_x, self.y, new_z)

    def rotated_around_z(self, angle: float, /) -> Vec3:
        """Return a vector rotated around the `Z` axis by `angle` radians.

        Args:
            angle (float): Radians to rotate with.

        Returns:
            Vec3: Rotated vector.
        """
        new_x = self.x * cos(angle) - self.y * sin(angle)
        new_y = self.x * sin(angle) + self.y * cos(angle)
        return Vec3(new_x, new_y, self.z)

    def rotated(self, angles: Vec3, /) -> Vec3:
        """Return a vector rotated by the given angles around each axis.

        Args:
            angles (Vec3): Angles to rotate around each axis.

        Returns:
            Vec3: Rotated vector.
        """
        return (
            self.rotated_around_x(angles.x)
            .rotated_around_y(angles.y)
            .rotated_around_z(angles.z)
        )

    def rotated_around(self, target: Vec3, /, angles: Vec3) -> Vec3:
        """Return a vector rotated by the given angles around each axis, around a target point.

        Args:
            target (Vec3): Point to rotate around.
            angles (Vec3): Angles to rotate around each axis.

        Returns:
            Vec3: Rotated vector around the target point.
        """
        rel = self - target
        rotated_rel = (
            rel.rotated_around_x(angles.x)
            .rotated_around_y(angles.y)
            .rotated_around_z(angles.z)
        )
        return rotated_rel + target
