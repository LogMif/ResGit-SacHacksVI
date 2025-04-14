import tkinter as tk
from tkinter import ttk
import tkinter_backend as backend
import screen_class

def main() -> None:
    screen = screen_class.Screen("ResGit")

    screen.add_name_label(row=0, col=0)
    username = screen.add_user_input(row=0, col=1)

    screen.add_password_label(row=0, col=2)
    password = screen.add_user_input(row=0, col=3, show="*")

    left_frame = screen.add_frame()

    output_box = screen.add_text(left_frame, row=2, col=0, width=50, height=6)

    login_button = screen.add_button(screen._populate_text, output_box, username, password, row=0, col=4)
    create_button = screen.add_button(screen._create_user, username, password, row=0, col=5, text="Create User")

    import_resume_button = screen.add_button(screen._create_user, username, password, row=2, col=2, text="Import Resume")




    screen.mainloop()

if __name__ == "__main__":
    main()