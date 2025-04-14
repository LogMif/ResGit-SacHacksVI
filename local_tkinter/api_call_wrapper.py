import tkinter.messagebox as msgbox
import traceback

def backend_caller(func):
    def decorator(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except Exception as e:
            msgbox.showerror("Error", e)
            print(traceback.format_exc())

    return decorator