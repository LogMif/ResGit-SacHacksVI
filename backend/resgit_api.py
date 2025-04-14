import json
import traceback
import dotenv
import os
from flask import jsonify
from modules import s3_io as s3
from modules import local_filesystem_io as localfs
from modules import history_class
from modules import latex_builder as lb
from modules import data_pairing as dp
from modules import job_scrapper
from modules import pdf_reader
import base64

from typing import module


dotenv.load_dotenv()

def get_data_storage(data_storage: str) -> module:
    if data_storage == 's3':
        return s3
    elif data_storage == 'local':
        return localfs

def add_user_history(bucket: str, pdf_binary: dict, username: str, password: str, data_storage: str = 's3') -> dict:
    pdf_text = pdf_reader.extract_text_from_pdf(pdf_binary)
    generated_dict = dp.parse_pdf_text_to_history(pdf_text)
    try:
        user_history = get_data_storage(data_storage).get_history(bucket, username, password)
        user_history.merge_histories(generated_dict)
    except:
        user_history = history_class.history(generated_dict)
    user_history_str = user_history.jsonify()
    history_dict = json.loads(user_history_str)
    get_data_storage(data_storage).create_history(bucket, username, password, history_dict)
    return {"history": user_history_str}
    
def get_ai_recommendation(bucket: str, job_link: str, username: str, password: str, data_storage: str = 's3') -> dict:
    full_history = get_data_storage(data_storage).get_history(bucket, username, password)
    job_string = job_scrapper.ai_summarize_job(job_link)
    hist = history_class.history(full_history)
    recommendation = dp.get_history_recommendation(job_string, hist.jsonify())
    return {"ai_recommendation": recommendation}

def add_user(bucket: str, username: str, password: str, data_storage: str = 's3') -> dict:
    get_data_storage(data_storage).create_user(bucket, username, password)
    return {"user_created_state": "success"}


def authenticate_user(bucket: str, username: str, password: str, data_storage: str = 's3') -> dict:
    get_data_storage(data_storage).auth_user(bucket, username, password)
    return {"user_created_state": "success"}

def get_past_resume_names(bucket: str, username: str, password: str, data_storage: str = 's3') -> dict:
    resume_names = get_data_storage(data_storage).get_all_generated_resume_names(bucket, username, password)
    return {"resume_names": resume_names}

def get_resume_pdf(bucket: str, username: str, password: str, resume_name: str, data_storage: str = 's3') -> dict:
    resume_binary = get_data_storage(data_storage).get_generated_resume(bucket, username, password, resume_name)
    encoded_binary = base64.b64encode(resume_binary).decode("utf-8")
    
    return {"resume": encoded_binary}

def get_user_history(bucket: str, username: str, password: str, data_storage: str = 's3') -> dict:
    current_history = get_data_storage(data_storage).get_history(bucket, username, password)
    return {"history": current_history}

def generate_resume(bucket: str, selected_history: str, username: str, password: str, resume_name: str, data_storage: str = 's3') -> dict:
    hist = history_class.history(selected_history)
    generated_resume_binary = lb.get_resume(hist)

    encoded_binary = base64.b64encode(generated_resume_binary).decode("utf-8")
    get_data_storage(data_storage).store_generated_resume(bucket, username, password, resume_name, generated_resume_binary)
    return {"resume": encoded_binary}

if __name__ == "__main__":
    add_user("Kierann", "password")
    