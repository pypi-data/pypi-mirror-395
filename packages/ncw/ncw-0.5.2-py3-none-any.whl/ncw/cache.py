# -*- coding: utf-8 -*-

"""
ParsingCache
"""

from collections import Counter
from collections.abc import Mapping
from json import JSONDecodeError, dumps, loads
from re import Match, compile as re_compile
from threading import Lock

from .commons import DOT, DOUBLE_QUOTE, EMPTY, IndexType, ScalarType
from .components import Address


NEXT_QUOTED = re_compile('^"([^"]+)"')
NEXT_IN_SUBSCRIPT_QUOTED = re_compile(r'^\["([^"]+)"\]')
NEXT_IN_SUBSCRIPT_SIMPLE = re_compile(r"^\[([^\]]+)\]")


class OneCharSeparated:
    """Base class having a separator property given at init"""

    def __init__(self, separator: str = DOT) -> None:
        """Initialize with a single-character separator"""
        if len(separator) != 1:
            raise TypeError("The separator must be a single character")
        #
        self.__separator = separator

    @property
    def separator(self) -> str:
        """Return the separator string"""
        return self.__separator

    def __repr__(self) -> str:
        """String representation"""
        return f"{self.__class__.__name__}(separator={self.separator!r})"


class SegmentsParser(OneCharSeparated):
    """Can build a tuple of segments from a string"""

    def __init__(self, separator: str = DOT) -> None:
        """Initialize with a single-character separator"""
        super().__init__(separator=separator)
        self._active = False
        self._expect_segment_end = False
        self._collected_segments: list[ScalarType] = []
        self._current_segment_sources: list[str] = []

    def _add_segment(self, segment_source: str) -> None:
        """Add a new segment from segment_source"""
        try:
            segment = loads(segment_source)
        except JSONDecodeError:
            segment = segment_source
        #
        self._collected_segments.append(segment)
        self._current_segment_sources.clear()

    def _store_and_reset_segment(self) -> None:
        """reset the internal state between segments"""
        if self._current_segment_sources:
            self._add_segment(EMPTY.join(self._current_segment_sources))
        #
        self._expect_segment_end = False

    def _add_match_and_get_end_pos(self, match: Match, quote: bool = False) -> int:
        """Add the matched portion that is quoted or in a subscript ([...])
        and return the match end position
        """
        self._expect_segment_end = True
        segment_source = f'"{match.group(1)}"' if quote else match.group(1)
        self._add_segment(segment_source)
        return match.end()

    def _check_for_fast_forward(self, path_source: str, pos: int) -> int:
        """Check if we can fast-forward"""
        if self._current_segment_sources:
            return 0
        #
        remainder = path_source[pos:]
        character = remainder[0]
        if character == DOUBLE_QUOTE:
            match = NEXT_QUOTED.match(remainder)
            if match:
                return self._add_match_and_get_end_pos(match, quote=True)
            #
        elif character == "[":
            quote = True
            match = NEXT_IN_SUBSCRIPT_QUOTED.match(remainder)
            if not match:
                quote = False
                match = NEXT_IN_SUBSCRIPT_SIMPLE.match(remainder)
            #
            if match:
                return self._add_match_and_get_end_pos(match, quote=quote)
            #
        #
        return 0

    def split_into_segments(self, path_source: str) -> Address:
        """Split a string into an Address instance suitable
        for addressing an item in a netsted collection
        """
        if self._active:
            raise ValueError(
                f"{self.__class__.__name__} instances are not thread-safe,"
                " concurrent execution on the same instance is not supported."
            )
        #
        self._active = True
        self._store_and_reset_segment()
        self._collected_segments.clear()
        pos = 0
        path_source_length = len(path_source)
        while pos < path_source_length:
            character = path_source[pos]
            if character == self.separator:
                self._store_and_reset_segment()
                pos += 1
                continue
            #
            if self._expect_segment_end:
                raise ValueError(
                    f"Expected segment end but read character {character!r}."
                    f" Collected segments so far: {self._collected_segments!r}"
                )
            #
            fast_forward = self._check_for_fast_forward(path_source, pos)
            if fast_forward:
                pos += fast_forward
            else:
                self._current_segment_sources.append(character)
                pos += 1
            #
        #
        self._store_and_reset_segment()
        found_segments = tuple(self._collected_segments)
        self._collected_segments.clear()
        self._active = False
        return Address(*found_segments)


class ParsingCache(OneCharSeparated):
    """Can build a tuple of segments from a string"""

    def __init__(self, separator: str = DOT) -> None:
        """Initialization argument:
        * separator - a single character used to separate path segments
        """
        super().__init__(separator=separator)
        self.__cache: dict[str, Address] = {}
        self.stats: Counter[str] = Counter()
        self.__lock = Lock()

    def __getitem__(self, pathspec: IndexType) -> Address:
        """Return an item from the cache if the pathspec is a string"""
        if isinstance(pathspec, str):
            return self.get_cached(pathspec)
        #
        self.stats.update(bypass=1)
        return Address(*pathspec)

    def get_cached(self, path_source: str) -> Address:
        """Return an item from the cache"""
        if not path_source:
            self.stats.update(bypass=1)
            return Address()
        #
        with self.__lock:
            stat_entries = []
            try:
                cached_address = self.__cache[path_source]
            except KeyError:
                parser = SegmentsParser(separator=self.separator)
                cached_address = self.__cache.setdefault(
                    path_source, parser.split_into_segments(path_source)
                )
                stat_entries.append("miss")
            else:
                stat_entries.append("hit")
            #
            self.stats.update(stat_entries)
            return cached_address
        #

    def canonical(self, source_address: Address) -> str:
        """Return the canonical source for the given segments tuple"""
        output: list[str] = []
        for item in source_address.segments:
            item_dump = dumps(item)
            if isinstance(item, str) and not any(
                char in item for char in (self.separator, DOUBLE_QUOTE, "[")
            ):
                item_dump = str(item)
            elif isinstance(item, (int, float)):
                # Number representations might contain the separator character
                if self.separator in item_dump:
                    item_dump = f"[{item_dump}]"
                #
            #
            output.append(item_dump)
        #
        reconstructed_key = self.separator.join(output)
        with self.__lock:
            cached_address = self.__cache.setdefault(reconstructed_key, source_address)
        #
        if cached_address != source_address:
            # should never occur, but added as consistency check
            raise ValueError("Unexpected: canonical representation mismatch")
        #
        return reconstructed_key


class CacheOfCaches(Mapping):
    """A cache of ParsingCache instances"""

    def __init__(self) -> None:
        """Initialize the internal cache"""
        self.__dot_cache = ParsingCache(separator=DOT)
        self.__other_caches: dict[str, ParsingCache] = {}

    def __getitem__(self, name: str) -> ParsingCache:
        """Return the matching ParsingCache, or create a new one"""
        if name == DOT:
            return self.__dot_cache
        #
        try:
            return self.__other_caches[name]
        except KeyError:
            return self.__other_caches.setdefault(name, ParsingCache(separator=name))
        #

    def __iter__(self):
        """Iterate over the keys"""
        yield DOT
        yield from self.__other_caches
        # keys = [DOT] + list(self.__other_caches)
        # return iter(keys)

    def __len__(self) -> int:
        """Number of stored caches"""
        return len(self.__other_caches) + 1


SINGLETON_CACHES = CacheOfCaches()


# vim: fileencoding=utf-8 ts=4 sts=4 sw=4 autoindent expandtab syntax=python:
