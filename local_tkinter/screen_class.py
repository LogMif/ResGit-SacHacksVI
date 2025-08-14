import tkinter as tk
from tkinter import ttk
import screeninfo

from pathlib import Path

import tkinter_backend as backend
from api_call_wrapper import backend_caller
from history_interactor import HistoryInteractor

from local_file_io import _file_selector, _display_file

class Frame:
    def __init__(self, parent):
        self._screen = parent

    def _add_label(self, row, col, text: str, side: str, anchor: str, padx: tuple[int, int] = (0,0)) -> None:
        """adds label to screen"""
        label = ttk.Label(self._screen, text=text)
        label.grid(row=row, column=col, padx=10, pady=5, sticky="w")

    def _add_input(self, row, col, width: int, stringvar: tk.StringVar, side: str, anchor: str, show, padx: tuple[int, int] = (0, 0)) -> None:
        """adds input to screen"""
        entry = ttk.Entry(self._screen, width=width, textvariable=stringvar, show=show)
        entry.grid(row=row, column=col, padx=10, pady=5, sticky="w")

    def _add_button(self, parent, row, col, text: str, command, side: str, anchor: str, sticky: str = "w", padx: tuple[int, int] = (10, 10)) -> None:
        """Adds a button to the screen with specified text and command."""
        button = ttk.Button(parent, text=text, command=command)
        button.grid(row=row, column=col, padx=padx, pady=5, sticky=sticky)



class Canvas:
    def __init__(self, canvas, parent, inner_frame):
        self.canvas = canvas

        self.scrollbar = tk.Scrollbar(parent, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)        

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.inner_frame = inner_frame
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")
        self.inner_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.inner_frame.bind("<Enter>", self._bind_mousewheel)
        self.inner_frame.bind("<Leave>", self._unbind_mousewheel)

    def _bind_mousewheel(self, event):
        # Windows and macOS
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        # Linux (optional, for completeness)
        self.canvas.bind_all("<Button-4>", self._on_mousewheel_linux)
        self.canvas.bind_all("<Button-5>", self._on_mousewheel_linux)

    def _unbind_mousewheel(self, event):
        self.canvas.unbind_all("<MouseWheel>")
        self.canvas.unbind_all("<Button-4>")
        self.canvas.unbind_all("<Button-5>")

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _on_mousewheel_linux(self, event):
        if event.num == 4:
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            self.canvas.yview_scroll(1, "units")



class Screen(Frame):
    def __init__(self, screen_name: str, parent: tk.Tk = tk.Tk()):
        super().__init__(parent)
        self._screen.title(screen_name)
        self._loaded_histories = None

        self.set_screen_size(int(self._screen.winfo_screenwidth()/2), int(self._screen.winfo_screenheight()/2))

    def set_screen_size(self, width: int, height: int) -> None:
        """sets screen size"""
        monitors = screeninfo.get_monitors()
        default_monitor = monitors[0]

        width = int(default_monitor.width/2)
        height = int(default_monitor.height/2)
        self._screen.geometry(f"{width}x{height}")


    def add_frame(self, *args, row, col, colspan, width, height) -> tk.Frame:
        """adds a tkinter frame to the screen"""
        panel = tk.Frame(self._screen, width=width, height=height, bg="lightgray")

        panel.grid(row=row, column=col, columnspan=colspan, padx=10, pady=5, sticky="w")
        panel.grid_propagate(False)

        # if strechable:
        #     self.make_frame_stretchable(panel)

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

    @staticmethod
    def make_frame_stretchable(frame_obj: tk.Frame):
        frame_obj.rowconfigure(0, weight=1)  # Make row 0 (text box) expandable
        frame_obj.columnconfigure(0, weight=1)
    
    def mainloop(self) -> None:
        """runs the screen mainloop"""
        self._screen.mainloop()


