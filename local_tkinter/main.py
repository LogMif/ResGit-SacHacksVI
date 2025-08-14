import sys
import os
original_dir = os.getcwd() 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend/modules')))
from history_class import history
os.chdir(original_dir)

import tkinter as tk
import screen_class
from history_display_class import History_display
from selected_histories import Select_histories
import tkinter_backend as backend

def _login_button_action(history_display_frame: History_display, selected_history_frame: Select_histories, username: tk.StringVar, password: tk.StringVar) -> None:
    """function that executes what needs to be done with login is done"""
    history_display_frame.populate_text(username, password)

    #this would need to be changed to init with empty object which will be populated when other button pressed
    history_obj = history(backend.get_user_history(username.get(), password.get()))
    selected_history_frame.add_text(history_obj)

def _add_screen_and_frames() -> tuple[screen_class.Screen, History_display, Select_histories, tk.StringVar, tk.StringVar, tk.Frame, tk.Frame]:
    """initalizes screens and frames needed for future actions"""

    screen = screen_class.Screen("ResGit")

    screen.add_name_label(row=0, col=0)
    username = screen.add_user_input(row=0, col=1)

    screen.add_password_label(row=0, col=2)
    password = screen.add_user_input(row=0, col=3, show="*")

    left_frame = screen.add_frame(row=1, col=0, colspan=3, width=400, height=300)
    screen_class.Screen.make_frame_stretchable(left_frame)

    right_frame = screen.add_frame(row=1, col=3, colspan=3, width=300, height=300)
    screen_class.Screen.make_frame_stretchable(right_frame)


    history_display_frame = History_display(left_frame, 400, 300)
    
    selected_history_frame = Select_histories(right_frame, 300, 300)

    return screen, history_display_frame, selected_history_frame, username, password, left_frame, right_frame

def _add_standard_buttons(screen: screen_class.Screen, history_display_frame: History_display, selected_history_frame: Select_histories, 
                          username: tk.StringVar, password: tk.StringVar, left_frame: tk.Frame, right_frame: tk.Frame) -> None:
    ogin_button = screen.add_button(_login_button_action, history_display_frame, selected_history_frame, username, password, 
                                     row=0, col=4, parent=screen._screen)
    
    create_button = screen.add_button(screen.create_user, username, password, row=0, col=5, parent=screen._screen, text="Create User")

    import_resume_button = screen.add_button(screen.import_resume, username, password, history_display_frame, row=3, col=0, parent=left_frame, sticky="nsew", text="Import Resume")

    create_resume_button = screen.add_button(screen.generate_resume, username, password, row=3, col=0, parent=right_frame, sticky="nsew", text="Create Resume")

def main() -> None:
    screen_components = _add_screen_and_frames()
    screen = screen_components[0]

    _add_standard_buttons(*screen_components)
    
    screen.mainloop()

if __name__ == "__main__":
    try:
        main()
    finally:
        tk.Tk().destroy()