"use client";

import { useState, useEffect } from "react";
import { decryptData } from '../config';
import Cookies from "js-cookie";

export default function SidebarComponent({ setSelectedResume, onGenerateNew, onShowHistory }) {
    const [responseData, setResponseData] = useState(null);
    const [error, setError] = useState(null);
    const [userSession, setUserSession] = useState(null);

    const handleHistoryClick = () => {
        onShowHistory(true);
    };

    useEffect(() => {
        const encryptedSession = Cookies.get("userSession");
        if (encryptedSession) {
            const decryptedSession = decryptData(encryptedSession);
            setUserSession(decryptedSession);
        }
    }, []);

    useEffect(() => {
        if (userSession && !responseData) {
            sendLoginData();
        }
    }, [userSession]);

    async function sendLoginData() {
        try {
            if (!userSession) {
                throw new Error("User session not found.");
            }

            const { username, password } = userSession;

            const res = await fetch("/api/resumeList", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    username: username,
                    password: password,
                }),
            });

            if (!res.ok) {
                throw new Error(`Error: ${res.status}`);
            }

            const data = await res.json();
            setResponseData(data);
        } catch (err) {
            console.error("Error:", err.message);
            setError(err.message);
        }
    }

    const resumeList = responseData?.data?.body ? JSON.parse(responseData.data.body).resume_names : [];

    return (
        <div className="text-black w-full h-full p-6">
            <div className='bg-white rounded-2xl p-2 mb-2 w-auto self-center py-4 px-8 hover:bg-gray-300'>
                <h2
                    className="text-2xl font-bold cursor-pointer"
                    onClick={handleHistoryClick}
                >History</h2>
            </div>

            {resumeList.length > 0 ? (
                <>
                    <ul className="space-y-2">
                        {resumeList.map((resume, index) => (
                            <li
                                key={index}
                                className="p-2 hover:bg-gray-300 cursor-pointer rounded-l-lg"
                                onClick={() => setSelectedResume(resume.replace(/\.pdf$/, ''))}
                            >
                                {resume.replace(/\.pdf$/, '')}
                            </li>
                        ))}
                    </ul>
                </>
            ) : (
                <p className="text-gray-500">No resumes found!</p>
            )}

            <button
                onClick={onGenerateNew}
                className="button-blue mt-2 p-2 rounded text-white text-xl font-bold py-2 px-4"
            >
                New Resume
            </button>

            {error && <p className="text-red-500 mt-4">{error}</p>}
        </div>
    );
}
