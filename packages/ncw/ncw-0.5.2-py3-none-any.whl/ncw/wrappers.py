# -*- coding: utf-8 -*-
# mypy: disable-error-code="index"

"""
Datastructure wrappers
"""

# import logging

from collections.abc import ItemsView, Iterator, Mapping, MutableMapping
from typing import Iterable, TypeVar, Union, overload, final

from .commons import (
    DOT,
    IndexType,
    SegmentsTuple,
    ValueType,
    assured_iterable,
    assured_index,
)
from .cache import ParsingCache, SINGLETON_CACHES
from .components import Address, get_node, EMPTY_ADDRESS
from .inner_structures import ComponentBasedStructure
from .locks import BoltTypeLock, DummyLock
from .nested_collections import iter_native, iter_nodes


__all__ = ["BaseStructure", "FrozenStructure", "MutableStructure"]

_T = TypeVar("_T")
_NO_DEFAULT = object()

# StructureDataType: TypeAlias = Union[ValueType, "BaseStructure"]
# StructureSourceItem: TypeAlias = tuple[IndexType, ValueType]


class BaseStructure:
    """A data structure, base class for mutable and immutable data structure classes"""

    def __init__(
        self,
        source: Union[
            "BaseStructure",
            Mapping[IndexType, ValueType],
            Iterable[tuple[IndexType, ValueType]],
        ] = (),
        /,
        separator: str = DOT,
    ) -> None:
        """Buikd abd store an internal ComponentBasedStructure
        mapping Node intnaces to Address instances
        """
        if isinstance(source, BaseStructure):
            source_iterable: Iterable[tuple[IndexType, ValueType]] = (
                source.stored_items()
            )
        elif isinstance(source, Mapping):
            source_iterable = source.items()
        elif isinstance(source, Iterable) and not isinstance(source, str):
            source_iterable = assured_iterable(source)
        else:
            raise ValueError(
                "Not a valid source,"
                f" maybe try {self.__class__.__name__}.from_native({source!r})"
            )
        #
        self.__addresses_cache: ParsingCache = SINGLETON_CACHES[separator]
        self.__lock: BoltTypeLock | DummyLock = (
            BoltTypeLock() if self.is_mutable else DummyLock()
        )
        with self.__lock.exclusive:
            self.__internal_cbs = ComponentBasedStructure(
                (self.__addresses_cache[assured_index(index)], get_node(value))
                for index, value in source_iterable
            )
        #

    @classmethod
    def from_native(
        cls, original: ValueType, /, separator: str = DOT
    ) -> "BaseStructure":
        """Create an instance from the native value original"""
        return cls(iter_native(original), separator=separator)

    def to_native(self) -> ValueType:
        """native data"""
        return self.__get_native_data()

    def __get_native_data(self, search_address: Address = EMPTY_ADDRESS) -> ValueType:
        """native data at address Address"""
        with self.__lock.shared:
            try:
                return self.__internal_cbs.get_native_data(search_address)
            except KeyError as error:
                raise KeyError(search_address.segments) from error
            #
        #

    @property
    def is_mutable(self) -> bool:
        """Return True only from on mutable subclasses"""
        raise NotImplementedError

    @property
    def separator(self) -> str:
        """Return the separator"""
        return self.__addresses_cache.separator

    def __getitem__(self, key: IndexType) -> ValueType:
        """Return the substructure determined by full_path"""
        return self.__get_native_data(self.__addresses_cache[key])

    def __repr__(self) -> str:
        """String representation"""
        return (
            f"{self.__class__.__name__}({repr(self.__as_stored_native_dict())},"
            f" separator={self.separator!r})"
        )

    @overload
    def get(self, key: IndexType, /) -> ValueType: ...
    @overload
    def get(self, key: IndexType, /, default: ValueType) -> ValueType: ...
    @overload
    def get(self, key: IndexType, /, default: _T) -> ValueType | _T: ...
    @final
    def get(self, key: IndexType, default=None) -> ValueType:
        """Return the native substructure determined by key"""
        try:
            return self.__get_native_data(self.__addresses_cache[key])
        except KeyError:
            return default
        #

    def __eq__(self, other) -> bool:
        """Equality test"""
        return all(
            (
                self.stored_items() == other.stored_items(),
                self.is_mutable == other.is_mutable,
                self.separator == other.separator,
            )
        )

    def iter_stored(self) -> Iterator[SegmentsTuple]:
        """Iterator over stored indexes"""
        return iter(address.segments for address in self.__internal_cbs)

    def _iter_all_addresses(self) -> Iterator[Address]:
        """Iterator over all addresses: stored and interpolated ones"""
        stored_addresses = list(self.__internal_cbs)
        yield from stored_addresses
        seen_addresses = set(stored_addresses)
        for single_stored_address in stored_addresses:
            current_address = single_stored_address
            while True:
                try:
                    current_address = current_address.parent
                except ValueError:
                    break
                #
                if current_address not in seen_addresses:
                    yield current_address
                #
                seen_addresses.add(current_address)
            #
        #

    def __contains__(self, key, /) -> bool:
        """Return True if key is contained in either stored or interpolated form"""
        address = self.__addresses_cache[key]
        for current_address in self._iter_all_addresses():
            if address == current_address:
                return True
            #
        #
        return False

    def __iter__(self) -> Iterator[SegmentsTuple]:
        """Iterator over (virtually available) indexes"""
        return iter(address.segments for address in self._iter_all_addresses())

    def __len__(self) -> int:
        """Number of stored keys"""
        return len(self.__internal_cbs)

    def __as_stored_native_dict(self) -> dict[SegmentsTuple, ValueType]:
        """Native dict from the cross struct"""
        with self.__lock.shared:
            native_dict = {
                address.segments: node.value
                for address, node in self.__internal_cbs.items()
            }
        #
        return native_dict

    def __as_full_native_dict(self) -> dict[SegmentsTuple, ValueType]:
        """Full native dict from the cross struct"""
        return {
            address.segments: self.__internal_cbs.get_native_data(address)
            for address in self._iter_all_addresses()
        }

    def stored_items(self) -> ItemsView[SegmentsTuple, ValueType]:
        """Iterator over (segments, value) tuples"""
        return self.__as_stored_native_dict().items()

    def items(self) -> ItemsView[SegmentsTuple, ValueType]:
        """Iterator over (segments, value) tuples"""
        return self.__as_full_native_dict().items()

    # TODO: list methods (append, extend, insert)

    def _set_item(self, key, value) -> None:
        """set an item"""
        if not self.is_mutable:
            raise TypeError("Immutable instances do not support item setting")
        #
        with self.__lock.exclusive:
            base_address = self.__addresses_cache[key]
            # Snapshot the data structure first,
            # then try to add all nodes created from the data structure
            with self.__internal_cbs.transaction:
                if value and isinstance(value, (dict, list)):
                    for offset_address, node in iter_nodes(value):
                        self.__internal_cbs[base_address + offset_address] = node
                    #
                #
                else:
                    self.__internal_cbs[base_address] = get_node(value)
                #
            #
        #

    def __or__(self, other: "BaseStructure"):
        """instance | other implementation via an
        intermediate MutableStructure instance
        """
        intermediate_mutable_instance = self.to_mutable_structure()
        intermediate_mutable_instance._update_from(other)
        if self.is_mutable:
            return intermediate_mutable_instance
        #
        return intermediate_mutable_instance.to_frozen_structure()

    def _update_from(self, other: "BaseStructure") -> None:
        """Add the stored items of other"""
        if not self.is_mutable:
            raise TypeError("Immutable instances do not support in-place update")
        #
        with self.__lock.exclusive:
            # Snapshot the data structure first,
            # then try to add all nodes created from the data structure
            with self.__internal_cbs.transaction:
                for segments, value in other.stored_items():
                    self.__internal_cbs[self.__addresses_cache[segments]] = get_node(
                        value
                    )
                #
            #
        #

    def _delete_item(self, key, /) -> None:
        """delete an item"""
        if not self.is_mutable:
            raise TypeError("Immutable instances do not support item deletion")
        #
        with self.__lock.exclusive, self.__internal_cbs.transaction:
            try:
                del self.__internal_cbs[self.__addresses_cache[key]]
            except KeyError as error:
                raise KeyError(key) from error
            #
        #

    @overload
    def _pop(self, key: IndexType, /) -> ValueType: ...
    @overload
    def _pop(self, key: IndexType, /, default: ValueType) -> ValueType: ...
    @overload
    def _pop(self, key: IndexType, /, default: _T) -> ValueType: ...
    @final
    def _pop(self, key: IndexType, default=_NO_DEFAULT) -> ValueType:
        """Return the value determined by key, and delete it"""
        if not self.is_mutable:
            raise TypeError("Immutable instances do not support item popping")
        #
        with self.__lock.exclusive, self.__internal_cbs.transaction:
            cropped = self.__internal_cbs.cropped_substructure(
                self.__addresses_cache[key]
            )
        #
        if not cropped:
            if (
                isinstance(default, (str, int, float, bool, dict, list))
                or default is None
            ):
                return default
            #
            raise KeyError(key)
        #
        return cropped.get_native_data()

    def to_frozen_structure(self) -> "FrozenStructure":
        """Return a FrozenStructure instance"""
        return FrozenStructure(self, separator=self.separator)

    def to_mutable_structure(self) -> "MutableStructure":
        """Return a MutableStructure instance"""
        return MutableStructure(self, separator=self.separator)


class FrozenStructure(BaseStructure, Mapping[IndexType, ValueType]):
    """An immutable data structure"""

    @property
    def is_mutable(self) -> bool:
        """Return True only from on mutable subclasses"""
        return False

    @classmethod
    def from_native(
        cls, original: ValueType, /, separator: str = DOT
    ) -> "FrozenStructure":
        """Create an instance from the native value original"""
        return cls(iter_native(original), separator=separator)

    def copy(self) -> "FrozenStructure":
        """(deep) copy of the instance"""
        return self.to_frozen_structure()

    def __ior__(self, other: BaseStructure):
        """Raises a TypeError explicitly"""
        raise TypeError(
            f"Cannot update {self!r} with {other!r}"
            " because immutable instances do not support in-place update"
        )


class MutableStructure(BaseStructure, MutableMapping[IndexType, ValueType]):
    """A mutable data structure"""

    @property
    def is_mutable(self) -> bool:
        """Return True on mutable instances"""
        return True

    @classmethod
    def from_native(
        cls, original: ValueType, /, separator: str = DOT
    ) -> "MutableStructure":
        """Create an instance from the native value original"""
        return cls(iter_native(original), separator=separator)

    def copy(self) -> "MutableStructure":
        """(deep) copy of the instance"""
        return self.to_mutable_structure()

    def __setitem__(self, key: IndexType, value: ValueType) -> None:
        """implementation of 'instance[key] = value'"""
        self._set_item(key, value)

    def __delitem__(self, key: IndexType) -> None:
        """implementation of 'del instance[key]'"""
        self._delete_item(key)

    # pylint:disable=arguments-differ ; ok for the type checkers
    @overload
    def pop(self, key: IndexType, /) -> ValueType: ...
    @overload
    def pop(self, key: IndexType, /, default: ValueType) -> ValueType: ...
    @overload
    def pop(self, key: IndexType, /, default: _T) -> ValueType | _T: ...
    @final
    def pop(self, key: IndexType, default=_NO_DEFAULT) -> ValueType:
        """Return the value determined by key, and delete it"""
        return self._pop(key, default=default)

    def __ior__(self, other: BaseStructure) -> "MutableStructure":
        """Add the stored items of other"""
        self._update_from(other)
        return self

    @overload
    def add(
        self,
        other: BaseStructure,
        /,
        **kwargs: ValueType,
    ) -> None: ...
    @overload
    def add(
        self,
        other: Mapping[IndexType, ValueType],
        /,
        **kwargs: ValueType,
    ) -> None: ...
    @overload
    def add(
        self,
        other: Iterable[tuple[IndexType, ValueType]],
        /,
        **kwargs: ValueType,
    ) -> None: ...
    @overload
    def add(self, /, **kwargs: ValueType) -> None: ...
    @final
    def add(
        self,
        other: BaseStructure
        | Mapping[IndexType, ValueType]
        | Iterable[tuple[IndexType, ValueType]] = (),
        /,
        **kwargs: ValueType,
    ) -> None:
        """Add the stored items of other.
        If kwargs are provided,
        calculate keys bay splitting the provided keys by the '_' character
        before adding the values.
        """
        other_structure = MutableStructure(other)
        for original_key, value in kwargs.items():
            calculated_key = tuple(original_key.split("_"))
            other_structure[calculated_key] = value
        #
        self._update_from(other_structure)


# vim: fileencoding=utf-8 ts=4 sts=4 sw=4 autoindent expandtab syntax=python:
