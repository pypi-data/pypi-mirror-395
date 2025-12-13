from __future__ import annotations as _annotations

import sys as _sys
from typing import TypeAlias as _TypeAlias, TypeVar as _TypeVar

if _sys.version_info >= (3, 11):
    from typing import Self as Self
else:
    from typing_extensions import Self as Self

Radians: _TypeAlias = float
Number = _TypeVar("Number", int, float)
