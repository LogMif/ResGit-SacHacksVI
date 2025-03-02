"use client";

import { useState, useEffect } from "react";
import Cookies from "js-cookie";
import { decryptData } from "../config";

export default function PDFViewComponent({ resumeName }) {
    const [pdfUrl, setPdfUrl] = useState(null);
    const [error, setError] = useState(null);
    const [userSession, setUserSession] = useState(null);

    useEffect(() => {
        const encryptedSession = Cookies.get("userSession");
        if (encryptedSession) {
            const decryptedSession = decryptData(encryptedSession);
            setUserSession(decryptedSession);
        }
    }, []);

    useEffect(() => {
        if (resumeName && userSession) {
            setPdfUrl(null);
            sendResumeRequest();
        }
    }, [resumeName, userSession]);

    async function sendResumeRequest() {
        try {
            if (!userSession) {
                throw new Error("User session not found.");
            }

            const { username, password } = userSession;

            const res = await fetch("/api/getResumePDF", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    username: username,
                    password: password,
                    resume_name: resumeName,
                }),
            });

            if (!res.ok) {
                throw new Error(`Error: ${res.status}`);
            }

            const data = await res.json();

            if (data.success && data.data.body) {
                const binaryData = JSON.parse(data.data.body).resume;

                const byteCharacters = atob(binaryData);
                const byteArrays = [];

                for (let offset = 0; offset < byteCharacters.length; offset += 512) {
                    const slice = byteCharacters.slice(offset, offset + 512);
                    const byteNumbers = new Array(slice.length);
                    for (let i = 0; i < slice.length; i++) {
                        byteNumbers[i] = slice.charCodeAt(i);
                    }
                    byteArrays.push(new Uint8Array(byteNumbers));
                }

                const blob = new Blob(byteArrays, { type: "application/pdf" });

                const objectUrl = URL.createObjectURL(blob);
                setPdfUrl(objectUrl);
            } else {
                throw new Error("Failed to load PDF: No binary data found.");
            }
        } catch (err) {
            console.error("Error:", err.message);
            setError(err.message);
        }
    }

    return (
        <div className="text-center w-full h-full">
            <h1 className="text-2xl font-bold mb-4">
                {resumeName.replace(/\.pdf$/, '')}
            </h1>

            {error && <p className="text-red-500">{error}</p>}

            {pdfUrl ? (
                <embed
                    src={pdfUrl}
                    type="application/pdf"
                    width="100%"
                    height="100%"
                    className="rounded-lg"
                />
            ) : (
                <p className="text-gray-500">Loading PDF...</p>
            )}
        </div>
    );
}
