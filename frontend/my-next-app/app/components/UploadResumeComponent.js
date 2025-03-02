// "use client";
//
// import { useEffect, useState } from "react";
// import Cookies from "js-cookie";
// import { decryptData } from "@/app/config";
// import {router} from "next/client";
//
// export default function UploadResumeComponent() {
//     // const [error, setError] = useState(null);
//     // const [userSession, setUserSession] = useState(null);
//     // const [pdfFile, setPDFile] = useState(null);
//     // const [loading, setLoading] = useState(false);
//     //
//     // async function SendFakeData() {
//     //     router.push("/resumes");
//     // }
//     //
//     // async function sendData() {
//     //     if (!pdfFile || !userSession) {
//     //         setError("No file selected or session data missing.");
//     //         return;
//     //     }
//     //
//     //     const { username, password } = userSession;
//     //
//     //     setLoading(true); // Start loading
//     //
//     //     const formData = new FormData();
//     //     formData.append("pdf_binary", pdfFile); // Append the PDF file as FormData
//     //     formData.append("username", username);
//     //     formData.append("password", password);
//     //
//     //     try {
//     //         const res = await fetch("/api/uploadResumePDF", {
//     //             method: "POST",
//     //             body: formData, // Send FormData (not JSON)
//     //         });
//     //
//     //         if (!res.ok) {
//     //             const errorText = await res.text();
//     //             console.error("External API error response:", errorText);
//     //             throw new Error(`Error: ${res.status} ${res.statusText} - ${errorText}`);
//     //         }
//     //
//     //         // Handle successful response (optional)
//     //         console.log("PDF uploaded successfully.");
//     //     } catch (err) {
//     //         console.error("Error:", err.message);
//     //         setError(err.message);
//     //     } finally {
//     //         setLoading(false); // Stop loading
//     //     }
//     // }
//     //
//     // useEffect(() => {
//     //     console.log(pdfFile)
//     // }, [pdfFile])
//     //
//     // const handleFileChange = async (e) => {
//     //     const file = e.target.files[0];
//     //
//     //     if (file) {
//     //         try {
//     //             setPDFile(file); // Set the file directly (no need to use arrayBuffer)
//     //         } catch (error) {
//     //             console.error("Error reading file:", error);
//     //             setError("Failed to read the file.");
//     //         }
//     //     }
//     // };
//
//     return (
//         // <div className="flex flex-col items-center bg-gray-100 h-screen">
//         //     <h1 className="text-5xl m-15">Upload your main resumé</h1>
//         //     <div className="bg-white flex flex-col p-20 rounded-xl drop-shadow-lg">
//         //         <h1 className="text-3xl mb-5 text-center">Upload File</h1>
//         //         <input
//         //             className="p-20 border-2 border-dashed border-gray-500 rounded-xl mb-10"
//         //             type="file"
//         //             id="fileInput"
//         //             name="file"
//         //             accept="application/pdf"  // Only accept PDF files
//         //             onChange={handleFileChange}
//         //         />
//         //         <button
//         //             className="button-blue text-white py-4 px-12 rounded-xl text-xl w-auto self-center"
//         //             onClick={sendData()}
//         //             disabled={loading} // Disable button while uploading
//         //         >
//         //             {loading ? "Uploading..." : "Upload PDF"}
//         //         </button>
//         //         {error && <p className="text-red-500 mt-4">{error}</p>}
//         //
//         //         <button
//         //             className="button-blue text-white py-4 px-12 rounded-xl text-xl w-auto self-center"
//         //             onClick={SendFakeData()}
//         //             disabled={loading} // Disable button while uploading
//         //         >
//         //             {loading ? "Uploading..." : "Fake Upload PDF"}
//         //         </button>
//         //     </div>
//         // </div>
//     );
// }
