"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import {decryptData, encryptData} from '../config'

import Cookies from "js-cookie";


export default function SavePopup() {
    const [resume_name, setResumeName] = useState("");
    const [isOpen, setIsOpen] = useState(false);
    const [error, setError] = useState(null);
    const [userSession, setUserSession] = useState(null);
    const [loadingSave, setLoadingSave] = useState(false);
    const router = useRouter();

    useEffect(() => {
        const encryptedSession = Cookies.get("userSession");
        if (encryptedSession) {
            const decryptedSession = decryptData(encryptedSession);
            setUserSession(decryptedSession);
        }
    }, []);

    async function sendData() {
        try {
            const { username, password } = userSession;
            setLoadingSave(true);

            const res = await fetch("/api/generateResume", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    username: username,
                    password: password,
                    resume_name: resume_name,
                    selected_data: {
                        "user info": {
                            "name": "testName",
                            "email": "testemail@gmail.com",
                            "linkedin url": "https://www.linkedin.com/in/kierann-chong/",
                            "personal url": "https://green-kiwie.github.io/Kierann////_Resume.github.io/",
                            "contact_number": "(949) 822-4004"
                        },
                        "education": {
                            "school 1 (university name)": {
                                "location (city/country)": "California",
                                "degree": "BSc in Computer Science",
                                "year status": "Sophomore",
                                "expected graduation": "May 2027",
                                "gpa": "3.9"
                            }
                        },
                        "technical skills": {
                            "skill category 1 (languages)": [
                                "Python",
                                "Pandas",
                                "Tensorflow",
                                "Gensim",
                                "LangChain",
                                "Yfinance",
                                "Huggingface",
                                "C++",
                                "SQL",
                                "HTML"
                            ],
                            "skill category 2 (tools)": [
                                "AWS (Bedrock, Glue, Lambda, DynamoDB, S3 Bucket)",
                                "Sharepoint",
                                "PowerApps",
                                "Git"
                            ]
                        },
                        "experiences": {
                            "arc 1 (job tile)": {
                                "company": "google",
                                "job dates": "July 2024-September 2024",
                                "perspectives": {
                                    "perspective": ["bullet 1", "bullet 2"],
                                    "perspective 2": ["bullet 1", "bullet 2"]
                                }
                            },
                            "arc 2 (job title)": {
                                "company": "disney",
                                "job dates": "July 2024-September 2024",
                                "perspectives": {
                                    "perspective": ["bullet 1", "bullet 2"],
                                    "perspective 2": ["bullet 1", "bullet 2"]
                                }
                            }
                        },
                        "awards": {
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
                                "award description": ["award!"]
                            }
                        }
                    }
                })
            });

            if (!res.ok) {
                throw new Error(`Error: ${res.status}`);
            }

            const data = await res.json();

            Cookies.set("userSession", encryptData({ username: username, password: password }), {
                expires: 7,
                path: "/",
            });

            setIsOpen(false);
            router.push("/resumes");
            window.location.reload();
        } catch (err) {
            console.error("Error:", err.message);
            setError(err.message);
        }
        finally {
            setLoadingSave(false);
        }
    }


    return (
        <div>
            <button
                onClick={() => setIsOpen(true)}
                className="button-blue px-12 py-3 text-white rounded-lg cursor-pointer font-bold"
            >
                SAVE
            </button>

            {isOpen && (
                <div className="fixed inset-0 flex items-center justify-center " style={{ backgroundColor: "rgba(0, 0, 0, 0.5)" }}>
                    <div className="bg-white p-6 rounded-lg shadow-lg w-96">
                        <input
                            type="text"
                            placeholder="Resume Name"
                            className="w-full mb-3 p-2 border rounded"
                            value={resume_name}
                            onChange={(e) => setResumeName(e.target.value)}
                        />
                        <button
                            className="text-white font-bold button-blue justify-center py-4 px-12 rounded-xl"
                            onClick={sendData}
                            disabled={loadingSave}
                        >
                            {loadingSave ? "Saving..." : "Sava"}
                        </button>

                        <button
                            onClick={() => setIsOpen(false)}
                            className="w-full mt-2 p-2 rounded"
                        >
                            Close
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
}
