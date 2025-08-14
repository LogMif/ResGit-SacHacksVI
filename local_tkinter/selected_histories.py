
import sys
import os
original_dir = os.getcwd() 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend/modules')))
from history_class import history
os.chdir(original_dir)

import tkinter as tk
import screen_class


class Select_histories(screen_class.Frame):
    def __init__(self, parent: tk.Frame, width: int, height: int):
        temp_canvas = tk.Canvas(parent, width=width, height=height)
        self.inner_frame = tk.Frame(temp_canvas)
        self.canvas = screen_class.Canvas(temp_canvas, parent, self.inner_frame)

        super().__init__(self.inner_frame)

        self._num_selected_records = 0

    def _record_unselect(self):
        pass

    def add_text(self, selected_histories: history, padx: tuple[int, int] = (0, 0)) -> None:
        """Adds buttons for each experience in selected_histories"""
        for record, padding in selected_histories:
            self._add_button(self._screen, self._num_selected_records, 0, 
                             record, self._record_unselect, side="left", 
                             anchor="nw", sticky="w", padx=padding)
            self._num_selected_records += 1
        
    

