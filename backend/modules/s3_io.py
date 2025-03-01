import boto3
import json

import boto3.exceptions


class FailedUserAuthError(Exception):
    def __init__(self, user_exists: bool):
        self._user_exists = user_exists

    def __str__(self) -> str:
        if self._user_exists:
            return "User does not exist."

        return "Password does not match the given username."
    

class UserAlreadyExistsError(Exception):
    def __str__(self) -> str:
        return "A user with that username already exists."


class S3Client:
    def __init__ (self):
        self._client = boto3.client('s3')

    
    def __enter__(self):
        return self


    def __exit__(self, exc_type, exc_value, exc_traceback):
        self._client.close()


def create_user(bucket: str, user_name: str, password: str) -> None:
    """
    Creates a user directory if it does not exist.
    """

    with S3Client() as s3_client:
        try:
            s3_client.put_object(Bucket = bucket, Key = user_name, Body="")
        except boto3.exceptions.S3UploadFailedError:
            raise UserAlreadyExistsError()
        

def read_history(bucket: str, user_name: str) -> str:
    """
    Reads the json history from a given user.
    """
    with boto3.client("s3") as s3_client:
        try:
            response = s3_client.get_object(Bucket = bucket, Key = f'{user_name}/history.json')
        except:
            pass

        
create_user('resgit-bucket', 'Boo', 'BestPasswordEver')


def _get_passwords(bucket: str):
    pass 


def _auth_user(bucket: str, user_name: str, password: str) -> S3Client:
    """
    Authenticates if the user even exists, if not it raises FailedUserAuthError
    """
    s3_client = boto3.client("s3")

    try:
        s3_client.get_object(Bucket = bucket, Key = user_name)

        password_response = s3_client.get_object(Bucket = bucket, Key = 'passwds.auth')
        passwords = password_response['Body'].read().decode('utf-8')

        print(passwords)

        if not password in passwords:
            pass

    except:
        pass

    return s3_client


#_auth_user('resgit-bucket', 'wow', 'password123')
