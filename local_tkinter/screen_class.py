import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

from pathlib import Path

import tkinter_backend as backend
import api_call_wrapper

class Screen:
    def __init__(self, screen_name: str):
        self._screen = tk.Tk()
        self._screen.title(screen_name)
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


    def add_frame(self, *args, row, col, colspan, width, height):
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

    @api_call_wrapper.backend_caller
    def create_user(self, username, password) -> None:
        backend.create_user(username.get(), password.get())

    @api_call_wrapper.backend_caller
    def populate_text(self, text_field, username: tk.StringVar, password: tk.StringVar) -> None:
#         backend.create_user(username.get(), password.get()
          text_field.insert("end", backend.get_user_history(username.get(), password.get()))

    def import_resume(self, username: tk.StringVar, password: tk.StringVar) -> None:
        resume_filepath = _file_selector('*pdf')
        with open(resume_filepath, 'rb') as file:
            resume_binary = file.read()
        
        backend.add_user_history(username.get(), password.get(), resume_binary)

    
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
    