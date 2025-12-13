# -*- coding: utf-8 -*-

"""
simple nested collections wrapper
"""

# pylint: disable=useless-import-alias ; re-import for public interface as
# suggested in <https://docs.astral.sh/ruff/rules/unused-import/#why-is-this-bad>

from .wrappers import (
    BaseStructure as BaseStructure,
    FrozenStructure as FrozenStructure,
    MutableStructure as MutableStructure,
)

from .commons import (
    assured_collection as assured_collection,
    assured_dict as assured_dict,
    assured_float as assured_float,
    assured_int as assured_int,
    assured_iterable as assured_iterable,
    assured_list as assured_list,
    assured_number as assured_number,
    assured_scalar as assured_scalar,
    assured_str as assured_str,
    to_text as to_text,
)


# vim: fileencoding=utf-8 ts=4 sts=4 sw=4 autoindent expandtab syntax=python:
