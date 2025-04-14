import tkinter as tk
from tkinter import ttk
import tkinter_backend as backend

class Screen:
    def __init__(self, screen_name: str):
        self._screen = tk.Tk()
        self._screen.title(screen_name)
        self.set_screen_size(int(self._screen.winfo_screenwidth()/2), int(self._screen.winfo_screenheight()/2))

    def set_screen_size(self, width: int, height: int) -> None:
        """sets screen size"""
        self._screen.geometry(f"{width}x{height}")
        

    def _add_label(self, text: str, side: str, anchor: str, padx: tuple[int, int] = (0,0)) -> None:
        """adds label to screen"""
        label = ttk.Label(self._screen, text=text)
        label.pack(side = side, anchor=anchor, padx=padx)

    def _add_input(self, width: int, stringvar: tk.StringVar, side: str, anchor: str, show, padx: tuple[int, int] = (0, 0)) -> None:
        """adds input to screen"""
        entry = ttk.Entry(self._screen, width=width, textvariable=stringvar, show=show)
        entry.pack(side=side, anchor = anchor)

    def _add_button(self, text: str, command, side: str, anchor: str, padx: tuple[int, int] = (0, 0)) -> None:
        """Adds a button to the screen with specified text and command."""
        button = ttk.Button(self._screen, text=text, command=command)
        button.pack(side=side, anchor=anchor, padx=padx)

    def add_name_label(self) -> None:
        """adds label for username input"""
        self._add_label("Username: ", "left", "nw", (0, 10))
    
    def add_password_label(self) -> None:
        """adds label for password"""
        self._add_label("Password: ", "left", "nw", (0, 10))

    def add_user_input(self, show: str = "") -> tk.StringVar:
            """adds input for the username"""
            var = tk.StringVar()
            self._add_input(width = 15, stringvar=var, side = "left", anchor="nw", show=show)
            return var

    def add_login_button(self, username: tk.StringVar, password: tk.StringVar):
        btn = self._add_button("Submit", lambda: backend.create_user(username, password), side="left", anchor="nw", padx=(10, 0))



    def print_input(self, username: tk.StringVar, password: tk.StringVar) -> None:
        print("Username: ", username.get())
        print("Password: ", password.get())

    
    def mainloop(self) -> None:
        """runs the screen mainloop"""
        self._screen.mainloop()

def main() -> None:
    screen = Screen("ResGit")

    screen.add_name_label()
    username = screen.add_user_input()

    screen.add_password_label()
    password = screen.add_user_input(show="*")

    button = screen.add_login_button(username, password)


    
    screen.mainloop()

if __name__ == "__main__":
    main()