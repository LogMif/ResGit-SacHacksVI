// // MainResumeViewComponent
// "use client";
//
// import { useEffect } from "react";
// import Image from "next/image";
//
// export default function GenerateResumeComponent({ selectedResume }) {
//     return (
//         <div className="flex w-full h-full">
//             <div className="flex-1 bg-white h-full">
//                 <div className="grid grid-cols-[20%_60%_20%] text-center h-full">
//                     <div className="flex items-center justify-center h-full">
//                         <button className='text-white font-bold button-blue justify-center py-4 px-12 rounded-xl'>CANCEL</button>
//                     </div>
//                     <div className="bg-gray-100 h-screen p-12 px-20 text-left rounded-tl-2xl rounded-tr-2xl">
//                         <h1 className="font-bold text-xl mb-4">Cerro Coso Community College</h1>
//                         <div className="bg-white p-10 mb-4 rounded-xl shadow-[inset_-2px_-2px_6px_rgba(0,0,0,0.2)] flex">
//                             <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. In eleifend scelerisque augue, nec maximus sem gravida id.</p>
//                             <Image src="/check_mark_green.jpg" alt="Hero Image" width={50} height={50} />
//                         </div>
//                         <div className="bg-white p-10 rounded-xl drop-shadow-lg flex">
//                             <p>Suspendisse potenti. Donec efficitur eros libero, ac malesuada metus venenatis a.</p>
//                             <Image src="/check_mark_gray.jpg" alt="Hero Image" width={50} height={50} />
//                         </div>
//
//                     </div>
//                     <div className="flex items-center justify-center h-full">
//                         <button className='text-white font-bold button-blue justify-center py-4 px-12 rounded-xl'>SAVE</button>
//                     </div>
//                 </div>
//             </div>
//         </div>
//     );
// }

"use client";

import {useEffect, useState} from "react";
import Image from "next/image";
import Cookies from "js-cookie";
import {decryptData} from "@/app/config";
import SaveNewResumePopupComponent from "@/app/components/SaveNewResumePopupComponent"
import ReactMarkdown from "react-markdown";


// JSON Data
const resumeData = {
    "education": {
        "UC I": {
            "location (city/country)": "US",
            "degree": "BSc in stupidify",
            "year status": "freshjuice",
            "expected graduation": "June 2020"
        }
    },
    "technical skills": {
        "interpersonal": ["kindness", "empathetic", "pathetic"],
        "hard skills": ["excel", "powerpoint"]
    },
    "experiences": {
        "microsfot server": {
            "company": "microsoft",
            "job dates": "insert fake dates here",
            "perspectives": {
                "my first idea": ["hehe", "haha"],
                "second idea": ["sad", "sadly"]
            }
        },
        "google clown": {
            "company": "clown inc",
            "job dates": "whoop",
            "perspectives": {
                "happy": ["hah", "hoho"],
                "sad": ["womp womp", "woomp"]
            }
        }
    },
    "awards": {
        "best person award": {
            "institution": "white house",
            "award date": "2003",
            "award description": ["Voted most loved person ever"]
        },
        "stupidest person award": {
            "institution": "fund house",
            "award date": "2100",
            "award description": ["lost the company 10 trillion"]
        }
    }
};

export default function GenerateResumeComponent({ selectedResume }) {
    const [error, setError] = useState(null);
    const [userSession, setUserSession] = useState(null);
    const [link_to_job, setLinkToJob] = useState("");
    const [loadingAI, setLoadingAI] = useState(false);
    const [responseAI, setResponseAI] = useState("");

    useEffect(() => {
        const encryptedSession = Cookies.get("userSession");
        if (encryptedSession) {
            const decryptedSession = decryptData(encryptedSession);
            setUserSession(decryptedSession);
        }
    }, []);

    async function sendAIData() {
        try {
            const { username, password } = userSession;
            setLoadingAI(true);

            const res = await fetch("/api/AIRecommend", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    username: username,
                    password: password,
                    job_link: link_to_job,
                })
            });

            if (!res.ok) {
                throw new Error(`Error: ${res.status}`);
            }

            const data = await res.json();

            setResponseAI(JSON.parse(data["data"]["body"])["ai_recommendation"]);
        } catch (err) {
            console.error("Error:", err.message);
            setError(err.message);
        }
        finally {
            setLoadingAI(false);
        }
    }

    // Initialize checkboxes for selectable sections as false
    const [checkedStates, setCheckedStates] = useState({
        education: Object.keys(resumeData["education"]).reduce((acc, school) => {
            acc[school] = false;
            return acc;
        }, {}),
        "technical skills": Object.keys(resumeData["technical skills"]).reduce((acc, category) => {
            acc[category] = false;
            return acc;
        }, {}),
        experiences: Object.keys(resumeData["experiences"]).reduce((acc, exp) => {
            acc[exp] = {
                selected: false,
                perspectives: Object.keys(resumeData["experiences"][exp]["perspectives"]).reduce(
                    (persAcc, perspective) => {
                        persAcc[perspective] = false;
                        return persAcc;
                    },
                    {}
                )
            };
            return acc;
        }, {}),
        awards: Object.keys(resumeData["awards"]).reduce((acc, award) => {
            acc[award] = false;
            return acc;
        }, {})
    });

    const togglePerspective = (job, perspective) => {
        setCheckedStates((prev) => {
            const prevExperience = prev.experiences[job];
            const newPerspectiveState = !prevExperience.perspectives[perspective];

            // If toggling ON a single perspective, make sure the experience itself is OFF
            const isExperienceSelected = prevExperience.selected;
            const perspectivesUpdated = {
                ...prevExperience.perspectives,
                [perspective]: newPerspectiveState
            };

            const anyPerspectiveSelected = Object.values(perspectivesUpdated).some((v) => v);

            return {
                ...prev,
                experiences: {
                    ...prev.experiences,
                    [job]: {
                        selected: anyPerspectiveSelected,
                        perspectives: perspectivesUpdated
                    }
                }
            };
        });
    };

    return (
        <div className="flex w-full h-full">
            <div className="flex-1 bg-white h-full">
                <div className="grid grid-cols-[30%_55%_15%] text-center h-full">
                    <div className="flex items-center justify-center h-full">
                        <div className=" mr-4 bg-gray-100 rounded-md overflow-auto" style={{ height: "calc(100vh - 80px)" }}>
                            <input
                                type="text"
                                placeholder="Link to job"
                                className="mt-4 mb-3 p-2 py-2 border rounded text-black bg-white"
                                value={link_to_job}
                                onChange={(e) => setLinkToJob(e.target.value)}
                            />

                            <button
                                className="text-white font-bold button-blue justify-center py-4 px-12 rounded-xl"
                                onClick={sendAIData}
                                disabled={loadingAI}
                            >
                                {loadingAI ? "Thinking.." : "Ask AI"}
                            </button>
                            <div className="bg-gray-100 w-full h-[80%] overflow-auto break-all mt-4">
                                {responseAI ? (
                                    <div className="max-w-full w-full break-words overflow-auto p-2 py-4">
                                        <ReactMarkdown>{responseAI}</ReactMarkdown>
                                    </div>
                                ) : (
                                    <p className="text-gray-500">No AI response yet.</p>
                                )}
                            </div>
                        </div>
                    </div>

                    {/* Main Section */}
                    <div className="bg-gray-100 h-full p-12 px-20 text-left rounded-tl-2xl rounded-tr-2xl overflow-auto">
                        {/* Education Section */}
                        <h1 className="font-bold text-xl mb-4">Education</h1>
                        {Object.entries(resumeData["education"]).map(([school, details], index) => (
                            <div
                                key={index}
                                className={`bg-white p-6 mb-4 rounded-xl flex items-center justify-between cursor-pointer transition-shadow border ${
                                    checkedStates.education[school]
                                        ? "shadow-[inset_-2px_-2px_6px_rgba(0,0,0,0.2)] border-green-600"
                                        : "drop-shadow-lg border-gray-400"
                                }`}
                                onClick={() =>
                                    setCheckedStates((prev) => ({
                                        ...prev,
                                        education: {
                                            ...prev.education,
                                            [school]: !prev.education[school]
                                        }
                                    }))
                                }
                            >
                                <div className="flex-1">
                                    <h2 className="font-semibold text-lg">{school}</h2>
                                    {Object.entries(details).map(([key, value], i) => (
                                        <p key={i} className="text-sm text-gray-600">
                                            <span className="font-medium">{key}:</span> {value}
                                        </p>
                                    ))}
                                </div>
                                <div className="flex items-center justify-center w-12 h-12">
                                    <Image
                                        src={checkedStates.education[school] ? "/check_mark_green.jpg" : "/check_mark_gray.jpg"}
                                        alt="Check"
                                        width={40}
                                        height={40}
                                    />
                                </div>
                            </div>
                        ))}

                        {/* Technical Skills Section */}
                        <h1 className="font-bold text-xl mb-4">Technical Skills</h1>
                        {Object.entries(resumeData["technical skills"]).map(([category, skills], categoryIndex) => (
                            <div
                                key={categoryIndex}
                                className={`bg-white p-6 mb-4 rounded-xl flex items-center justify-between cursor-pointer transition-shadow border ${
                                    checkedStates["technical skills"][category]
                                        ? "shadow-[inset_-2px_-2px_6px_rgba(0,0,0,0.2)] border-green-600"
                                        : "drop-shadow-lg border-gray-400"
                                }`}
                                onClick={() =>
                                    setCheckedStates((prev) => ({
                                        ...prev,
                                        "technical skills": {
                                            ...prev["technical skills"],
                                            [category]: !prev["technical skills"][category]
                                        }
                                    }))
                                }
                            >
                                <div className="flex-1">
                                    <h2 className="font-semibold">{category}:</h2>
                                    <p className="text-sm text-gray-600">{skills.join(", ")}</p>
                                </div>
                                <div className="flex items-center justify-center w-12 h-12">
                                    <Image
                                        src={checkedStates["technical skills"][category] ? "/check_mark_green.jpg" : "/check_mark_gray.jpg"}
                                        alt="Check"
                                        width={40}
                                        height={40}
                                    />
                                </div>
                            </div>
                        ))}

                        {/* Experiences Section */}
                        <h1 className="font-bold text-xl mb-4">Experiences</h1>
                        {Object.entries(resumeData["experiences"]).map(([job, details], jobIndex) => (
                            <div key={jobIndex} className="mb-4">
                                {/* Experience Block */}
                                <div
                                    className={`bg-white p-6 rounded-xl cursor-pointer transition-shadow border ${
                                        checkedStates.experiences[job].selected
                                            ? "shadow-[inset_-2px_-2px_6px_rgba(0,0,0,0.2)] border-green-600"
                                            : "drop-shadow-lg border-gray-400"
                                    }`}
                                    onClick={() => {}}
                                >
                                    <div className="flex justify-between items-center">
                                        <div className="flex-1">
                                            <h2 className="font-semibold text-lg">{job}</h2>
                                            <p className="text-sm text-gray-600">
                                                <span className="font-medium">Company:</span> {details.company}
                                            </p>
                                            <p className="text-sm text-gray-600">
                                                <span className="font-medium">Job Dates:</span> {details["job dates"]}
                                            </p>
                                        </div>
                                        <div className="flex items-center justify-center w-12 h-12">
                                            <Image
                                                src={checkedStates.experiences[job].selected ? "/check_mark_green.jpg" : "/check_mark_gray.jpg"}
                                                alt="Check"
                                                width={40}
                                                height={40}
                                            />
                                        </div>
                                    </div>

                                    {/* Nested Perspectives Inside the Experience Block */}
                                    <div className="mt-4 space-y-2">
                                        {Object.entries(details.perspectives).map(([perspective, points], perspectiveIndex) => (
                                            <div
                                                key={perspectiveIndex}
                                                className={`bg-gray-100 p-4 rounded-lg flex items-center justify-between cursor-pointer transition-shadow border ${
                                                    checkedStates.experiences[job].perspectives[perspective]
                                                        ? "shadow-[inset_-2px_-2px_6px_rgba(0,0,0,0.2)] border-green-500"
                                                        : "drop-shadow-sm border-gray-300"
                                                }`}
                                                onClick={() => togglePerspective(job, perspective)}
                                            >
                                                <div className="flex-1">
                                                    <h3 className="font-medium">{perspective}</h3>
                                                    <ul className="text-sm text-gray-600 list-disc pl-5">
                                                        {points.map((point, i) => (
                                                            <li key={i}>{point}</li>
                                                        ))}
                                                    </ul>
                                                </div>
                                                <div className="flex items-center justify-center w-10 h-10">
                                                    <Image
                                                        src={
                                                            checkedStates.experiences[job].perspectives[perspective]
                                                                ? "/check_mark_green.jpg"
                                                                : "/check_mark_gray.jpg"
                                                        }
                                                        alt="Check"
                                                        width={30}
                                                        height={30}
                                                    />
                                                </div>
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            </div>
                        ))}
                        {/* Awards Section */}
                        <h1 className="font-bold text-xl mb-4">Awards</h1>
                        {Object.entries(resumeData["awards"]).map(([award, details], awardIndex) => (
                            <div
                                key={awardIndex}
                                className={`bg-white p-6 mb-4 rounded-xl flex items-center justify-between cursor-pointer transition-shadow border ${
                                    checkedStates.awards[award]
                                        ? "shadow-[inset_-2px_-2px_6px_rgba(0,0,0,0.2)] border-green-600"
                                        : "drop-shadow-lg border-gray-400"
                                }`}
                                onClick={() =>
                                    setCheckedStates((prev) => ({
                                        ...prev,
                                        awards: {
                                            ...prev.awards,
                                            [award]: !prev.awards[award]
                                        }
                                    }))
                                }
                            >
                                <div className="flex-1">
                                    <h2 className="font-semibold">{award}</h2>
                                    <p className="text-sm text-gray-600">
                                        <span className="font-medium">Institution:</span> {details.institution}
                                    </p>
                                    <p className="text-sm text-gray-600">
                                        <span className="font-medium">Award Date:</span> {details["award date"]}
                                    </p>
                                </div>
                                <div className="flex items-center justify-center w-12 h-12">
                                    <Image
                                        src={checkedStates.awards[award] ? "/check_mark_green.jpg" : "/check_mark_gray.jpg"}
                                        alt="Check"
                                        width={40}
                                        height={40}
                                    />
                                </div>
                            </div>
                        ))}
                    </div>

                    <div className="flex items-center justify-center h-full">
                        <div className="flex items-center justify-center h-full flex-col">
                            <SaveNewResumePopupComponent />
                            <br />
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}





