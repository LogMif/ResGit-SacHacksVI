from pathlib import Path
from tkinter import filedialog
import os
import subprocess
import platform

import tkinter_backend as backend

def _file_selector(filetype: str) -> Path:
        """opens file selector dialogue and returns the filepath. possible filetypes: '*txt', '*pdf' """
        file_path = filedialog.askopenfilename(
            title = "Select a resume pdf",
            filetypes=[("PDF files", filetype)]
        )
        return Path(file_path)
    
def _display_file(filepath: Path) -> None:
    """displays a file"""
    if platform.system() == "Windows":
        os.startfile(filepath)
    elif platform.system() == "Darwin":  # macOS
        subprocess.call(["open", filepath])
    else:  # Linux
        subprocess.call(["xdg-open", filepath])