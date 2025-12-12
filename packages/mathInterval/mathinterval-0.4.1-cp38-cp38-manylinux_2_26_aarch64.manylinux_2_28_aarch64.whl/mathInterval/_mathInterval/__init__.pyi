"""

mathInterval
============

C++ interval arithmetic exposed to Python.

This module provides classes and algorithms for working
with mathematical multitudes. It supports:

- Construction of multitudes with finite or infinite bounds.
- Smart search algorithms using user-provided lambdas.
- Conversion and custom transfer of interval data.
- Executing multiple operators between multitudes.

All classes and functions are documented with Python-style docstrings.
"""
from __future__ import annotations
import collections.abc
import typing
from . import policy
__all__: list[str] = ['Interval', 'policy']
class _Interval_FloatTypePolicy:
    maximal: typing.ClassVar[__Interval_FloatTypePolicy_maximal]  # value = <maximal>
    minimal: typing.ClassVar[__Interval_FloatTypePolicy_minimal]  # value = <minimal>
    @typing.overload
    def __add__(self, b: _Interval_FloatTypePolicy) -> _Interval_FloatTypePolicy:
        """
        returns a new multitude containing the union of the elements of the previous multitudes
        """
    @typing.overload
    def __add__(self, b: typing.SupportsFloat) -> _Interval_FloatTypePolicy:
        """
        returns a new multitude with the points shifted forward by the distance val
        """
    def __and__(self, b: _Interval_FloatTypePolicy) -> _Interval_FloatTypePolicy:
        """
        returns a new multitude containing the intersection of the elements of the previous multitudes
        """
    @typing.overload
    def __contains__(self, a: _Interval_FloatTypePolicy) -> bool:
        """
        return true if this multitude is subset of another multitude, else return false
        """
    @typing.overload
    def __contains__(self, a: _mathInterval.__Interval_FloatTypePolicy_minimal | _mathInterval.__Interval_FloatTypePolicy_maximal | typing.SupportsFloat | tuple[typing.SupportsInt, typing.SupportsFloat]) -> bool:
        """
        return true if this point in multitude, else return false
        """
    @typing.overload
    def __iadd__(self, b: _Interval_FloatTypePolicy) -> _Interval_FloatTypePolicy:
        """
        adds elements of another multitude
        """
    @typing.overload
    def __iadd__(self, b: typing.SupportsFloat) -> _Interval_FloatTypePolicy:
        """
        shift the points forward by a distance of val
        """
    def __iand__(self, b: _Interval_FloatTypePolicy) -> _Interval_FloatTypePolicy:
        """
        intersect elements with another multitude
        """
    @typing.overload
    def __imul__(self, b: _Interval_FloatTypePolicy) -> _Interval_FloatTypePolicy:
        """
        intersect elements with another multitude
        """
    @typing.overload
    def __imul__(self, b: typing.SupportsFloat) -> _Interval_FloatTypePolicy:
        """
        multiplies the points of a multitude by a factor of val
        """
    def __init__(self) -> None:
        ...
    def __ior__(self, b: _Interval_FloatTypePolicy) -> _Interval_FloatTypePolicy:
        """
        adds elements of another multitude
        """
    @typing.overload
    def __isub__(self, b: _Interval_FloatTypePolicy) -> _Interval_FloatTypePolicy:
        """
        remove elements of another multitude
        """
    @typing.overload
    def __isub__(self, b: typing.SupportsFloat) -> _Interval_FloatTypePolicy:
        """
        shift the points backward by a distance of val
        """
    def __itruediv__(self, b: typing.SupportsFloat) -> _Interval_FloatTypePolicy:
        """
        divides the points of a multitude by a factor of val
        """
    def __ixor__(self, b: _Interval_FloatTypePolicy) -> _Interval_FloatTypePolicy:
        """
         generating symmetric difference with elements of another multitude
        """
    @typing.overload
    def __mul__(self, b: _Interval_FloatTypePolicy) -> _Interval_FloatTypePolicy:
        """
        returns a new multitude containing the intersection of the elements of the previous multitudes
        """
    @typing.overload
    def __mul__(self, b: typing.SupportsFloat) -> _Interval_FloatTypePolicy:
        """
        returns a new multitude with the points multiplied by a factor of val
        """
    def __or__(self, b: _Interval_FloatTypePolicy) -> _Interval_FloatTypePolicy:
        """
        returns a new multitude containing the union of the elements of the previous multitudes
        """
    def __str__(self) -> str:
        """
        return string with all data in mathematical style
        """
    @typing.overload
    def __sub__(self, b: _Interval_FloatTypePolicy) -> _Interval_FloatTypePolicy:
        """
        returns a new multitude containing the difference of the elements of the previous multitudes
        """
    @typing.overload
    def __sub__(self, b: typing.SupportsFloat) -> _Interval_FloatTypePolicy:
        """
        returns a new multitude with the points shifted backward by the distance val
        """
    def __truediv__(self, b: typing.SupportsFloat) -> _Interval_FloatTypePolicy:
        """
        returns a new multitude with the points divided by a factor of val
        """
    def __xor__(self, b: _Interval_FloatTypePolicy) -> _Interval_FloatTypePolicy:
        """
        returns a new multitude containing the symmetric difference of the elements of the previous multitudes
        """
    def add_interval(self, a: _mathInterval.__Interval_FloatTypePolicy_minimal | _mathInterval.__Interval_FloatTypePolicy_maximal | typing.SupportsFloat | tuple[typing.SupportsInt, typing.SupportsFloat], b: _mathInterval.__Interval_FloatTypePolicy_minimal | _mathInterval.__Interval_FloatTypePolicy_maximal | typing.SupportsFloat | tuple[typing.SupportsInt, typing.SupportsFloat]) -> bool:
        """
        returns false if all this interval was inside this multitude, else return true
        """
    def add_point(self, a: _mathInterval.__Interval_FloatTypePolicy_minimal | _mathInterval.__Interval_FloatTypePolicy_maximal | typing.SupportsFloat | tuple[typing.SupportsInt, typing.SupportsFloat]) -> bool:
        """
        returns false if this point was inside this multitude, else return true. Note that the added point cannot be -INF and +INF
        """
    @typing.overload
    def any(self) -> float | None:
        """
        ### any
        
        Return any element that is in data.
        
        The function can return `None`, because the returning value does not always exist.
        
        ---
        
        - If there is any point, it will be returned.
        - If there is an interval `(-INF; +INF)`, the function will return `None`.
        - If activated `policy.IntTypePolicy` or `policy.FloatTypePolicy`,
          a smart algorithm will try to find any number in the intervals.
        - If it is standard `Interval`, or if the algorithm does not find any element in data,
          the function will return `None`.
        
        ---
        
        For custom types and algorithms, consider using this function with additional arguments.
        """
    @typing.overload
    def any(self, MINUS_INF_x: collections.abc.Callable[[typing.SupportsFloat], float | None], x_PLUS_INF: collections.abc.Callable[[typing.SupportsFloat], float | None], x_y: collections.abc.Callable[[typing.SupportsFloat, typing.SupportsFloat], float | None], MINUS_INF_PLUS_INF: typing.SupportsFloat) -> float | None:
        """
        ### any()
        
        Return any element that is in data.
        
        The function can return `None`, because the returning value does not always exist.
        
        This function takes **three lambda functions** and **one value**:
        
        ---
        
        - **First lambda** – called if there is an interval `(-INF; x)`,
          receives one argument (x).
        - **Second lambda** – called if there is an interval `(x; +INF)`,
          receives one argument (x).
        - **Third lambda** – called if there is an interval `(x; y)`,
          receives two arguments (x, y).
        - **Value** - result for interval `(-INF, +INF)`
        
        ---
        
        A lambdas may return `None`, if the interval has no matching value.
        """
    @typing.overload
    def apply_policy(self, policy: policy.EmptyPrintPolicy) -> None:
        """
        allow to change any not-type policy
        """
    @typing.overload
    def apply_policy(self, policy: policy.MinMaxPrintPolicy) -> None:
        """
        allow to change any not-type policy
        """
    def clear(self) -> None:
        """
        clear multitude data
        """
    def contains(self, a: _mathInterval.__Interval_FloatTypePolicy_minimal | _mathInterval.__Interval_FloatTypePolicy_maximal | typing.SupportsFloat | tuple[typing.SupportsInt, typing.SupportsFloat], b: _mathInterval.__Interval_FloatTypePolicy_minimal | _mathInterval.__Interval_FloatTypePolicy_maximal | typing.SupportsFloat | tuple[typing.SupportsInt, typing.SupportsFloat]) -> bool:
        """
        return true if interval (a, b) in multitude, else return false
        """
    @typing.overload
    def custom_transfer(self, fun: collections.abc.Callable[[typing.SupportsFloat], float]) -> _Interval_FloatTypePolicy:
        """
        ### custom_transfer()
        
        Transfer all elements that are in this multitude and return a new multitude.
        
        The function takes **one lambda function**.
        `-INF` and `+INF` remain unchanged.
        
        ---
        
        - **Lambda** – returns a new value of a point/border of an interval,
          receives one argument - old value of a point/border of an interval.
        
        ---
        
        If the first value of an interval becomes greater than the second,
        the function will swap them automatically.
        """
    @typing.overload
    def custom_transfer(self, fun: collections.abc.Callable[[typing.SupportsFloat], float], MINUS_INF: typing.SupportsFloat, PLUS_INF: typing.SupportsFloat) -> _Interval_FloatTypePolicy:
        """
        ### custom_transfer()
        
        Transfer all elements that are in this multitude and return a new multitude.
        
        The function takes **one lambda function**
        and **two values** – the converted values of `-INF` and `+INF`.
        New values cannot themselves be `-INF` or `+INF`.
        
        ---
        
        - **Lambda** – returns a new value of a point/border of an interval,
          receives one argument - old value of a point/border of an interval.
        - **First value** – new value of the border of the interval, that begins from `-INF` - old value of a border of an interval.
        - **Second value** – new value of the border of the interval, that ends with `+INF` - old value of a border of an interval.
        
        ---
        
        If the first value of an interval becomes greater than the second,
        the function will swap them automatically.
        """
    def empty(self) -> bool:
        """
        return true if this multitude is empty, else return false
        """
    def inverse(self) -> _Interval_FloatTypePolicy:
        """
        returns the multitude that is the inverse of the given one
        """
    def isdisjoint(self, b: _Interval_FloatTypePolicy) -> bool:
        """
        return true if these multitudes has no common points, else return false
        """
    def issubset(self, b: _Interval_FloatTypePolicy) -> bool:
        """
        return true if this multitude is subset of another multitude, else return false
        """
    def issuperset(self, b: _Interval_FloatTypePolicy) -> bool:
        """
        return true if this multitude is subset of another multitude, else return false
        """
    def points_only(self) -> bool:
        """
        return true if multitude has only separate points (or empty), else return false
        """
    def remove_interval(self, a: _mathInterval.__Interval_FloatTypePolicy_minimal | _mathInterval.__Interval_FloatTypePolicy_maximal | typing.SupportsFloat | tuple[typing.SupportsInt, typing.SupportsFloat], b: _mathInterval.__Interval_FloatTypePolicy_minimal | _mathInterval.__Interval_FloatTypePolicy_maximal | typing.SupportsFloat | tuple[typing.SupportsInt, typing.SupportsFloat]) -> bool:
        """
        returns false if all this interval was not inside this multitude, else return true
        """
    def remove_point(self, a: _mathInterval.__Interval_FloatTypePolicy_minimal | _mathInterval.__Interval_FloatTypePolicy_maximal | typing.SupportsFloat | tuple[typing.SupportsInt, typing.SupportsFloat]) -> bool:
        """
        returns false if this point was not inside this multitude, else return true. Note that the removed point cannot be -INF and +INF
        """
class _Interval_IntTypePolicy:
    maximal: typing.ClassVar[__Interval_IntTypePolicy_maximal]  # value = <maximal>
    minimal: typing.ClassVar[__Interval_IntTypePolicy_minimal]  # value = <minimal>
    @typing.overload
    def __add__(self, b: _Interval_IntTypePolicy) -> _Interval_IntTypePolicy:
        """
        returns a new multitude containing the union of the elements of the previous multitudes
        """
    @typing.overload
    def __add__(self, b: typing.SupportsInt) -> _Interval_IntTypePolicy:
        """
        returns a new multitude with the points shifted forward by the distance val
        """
    def __and__(self, b: _Interval_IntTypePolicy) -> _Interval_IntTypePolicy:
        """
        returns a new multitude containing the intersection of the elements of the previous multitudes
        """
    @typing.overload
    def __contains__(self, a: _Interval_IntTypePolicy) -> bool:
        """
        return true if this multitude is subset of another multitude, else return false
        """
    @typing.overload
    def __contains__(self, a: _mathInterval.__Interval_IntTypePolicy_minimal | _mathInterval.__Interval_IntTypePolicy_maximal | typing.SupportsInt | tuple[typing.SupportsInt, typing.SupportsInt]) -> bool:
        """
        return true if this point in multitude, else return false
        """
    def __floordiv__(self, b: typing.SupportsInt) -> _Interval_IntTypePolicy:
        """
        returns a new multitude with the points divided by a factor of val
        """
    @typing.overload
    def __iadd__(self, b: _Interval_IntTypePolicy) -> _Interval_IntTypePolicy:
        """
        adds elements of another multitude
        """
    @typing.overload
    def __iadd__(self, b: typing.SupportsInt) -> _Interval_IntTypePolicy:
        """
        shift the points forward by a distance of val
        """
    def __iand__(self, b: _Interval_IntTypePolicy) -> _Interval_IntTypePolicy:
        """
        intersect elements with another multitude
        """
    def __ifloordiv__(self, b: typing.SupportsInt) -> _Interval_IntTypePolicy:
        """
        divides the points of a multitude by a factor of val
        """
    def __imod__(self, b: typing.SupportsInt) -> _Interval_IntTypePolicy:
        """
        replaces the points with the remainder of the division by val
        """
    @typing.overload
    def __imul__(self, b: _Interval_IntTypePolicy) -> _Interval_IntTypePolicy:
        """
        intersect elements with another multitude
        """
    @typing.overload
    def __imul__(self, b: typing.SupportsInt) -> _Interval_IntTypePolicy:
        """
        multiplies the points of a multitude by a factor of val
        """
    def __init__(self) -> None:
        ...
    def __ior__(self, b: _Interval_IntTypePolicy) -> _Interval_IntTypePolicy:
        """
        adds elements of another multitude
        """
    @typing.overload
    def __isub__(self, b: _Interval_IntTypePolicy) -> _Interval_IntTypePolicy:
        """
        remove elements of another multitude
        """
    @typing.overload
    def __isub__(self, b: typing.SupportsInt) -> _Interval_IntTypePolicy:
        """
        shift the points backward by a distance of val
        """
    def __ixor__(self, b: _Interval_IntTypePolicy) -> _Interval_IntTypePolicy:
        """
         generating symmetric difference with elements of another multitude
        """
    def __mod__(self, b: typing.SupportsInt) -> _Interval_IntTypePolicy:
        """
        returns a new multitude with points taken as the remainder of the division by val
        """
    @typing.overload
    def __mul__(self, b: _Interval_IntTypePolicy) -> _Interval_IntTypePolicy:
        """
        returns a new multitude containing the intersection of the elements of the previous multitudes
        """
    @typing.overload
    def __mul__(self, b: typing.SupportsInt) -> _Interval_IntTypePolicy:
        """
        returns a new multitude with the points multiplied by a factor of val
        """
    def __or__(self, b: _Interval_IntTypePolicy) -> _Interval_IntTypePolicy:
        """
        returns a new multitude containing the union of the elements of the previous multitudes
        """
    def __str__(self) -> str:
        """
        return string with all data in mathematical style
        """
    @typing.overload
    def __sub__(self, b: _Interval_IntTypePolicy) -> _Interval_IntTypePolicy:
        """
        returns a new multitude containing the difference of the elements of the previous multitudes
        """
    @typing.overload
    def __sub__(self, b: typing.SupportsInt) -> _Interval_IntTypePolicy:
        """
        returns a new multitude with the points shifted backward by the distance val
        """
    def __xor__(self, b: _Interval_IntTypePolicy) -> _Interval_IntTypePolicy:
        """
        returns a new multitude containing the symmetric difference of the elements of the previous multitudes
        """
    def add_interval(self, a: _mathInterval.__Interval_IntTypePolicy_minimal | _mathInterval.__Interval_IntTypePolicy_maximal | typing.SupportsInt | tuple[typing.SupportsInt, typing.SupportsInt], b: _mathInterval.__Interval_IntTypePolicy_minimal | _mathInterval.__Interval_IntTypePolicy_maximal | typing.SupportsInt | tuple[typing.SupportsInt, typing.SupportsInt]) -> bool:
        """
        returns false if all this interval was inside this multitude, else return true
        """
    def add_point(self, a: _mathInterval.__Interval_IntTypePolicy_minimal | _mathInterval.__Interval_IntTypePolicy_maximal | typing.SupportsInt | tuple[typing.SupportsInt, typing.SupportsInt]) -> bool:
        """
        returns false if this point was inside this multitude, else return true. Note that the added point cannot be -INF and +INF
        """
    @typing.overload
    def any(self) -> int | None:
        """
        ### any
        
        Return any element that is in data.
        
        The function can return `None`, because the returning value does not always exist.
        
        ---
        
        - If there is any point, it will be returned.
        - If there is an interval `(-INF; +INF)`, the function will return `None`.
        - If activated `policy.IntTypePolicy` or `policy.FloatTypePolicy`,
          a smart algorithm will try to find any number in the intervals.
        - If it is standard `Interval`, or if the algorithm does not find any element in data,
          the function will return `None`.
        
        ---
        
        For custom types and algorithms, consider using this function with additional arguments.
        """
    @typing.overload
    def any(self, MINUS_INF_x: collections.abc.Callable[[typing.SupportsInt], int | None], x_PLUS_INF: collections.abc.Callable[[typing.SupportsInt], int | None], x_y: collections.abc.Callable[[typing.SupportsInt, typing.SupportsInt], int | None], MINUS_INF_PLUS_INF: typing.SupportsInt) -> int | None:
        """
        ### any()
        
        Return any element that is in data.
        
        The function can return `None`, because the returning value does not always exist.
        
        This function takes **three lambda functions** and **one value**:
        
        ---
        
        - **First lambda** – called if there is an interval `(-INF; x)`,
          receives one argument (x).
        - **Second lambda** – called if there is an interval `(x; +INF)`,
          receives one argument (x).
        - **Third lambda** – called if there is an interval `(x; y)`,
          receives two arguments (x, y).
        - **Value** - result for interval `(-INF, +INF)`
        
        ---
        
        A lambdas may return `None`, if the interval has no matching value.
        """
    @typing.overload
    def apply_policy(self, policy: policy.EmptyPrintPolicy) -> None:
        """
        allow to change any not-type policy
        """
    @typing.overload
    def apply_policy(self, policy: policy.MinMaxPrintPolicy) -> None:
        """
        allow to change any not-type policy
        """
    def clear(self) -> None:
        """
        clear multitude data
        """
    def contains(self, a: _mathInterval.__Interval_IntTypePolicy_minimal | _mathInterval.__Interval_IntTypePolicy_maximal | typing.SupportsInt | tuple[typing.SupportsInt, typing.SupportsInt], b: _mathInterval.__Interval_IntTypePolicy_minimal | _mathInterval.__Interval_IntTypePolicy_maximal | typing.SupportsInt | tuple[typing.SupportsInt, typing.SupportsInt]) -> bool:
        """
        return true if interval (a, b) in multitude, else return false
        """
    @typing.overload
    def custom_transfer(self, fun: collections.abc.Callable[[typing.SupportsInt], int]) -> _Interval_IntTypePolicy:
        """
        ### custom_transfer()
        
        Transfer all elements that are in this multitude and return a new multitude.
        
        The function takes **one lambda function**.
        `-INF` and `+INF` remain unchanged.
        
        ---
        
        - **Lambda** – returns a new value of a point/border of an interval,
          receives one argument - old value of a point/border of an interval.
        
        ---
        
        If the first value of an interval becomes greater than the second,
        the function will swap them automatically.
        """
    @typing.overload
    def custom_transfer(self, fun: collections.abc.Callable[[typing.SupportsInt], int], MINUS_INF: typing.SupportsInt, PLUS_INF: typing.SupportsInt) -> _Interval_IntTypePolicy:
        """
        ### custom_transfer()
        
        Transfer all elements that are in this multitude and return a new multitude.
        
        The function takes **one lambda function**
        and **two values** – the converted values of `-INF` and `+INF`.
        New values cannot themselves be `-INF` or `+INF`.
        
        ---
        
        - **Lambda** – returns a new value of a point/border of an interval,
          receives one argument - old value of a point/border of an interval.
        - **First value** – new value of the border of the interval, that begins from `-INF` - old value of a border of an interval.
        - **Second value** – new value of the border of the interval, that ends with `+INF` - old value of a border of an interval.
        
        ---
        
        If the first value of an interval becomes greater than the second,
        the function will swap them automatically.
        """
    def empty(self) -> bool:
        """
        return true if this multitude is empty, else return false
        """
    def inverse(self) -> _Interval_IntTypePolicy:
        """
        returns the multitude that is the inverse of the given one
        """
    def isdisjoint(self, b: _Interval_IntTypePolicy) -> bool:
        """
        return true if these multitudes has no common points, else return false
        """
    def issubset(self, b: _Interval_IntTypePolicy) -> bool:
        """
        return true if this multitude is subset of another multitude, else return false
        """
    def issuperset(self, b: _Interval_IntTypePolicy) -> bool:
        """
        return true if this multitude is subset of another multitude, else return false
        """
    def points_only(self) -> bool:
        """
        return true if multitude has only separate points (or empty), else return false
        """
    def remove_interval(self, a: _mathInterval.__Interval_IntTypePolicy_minimal | _mathInterval.__Interval_IntTypePolicy_maximal | typing.SupportsInt | tuple[typing.SupportsInt, typing.SupportsInt], b: _mathInterval.__Interval_IntTypePolicy_minimal | _mathInterval.__Interval_IntTypePolicy_maximal | typing.SupportsInt | tuple[typing.SupportsInt, typing.SupportsInt]) -> bool:
        """
        returns false if all this interval was not inside this multitude, else return true
        """
    def remove_point(self, a: _mathInterval.__Interval_IntTypePolicy_minimal | _mathInterval.__Interval_IntTypePolicy_maximal | typing.SupportsInt | tuple[typing.SupportsInt, typing.SupportsInt]) -> bool:
        """
        returns false if this point was not inside this multitude, else return true. Note that the removed point cannot be -INF and +INF
        """
class _Interval_UnknownTypePolicy:
    maximal: typing.ClassVar[__Interval_UnknownTypePolicy_maximal]  # value = <maximal>
    minimal: typing.ClassVar[__Interval_UnknownTypePolicy_minimal]  # value = <minimal>
    def __add__(self, b: _Interval_UnknownTypePolicy) -> _Interval_UnknownTypePolicy:
        """
        returns a new multitude containing the union of the elements of the previous multitudes
        """
    def __and__(self, b: _Interval_UnknownTypePolicy) -> _Interval_UnknownTypePolicy:
        """
        returns a new multitude containing the intersection of the elements of the previous multitudes
        """
    @typing.overload
    def __contains__(self, a: _Interval_UnknownTypePolicy) -> bool:
        """
        return true if this multitude is subset of another multitude, else return false
        """
    @typing.overload
    def __contains__(self, a: _mathInterval.__Interval_UnknownTypePolicy_minimal | _mathInterval.__Interval_UnknownTypePolicy_maximal | typing.Any | tuple[typing.SupportsInt, typing.Any]) -> bool:
        """
        return true if this point in multitude, else return false
        """
    def __iadd__(self, b: _Interval_UnknownTypePolicy) -> _Interval_UnknownTypePolicy:
        """
        adds elements of another multitude
        """
    def __iand__(self, b: _Interval_UnknownTypePolicy) -> _Interval_UnknownTypePolicy:
        """
        intersect elements with another multitude
        """
    def __imul__(self, b: _Interval_UnknownTypePolicy) -> _Interval_UnknownTypePolicy:
        """
        intersect elements with another multitude
        """
    def __init__(self) -> None:
        ...
    def __ior__(self, b: _Interval_UnknownTypePolicy) -> _Interval_UnknownTypePolicy:
        """
        adds elements of another multitude
        """
    def __isub__(self, b: _Interval_UnknownTypePolicy) -> _Interval_UnknownTypePolicy:
        """
        remove elements of another multitude
        """
    def __ixor__(self, b: _Interval_UnknownTypePolicy) -> _Interval_UnknownTypePolicy:
        """
         generating symmetric difference with elements of another multitude
        """
    def __mul__(self, b: _Interval_UnknownTypePolicy) -> _Interval_UnknownTypePolicy:
        """
        returns a new multitude containing the intersection of the elements of the previous multitudes
        """
    def __or__(self, b: _Interval_UnknownTypePolicy) -> _Interval_UnknownTypePolicy:
        """
        returns a new multitude containing the union of the elements of the previous multitudes
        """
    def __str__(self) -> str:
        """
        return string with all data in mathematical style
        """
    def __sub__(self, b: _Interval_UnknownTypePolicy) -> _Interval_UnknownTypePolicy:
        """
        returns a new multitude containing the difference of the elements of the previous multitudes
        """
    def __xor__(self, b: _Interval_UnknownTypePolicy) -> _Interval_UnknownTypePolicy:
        """
        returns a new multitude containing the symmetric difference of the elements of the previous multitudes
        """
    def add_interval(self, a: _mathInterval.__Interval_UnknownTypePolicy_minimal | _mathInterval.__Interval_UnknownTypePolicy_maximal | typing.Any | tuple[typing.SupportsInt, typing.Any], b: _mathInterval.__Interval_UnknownTypePolicy_minimal | _mathInterval.__Interval_UnknownTypePolicy_maximal | typing.Any | tuple[typing.SupportsInt, typing.Any]) -> bool:
        """
        returns false if all this interval was inside this multitude, else return true
        """
    def add_point(self, a: _mathInterval.__Interval_UnknownTypePolicy_minimal | _mathInterval.__Interval_UnknownTypePolicy_maximal | typing.Any | tuple[typing.SupportsInt, typing.Any]) -> bool:
        """
        returns false if this point was inside this multitude, else return true. Note that the added point cannot be -INF and +INF
        """
    @typing.overload
    def any(self) -> typing.Any | None:
        """
        ### any
        
        Return any element that is in data.
        
        The function can return `None`, because the returning value does not always exist.
        
        ---
        
        - If there is any point, it will be returned.
        - If there is an interval `(-INF; +INF)`, the function will return `None`.
        - If activated `policy.IntTypePolicy` or `policy.FloatTypePolicy`,
          a smart algorithm will try to find any number in the intervals.
        - If it is standard `Interval`, or if the algorithm does not find any element in data,
          the function will return `None`.
        
        ---
        
        For custom types and algorithms, consider using this function with additional arguments.
        """
    @typing.overload
    def any(self, MINUS_INF_x: collections.abc.Callable[[typing.Any], typing.Any | None], x_PLUS_INF: collections.abc.Callable[[typing.Any], typing.Any | None], x_y: collections.abc.Callable[[typing.Any, typing.Any], typing.Any | None], MINUS_INF_PLUS_INF: typing.Any) -> typing.Any | None:
        """
        ### any()
        
        Return any element that is in data.
        
        The function can return `None`, because the returning value does not always exist.
        
        This function takes **three lambda functions** and **one value**:
        
        ---
        
        - **First lambda** – called if there is an interval `(-INF; x)`,
          receives one argument (x).
        - **Second lambda** – called if there is an interval `(x; +INF)`,
          receives one argument (x).
        - **Third lambda** – called if there is an interval `(x; y)`,
          receives two arguments (x, y).
        - **Value** - result for interval `(-INF, +INF)`
        
        ---
        
        A lambdas may return `None`, if the interval has no matching value.
        """
    @typing.overload
    def apply_policy(self, policy: policy.EmptyPrintPolicy) -> None:
        """
        allow to change any not-type policy
        """
    @typing.overload
    def apply_policy(self, policy: policy.MinMaxPrintPolicy) -> None:
        """
        allow to change any not-type policy
        """
    def clear(self) -> None:
        """
        clear multitude data
        """
    def contains(self, a: _mathInterval.__Interval_UnknownTypePolicy_minimal | _mathInterval.__Interval_UnknownTypePolicy_maximal | typing.Any | tuple[typing.SupportsInt, typing.Any], b: _mathInterval.__Interval_UnknownTypePolicy_minimal | _mathInterval.__Interval_UnknownTypePolicy_maximal | typing.Any | tuple[typing.SupportsInt, typing.Any]) -> bool:
        """
        return true if interval (a, b) in multitude, else return false
        """
    @typing.overload
    def custom_transfer(self, fun: collections.abc.Callable[[typing.Any], typing.Any]) -> _Interval_UnknownTypePolicy:
        """
        ### custom_transfer()
        
        Transfer all elements that are in this multitude and return a new multitude.
        
        The function takes **one lambda function**.
        `-INF` and `+INF` remain unchanged.
        
        ---
        
        - **Lambda** – returns a new value of a point/border of an interval,
          receives one argument - old value of a point/border of an interval.
        
        ---
        
        If the first value of an interval becomes greater than the second,
        the function will swap them automatically.
        """
    @typing.overload
    def custom_transfer(self, fun: collections.abc.Callable[[typing.Any], typing.Any], MINUS_INF: typing.Any, PLUS_INF: typing.Any) -> _Interval_UnknownTypePolicy:
        """
        ### custom_transfer()
        
        Transfer all elements that are in this multitude and return a new multitude.
        
        The function takes **one lambda function**
        and **two values** – the converted values of `-INF` and `+INF`.
        New values cannot themselves be `-INF` or `+INF`.
        
        ---
        
        - **Lambda** – returns a new value of a point/border of an interval,
          receives one argument - old value of a point/border of an interval.
        - **First value** – new value of the border of the interval, that begins from `-INF` - old value of a border of an interval.
        - **Second value** – new value of the border of the interval, that ends with `+INF` - old value of a border of an interval.
        
        ---
        
        If the first value of an interval becomes greater than the second,
        the function will swap them automatically.
        """
    def empty(self) -> bool:
        """
        return true if this multitude is empty, else return false
        """
    def inverse(self) -> _Interval_UnknownTypePolicy:
        """
        returns the multitude that is the inverse of the given one
        """
    def isdisjoint(self, b: _Interval_UnknownTypePolicy) -> bool:
        """
        return true if these multitudes has no common points, else return false
        """
    def issubset(self, b: _Interval_UnknownTypePolicy) -> bool:
        """
        return true if this multitude is subset of another multitude, else return false
        """
    def issuperset(self, b: _Interval_UnknownTypePolicy) -> bool:
        """
        return true if this multitude is subset of another multitude, else return false
        """
    def points_only(self) -> bool:
        """
        return true if multitude has only separate points (or empty), else return false
        """
    def remove_interval(self, a: _mathInterval.__Interval_UnknownTypePolicy_minimal | _mathInterval.__Interval_UnknownTypePolicy_maximal | typing.Any | tuple[typing.SupportsInt, typing.Any], b: _mathInterval.__Interval_UnknownTypePolicy_minimal | _mathInterval.__Interval_UnknownTypePolicy_maximal | typing.Any | tuple[typing.SupportsInt, typing.Any]) -> bool:
        """
        returns false if all this interval was not inside this multitude, else return true
        """
    def remove_point(self, a: _mathInterval.__Interval_UnknownTypePolicy_minimal | _mathInterval.__Interval_UnknownTypePolicy_maximal | typing.Any | tuple[typing.SupportsInt, typing.Any]) -> bool:
        """
        returns false if this point was not inside this multitude, else return true. Note that the removed point cannot be -INF and +INF
        """
class __Interval_FloatTypePolicy_maximal:
    def __init__(self) -> None:
        ...
    def __repr__(self) -> str:
        ...
class __Interval_FloatTypePolicy_minimal:
    def __init__(self) -> None:
        ...
    def __repr__(self) -> str:
        ...
class __Interval_IntTypePolicy_maximal:
    def __init__(self) -> None:
        ...
    def __repr__(self) -> str:
        ...
class __Interval_IntTypePolicy_minimal:
    def __init__(self) -> None:
        ...
    def __repr__(self) -> str:
        ...
class __Interval_UnknownTypePolicy_maximal:
    def __init__(self) -> None:
        ...
    def __repr__(self) -> str:
        ...
class __Interval_UnknownTypePolicy_minimal:
    def __init__(self) -> None:
        ...
    def __repr__(self) -> str:
        ...
@typing.overload
def Interval(policy: None = None) -> _Interval_UnknownTypePolicy: ...
@typing.overload
def Interval(policy: FloatTypePolicy) -> _Interval_FloatTypePolicy: ...

@typing.overload
def Interval(policy: IntTypePolicy) -> _Interval_IntTypePolicy: ...

@typing.overload
def Interval(policy: UnknownTypePolicy) -> _Interval_UnknownTypePolicy: ...
