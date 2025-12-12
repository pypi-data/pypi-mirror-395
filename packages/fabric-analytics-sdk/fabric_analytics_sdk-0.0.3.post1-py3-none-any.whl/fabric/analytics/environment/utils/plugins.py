import importlib.metadata
import sys
from typing import no_type_check


@no_type_check
def _get_entry_points(group: str):
    if sys.version_info >= (3, 10):
        return importlib.metadata.entry_points(group=group)

    entrypoints = importlib.metadata.entry_points()
    try:
        return entrypoints.get(group, [])
    except AttributeError:
        return entrypoints.select(group=group)


@no_type_check
def get_entry_points(group: str):
    return _get_entry_points(group)
