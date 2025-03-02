#anthropic.claude-3-haiku-20240307-v1:0
import boto3

import urllib.request
from bs4 import BeautifulSoup

import json
import os

def _scrape_webpage(url: str) -> BeautifulSoup:
    """
    Takes a url and gets its webpage content.
    """
    request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 ResGit SacHacksVI'})
    
    try:
        response = urllib.request.urlopen(request)
        
        soup = BeautifulSoup(response, features='html.parser')
        return soup.get_text(' ', strip=True)
    except urllib.error.URLError:
        print('Failed to open.')


def _ai_summarize_job(page_text: str) -> str:
    """
    Takes a webpage's content and parses it down to the first job's description.
    """
    bedrock_client = boto3.client(
        service_name = 'bedrock-runtime',
        region_name = os.getenv('AWS_REGION')
    )

    model_id = 'amazon.nova-lite-v1:0'

    prompt = f'''
            Give me the entire job description from the first job in this list of text,
            stopping before any other job: {page_text}
            '''


    ai_response = bedrock_client.converse(
        modelId = model_id,
        messages = [
                {
                    "role": "user",
                    "content": [{
                        'text': prompt
                    }
                    ]
                }
        ],
        inferenceConfig = {
            'maxTokens': 2048,
            'temperature': 0,
            'topP': 1,
            'stopSequences': [
                'string'
            ]
        }
    )

    generated_text = ai_response['output']['message']['content'][0]['text']

    return generated_text


def ai_job_summary(url: str) -> str:
    """
    Scrapes the given job page and passes the response to 
    an Amazon LLM, which parses the page for the job description.
    """
    page_text  = _scrape_webpage(url)

    return _ai_summarize_job(page_text)