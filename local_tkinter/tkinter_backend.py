
import sys
import os

original_dir = os.getcwd() 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))
import resgit_api as rgapi
os.chdir(original_dir)

from typing import Callable


def _get_local_data_storage_directory() -> str:
    return "local_tkinter_data"

def _invoke_api(function: Callable, kwargs: dict) -> any:
    """invokes api function my modifies data_storage parameter"""
    kwargs["data_storage"] = 'local'
    return function(**kwargs)

def create_user(username: str, password: str) -> None:
    """creates user. throws 'UserAlreadyExistsError' error if username already exists"""
    print("attempting to create user: ", username, "\npassword: ", password)
    directory = _get_local_data_storage_directory()
    _invoke_api(rgapi.add_user, {"bucket": directory, "username": username, "password": password})

def get_user_history(username: str, password: str) -> dict:
    """gets all the user history as a dict"""
    directory = _get_local_data_storage_directory()
    return _invoke_api(rgapi.get_user_history, {"bucket": directory, "username": username, "password": password})
    
def add_user_history(username: str, password: str, pdf_binary: bytes) -> None:
    """updates user history based on pdf file passed in as bytes/binary"""
    directory = _get_local_data_storage_directory()
    _invoke_api(rgapi.add_user_history, {"bucket": directory, "pdf_binary": pdf_binary, "username": username, "password": password})
