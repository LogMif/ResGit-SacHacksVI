import tkinter as tk
from tkinter import ttk

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

    def _add_input(self, width: int, stringvar: tk.StringVar, side: str, anchor: str, padx: tuple[int, int] = (0, 0)) -> None:
        """adds input to screen"""
        entry = ttk.Entry(self._screen, width=width, textvariable=stringvar)
        entry.pack(side=side, anchor = anchor)


    def add_name_label(self) -> None:
        """adds label for username input"""
        self._add_label("Username: ", "left", "nw", (0, 10))

    def add_name_input(self) -> tk.StringVar:
        """adds input for the username"""
        user_name = tk.StringVar()
        self._add_input(width = 15, stringvar=user_name, side = "left", anchor="nw")
        return user_name
    
    def add_password_label(self) -> None:
        """adds lavel for password"""
        self._add_label("Password: ", "left", "nw", (0, 10))


    
    def mainloop(self) -> None:
        """runs the screen mainloop"""
        self._screen.mainloop()

def main() -> None:
    screen = Screen("ResGit")

    screen.add_name_label()
    username = screen.add_name_input()

    screen.add_password_label()


    
    screen.mainloop()

if __name__ == "__main__":
    main()