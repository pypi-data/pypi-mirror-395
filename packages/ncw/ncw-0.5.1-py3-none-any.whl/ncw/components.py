# -*- coding: utf-8 -*-

"""
components of nested collections: Addresses, Nodes, and Items
"""

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any, final, overload

from .commons import ScalarType, COMMA_BLANK, assured_int, assured_scalar


def get_segments_representation(*segments: ScalarType) -> str:
    """Return a representation of the segments"""
    return COMMA_BLANK.join([repr(item) for item in segments])


class NoMutableCollectionError(Exception):
    """Raised when trying to traverse throush a leaf of a nested collection"""


class CompoundKeyError(Exception):
    """Raised with the consumed keys if traversal failed"""

    def __init__(self, *segments) -> None:
        """Store the segments"""
        self.segments = segments

    def __repr__(self) -> str:
        """Representation"""
        return (
            f"{self.__class__.__name__}({get_segments_representation(*self.segments)})"
        )

    def __str__(self) -> str:
        """String value"""
        return repr(self.segments)


class Address(Sequence[ScalarType]):
    """Address in a nested collection, basically a tuple of scalars"""

    def __init__(self, *segments: ScalarType) -> None:
        """Store the segments"""
        self.segments: tuple[ScalarType, ...] = segments

    @overload
    def __getitem__(self, index: int) -> ScalarType: ...
    @overload
    def __getitem__(self, index: slice) -> "Address": ...
    @final
    def __getitem__(self, index: slice | int) -> Any:
        """Direct segments access"""
        if isinstance(index, slice):
            new_segments: tuple[ScalarType, ...] = self.segments[index]
            return Address(*new_segments)
        #
        return assured_scalar(self.segments[assured_int(index)])

    def __repr__(self) -> str:
        """Representation"""
        return (
            f"{self.__class__.__name__}({get_segments_representation(*self.segments)})"
        )

    def __str__(self) -> str:
        """String value"""
        return repr(self.segments)

    def __hash__(self) -> int:
        """hash value"""
        return hash(repr(self))

    def __eq__(self, other) -> bool:
        """rich comparision: equals"""
        return repr(self) == repr(other)

    def __bool__(self) -> bool:
        """bool value"""
        return bool(self.segments)

    def __len__(self) -> int:
        """length"""
        return len(self.segments)

    def __add__(self, other) -> "Address":
        """append other"""
        added_segments = self.segments + other.segments
        return Address(*added_segments)

    @property
    def parent(self) -> "Address":
        """return the parent address"""
        if not self:
            raise ValueError("An empty address has no parent")
        #
        return Address(*self.segments[:-1])

    def startswith(self, other: "Address") -> bool:
        """Return True if the segments begin with other’s segments"""
        if not other:
            return True
        #
        if len(other) > len(self):
            return False
        #
        for index, item in enumerate(other.segments):
            if self.segments[index] != item:
                return False
            #
        #
        return True

    def relative_to(self, other: "Address") -> "Address":
        """return the addtress of self relative to other"""
        if self.startswith(other):
            return Address(*self.segments[len(other) :])
        #
        raise ValueError(f"{self} does not start with {other}")


EMPTY_ADDRESS = Address()


# pylint: disable = too-few-public-methods


class Node:
    """Node in a nested collection"""

    @property
    def value(self):
        """return the value"""
        raise NotImplementedError

    def __eq__(self, other) -> bool:
        """rich comparision: equals"""
        return self.value == other.value


class ScalarNode(Node):
    """Scalar value in a nested collection"""

    def __init__(self, value) -> None:
        """set value"""
        self.__value: ScalarType = assured_scalar(value)

    @property
    def value(self) -> ScalarType:
        """return the value"""
        return self.__value

    def __repr__(self) -> str:
        """Representation"""
        return f"{self.__class__.__name__}({self.value!r})"


class CollectionNode(Node):
    """Collection"""

    @property
    def value(self):
        """return the value"""
        raise NotImplementedError

    def __repr__(self) -> str:
        """Representation"""
        return f"{self.__class__.__name__}()"


class ListNode(CollectionNode):
    """list in a nested collection"""

    @property
    def value(self):
        """return an empty list"""
        return []


class MappingNode(Node):
    """mapping (ie. dict) in a nested collection"""

    @property
    def value(self):
        """return an empty dict"""
        return {}


LIST_NODE = ListNode()
MAPPING_NODE = MappingNode()


@dataclass(frozen=True)
class Item:
    """Item in a collection"""

    address: Address
    node: Node


def get_node(value: Any) -> Node:
    """Return a node from the original value"""
    if isinstance(value, list):
        return LIST_NODE
    #
    if isinstance(value, dict):
        return MAPPING_NODE
    #
    return ScalarNode(value)


def all_positive_indexes_at_position(addresses: list[Address], position: int) -> bool:
    """Return True if all addresses in the list have a positive index number
    at the specified position
    """
    for single_address in addresses:
        try:
            if assured_int(single_address[position]) < 0:
                return False
            #
        except (IndexError, TypeError):
            # IndexError: Address to short
            # TypeError: single_address[position] is not an int
            return False
        #
    #
    return True


def assured_node(
    original: Any, error_message: str = "Expected a Node instance"
) -> Node:
    """assure the original is a Node instance"""
    if isinstance(original, Node):
        return original
    #
    raise TypeError(error_message)


# vim: fileencoding=utf-8 ts=4 sts=4 sw=4 autoindent expandtab syntax=python:
