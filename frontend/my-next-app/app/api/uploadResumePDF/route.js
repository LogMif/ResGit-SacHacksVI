import { BASE_URL } from '../../config'

export async function POST(req) {
    try {
        const body = await req.json();
        console.log("Received body:", body);

        const res = await fetch(BASE_URL + 'add_to_history', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body),
        });

        console.log("External API response status:", res.status, res.statusText);

        if (!res.ok) {
            const errorText = await res.text();
            console.error("External API error response:", errorText);
            throw new Error(`Error: ${res.status} ${res.statusText} - ${errorText}`);
        }

        const data = await res.json();
        return Response.json({ success: true, data });
    } catch (error) {
        console.error("Server Error:", error);
        return Response.json({ success: false, error: error.message }, { status: 500 });
    }
}

