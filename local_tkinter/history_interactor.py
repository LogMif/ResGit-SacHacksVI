# import sys
# import os

# original_dir = os.getcwd() 
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend/modules')))
# import history_class
# os.chdir(original_dir)

from typing import Iterator

class HistoryInteractor:
    def __init__(self, all_history: dict):
        self._history = all_history

    def iter_histories(self) -> Iterator[tuple[str, str|dict]]:
        for arc_index, arc in self._history.items():
            yield arc_index, arc