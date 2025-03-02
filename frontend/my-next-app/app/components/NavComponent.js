"use client";

import Image from "next/image";
import LoginPopup from "@/app/components/LoginPopup";
import { useState, useEffect } from "react";
import { decryptData } from '../config'
import { useRouter } from "next/navigation";

import Cookies from "js-cookie";

export default function NavComponent() {
    const [userSession, setUserSession] = useState(null);
    const router = useRouter();

    useEffect(() => {
        const encryptedSession = Cookies.get("userSession");
        if (encryptedSession) {
            const decryptedSession = decryptData(encryptedSession);
            setUserSession(decryptedSession);
        }
    }, []);

    const logout = () => {
        Cookies.remove("userSession", { path: "/" });
        setUserSession(null);
        router.push("/");
    };

    const goToHome = () => {
        router.push("/");
    };

    const goToResumeView = () => {
        router.push("/resumes");
    };

    return (
        <nav className="sticky top-0 bg-white w-full z-10">
            <div className="flex items-center justify-between p-4 max-w-screen-2xl mx-auto">
                {userSession ? (
                    <Image
                        src="/logo.jpg"
                        alt="Logo Image" width={50} height={50}
                        onClick={goToResumeView}
                    />
                    ) : (
                    <Image
                        src="/logo.jpg"
                        alt="Hero Image" width={50} height={50}
                        onClick={goToHome}
                    />
                    )}
                <div className="ml-auto">
                    {userSession ? (
                        <button
                            onClick={logout}
                            className="px-12 py-3 text-black rounded-lg cursor-pointer text-3xl font-bold"
                        >
                            Logout
                        </button>
                    ) : (
                        <LoginPopup />
                    )}
                </div>
            </div>
        </nav>
    );
}
