"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import MainResumeViewComponent from "@/app/components/MainResumeViewComponent";
import SidebarComponent from "@/app/components/SidebarComponent";
import NavComponent from "@/app/components/NavComponent";
import { decryptData } from "../config";
import Cookies from "js-cookie";

export default function ResumeView() {
    const [userSession, setUserSession] = useState(null);
    const [generateNew, setGenerateNew] = useState(false);
    const [selectedResume, setSelectedResume] = useState(null);
    const [showHistory, setShowHistory] = useState(false);
    const [mainResumeExists, setMainResumeExists] = useState(true);

    const handleShowHistory = () => {
        setGenerateNew(false);
        setSelectedResume(null);
        setShowHistory(true);
    };

    const handleGenerateNew = () => {
        setShowHistory(false);
        setSelectedResume(null);
        setGenerateNew(true);
    };

    const handleSelectResume = (resume) => {
        setGenerateNew(false);
        setSelectedResume(resume);
        setShowHistory(false);
    };

    // Fetch user session from cookies
    useEffect(() => {
        const encryptedSession = Cookies.get("userSession");
        if (encryptedSession) {
            const decryptedSession = decryptData(encryptedSession);
            setUserSession(decryptedSession);
        }
    }, []);

    // Fetch user history to check if mainResumeExists should be false
    useEffect(() => {
        if (userSession) {
            checkUserHistory();
        }
    }, [userSession]);

    async function checkUserHistory() {
        try {
            const { username, password } = userSession;

            const res = await fetch("/api/getHistory", { // ✅ Use the correct API route
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ username, password }),
            });

            if (!res.ok) {
                throw new Error(`Error: ${res.status}`);
            }

            const data = await res.json();

            if (!data.success) {
                setMainResumeExists(false);
            }
        } catch (error) {
            console.error("Error fetching user history:", error);
            setMainResumeExists(false); // If an error occurs, assume no history exists
        }
    }

    if (!userSession) {
        return (
            <div className="w-full min-h-screen font-[family-name:var(--font-geist-sans)] flex flex-col items-center">
                <NavComponent />
                <div className="text-center">
                    <h2 className="text-2xl font-bold mb-4">No User Logged In</h2>
                </div>
            </div>
        );
    }

    return (
        <div className="w-full min-h-screen font-[family-name:var(--font-geist-sans)] flex flex-col items-center pb-0">
            <NavComponent />
            <main className="main-layout w-full h-full pb-0">
                {mainResumeExists ? ( // ✅ Dynamically update based on API response
                    <div className="bg-gray-100 pt-8 pb-0 w-full">
                        <div className="resume-layout-2-columns flex">
                            <div className="flex flex-col h-screen w-full text-center">
                                <SidebarComponent
                                    setSelectedResume={handleSelectResume}
                                    onGenerateNew={handleGenerateNew}
                                    onShowHistory={handleShowHistory}
                                />
                            </div>
                            <div className="flex justify-center w-full lg:w-auto bg-white h-screen rounded-tl-2xl">
                                <div className="w-full h-full px-14">
                                    <MainResumeViewComponent
                                        selectedResume={selectedResume}
                                        generateNew={generateNew}
                                        onShowHistory={showHistory}
                                    />
                                </div>
                            </div>
                        </div>
                    </div>
                ) : (
                    <div className="resume-layout-1-column">
                        <MainResumeViewComponent
                            selectedResume={selectedResume}
                            generateNew={generateNew}
                            onShowHistory={showHistory}
                        />
                    </div>
                )}
            </main>
            <footer className="flex flex-wrap items-center justify-center">
                {/* Footer content */}
            </footer>
        </div>
    );
}
