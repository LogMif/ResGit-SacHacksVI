
import sys
import os

original_dir = os.getcwd() 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))
import resgit_api as rgapi
os.chdir(original_dir)

from typing import Callable
import time
from pathlib import Path
import base64

def _get_local_data_storage_directory() -> str:
    return "local_tkinter_data"

def _get_curr_time() -> int:
    return int(time.time())

def _invoke_api(function: Callable, kwargs: dict) -> any:
    """invokes api function my modifies data_storage parameter"""
    kwargs["data_storage"] = 'local'
    kwargs["bucket"] = _get_local_data_storage_directory()
    return function(**kwargs)

def create_user(username: str, password: str) -> None:
    """creates user. throws 'UserAlreadyExistsError' error if username already exists"""
    print("attempting to create user: ", username, "\npassword: ", password)
    _invoke_api(rgapi.add_user, {"username": username, "password": password})

def get_user_history(username: str, password: str) -> dict:
    """gets all the user history as a dict"""
    history_dict = _invoke_api(rgapi.get_user_history, {"username": username, "password": password})
    return history_dict["history"]

def import_user_history(username: str, password: str, pdf_filename: Path) -> None:
    """updates user history based on pdf file passed in as bytes/binary"""
    with open(pdf_filename, 'rb') as file:
        resume_binary = file.read()
    _invoke_api(rgapi.add_user_history, {"pdf_binary": resume_binary, "username": username, "password": password})


def generate_resume(username: str, password: str, selected_history: dict) -> Path:
    """generates resume and returns the resume filename"""
    resume_name = 'resume'+ str(_get_curr_time()) + '.pdf'
    binary_resume = _invoke_api(rgapi.generate_resume, {"selected_history": selected_history, "username": username, "password": password, "resume_name": resume_name})["resume"]
    resume_path = Path(_get_local_data_storage_directory() + '/' + resume_name)

    pdf_bytes = base64.b64decode(binary_resume)
    with open(resume_path, 'wb') as file:
        file.write(pdf_bytes)

    return resume_path