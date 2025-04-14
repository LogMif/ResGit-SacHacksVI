import json
from pathlib import Path
import os

class FailedUserAuthError(Exception):
    def __init__(self, user_exists: bool):
        self._user_exists = user_exists

    def __str__(self) -> str:
        if not self._user_exists:
            return "User does not exist."

        return "Password does not match the given username."
    

class UserAlreadyExistsError(Exception):
    def __str__(self) -> str:
        return "A user with that username already exists."


class GeneratedResumeDNEError(Exception):
    def __str__(self):
        return 'Given generated resume does not exist.'

def password_filename() -> str:
    """returns the filename of the password file"""
    return 'passwds.auth'

def _get_path(input_directory: str, input_file_name:str) -> Path:
    """returns a path object given the directory and filename"""
    return Path(input_directory+'/'+input_file_name)

def _get_object(directory: str, file_name: str) -> dict[str, str] | None:
    """
    Gets an object from the given file_name and path
    """
    try:
        file_path = _get_path(directory, file_name)
        with open(file_path, 'r') as file:
            output = json.load(file)
        return output
    except:
        return None
    
def _put_object(directory: str, file_name: str, file_data: str) -> None:
    """creates a file of specific file name in given directory"""
    file_path = _get_path(directory, file_name)
    with open(file_path, 'w') as file:
        file.write(file_data)

def _create_directory(directory) -> None:
    """creates given directory"""
    os.makedirs(directory)

def _get_auth_pairs(directory: str) -> 'json':
    """
    Gets the user_name and password pairs.
    """
    password_response = _get_object(directory, password_filename())

    if password_response is None:
        _put_object(directory = directory, file_name = password_filename(), file_data = '{}')
        password_response = _get_object(directory, password_filename())

    return password_response

def auth_user(directory: str, user_name: str, password: str) -> None:
    """
    Authenticates if the user even exists and if their password matches, 
    if not it raises FailedUserAuthError.
    """
    auth_pairs = _get_auth_pairs(directory)
    
    if not user_name in auth_pairs:
        raise FailedUserAuthError(False)
    
    if auth_pairs[user_name] != password:
        raise FailedUserAuthError(True)

def create_user(directory: str, user_name: str, password: str) -> None:
    """
    Creates a user directory if it does not exist.
    """
    auth_pairs = _get_auth_pairs(directory)
    
    if user_name in auth_pairs:
        raise UserAlreadyExistsError()
    
    auth_pairs[user_name] = password

    json_auth_pairs = json.dumps(auth_pairs)

    _create_directory(user_name)
    _put_object(directory = directory, filename = f'passwds.auth', file_data = json_auth_pairs)

def get_history(directory: str, user_name: str, password: str) -> dict[str, 'perspectives']:
    """
    Reads the json history from a given user.
    """
    auth_user(directory, user_name, password)

    history_response = _get_object(directory, f'{user_name}/history.json')

    return history_response

def create_history(directory: str, user_name: str, password: str, history: dict) -> None:
    """
    Creates a history for a given user.
    """
    auth_user(directory, user_name, password)
    _put_object(directory = directory, file_name = f'{user_name}/history.json', file_data = json.dumps(history))

def _list_objects(directory: str, user_name: str):
    """lists all files in given username directory"""
    path = _get_path(directory, user_name)
    return os.listdir(path)


def get_all_generated_resume_names(directory: str, user_name: str, password: str) -> list[str]:
    """
    Gets the names of all of the previously generated resume's for the user.
    """
    auth_user(directory, user_name, password)
    generated_resume_objects = _list_objects(directory = directory, username = user_name)

    generated_resumes_list = []

    for generated_resume_object in generated_resume_objects: 
        if generated_resume_object.endswith('.pdf'):
            generated_resumes_list.append(generated_resume_object[len(user_name) + 1:])

    return generated_resumes_list


def get_generated_resume(directory: str, user_name: str, password: str, resume_name: str) -> bytes:
    """
    Gets a generated resume from the given user.
    """
    auth_user(directory, user_name, password)
    resume_response = _get_object(directory, f'{user_name}/{resume_name}.pdf')
        
    if resume_response is None:
        raise GeneratedResumeDNEError()
    
    return resume_response
    

def store_generated_resume(directory: str, user_name: str, password: str, resume_name: str, generated_resume: bytes):
    """
    Stores the given resume for the given user.
    """
    auth_user(directory, user_name, password)
    _put_object(directory = directory, file_name = f'{user_name}/{resume_name}.pdf', file_data = generated_resume)








