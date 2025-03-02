import CryptoJS from "crypto-js";
import 'dotenv/config'

export const BASE_URL = "https://80e9-76-78-137-88.ngrok-free.app/";
export const SECRET_KEY = 'ekLKGgheI-GLEShglsa';

export const decryptData = (encryptedData) => {
    const bytes = CryptoJS.AES.decrypt(encryptedData, SECRET_KEY);
    const decryptedData = bytes.toString(CryptoJS.enc.Utf8);
    return decryptedData ? JSON.parse(decryptedData) : null;
};

export const encryptData = (data) => {
    return CryptoJS.AES.encrypt(JSON.stringify(data), SECRET_KEY).toString();
};

// Code to use when printing an api return
// {response && <pre className="mt-4 p-3 bg-gray-200 rounded-lg">{JSON.stringify(response, null, 2)}</pre>}
// {error && <p className="text-red-500">{error}</p>}