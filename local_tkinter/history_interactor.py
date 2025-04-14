# import sys
# import os

# original_dir = os.getcwd() 
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend/modules')))
# import history_class
# os.chdir(original_dir)

from typing import Iterator, Generator
from dataclasses import dataclass


@dataclass
class OneRecord:
    arc_index: str
    arc_contents: str
    nested_layer: int


class HistoryInteractor:
    def __init__(self, all_history: dict):
        self._history = all_history
        self._selected_history = dict()

    def iter_histories(self) -> Iterator[tuple[str, str|dict]]:
        """iterates dictionary and returns OneRecord object"""
        for arc_index, arc, nested_layer in _recurse_dict(self._history):
            yield OneRecord(arc_index=arc_index, arc_contents=arc, nested_layer=nested_layer)

    def selected_history(self) -> dict:
        """returns selected items"""
        return self._history #temporary for testing
            

def _recurse_dict(input_dict: dict, nested_layer = 0) -> Iterator[tuple[str, str, int]]:
    """go through dict recursively"""
    for key, value in input_dict.items():
        # print("value: ", type(value), value)
        if type(value) != dict:\
        
            yield str(key), str(value), nested_layer
        else:
            yield key, " ", nested_layer
            yield from _recurse_dict(value, nested_layer + 1)
