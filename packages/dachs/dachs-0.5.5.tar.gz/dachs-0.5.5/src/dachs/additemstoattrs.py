#!/usr/bin/env python
# coding: utf-8

"""
An add=on that will add an items() method to an attrs-created dataclass.
Useful for iterating over keys, for example for storing in an HDF5 file.
"""

__author__ = "Brian R. Pauw"
__contact__ = "brian@stack.nl"
__license__ = "GPLv3+"
__date__ = "2022/11/07"
__status__ = "beta"

from collections.abc import Iterable
from typing import Any, NoReturn

from attrs import fields

# Mixin class for making a dict-like object out of an attrs class
# from: https://github.com/python-attrs/attrs/issues/879


class addItemsToAttrs:  # used to be MutableMappingMixin(MutableMapping)
    """Mixin class to make attrs classes quack like a dictionary (well,
    technically a mutable mapping). ONLY use this with attrs classes.

    Provides keys(), values(), and items() methods in order to be
    dict-like in addition to MutableMapping-like. Also provides pop(),
    but it just raises a TypeError :)
    """

    __slots__ = ()  # May as well save on memory?
    _storeKeys = list()
    _loadKeys = list()

    def __iter__(self) -> Iterable:
        for ifield in fields(self.__class__):
            yield ifield.name

    def __len__(self) -> int:
        return len(fields(self.__class__))

    def __getitem__(self, k: str) -> Any:
        """
        Adapted from:
        https://github.com/python-attrs/attrs/issues/487#issuecomment-660727537
        """
        try:
            return self.__getattribute__(k)
        except AttributeError as exc:
            raise KeyError(str(exc)) from None

    def __delitem__(self, v: str) -> NoReturn:
        raise TypeError("Cannot delete fields for attrs classes.")

    def __setitem__(self, k: str, v: Any) -> None:
        self.__setattr__(k, v)

    def pop(self, key, default=None) -> NoReturn:
        raise TypeError("Cannot pop fields from attrs classes.")

    def keys(self) -> Iterable:
        return self.__iter__()

    def values(self) -> Iterable:
        for key in self.__iter__():
            yield self.__getattribute__(key)

    def items(self) -> Iterable:
        for key in self.__iter__():
            yield key, self.__getattribute__(key)

    def __attrs_post_init__(self):
        # auto-generate the store and load key lists:
        self._storeKeys = [i for i in self.keys() if (i not in self._excludeKeys and not i.startswith("_"))]
        self._loadKeys = [i for i in self.keys() if (i not in self._excludeKeys and not i.startswith("_"))]
