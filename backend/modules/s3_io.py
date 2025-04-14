import boto3
import json

import boto3.exceptions

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


class S3Client:
    def __init__ (self):
        self._client = boto3.client('s3')

    
    def __enter__(self):
        return self._client


    def __exit__(self, exc_type, exc_value, exc_traceback):
        self._client.close()


def create_user(bucket: str, user_name: str, password: str) -> None:
    """
    Creates a user directory if it does not exist.
    """

    with S3Client() as s3_client:
        auth_pairs = _get_auth_pairs(s3_client, bucket)
        
        if user_name in auth_pairs:
            raise UserAlreadyExistsError()
        
        auth_pairs[user_name] = password

        json_auth_pairs = json.dumps(auth_pairs)

        s3_client.put_object(Bucket = bucket, Key = f'{user_name}/')
        s3_client.put_object(Bucket = bucket, Key = f'passwds.auth', Body = json_auth_pairs)


def get_history(bucket: str, user_name: str, password: str) -> dict[str, 'perspectives']:
    """
    Reads the json history from a given user.
    """
    with auth_user(bucket, user_name, password) as s3_client:
        history_response = _get_object(s3_client, bucket, f'{user_name}/history.json')
        history = json.loads(history_response['Body'].read())

        return history


def create_history(bucket: str, user_name: str, password: str, history: dict) -> None:
    """
    Creates a history for a given user.
    """
    with auth_user(bucket, user_name, password) as s3_client:
        s3_client.put_object(Bucket = bucket, Key = f'{user_name}/history.json', Body = json.dumps(history))


def get_all_generated_resume_names(bucket: str, user_name: str, password: str) -> list[str]:
    """
    Gets the names of all of the previously generated resume's for the user.
    """
    with auth_user(bucket, user_name, password) as s3_client:
        generated_resume_objects = s3_client.list_objects(Bucket = bucket, Prefix = f'{user_name}/', Delimiter='/')

        generated_resumes_list = []

        for generated_resume_object in generated_resume_objects['Contents']: 
            if generated_resume_object['Key'].endswith('.pdf'):
                generated_resumes_list.append(generated_resume_object['Key'][len(user_name) + 1:])

        return generated_resumes_list


def get_generated_resume(bucket: str, user_name: str, password: str, resume_name: str) -> bytes:
    """
    Gets a generated resume from the given user.
    """
    with auth_user(bucket, user_name, password) as s3_client:
        resume_response = _get_object(s3_client, bucket, f'{user_name}/{resume_name}.pdf')
            
        if resume_response is None:
            raise GeneratedResumeDNEError()
        
        return resume_response['Body'].read()
    

def store_generated_resume(bucket: str, user_name: str, password: str, resume_name: str, generated_resume: bytes):
    """
    Stores the given resume for the given user.
    """
    with auth_user(bucket, user_name, password) as s3_client:
        s3_client.put_object(Bucket = bucket, Key = f'{user_name}/{resume_name}.pdf', Body = generated_resume)


def _get_object(s3_client, bucket: str, path: str) -> dict[str, str] | None:
    """
    Gets an object from the given bucket at the given path,
    returning None if the objected does not exist.
    """
    try:
        item = s3_client.get_object(Bucket = bucket, Key = path)
        return item
    except:
        return None


def _get_auth_pairs(s3_client: 's3_client', bucket: str) -> 'json':
    """
    Gets the user_name and password pairs.
    """
    password_response = _get_object(s3_client, bucket, 'passwds.auth')

    if password_response is None:
        s3_client.put_object(Bucket = bucket, Key = 'passwds.auth', Body = '{}')
        password_response = _get_object(s3_client, bucket, 'passwds.auth')

    passwords = password_response['Body'].read().decode('utf-8')

    auth_pairs = json.loads(passwords)

    return auth_pairs


def auth_user(bucket: str, user_name: str, password: str) -> S3Client:
    """
    Authenticates if the user even exists and if their password matches, 
    if not it raises FailedUserAuthError.
    """
    with S3Client() as s3_client:
        auth_pairs = _get_auth_pairs(s3_client, bucket)
        
        if not user_name in auth_pairs:
            raise FailedUserAuthError(False)
        
        if auth_pairs[user_name] != password:
            raise FailedUserAuthError(True)

        return S3Client()