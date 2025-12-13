from __future__ import annotations

from typing import Literal

from .typing import Number


def lerp(
    start: int | float,
    stop: int | float,
    weight: float,
    /,
) -> float:
    """Lerp between `start` and `stop` with `weight` ranging from `0` to `1`.

    Args:
        start (int | float): Starting number.
        stop (int | float): Target number.
        weight (float): Percentage to lerp.

    Returns:
        float: Result of the interpolation.
    """
    return (1.0 - weight) * start + (weight * stop)


def sign(number: int | float, /) -> Literal[-1, 0, 1]:
    """Return the sign of the number.

    The number `0` will return `0`.

    Args:
        number (int | float): Number to get the sign of.

    Returns:
        Literal[-1, 0, 1]: Sign.
    """
    if number > 0:
        return 1
    if number < 0:
        return -1
    return 0


def clamp(
    number: Number,
    smallest: Number,
    largest: Number,
    /,
) -> Number:
    """Return the number clamped between `smallest` and `largest` (inclusive).

    Args:
        number (Number): Number to clamp.
        smallest (Number): Lower bound.
        largest (Number): Upper bound.

    Returns:
        Number: Clamped number.
    """
    return max(smallest, min(largest, number))


def move_toward(
    start: Number,
    stop: Number,
    /,
    change: Number,
) -> Number:
    """Move toward target number.

    Args:
        start (Number): Starting number.
        stop (Number): Target number.
        change (Number): Step length when moving toward `stop`.

    Returns:
        float: Point after move.
    """
    if abs(stop - start) <= change:
        return stop
    elif start < stop:
        return start + change
    else:
        return start - change
