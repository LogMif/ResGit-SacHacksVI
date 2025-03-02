"use client";

import {useEffect, useState} from "react";
import Cookies from "js-cookie";
import {decryptData} from "@/app/config";

export default function UploadResumeComponent({ selectedResume, generateNew, onShowHistory }) {
    const [error, setError] = useState(null);
    const [userSession, setUserSession] = useState(null);
    const [pdfFile, setPDFile] = useState(null);

    useEffect(() => {
        const encryptedSession = Cookies.get("userSession");
        if (encryptedSession) {
            const decryptedSession = decryptData(encryptedSession);
            setUserSession(decryptedSession);
        }
    }, []);

    async function sendData() {
        const {username, password} = userSession;

        useEffect(() =>
                console.log(pdfFile)
        , [])

        pdfFile.arrayBuffer().then(pdfBinary => {
            useEffect(() =>
                    console.log(pdfFile)
                , [])

            fetch("/api/uploadResumePDF", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({
                    pdf_binary: pdfBinary,
                    username: username,
                    password: password
                })
            });
        }).then(res => {
            if (!res.ok) {
                throw new Error(`Error: ${res.status}`);
            }
        }).catch(err => {
            console.error("Error:", err.message);
            setError(err.message);
        });
    }

    return (
        <div className="flex flex-col items-center bg-gray-100 h-screen">
            <h1 className="text-5xl m-15">Upload your main resumé</h1>
            <div className="bg-white flex flex-col p-20 rounded-xl drop-shadow-lg">
                <h1 className="text-3xl mb-5">Upload File</h1>
                <input className="p-20 border-2 border-dashed border-gray-500 rounded-xl mb-10"
                       type="file"
                       id="fileInput"
                       name="file"
                       accept="application/pdf"
                       onChange={(e) => setPDFile(e.target.files[0])}
                />
                <button className="button-blue text-white py-4 px-12 rounded-xl text-xl w-auto self-center"
                        onClick={() => sendData()}>
                            Upload PDF
                </button>
            </div>
        </div>
    );
}
