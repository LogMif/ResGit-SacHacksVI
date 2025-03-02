import boto3
import os
import dotenv

dotenv.load_dotenv('../.env')


def parse_pdf_text_to_history(pdf_text: str) -> dict:
    """
    Gets a dictionary in the format of a history, filled out
    based on the resume pdf given.
    """
    bedrock_client = boto3.client(
        service_name = 'bedrock-runtime',
        region_name = os.getenv('AWS_REGION')
    )

    model_id = 'amazon.nova-lite-v1:0'

    history_template = {
    "user info": {
        "name": "testName",
        "email": "testemail@gmail.com",
        "address": "12345 Street Name, City, State",
        "phone": "1234567891"
    },
    "education": {
        "school 1": {
            "dates": "September 2024, June 2026",
            "major": "Computer Science, BS"
        }
    },
    "technical skills": {
        "skill 1": "Such a good programmer",
        "skill 2": "The stupid API back-end made didn't accept POST :)"
    },
    "experiences": {
        "arc 1": {
            "perspective": ["bullet 1", "bullet 2"],
            "perspective 2": ["bullet 1", "bullet 2"],
        },
        "arc 2": {
            "perspective": ["bullet 1", "bullet 2"],
            "perspective 2": ["bullet 1", "bullet 2"],
        }
    }
}

    history_template2 = {
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
    prompt = f'''
            Here is a template: {history_template}
            Here is another sample of the same template: {history_template2}
            \n\n
            This template is to be filled out with the following text that represents a resume,
            putting the data from that text into the approriate sections of the dictionary template.
            Do not change the data type for the values in the template. If it is a string, keep it as a string. if it is a list, keep it as a list. 
            Here is the data to fill the template: {pdf_text}
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



def get_history_ranking(job_summary: str, history: dict) -> list[(str, str)]:
    """
    Using the given job summary and history, return a list-ranking
    of history perspectives by relevance to the job summary.
    """
    del history['user info']

    bedrock_client = boto3.client(
        service_name = 'bedrock-runtime',
        region_name = os.getenv('AWS_REGION')
    )

    model_id = 'amazon.nova-lite-v1:0'

    prompt = f'''
            Comparing the following job description with the following dictionary's deepest values,
            return only a list of lists that are ordered in the most relavent dictionary values to the job description
            to the least relavent dictionary values to the job description: 
            Job Summary: {job_summary}\n\n
            Dictionary: {history}

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

# history = """{
#     "user info": {
#         "name": my_name,
#         "email": my_email,
#         "linkedin url": some_linked_in_link,
#         "personal url": some_extra_link_if_it_exists,
#         "contact_number": the_provided_number_if_applicable
#     },
#     "education": {
#         some university name: {
#             "location (city/country)": some location,
#             "degree": the degree on the resume,
#             "year status": the stated year status at the university,
#             "expected graduation": stated graduation month and year
#         }
#         ...
#     },
#     "technical skills": {
#         skill category: A list that corresponds with this category of skills found on the resume,
#         skill category 2: Another list, but that corresponds with with category of skills found on the resume
#         ...
#     },
#     "experiences": {
#         A job tile: {
#             "company": The first company on the resume,
#             "job dates": timeframe worked at the company,
#             "perspective": [the first bullet point, the second bullet point, ...]
#         },
#         Another job title: {
#             "company": The second company on the resume,
#             "job dates": timeframe worked at this company,
#             "perspective": [the first bullet point for this job, the second bullet point, ...]
#             }
#         }
#         ...
#     },
#     "awards":{
#         The first award on the resume: {
#             "institution": The issuer of the award on the resume,
#             "award date": the date the award was issued,
#             "award description": [
#                 Text from the first award's description.
#             ]
#         },
#         The second award on the resume: {
#             "institution": The issuer of this award on the resume,
#             "award date": The date this award was issued,
#             "award description": [
#                 Text from the second award's description.
#             ]
#         }
#         ...
#     }
# }"""

if __name__ == "__main__":
    print(parse_pdf_text_to_history('''Logan Mifflin 24510 Arroyo Dr., Irvine, CA 92617 | Email: logan.mifflin@gmail.com | Cell: (760)-223-9085 EDUCATION
    University of California, Irvine
        B.S. in Computer Science
    Sept. 2024 - ONGOING
    GPA: 4.00
    Mt. San Jacinto College
        A.S. in Computer Science for Transfer
        A.S. in Mathematics for Transfer
        A.A. in Mathematics and Science

    May 2024
    GPA: 3.92

        Relevant Coursework: Data Structures & Algorithms, Discrete Structures, Linear Algebra, Differential 
            Equations.

    TECHNICAL SKILLS
        Programming Languages: C++, C#, Java, Javascript, Python, HTML, SQL, Assembly
        Operating Systems: Windows (11, 10, 7), Linux (Mint, CentOS)
        Software Proficiencies: Git, Github Desktop

    PROJECTS
    FastFoodComparer
    Full Stack Developer
    Tech Used: HTML, CSS, ReactJS, NodeJS, Python, SQLite, Beautifulsoup
    July 2024 - August 2024

    Created a React web application which filters and ranks 10,000s of fast food items based on chosen macronutrient comparisons.
    Implemented an efficient NodeJS server to service clients who use the React web application with requested fast food items from an SQLite database.
    Scraped and parsed fast food item data from fast food websites with Beautifulsoup into an SQLite database.
    PeriodicTable
    Independent Developer
    Tech Used: C++
    May 2023

    Developed a console application that parses a CSV file into an AVL tree that is used by the client to query for elements based on either their atomic number or their name.
    Efficiently stored the data using an AVL tree and called for data using depth and breadth first searches, making the queries fast for user experience.
    EbayInventory
    Solo Developer
    Tech Used: Java, JavaFX, Ebay RESTful API 
    March 2022 - May 2022

    Developed a GUI application to display a client’s 1000+ Ebay listings with certain data about the listings and filtering functionality, allowing the client to make well-informed decisions on their current listings.
    Wrote design documentation and responded quickly to client needs and required dynamic modifications, implementing requests into the software’s development.
    Used UX design principles to develop an intuitive and easy-to-read interface for the client to interact with.
    '''))
#print(get_history_ranking(job_scrapper.ai_summarize_job('https://www.linkedin.com/jobs/view/sr-administrative-assistant-at-linkedin-4168614516?trk=public_jobs_topcard-title'), history))