import tkinter as tk
import screen_class
from api_call_wrapper import backend_caller
from history_interactor import HistoryInteractor

import tkinter_backend as backend



class History_display(screen_class.Frame):
    
    def __init__(self, parent: tk.Frame, width=50, height=10) -> None:
        """class for the purpose of rendering selected histories"""

        temp_canvas = tk.Canvas(parent, width=width, height=height)
        self.inner_frame = tk.Frame(temp_canvas)
        self.canvas = screen_class.Canvas(temp_canvas, parent, self.inner_frame)

        super().__init__(self.inner_frame)

        self._num_records = 0


    def _record_select(self) -> None:
        """function that activates when record selected"""

    @backend_caller #to change this
    def populate_text(self, username: tk.StringVar, password: tk.StringVar) -> None:
        """function that populates a left scroll area based on user history"""

        user_history_dict = backend.get_user_history(username.get(), password.get())
        self._loaded_histories = HistoryInteractor(user_history_dict)
        for record in self._loaded_histories.iter_histories():
            display_str = record.nested_layer * '  ' + record.arc_index + ': ' + str(record.arc_contents)
            self._add_button(self._screen, self._num_records, 0, display_str, self._record_select, side="left", anchor="nw", sticky="w", padx=(0, 0))
            self._num_records += 1

