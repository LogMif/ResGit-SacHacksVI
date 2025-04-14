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
        

    def _add_label(self, row, col, text: str, side: str, anchor: str, padx: tuple[int, int] = (0,0)) -> None:
        """adds label to screen"""
        label = ttk.Label(self._screen, text=text)
        label.grid(row=row, column=col, padx=10, pady=5, sticky="w")

    def _add_input(self, row, col, width: int, stringvar: tk.StringVar, side: str, anchor: str, show, padx: tuple[int, int] = (0, 0)) -> None:
        """adds input to screen"""
        entry = ttk.Entry(self._screen, width=width, textvariable=stringvar, show=show)
        entry.grid(row=row, column=col, padx=10, pady=5, sticky="w")

    def _add_button(self, row, col, text: str, command, side: str, anchor: str, padx: tuple[int, int] = (0, 0)) -> None:
        """Adds a button to the screen with specified text and command."""
        button = ttk.Button(self._screen, text=text, command=command)
        button.grid(row=row, column=col, padx=10, pady=5, sticky="w")

    def add_frame(self):
        screen_width = self._screen.winfo_screenwidth()
        half_width = screen_width // 2
        left_panel = tk.Frame(self._screen, width=half_width, height=300, bg="lightgray")

        left_panel.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="w")


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

    def add_login_button(self, username: tk.StringVar, password: tk.StringVar, row, col) -> None:
        """adds a button to create a user"""
        btn = self._add_button(row, col, "Create User", lambda: backend.create_user(username.get(), password.get()), side="left", anchor="nw", padx=(10, 0))



    def print_input(self, username: tk.StringVar, password: tk.StringVar) -> None:
        print("Username: ", username.get())
        print("Password: ", password.get())

    
    def mainloop(self) -> None:
        """runs the screen mainloop"""
        self._screen.mainloop()

def main() -> None:
    screen = Screen("ResGit")

    screen.add_name_label(row=0, col=0)
    username = screen.add_user_input(row=0, col=1)

    screen.add_password_label(row=0, col=2)
    password = screen.add_user_input(row=0, col=3, show="*")

    button = screen.add_login_button(username, password, row=0, col=4)
    screen.add_frame()

    
    screen.mainloop()

if __name__ == "__main__":
    main()