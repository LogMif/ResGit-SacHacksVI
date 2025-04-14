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

    left_frame = screen.add_frame(row=1, col=0, colspan=3, width=400, height=300)

    right_frame = screen.add_frame(row=1, col=3, colspan=3, width=300, height=300)

    output_box = screen.add_text(left_frame, row=2, col=0, width=50, height=6)

    login_button = screen.add_button(screen.populate_text, output_box, username, password, row=0, col=4, parent=screen._screen)
    create_button = screen.add_button(screen.create_user, username, password, row=0, col=5, parent=screen._screen, text="Create User")

    import_resume_button = screen.add_button(screen.create_user, username, password, row=2, col=2, parent=screen._screen, text="Import Resume")




    screen.mainloop()

if __name__ == "__main__":
    main()