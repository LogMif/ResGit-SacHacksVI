'use client';

import {useEffect, useState} from "react";
import Cookies from "js-cookie";
import {decryptData} from "@/app/config";

// **Utility Function: Deep Clone Object**
const deepClone = (obj) => JSON.parse(JSON.stringify(obj));

// **Utility Function: Update Nested JSON Data Immutably**
const updateNestedState = (obj, path, value) => {
    if (path.length === 1) {
        return { ...obj, [path[0]]: value };
    }

    return {
        ...obj,
        [path[0]]: updateNestedState(obj[path[0]], path.slice(1), value)
    };
};

// **Editable JSON Component**
const EditableJson = ({ data, onChange, path = [] }) => {
    const handleValueChange = (valuePath, newValue) => {
        onChange((prevData) => updateNestedState(deepClone(prevData), valuePath, newValue));
    };

    const handleKeyRename = (oldKey, newKey, path) => {
        onChange((prevData) => {
            const updatedData = deepClone(prevData);
            let temp = updatedData;

            for (let i = 0; i < path.length - 1; i++) {
                temp = temp[path[i]];
            }

            temp[newKey] = temp[oldKey];
            delete temp[oldKey];

            return updatedData;
        });
    };

    const renderJson = (data, path) => {
        const depth = path.length;
        const parentKey = path[0] || "";

        if (typeof data === "string") {
            return (
                <input
                    type="text"
                    value={data}
                    onChange={(e) => handleValueChange(path, e.target.value)}
                    className="border p-2 rounded w-full bg-white text-gray-800 shadow-sm"
                />
            );
        }
        if (Array.isArray(data)) {
            return (
                <div className="flex flex-wrap gap-2">
                    {data.map((item, index) => (
                        <input
                            key={index}
                            type="text"
                            value={item}
                            onChange={(e) => {
                                const updatedArray = [...data];
                                updatedArray[index] = e.target.value;
                                handleValueChange(path, updatedArray);
                            }}
                            className="border p-2 rounded w-auto min-w-[120px] bg-white text-gray-800 shadow-sm text-center"
                        />
                    ))}
                </div>
            );
        }
        if (typeof data === "object" && data !== null) {
            return (
                <div className="pl-4 border-l-2 border-gray-300">
                    {Object.entries(data).map(([key, value]) => (
                        <div key={key} className="mb-2">
                            {/* Read-Only Top-Level Keys */}
                            {depth === 0 ? (
                                <h2 className="text-lg font-bold text-gray-800">{key}</h2>
                            ) : depth === 1 && (parentKey === "education" || parentKey === "experiences" || parentKey === "awards") ? (
                                // Depth 1 Keys are Editable (e.g., "school 1 (university name)")
                                <input
                                    type="text"
                                    value={key}
                                    onChange={(e) => handleKeyRename(key, e.target.value, path)}
                                    className="border p-2 rounded w-full bg-gray-100 text-gray-800 shadow-sm font-semibold"
                                />
                            ) : (
                                // Read-Only Key Labels for Everything Else
                                <p className="font-medium text-gray-700">{key}</p>
                            )}

                            {renderJson(value, [...path, key])}
                        </div>
                    ))}
                </div>
            );
        }
        return null;
    };

    return (
        <div>
            {renderJson(data, path)}
        </div>
    );
};

// **Main JSON Editor Component**
export default function JsonEditor() {
    const [error, setError] = useState(null);
    const [userSession, setUserSession] = useState(null);
    const [response, setResponse] = useState(null);

    useEffect(() => {
        const encryptedSession = Cookies.get("userSession");
        if (encryptedSession) {
            const decryptedSession = decryptData(encryptedSession);
            setUserSession(decryptedSession);
        }
    }, []);

    useEffect(() => {
        if (userSession) {
            sendResumeRequest();
        }
    }, [userSession]);

    const [jsonData, setJsonData] = useState('');


    async function sendResumeRequest() {
        try {
            if (!userSession) {
                throw new Error("User session not found.");
            }

            const { username, password } = userSession;

            const res = await fetch("/api/getHistory", {
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

            const data = await res.json()
            setResponse(JSON.parse(data["data"]["body"])["history"]);
            setJsonData(JSON.parse(data["data"]["body"])["history"]);
        } catch (err) {
            console.error("Error:", err.message);
            setError(err.message);
        }
    }

    // Function to save JSON
    const saveJson = () => {
        const jsonString = JSON.stringify(jsonData, null, 2);
        const blob = new Blob([jsonString], { type: "application/json" });
        const url = URL.createObjectURL(blob);
        const link = document.createElement("a");
        link.href = url;
        link.download = "edited_data.json";
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    };

    return (
        <div className="max-w-screen-lg w-full mx-auto p-6 bg-white shadow-md rounded-lg">
            <h2 className="text-2xl font-bold mb-4 text-center">Editable JSON Viewer</h2>

            {/* Editable JSON Viewer */}
            <div className="h-[75vh] overflow-auto p-4 border border-gray-300 rounded-lg bg-gray-50">
                <EditableJson data={jsonData} onChange={setJsonData} />
            </div>

            {/* Save JSON Button */}
            <button
                onClick={saveJson}
                className="mt-4 px-6 py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600 block mx-auto"
            >
                Save JSON
            </button>
        </div>
    );
}
