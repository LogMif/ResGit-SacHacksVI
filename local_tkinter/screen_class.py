import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

from pathlib import Path

import tkinter_backend as backend
from api_call_wrapper import backend_caller
from history_interactor import HistoryInteractor

import os
import subprocess
import platform

class Screen:
    def __init__(self, screen_name: str):
        self._screen = tk.Tk()
        self._screen.title(screen_name)
        self._loaded_histories = None
        self.set_screen_size(int(self._screen.winfo_screenwidth()/2), int(self._screen.winfo_screenheight()/2))

    def set_screen_size(self, width: int, height: int) -> None:
        """sets screen size"""
        self._screen.geometry(f"{width}x{height}")


    def _add_label(self, row, col, text: str, side: str, anchor: str, padx: tuple[int, int] = (0,0)) -> None:
        """adds label to screen"""
        label = ttk.Label(self._screen, text=text)
        label.grid(row=row, column=col, padx=10, pady=5, sticky="w")

    def _add_input(self, row, col, width: int, stringvar: tk.StringVar, side: str, anchor: str, show, padx: tuple[int, int] = (0, 0)) -> None:
        """adds input to screen"""
        entry = ttk.Entry(self._screen, width=width, textvariable=stringvar, show=show)
        entry.grid(row=row, column=col, padx=10, pady=5, sticky="w")

    def _add_button(self, parent, row, col, text: str, command, side: str, anchor: str, sticky: str = "w", padx: tuple[int, int] = (0, 0)) -> None:
        """Adds a button to the screen with specified text and command."""
        button = ttk.Button(parent, text=text, command=command)
        button.grid(row=row, column=col, padx=10, pady=5, sticky=sticky)

    def add_text(self, parent, row: int, col: int, width: int = 40, height: int = 5, sticky: str = "w", padx: tuple[int, int] = (0, 0)) -> tk.Text:
        """Adds a multi-line Text widget and returns it so you can insert/update text."""
        text_widget = tk.Text(parent, width=width, height=height)
        text_widget.grid(row=row, column=col, padx=padx, pady=5, sticky=sticky)
        return text_widget


    def add_frame(self, *args, row, col, colspan, width, height) -> tk.Frame:
        """adds a tkinter frame to the screen"""
        panel = tk.Frame(self._screen, width=width, height=height, bg="lightgray")

        panel.grid(row=row, column=col, columnspan=colspan, padx=10, pady=5, sticky="w")
        panel.grid_propagate(False)
        return panel


    def add_name_label(self, row, col) -> None:
        """adds label for username input"""
        self._add_label(row, col, "Username: ", "left", "nw", (0, 10))

    def add_password_label(self, row, col) -> None:
        """adds label for password"""
        self._add_label(row, col, "Password: ", "left", "nw", (0, 10))

    def add_user_input(self, row, col, show: str = "") -> tk.StringVar:
            """adds input for the username"""
            var = tk.StringVar()
            self._add_input(row, col, width = 15, stringvar=var, side = "left", anchor="nw", show=show)
            return var

    def add_button(self, function, *args, parent, row, col, text: str = "Login", sticky: str = "w",) -> None:
        """adds a button to create a user"""
        btn = self._add_button(parent, row, col, text, lambda: function(*args), side="left", anchor="nw", sticky=sticky, padx=(10, 0))

    @backend_caller
    def create_user(self, username: tk.StringVar, password: tk.StringVar) -> None:
        """function that creates user"""
        backend.create_user(username.get(), password.get())

    @backend_caller
    def populate_text(self, text_field: tk.Text, username: tk.StringVar, password: tk.StringVar) -> None:
        """function that populates a textbox based on user history"""
        text_field.delete("1.0", "end") 
        user_history_dict = backend.get_user_history(username.get(), password.get())
        self._loaded_histories = HistoryInteractor(user_history_dict)
        for record in self._loaded_histories.iter_histories():
            text_field.insert("end", record.nested_layer * '  ' + record.arc_index + ': ' + str(record.arc_contents) + '\n')

    @backend_caller
    def import_resume(self, username: tk.StringVar, password: tk.StringVar, text_field: tk.Text) -> None:
        """function that imports resume then updates textbox"""
        resume_filepath = _file_selector('*pdf')
        backend.import_user_history(username.get(), password.get(), resume_filepath)
        self.populate_text(text_field, username, password)

    @backend_caller
    def generate_resume(self, username: tk.StringVar, password: tk.StringVar) -> Path:
        """function the generates resume and displays that resume"""
        generated_resume_path = backend.generate_resume(username.get(), password.get(), self._loaded_histories.selected_history())
        _display_file(generated_resume_path)


    
    def mainloop(self) -> None:
        """runs the screen mainloop"""
        self._screen.mainloop()

def _file_selector(filetype: str) -> Path:
        """opens file selector dialogue and returns the filepath. possible filetypes: '*txt', '*pdf' """
        file_path = filedialog.askopenfilename(
            title = "Select a resume pdf",
            filetypes=[("PDF files", filetype)]
        )
        return Path(file_path)
    
def _display_file(filepath: Path) -> None:
    """displays a file"""
    if platform.system() == "Windows":
        os.startfile(filepath)
    elif platform.system() == "Darwin":  # macOS
        subprocess.call(["open", filepath])
    else:  # Linux
        subprocess.call(["xdg-open", filepath])
