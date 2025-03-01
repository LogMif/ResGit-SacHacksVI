import json
import traceback
from flask import jsonify

def _create_success_output(kwargs) -> "jsonify":
    output = {
        "statusCode": 200,
        "body": json.dumps(kwargs)
    }
    output = jsonify(output)

    return output

def _create_fail_output(error: Exception) -> 'jsonify':
    stack_trace = traceback.format_exc()
    print(stack_trace)
    return {
            "statusCode": 500,
            "body": json.dumps({"error": str(error)}),
            "location": stack_trace
        } 

def flask_function(func: function) -> dict[str, int | str]:
    def executable(*args, **kwargs):
        try:
            function_output = func(*args, **kwargs)

            api_output = _create_success_output(function_output)
            return api_output
        
        except Exception as e:
            return _create_fail_output(e)
        
    return executable

@flask_function
def add_user_history(new_user_history: dict, username: str, password: str) -> dict:
    current_history = ""
    updated_history = ""
    return {"history": updated_history}
    
@flask_function
def add_user(username: str, password: str) -> dict:
    #add user function here
    return {}

@flask_function
def get_user_history(username: str, password: str) -> dict:
    #read user history code here
    current_history = ""
    return {"history": current_history}

@flask_function
def generate_resume(selected_history: dict, username: str, password: str) -> dict:
    #generating function here
    generated_resume_binary = ""

    return {"resume": generated_resume_binary}
