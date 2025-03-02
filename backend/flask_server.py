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

@app.route("/get_resume_pdf", methods=["POST"])
def flask_get_resume_pdf() -> dict[str, int | str]:
    """api function gets past resume names from database"""
    warnings.filterwarnings("ignore")
    data = request.get_json()

    username = data.get("username", "")
    password = data.get("password", "")
    resume_name = data.get("resume_name", "")

    response = rg.get_resume_pdf(username, password, resume_name)
    return response

@app.route("/get_user_history", methods=["POST"])
def flask_get_user_history() -> dict[str, int | str]:
    """api function returns user history"""
    warnings.filterwarnings("ignore")
    data = request.get_json()

    username = data.get("username", "")
    password = data.get("password", "")

    return rg.get_user_history(username, password)

@app.route("/generate_resume", methods=["POST"])
def flask_generate_resume() -> dict[str, int | str]:
    """api function generates resume with selected information"""
    warnings.filterwarnings("ignore")
    data = request.get_json()

    username = data.get("username", "")
    password = data.get("password", "")
    selected_items = data.get("selected_data", "")

    return rg.generate_resume(selected_items, username, password)



if __name__ == '__main__':
    public_url = ngrok.connect(5000)

    print(f"ngrok tunnel available at {public_url}")
    app.run(port=5000)


{
    "user info": {
        "name": "testName",
        "email": "testemail@gmail.com",
        "linkedin url": "https://www.linkedin.com/in/kierann-chong",
        "personal url": "https://green-kiwie.github.io/Kierann\_Resume.github.io",
        "contact_number": "(949) 822-4004"
    },
    "education": {
        "school 1 (university name)": {
            "location (city/country)": "California",
            "degree": "BSc in Computer Science",
            "year status": "Sophomore",
            "expected graduation": "May 2027"
        }
    },
    "technical skills": {
        "skill category 1 (languages)": ["Python", "Pandas", "Tensorflow", "Gensim", "LangChain", "Yfinance", "Huggingface", "C++", "SQL", "HTML"],
        "skill category 2 (tools)": ["AWS (Bedrock, Glue, Lambda, DynamoDB, S3 Bucket)", "Sharepoint", "PowerApps", "Git"]
    },
    "experiences": {
        "arc 1 (job tile)": {
            "company": "google",
            "job dates": "July 2024-September 2024",
            "perspectives": {
                "perspective": ["bullet 1", "bullet 2"],
                "perspective 2": ["bullet 1", "bullet 2"],
            }
        },
        "arc 2 (job title)": {
            "company": "disney",
            "job dates": "July 2024-September 2024",
            "perspectives": {
                "perspective": ["bullet 1", "bullet 2"],
                "perspective 2": ["bullet 1", "bullet 2"],
            }
        }
    },
    "awards":{
        "award 1 (award title)": {
            "institution": "UC Irvine, California",
            "award date": "2024-2025",
            "award description": [
                "Awarded for research on the statistical distribution of distant galaxies to analyze the young universe."
            ]
        },
        "award 2 (award title)": {
            "institution": "UC Irvine, California",
            "award date": "2024-2025",
            "award description": [
                "award!"
            ]
        }
    }
}

{
    "user info": {
        "name": "pft",
        "email": "pft@gmail.com",
        "linkedin url": "hhehe love linkedin",
        "personal url": "github nerds",
        "contact_number": "insert pphone numbers here"
    },
    "education": {
        "UC I": {
            "location (city/country)": "US",
            "degree": "BSc in stupidify",
            "year status": "freshjuice",
            "expected graduation": "June 2020"
        }
    },
    "technical skills": {
        "interpersonnel": ["kindness", "empathatic", "pathetic"],
        "hard skills": ["excel", "powerpoint"]
    },
    "experiences": {
        "microsfot server": {
            "company": "microsoft",
            "job dates": "insert fake dates here",
            "perspectives": {
                "my first idea": ["hehe", "haha"],
                "second idea": ["sad", "sadly"],
            }
        },
        "google clown": {
            "company": "clown inc",
            "job dates": "whoop",
            "perspectives": {
                "happy": ["hah", "hoho"],
                "sad": ["womp womp", "woomp"],
            }
        }
    },
    "awards":{
        "best person award": {
            "institution": "white house",
            "award date": "2003",
            "award description": [
                "Voted most loved person ever"
            ]
        },
        "stupidest person award": {
            "institution": "fund house",
            "award date": "2100",
            "award description": [
                "lost the company 10 trillion"
            ]
        }
    }
}