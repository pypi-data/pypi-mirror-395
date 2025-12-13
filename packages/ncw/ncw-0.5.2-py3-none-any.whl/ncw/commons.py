# -*- coding: utf-8 -*-
# mypy: disable-error-code="index"

"""
common type aliases, constants and helper functions
"""

from typing import Any, Iterable, TypeAlias


ScalarType: TypeAlias = str | int | float | bool | None
CollectionType: TypeAlias = dict | list
ValueType: TypeAlias = ScalarType | CollectionType

SegmentsTuple: TypeAlias = tuple[ScalarType, ...]
IndexType: TypeAlias = str | SegmentsTuple


COMMA_BLANK = ", "
DOT = "."
EMPTY = ""
DOUBLE_QUOTE = '"'
SLASH = "/"


def assured_collection(
    original: Any,
    error_message: str = "Expected a collection (ie. a dict or a list",
) -> CollectionType:
    """assure the original is a dict or a list"""
    if isinstance(original, (dict, list)):
        return original
    #
    raise TypeError(error_message)


def assured_number(
    original: Any, error_message: str = "Expected a number (float or int, not bool)"
) -> float | int:
    """assure the original is a int or float"""
    if not isinstance(original, bool) and isinstance(original, (float, int)):
        return original
    #
    raise TypeError(error_message)


def assured_scalar(
    original: Any,
    error_message: str = "Expected a scalar (ie. a string, an int, a float,"
    " or a bool), or None",
) -> ScalarType:
    """assure the original is a scalar"""
    if isinstance(original, (str, int, float, bool)) or original is None:
        return original
    #
    raise TypeError(error_message)


def assured_segments_tuple(
    original: Any,
    error_message: str = "Expected a segments tuple",
) -> SegmentsTuple:
    """assure the original is a segments tuple"""
    if isinstance(original, tuple):
        collector: list[ScalarType] = []
        for item in original:
            collector.append(assured_scalar(item, error_message=error_message))
        #
        return tuple(collector)
    #
    raise TypeError(error_message)


def assured_index(original: Any) -> IndexType:
    """assure the original is a valid index"""
    if isinstance(original, str):
        return original
    #
    return assured_segments_tuple(original, error_message="Expected a valid index")


def assured_dict(original: Any, error_message: str = "Expected a dict") -> dict:
    """assure the original is a dict"""
    if isinstance(original, dict):
        return original
    #
    raise TypeError(error_message)


def assured_float(original: Any, error_message: str = "Expected a float") -> float:
    """assure the original is a float"""
    if isinstance(original, float):
        return original
    #
    raise TypeError(error_message)


def assured_int(
    original: Any, error_message: str = "Expected an int (not bool)"
) -> int:
    """assure the original is an int"""
    if not isinstance(original, bool) and isinstance(original, int):
        return original
    #
    raise TypeError(error_message)


def assured_str(original: Any, error_message: str = "Expected a string") -> str:
    """assure the original is a str"""
    if isinstance(original, str):
        return original
    #
    raise TypeError(error_message)


def assured_list(original: Any, error_message: str = "Expected a list") -> list:
    """assure the original is a list"""
    if isinstance(original, list):
        return original
    #
    raise TypeError(error_message)


def assured_iterable(
    original: Any, error_message: str = "Expected an iterable"
) -> Iterable:
    """assure the original is an iterable"""
    if isinstance(original, Iterable):
        return original
    #
    raise TypeError(error_message)


def to_text(
    original: Any,
    encoding: str = "utf-8",
    error_message: str = "Expected a string or bytes",
) -> str:
    """Return a str from original.
    If the error message is left blank, convert any type to str
    """
    if isinstance(original, str):
        return original
    #
    if isinstance(original, (bytes, bytearray)):
        return original.decode(encoding)
    #
    if error_message:
        raise TypeError(error_message)
    #
    return str(original)


# vim: fileencoding=utf-8 ts=4 sts=4 sw=4 autoindent expandtab syntax=python:
