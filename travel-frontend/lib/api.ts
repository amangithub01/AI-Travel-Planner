export async function planTrip(data: {
    origin: string;
    destination: string;
    start_date: string;
    end_date: string;
    max_price: number;
}) {
    const response = await fetch("http://127.0.0.1:8000/plan-trip", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
    });

    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Failed to fetch itinerary");
    }

    return response.json();
}