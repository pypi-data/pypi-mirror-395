# -*- coding: utf-8 -*-
# mypy: disable-error-code="index"

"""
all things directly related to collections nesting
"""

import logging

from collections.abc import Iterator, Sequence

from .commons import (
    ScalarType,
    ValueType,
    SegmentsTuple,
    assured_int,
    assured_collection,
)
from .components import (
    CompoundKeyError,
    NoMutableCollectionError,
    Address,
    Node,
    ScalarNode,
    ListNode,
    Item,
    EMPTY_ADDRESS,
    get_node,
)


class RecursionDetected(Exception):
    """Raised when a recursion was detected"""

    def __init__(self, message: str):
        """Store the message"""
        self.message = message


class RecursionCircuitBreaker:
    """Circuit breaker for avoiding infinite loops/recursions"""

    def __init__(self, placeholder: ScalarType = None, initial_value: ValueType = None):
        """Store the placeholder"""
        self.__placeholder: ScalarType = placeholder
        self.__registered_ids: list[int] = []
        self.register_id(initial_value)

    def checked_collection_id(
        self, value: ValueType, registry: Sequence[int], verbose: bool = False
    ) -> int:
        """Check if the id of a dict or list is not registered yet.
        Raise an exception if it is.
        """
        if isinstance(value, (dict, list)):
            current_id = id(value)
            if current_id in registry:
                details = f", replacing it by {self.__placeholder!r}" if verbose else ""
                raise RecursionDetected(f"ignoring {value!r} nested in itself{details}")
            #
            return current_id
        #
        raise NoMutableCollectionError

    def register_id(self, value: ValueType, verbose: bool = False) -> None:
        """Register the id of dict or list instances only after checking it"""
        try:
            current_id = self.checked_collection_id(
                value, self.__registered_ids, verbose=verbose
            )
        except NoMutableCollectionError:
            ...
        else:
            self.__registered_ids.append(current_id)
        #

    @property
    def placeholder(self) -> ScalarType:
        """Return the configured placeholder"""
        return self.__placeholder


def get_collection_member(collection: ValueType, key: ScalarType) -> ValueType:
    """Get the member of a dict or list"""
    if isinstance(collection, (dict, list)):
        return collection[key]  # type: ignore[index]
    #
    raise NoMutableCollectionError(
        "Not a collection in the sense of this package,"
        f" cannot retrieve {collection!r}[{key!r}]"
    )


def permissive_partial_traverse(
    start: ValueType,
    address: Address,
    min_remaining_segments: int = 0,
    recursion_placeholder: ScalarType = None,
) -> tuple[ValueType, Address, Address]:
    """Traverse through a data structure starting at the start node,
    until minimum min_remaining_segments of the path are left
    """
    if min_remaining_segments < 0:
        raise ValueError("No negative value allowed here")
    #
    breaker = RecursionCircuitBreaker(
        placeholder=recursion_placeholder, initial_value=start
    )
    pointer = start
    consumed_segments: list[ScalarType] = []
    remaining_segments: list[ScalarType] = list(address.segments)
    while len(remaining_segments) > min_remaining_segments:
        key = remaining_segments.pop(0)
        try:
            pointer = get_collection_member(pointer, key)
        except (IndexError, KeyError, TypeError, NoMutableCollectionError):
            return (
                pointer,
                Address(*consumed_segments),
                Address(key, *remaining_segments),
            )
        #
        consumed_segments.append(key)
        try:
            breaker.register_id(pointer, verbose=True)
        except RecursionDetected as recursion_error:
            logging.warning(str(recursion_error))
            return (
                breaker.placeholder,
                Address(*consumed_segments),
                Address(*remaining_segments),
            )
        #
    #
    return pointer, Address(*consumed_segments), Address(*remaining_segments)


def full_traverse(
    start: ValueType,
    address: Address,
    recursion_placeholder: ScalarType = None,
) -> ValueType:
    """Traverse through a data structure starting at the start node"""
    breaker = RecursionCircuitBreaker(
        placeholder=recursion_placeholder, initial_value=start
    )
    pointer = start
    consumed_segments: list[ScalarType] = []
    remaining_segments: list[ScalarType] = list(address.segments)
    while remaining_segments:
        key = remaining_segments.pop(0)
        consumed_segments.append(key)
        try:
            pointer = get_collection_member(pointer, key)
        except (IndexError, KeyError) as error:
            raise CompoundKeyError(*consumed_segments) from error
        #
        try:
            breaker.register_id(pointer, verbose=True)
        except RecursionDetected as recursion_error:
            logging.warning(str(recursion_error))
            return breaker.placeholder
        #
    #
    return pointer


def traverse_with_default(
    start: ValueType,
    address: Address,
    default: ValueType = None,
) -> ValueType:
    """Traverse through a data structure starting at the start node
    and return the result or the default
    """
    try:
        return full_traverse(start, address)
    except CompoundKeyError:
        return default
    #


def _inner_iter_native(
    breaker: RecursionCircuitBreaker,
    start: ValueType,
    *previous_collection_ids: int,
    previous_segments: SegmentsTuple = (),
) -> Iterator[tuple[SegmentsTuple, ValueType]]:
    """Return an iterator over all SegmentTuples and values"""
    # recursion circuit breaker: in straight line only
    try:
        current_collection_id = breaker.checked_collection_id(
            start, previous_collection_ids, verbose=True
        )
    except RecursionDetected as recursion_error:
        logging.warning(str(recursion_error))
        yield previous_segments, breaker.placeholder
        return
    except NoMutableCollectionError:
        yield previous_segments, start
        return
    #
    subitems: list[tuple[ScalarType, ValueType]] = []
    if isinstance(start, dict):
        subitems = list(start.items())
        if not subitems:
            yield previous_segments, {}
        #
    elif isinstance(start, list):
        subitems = list(enumerate(start))
        yield previous_segments, []
    #
    for key, value in subitems:
        yield from _inner_iter_native(
            breaker,
            value,
            *previous_collection_ids,
            current_collection_id,
            previous_segments=(*previous_segments, key),
        )
    #


def iter_native(
    start: ValueType,
    previous_segments: SegmentsTuple = (),
    recursion_placeholder: ScalarType = None,
) -> Iterator[tuple[SegmentsTuple, ValueType]]:
    """Return an iterator over all native addresses and values
    required to represent a data structure
    """
    breaker = RecursionCircuitBreaker(placeholder=recursion_placeholder)
    yield from _inner_iter_native(
        breaker,
        start,
        previous_segments=previous_segments,
    )


def iter_nodes(
    start: ValueType,
    previous_address: Address = Address(),
    recursion_placeholder: ScalarType = None,
) -> Iterator[tuple[Address, Node]]:
    """Return an iterator over all addressable nodes in a data structure"""
    for segments, value in iter_native(
        start,
        previous_segments=previous_address.segments,
        recursion_placeholder=recursion_placeholder,
    ):
        yield Address(*segments), get_node(value)


def iter_collection_items(
    start: ValueType,
    previous_address: Address = Address(),
) -> Iterator[Item]:
    """Return an iterator over all addressable endpoint items in a data structure"""
    for address, node in iter_nodes(start, previous_address=previous_address):
        yield Item(address, node)
    #


def iter_addresses(
    start: ValueType,
    previous_address: Address = Address(),
) -> Iterator[Address]:
    """Return an iterator over all endpoint paths in the data structure"""
    for address, _ in iter_nodes(start, previous_address=previous_address):
        yield address
    #


def construct(crosswise: dict[SegmentsTuple, ValueType]) -> ValueType:
    """construct a nested collection from a mapping"""
    if not crosswise:
        raise ValueError(
            "Constructing a nested collection from an empty dict is not supported"
        )
    #
    base_value = crosswise.pop((), {})
    if not crosswise:
        return base_value
    #
    child_nodes: dict[ScalarType, list[SegmentsTuple]] = {}
    for subaddress in crosswise:
        current_key = subaddress[0]
        child_nodes.setdefault(current_key, []).append(subaddress)
    #
    if isinstance(base_value, list):
        indexes: list[int] = [-1]
        indexes.extend(map(assured_int, child_nodes))
        for _ in range(max(indexes) + 1):
            base_value.append(None)
        #
    elif not isinstance(base_value, dict):
        logging.debug(
            "Traversing through a leaf, overriding value %r",
            base_value,
        )
        base_value = {}
    #
    base_value = assured_collection(base_value)
    for key, subkeys in child_nodes.items():
        subcrosswise: dict[SegmentsTuple, ValueType] = {
            segments[1:]: crosswise.pop(segments) for segments in subkeys
        }
        base_value[key] = construct(subcrosswise)  # ty: ignore[invalid-assignment]
    #
    if crosswise:
        # should never occur, so not really testable
        raise ValueError(
            f"Unexpected: not all addresses consumed, remaining: {crosswise!r}"
        )
    #
    return base_value


def get_child_addresses(
    components_mapping: dict[Address, Node], key: Address
) -> list[Address]:
    """Return a list of child addresses of components_mapping[key]"""
    key_length = len(key)
    return [
        child_address
        for child_address in components_mapping
        if child_address.startswith(key) and len(child_address) > key_length
    ]


def cleanup_after_removal(
    components_mapping: dict[Address, Node], removed_key: Address
) -> None:
    """Do cleanup in a components mapping after removed_key has been deleted
    from it, modifying components_mapping in place
    """
    # cleanup of collection nodes whose children have all been removed
    # (by removing removed_key)
    current_ancestor_address = removed_key
    # pylint: disable=too-many-nested-blocks ; refactoring candidate
    while True:
        try:
            current_ancestor_address = current_ancestor_address.parent
        except ValueError:
            break
        #
        if current_ancestor_address not in components_mapping:
            continue
        #
        children = get_child_addresses(components_mapping, current_ancestor_address)
        if children:
            # logging.warning("Fixing list %r", children)
            # Rearrange list node children if required,
            # e.g. if a list contained 6 elements,
            #      and index 2 got deleted, then:
            #           [0] [1] [2] [3] [4] [5]                 (original)
            #           [0] [1] [X] [3] {4] [5]                 (deletion)
            #           [0→0] [1→1] [2→void] [3→2] [4→3] [5→4]  (re-map)
            #           [0] [1] [2] [3] [4]                     (result)
            current_address_length = len(current_ancestor_address)
            if isinstance(components_mapping[current_ancestor_address], ListNode):
                indexes = sorted(
                    set(
                        assured_int(child_address[current_address_length])
                        for child_address in children
                    )
                )
                key_subindex = assured_int(removed_key[current_address_length])
                if key_subindex not in indexes and key_subindex < max(indexes):
                    for child_address in children:
                        child_subindex = assured_int(
                            child_address[current_address_length]
                        )
                        if child_subindex > key_subindex:
                            new_segments = list(child_address.segments)
                            new_segments[current_address_length] = child_subindex - 1
                            # no .pop() here for type safety
                            saved_node = components_mapping[child_address]
                            del components_mapping[child_address]
                            components_mapping[Address(*new_segments)] = saved_node
                        #
                    #
                #
            #
            # Exit the loop if any children were found, no further cleanup necessary
            break
        #
        del components_mapping[current_ancestor_address]
    #


def check_ancestors_before_adding_address(
    components_mapping: dict[Address, Node], add_candidate: Address
) -> None:
    """Check all ancestors if the added key fits the list"""
    current_key = add_candidate
    while True:
        try:
            current_key = current_key.parent
        except ValueError:
            break
        #
        if current_key not in components_mapping:
            continue
        #
        current_value = components_mapping[current_key]
        if isinstance(current_value, ScalarNode):
            # Remove any ScalarNode at an ancestor position
            del components_mapping[current_key]
        elif isinstance(current_value, ListNode):
            current_key_length = len(current_key)
            significant_index = assured_int(add_candidate[current_key_length])
            if significant_index < 0:
                raise IndexError("Cannot use a negative index here")
            #
            children = get_child_addresses(components_mapping, current_key)
            existing_indexes = sorted(
                set(
                    assured_int(child_address[current_key_length])
                    for child_address in children
                )
            )
            if existing_indexes:
                pos_after_list = significant_index - max(existing_indexes)
                if pos_after_list > 1:
                    raise ValueError(
                        "Implicitly extending a list by more than one item"
                        " is not implemented"
                    )
                #
                if pos_after_list == 1:
                    logging.info("Implicitly extending list by one item")
                #
            #
        #
        break
    #


def matching_items(
    components_mapping: dict[Address, Node],
    /,
    search_address: Address = EMPTY_ADDRESS,
) -> list[tuple[Address, Node]]:
    """Get a list of matching item tuples"""
    return [
        (stored_address, stored_node)
        for (stored_address, stored_node) in components_mapping.items()
        if stored_address.startswith(search_address)
    ]


# vim: fileencoding=utf-8 ts=4 sts=4 sw=4 autoindent expandtab syntax=python:
