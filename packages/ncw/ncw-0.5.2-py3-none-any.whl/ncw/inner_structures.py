# -*- coding: utf-8 -*-
# mypy: disable-error-code="index"

"""
Inner datasructure for the wrappers
"""

import logging

from collections.abc import ItemsView, Iterator, MutableMapping
from typing import Any, Iterable

from .commons import ValueType, assured_int
from .components import (
    Address,
    Node,
    ScalarNode,
    ListNode,
    all_positive_indexes_at_position,
    EMPTY_ADDRESS,
    MAPPING_NODE,
)
from .nested_collections import (
    construct,
    cleanup_after_removal,
    get_child_addresses,
    check_ancestors_before_adding_address,
    matching_items,
)

__all__ = ["ComponentBasedStructure", "Transaction"]

_NOT_PROVIDED = object()


class ComponentBasedStructure(MutableMapping[Address, Node]):
    """A non-threadsafe, mutable datastructure with cross-addressing"""

    def __init__(
        self,
        source: Iterable | "ComponentBasedStructure" | dict[Address, Node] = (),
    ) -> None:
        """build the internal structure"""
        if isinstance(source, (ComponentBasedStructure, dict)):
            data_source: Iterable = list(source.items())
        else:
            data_source = source
        #
        self.__data: dict[Address, Node] = {}
        self.replace_data(data_source)
        self.transaction = Transaction(self)

    def replace_data(self, source: Iterable) -> None:
        """Replace internal data by source"""
        self.__data.clear()
        self.__data.update(source)

    def __getitem__(self, address: Address) -> Node:
        """Return the substructure determined by full_path"""
        return self.__data[address]

    def __delitem__(self, address: Address) -> None:
        """Delete an item"""
        self.delete(address)

    def __setitem__(self, address: Address, value: Node) -> None:
        """set an item"""
        check_ancestors_before_adding_address(self.__data, address)
        #
        # Check descendants
        children = get_child_addresses(self.__data, address)
        if isinstance(value, ScalarNode):
            # ScalarNode instances may not have any children
            for surplus_child_address in children:
                del self.__data[surplus_child_address]
            #
        elif isinstance(value, ListNode):
            # ensure all children have a positive numeric index
            if not all_positive_indexes_at_position(children, len(address)):
                raise ValueError("Existing descendants do not fit a list")
            #
        #
        self.__data[address] = value

    def get_native_data(self, /, search_address: Address = EMPTY_ADDRESS) -> ValueType:
        """Return native data constructed from the stored address, node ..."""
        filtered = matching_items(self.__data, search_address=search_address)
        if not filtered:
            if search_address == EMPTY_ADDRESS:
                return {}
            #
            raise KeyError(search_address)
        #
        return construct(
            {
                found_address.relative_to(search_address).segments: node.value
                for found_address, node in filtered
            }
        )

    def items(self) -> ItemsView[Address, Node]:
        """internally stored items"""
        return self.__data.items()

    def __contains__(self, address, /) -> bool:
        """Number of items"""
        return address in self.__data

    def __iter__(self) -> Iterator[Address]:
        """Iterator over addresses"""
        return iter(self.__data)

    def __len__(self) -> int:
        """Number of items"""
        return len(self.__data)

    def __eq__(self, other) -> bool:
        """Rich comparison: equal items"""
        return self.items() == other.items()

    def get(self, key: Address, default=None) -> Any:
        """Return the Node instance determined by key, or default"""
        try:
            return self.__data[key]
        except KeyError:
            return default
        #

    def _popped_items(
        self,
        address: Address,
        /,
    ) -> Iterator[tuple[Address, Node]]:
        """Return items deleted by the pop operation"""
        filtered = matching_items(self.__data, search_address=address)
        for found_address, node in filtered:
            del self.__data[found_address]
            yield found_address, node
        #

    def cropped_substructure(self, address: Address) -> "ComponentBasedStructure":
        """Return the cropped substructure with addresses relative to address"""
        return ComponentBasedStructure(
            [
                (cropped_address.relative_to(address), node)
                for (cropped_address, node) in self._popped_items(address)
            ]
        )

    def graft(
        self, address: Address, scion: "ComponentBasedStructure", cutoff: bool = False
    ) -> None:
        """modify the instance in place by adding another instance –
        called "scion" here – at address, similar to grafting in horticulture.
        If cutoff is set True, remove all addresses starting with address
        before adding scion.
        This method should preferably called within a transaction
        to ensure a consistent state.
        """
        if not scion:
            return
        #
        if EMPTY_ADDRESS not in scion and address in self.__data:
            if isinstance(self.__data[address], ListNode):
                for sub_address in scion:
                    if sub_address:
                        candidate = sub_address[0]
                        assured_int(
                            candidate,
                            error_message=f"{candidate!r} is not a valid list index",
                        )
                    #
                #
            else:
                del self.__data[address]
            #
        #
        if cutoff:
            list(self._popped_items(address))
        #
        for sub_address, new_node in scion.items():
            self.__data[address + sub_address] = new_node
        #

    # pylint: disable=arguments-renamed ; renamed for consitency
    def pop(self, address: Address, default: Any = _NOT_PROVIDED) -> Any:
        """Return the Node instance determined by address, and delete it
        and its descendants, but do not dot remove any ancestors left childless
        """
        found_items = dict(self._popped_items(address))
        if not found_items:
            if isinstance(default, Node):
                return default
            #
            raise KeyError(address)
        #
        real_default: Node = MAPPING_NODE
        if isinstance(default, Node):
            real_default = default
        #
        found_value: Node = found_items.pop(address, real_default)
        for descendant_address, descendant_value in found_items.items():
            logging.debug("Also removed %r → %r", descendant_address, descendant_value)
        #
        return found_value

    def delete(self, address: Address, /) -> None:
        """Delete an item without returning it"""
        found_items = dict(self._popped_items(address))
        if not found_items:
            raise KeyError(address)
        #
        try:
            del found_items[address]
        except KeyError as error:
            logging.debug("implicit match for %r", str(error))
        #
        cleanup_after_removal(self.__data, address)


class Transaction:
    """Transaction around an update of a ComponentBasedStructure instance"""

    def __init__(self, cbs_instance: ComponentBasedStructure) -> None:
        """Store the ComponentBasedStructure instance"""
        self.__cbs_instance = cbs_instance
        self.__snapshot: tuple[tuple[Address, Node], ...] = ()

    def _draw_snapshot(self) -> None:
        """Store a snapshot of the instance"""
        self.__snapshot = tuple(self.__cbs_instance.items())

    def _restore_snapshot(self) -> None:
        """Resore the instance to the snapshot"""
        self.__cbs_instance.replace_data(self.__snapshot)

    def __enter__(self):
        """Cpontect manager enter: draw a snapshot"""
        self._draw_snapshot()
        return self

    def __exit__(self, exc_type, unused_exc_value, unused_traceback):
        """Context manager exit: Restore the snapshot if anything went wrong"""
        if exc_type is not None:
            self._restore_snapshot()
        #


# vim: fileencoding=utf-8 ts=4 sts=4 sw=4 autoindent expandtab syntax=python:
