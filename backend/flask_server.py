import warnings

from flask import Flask, request
from flask_cors import CORS
from pyngrok import ngrok

import resgit_api as rg

app = Flask(__name__)
CORS(app)

# @app.route("/add_to_history", methods=["POST"])
# def flask_add_to_history() -> dict[str, int | str]:
#     """api function merges current history with new added history"""
#     warnings.filterwarnings("ignore")
#     data = request.get_json()

#     new_history = data.get("new_history", "")
#     username = data.get("username", "")
#     password = data.get("password", "")

#     return rg.add_user_history(new_history, "", "")

@app.route("/create_user", methods=["POST"])
def flask_create_user() -> dict[str, int | str]:
    """api function creates user in database"""
    warnings.filterwarnings("ignore")
    data = request.get_json()

    username = data.get("username", "")
    password = data.get("password", "")

    return rg.add_user(username, password)

@app.route("/auth_user", methods=["POST"])
def flask_authenticate_user() -> dict[str, int | str]:
    """api function authenticates user with database"""
    warnings.filterwarnings("ignore")
    data = request.get_json()

    username = data.get("username", "")
    password = data.get("password", "")

    response = rg.authenticate_user(username, password)
    return response

@app.route("/get_past_resume_names", methods=["POST"])
def flask_get_past_resume_names() -> dict[str, int | str]:
    """api function gets past resume names from database"""
    warnings.filterwarnings("ignore")
    data = request.get_json()

    username = data.get("username", "")
    password = data.get("password", "")

    response = rg.get_past_resume_names(username, password)
    return response

# @app.route("/get_user_history", methods=["POST"])
# def flask_get_user_history() -> dict[str, int | str]:
#     """api function returns user history"""
#     warnings.filterwarnings("ignore")
#     data = request.get_json()

#     username = data.get("username", "")
#     password = data.get("password", "")

#     return rg.get_user_history(username, password)

# @app.route("/generate_resume", methods=["POST"])
# def flask_generate_resume() -> dict[str, int | str]:
#     """api function generates resume with selected information"""
#     warnings.filterwarnings("ignore")
#     data = request.get_json()

#     username = data.get("username", "")
#     password = data.get("password", "")
#     selected_items = data.get("selected_data", "")

#     return rg.generate_resume(selected_items, username, password)



if __name__ == '__main__':
    public_url = ngrok.connect(5000)

    print(f"ngrok tunnel available at {public_url}")
    app.run(port=5000)