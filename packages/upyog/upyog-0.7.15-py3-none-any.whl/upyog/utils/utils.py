import math
import uuid
from itertools import islice
from typing import Any, Collection, Iterable, List, Tuple, Union

import numpy as np


__all__ = [
    "flatten",
    "uniqueify",
    "chunk",
    "notnone",
    "lmap",
    "allequal",
    "zipsafe",
    "convert_size",
    "convert_to_tuple",
    "convert_to_list",
    "is_collection",
]


def flatten(x: Any) -> List[Any]:
    flattened_list = []
    for item in x:
        if hasattr(item, "__iter__") and not isinstance(item, (str, bytes)):
            [flattened_list.append(i) for i in item]
        else:
            flattened_list.append(item)
    return flattened_list


def convert_to_list(x: Union[str, Iterable[str]]):
    # fmt: off
    if   isinstance(x, list):       return x
    elif isinstance(x, np.ndarray): return x.tolist()
    elif isinstance(x, tuple):      return list(x)
    elif isinstance(x, str):        return [x]
    else: raise TypeError(f"Expected {str}, got {type(x)}")
    # fmt: on


def convert_to_tuple(x: Union[str, Iterable[str]]) -> Tuple[str]:
    # fmt: off
    if   isinstance(x, list):              return tuple(x)
    elif isinstance(x, np.ndarray):        return tuple(x)
    elif isinstance(x, tuple):             return x
    elif isinstance(x, (str, int, float)): return x,
    else: raise TypeError(f"Expected {{str|int|float|list|np.ndarray|tuple}}, got {type(x)}")
    # fmt: on


def uniqueify(x: Collection) -> Collection:
    return sorted(list(set(x)))


def sort_dict_by_keys(x) -> dict:
    return dict(sorted(x.items()))


def get_uuid(n=10) -> str:
    return uuid.uuid4().hex[:n].lower()


# Borrowed from https://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks
def chunk(items: Collection[Any], size: int, strict=True) -> list:
    if strict:
        assert len(items) % size == 0

    items = iter(items)
    return list(iter(lambda: tuple(islice(items, size)), ()))


# Borrowed from icevision.utils
def notnone(x):
    return x is not None


def lmap(f, xs):
    return list(map(f, xs)) if notnone(xs) else None


def allequal(l):
    return l.count(l[0]) == len(l) if l else True


def zipsafe(*its):
    if not allequal(lmap(len, its)):
        raise ValueError("The elements have different leghts")
    return zip(*its)


# https://stackoverflow.com/questions/5194057/better-way-to-convert-file-sizes-in-python
def convert_size(size_bytes: int) -> str:
    "Convert bytes into appropriate unit and return a human readable string for file size"
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])


def is_collection(x):
    from collections.abc import Iterable

    return isinstance(x, Iterable) and not isinstance(x, (str, bytes))
