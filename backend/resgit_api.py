import json
import traceback
import dotenv
import os
from flask import jsonify
from modules import s3_io as s3

dotenv.load_dotenv()
def _create_success_output(kwargs) -> "jsonify":
    output = {
        "body": json.dumps(kwargs)
    }
    output = jsonify(output)
    return output, 200

def _create_fail_output(error: Exception) -> 'jsonify':
    stack_trace = traceback.format_exc()
    print(stack_trace)
    output = {
            "body": {
                "error" : json.dumps({"error": str(error)}),
                "location": stack_trace
            }
        } 
    return jsonify(output), 500

def flask_function(func: callable) -> dict[str, int | str]:
    def executable(*args, **kwargs):
        try:
            bucket = os.getenv("IO_BUCKET")
            function_output = func(bucket, *args, **kwargs)

            api_output = _create_success_output(function_output)
            return api_output
        
        except Exception as e:
            return _create_fail_output(e)
        
    return executable

# @flask_function
# def add_user_history(bucket, new_user_history: dict, username: str, password: str) -> dict:
#     current_history = ""
#     updated_history = ""
#     return {"history": updated_history}
    
@flask_function
def add_user(bucket, username: str, password: str) -> dict:
    s3.create_user(bucket, username, password)
    return {"user_created_state": "success"}

@flask_function
def authenticate_user(bucket, username: str, password: str) -> dict:
    s3.auth_user(bucket, username, password)
    return {"user_created_state": "success"}

@flask_function
def get_past_resume_names(bucket, username: str, password: str) -> dict:
    s3.auth_user(bucket, username, password)
    pass

# @flask_function
# def get_user_history(bucket, username: str, password: str) -> dict:
#     #read user history code here
#     current_history = ""
#     return {"history": current_history}

# @flask_function
# def generate_resume(bucket, selected_history: dict, username: str, password: str) -> dict:
#     #generating function here
#     generated_resume_binary = ""

#     return {"resume": generated_resume_binary}


if __name__ == "__main__":
    add_user("Kierann", "password")