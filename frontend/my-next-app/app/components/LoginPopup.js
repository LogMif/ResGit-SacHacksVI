"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { encryptData } from '../config'

import Cookies from "js-cookie";

export default function LoginPopup() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [isOpen, setIsOpen] = useState(false);
    const [error, setError] = useState(null);
    const [loadingLogin, setLoadingLogin] = useState(false);
    const [loadingSignup, setLoadingSignup] = useState(false);
    const router = useRouter();

    async function sendLoginData() {
        try {
            setLoadingLogin(true);

            const res = await fetch("/api/login", {
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

            Cookies.set("userSession", encryptData({ username: username, password: password }), {
                expires: 7,
                path: "/",
            });

            setIsOpen(false);
            router.push("/resumes");
        } catch (err) {
            console.error("Error:", err.message);
            setError(err.message);
        } finally {
            setLoadingLogin(false);
        }
    }

    async function sendSignupData() {
        try {
            setLoadingSignup(true);

            const res = await fetch("/api/signup", {
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

            Cookies.set("userSession", encryptData({ username: "Boo", password: "Password123" }), {
                expires: 7,
                path: "/",
            });

            setIsOpen(false);
            router.push("/resumes");
        } catch (err) {
            console.error("Error:", err.message);
            setError(err.message);
        } finally {
            setLoadingSignup(false);
        }
    }

    return (
        <div>
            <button
                onClick={() => setIsOpen(true)}
                className="px-12 py-3 text-black rounded-lg cursor-pointer text-3xl font-bold"
            >
                Login
            </button>

            {isOpen && (
                <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-20">
                    <div className="bg-white p-6 rounded-lg shadow-lg w-96">
                        <h2 className="text-xl font-bold mb-4">Login</h2>
                        <input
                            type="text"
                            placeholder="Username"
                            className="w-full mb-3 p-2 border rounded"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                        />
                        <input
                            type="password"
                            placeholder="Password"
                            className="w-full mb-3 p-2 border rounded"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                        />
                        {error && (
                            <p className="text-red-500 text-sm mb-3 text-center">
                                Incorrect username or password.
                            </p>
                        )}
                        <button
                            onClick={sendLoginData}
                            className="w-full bg-blue-500 text-white p-2 rounded"
                            disabled={loadingLogin}
                        >
                            {loadingLogin ? "Logging in..." : "Login"}
                        </button>
                        <button
                            onClick={sendSignupData}
                            className="w-full mt-2 p-2 rounded"
                            disabled={loadingSignup}
                        >
                            {loadingSignup ? "Creating User..." : "Create User"}
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
