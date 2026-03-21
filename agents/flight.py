import os
import requests
from state import TravelState

def flight_node(state: TravelState):
    """Fetches LIVE flight data scraping Google Flights via SerpAPI."""
    origin = state.get("origin", "JFK")
    destination = state.get("destination", "DXB")
    start_date = state.get("start_date", "2026-04-01")
    end_date = state.get("end_date", "2026-04-07") # <--- ADDED END DATE
    
    print(f"✈️ [Flight Agent] Searching LIVE Google Flights: {origin} to {destination}...")

    # Securely grab the API key from your .env file
    api_key = os.getenv("SERPAPI_API_KEY")
    if not api_key:
        print("❌ Missing SERPAPI_API_KEY in .env file.")
        return {"flight_candidates": []}

    # Set up the API request parameters for Google Flights
    params = {
        "engine": "google_flights",
        "departure_id": origin,
        "arrival_id": destination,
        "outbound_date": start_date,
        "return_date": end_date,      # <--- ADDED RETURN DATE FOR ROUND TRIP
        "currency": "USD",
        "hl": "en",
        "api_key": api_key
    }

    try:
        # Make the live API call
        response = requests.get("https://serpapi.com/search", params=params)
        data = response.json()
        
        # --- NEW DEBUG LINES ---
        if "error" in data:
            print(f"🚨 SerpAPI FLIGHT Error: {data['error']}")
        # -----------------------
        
        # Extract the top flights from the 'best_flights' list
        best_flights = data.get("best_flights", [])
        
        live_flights = []
        for flight in best_flights[:3]: # Grab the top 3 deals
            # Safely navigate the JSON response
            airline = flight.get("flights", [{}])[0].get("airline", "Unknown Airline")
            price = flight.get("price", 0)
            url = f"https://www.google.com/travel/flights?q=Flights%20from%20{origin}%20to%20{destination}"
            
            live_flights.append({
                "airline": airline,
                "price": price,
                "url": url
            })
        
        if live_flights:
            print(f"✅ Live Flights Found: {len(live_flights)} options.")
        else:
            print("⚠️ No live flights found for this route/date.")
            
        return {"flight_candidates": live_flights}

    except Exception as e:
        print(f"❌ API Error: {e}")
        return {"flight_candidates": []}