"""
Linflex
=======

A linear algebra package written in Python

Includes
--------

- Functions:
  - `lerp`
  - `sign`
  - `clamp`
  - `move_toward`
- Classes:
  - `Vec2`
  - `Vec2i`
  - `Vec3`
- Modules
  - `typing`
"""

__all__ = (
    # Functions
    "lerp",
    "sign",
    "clamp",
    "move_toward",
    # Classes
    "Vec2",
    "Vec2i",
    "Vec3",
    # Modules
    "typing",
)

from . import typing
from ._numerical_tools import lerp, sign, clamp, move_toward
from ._vec2 import Vec2
from ._vec2i import Vec2i
from ._vec3 import Vec3
