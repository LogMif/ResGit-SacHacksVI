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
    # This should prob be in the add_frame function
    left_frame.rowconfigure(0, weight=1)  # Make row 0 (text box) expandable
    left_frame.columnconfigure(0, weight=1)  # Allow stretching horizontally


    right_frame = screen.add_frame(row=1, col=3, colspan=3, width=300, height=300)
    right_frame.rowconfigure(0, weight=1)  # Make row 0 (text box) expandable
    right_frame.columnconfigure(0, weight=1)  # Allow stretching horizontally

    output_box = screen.add_text(left_frame, row=0, col=0, width=50, height=10, sticky="nsew")
    output_box_right = screen.add_text(right_frame, row=0, col=0, width=50, height=10, sticky="nsew")


    login_button = screen.add_button(screen.populate_text, output_box, username, password, row=0, col=4, parent=screen._screen)
    create_button = screen.add_button(screen.create_user, username, password, row=0, col=5, parent=screen._screen, text="Create User")

    import_resume_button = screen.add_button(screen.import_resume, username, password, output_box, row=3, col=0, parent=left_frame, sticky="nsew", text="Import Resume")

    create_resume_button = screen.add_button(screen.generate_resume, username, password, row=3, col=0, parent=right_frame, sticky="nsew", text="Create Resume")




    screen.mainloop()

if __name__ == "__main__":
    main()