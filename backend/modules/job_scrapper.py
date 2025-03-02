#anthropic.claude-3-haiku-20240307-v1:0
import boto3

import urllib.request
from bs4 import BeautifulSoup

import json
import os

import dotenv

dotenv.load_dotenv('../.env')

def _scrape_webpage(url: str) -> BeautifulSoup:
    """
    Takes a url and gets its webpage content.
    """
    request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 ResGit SacHacksVI'})
    
    try:
        response = urllib.request.urlopen(request)
        
        soup = BeautifulSoup(response)
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
            Give me the entire job description for the first job listing on this webpage. 
            Ignore any unrelated text to the job description and all job listings after the first. 
            Only provide the description for the first job from the following webpage: {page_text}
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
            'temperature': 0.9,
            'topP': 1,
            'stopSequences': [
                'string'
            ]
        }
    )

    ai_summary = json.loads(ai_response['Body'].read())
    generated_text = "".join([output['text'] for output in ai_summary['content']])

    return generated_text

    

print(_ai_summarize_job('https://www.linkedin.com/jobs/view/part-time-work-from-home-data-entry-clerk-100%25-remote-at-bekafor-llc-4172143699?trk=public_jobs_topcard-title'))