import json
import traceback
import dotenv
import os
from flask import jsonify
import resgit_api as rgapi



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

@flask_function
def add_user_history(bucket, pdf_binary: dict, username: str, password: str) -> dict:
    return rgapi.add_user_history(bucket, pdf_binary, username, password)
    
@flask_function
def get_ai_recommendation(bucket, job_link: str, username: str, password: str) -> dict:
    return rgapi.get_ai_recommendation(bucket, job_link, username, password)

@flask_function
def add_user(bucket, username: str, password: str) -> dict:
    return rgapi.add_user(bucket, username, password)
    

@flask_function
def authenticate_user(bucket, username: str, password: str) -> dict:
    return rgapi.authenticate_user(bucket, username, password)

@flask_function
def get_past_resume_names(bucket, username: str, password: str) -> dict:
    return rgapi.get_past_resume_names(bucket, username, password)

@flask_function
def get_resume_pdf(bucket, username: str, password: str, resume_name: str) -> dict:
    return rgapi.get_resume_pdf(bucket, username, password, resume_name)

@flask_function
def get_user_history(bucket, username: str, password: str) -> dict:
    return rgapi.get_user_history(bucket, username, password)

@flask_function
def generate_resume(bucket, selected_history: str, username: str, password: str, resume_name: str) -> dict:
    return generate_resume(bucket, selected_history, username, password, resume_name)

if __name__ == "__main__":
    add_user("Kierann", "password")
    