'use client';

import { useState } from 'react';

const data = {
    "user info": {
        "name": "testName",
        "email": "testemail@gmail.com",
        "linkedin url": "https://www.linkedin.com/in/kierann-chong",
        "personal url": "https://green-kiwie.github.io/Kierann_Resume.github.io",
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
};

export default function SendDataComponent() {
    const [response, setResponse] = useState(null);
    const [error, setError] = useState(null);

    async function sendData() {
        try {
            const res = await fetch('/api/send', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(
                    {
                        "user info" : 'Hello from Next.js'
                    }
                ),
            });

            if (!res.ok) {
                throw new Error(`Error: ${res.status}`);
            }

            const data = await res.json();
            setResponse(data);
        } catch (err) {
            setError(err.message);
        }
    }

    return (
        <div>
            <button onClick={sendData} className="px-6 py-3 bg-blue-500 text-white rounded-lg">
                Send Data
            </button>
            <br />

            {response && <pre className="mt-4 p-3 bg-gray-200 rounded-lg">{JSON.stringify(response, null, 2)}</pre>}
            {error && <p className="text-red-500">{error}</p>}
        </div>
    );
}