import os
import requests
from state import TravelState

def attractions_node(state: TravelState):
    """Fetches LIVE tourist attractions using Foursquare Places API."""
    destination = state.get("destination", "Tokyo")
    print(f"🏛️ [Attraction Agent] Finding the best sights in {destination}...")

    api_key = os.getenv("FOURSQUARE_API_KEY")
    
    headers = {
        "accept": "application/json",
        "Authorization": api_key
    }

    # We search for 'Sights & Museums' (Category 10000)
    params = {
        "near": destination,
        "categories": "10000",
        "limit": 5
    }

    try:
        response = requests.get("https://api.foursquare.com/v3/places/search", params=params, headers=headers)
        data = response.json()
        
        results = data.get("results", [])
        sights = []
        
        for place in results:
            sights.append({
                "name": place.get("name"),
                "address": place.get("location", {}).get("formatted_address"),
                "category": place.get("categories", [{}])[0].get("name", "Sights")
            })
        
        if sights:
            print(f"✅ Foursquare Found: {len(sights)} attractions.")
        return {"attraction_candidates": sights}

    except Exception as e:
        print(f"❌ Foursquare API Error: {e}")
        return {"attraction_candidates": []}