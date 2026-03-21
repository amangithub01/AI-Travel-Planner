import os
import requests
from state import TravelState

def food_node(state: TravelState):
    """Fetches LIVE restaurant data from Google Local via SerpAPI."""
    destination = state.get("destination", "Tokyo")
    print(f"🍽️ [Food Agent] Searching for top-rated local eats in {destination}...")

    api_key = os.getenv("SERPAPI_API_KEY")
    
    params = {
        "engine": "google_local",
        "q": f"best local food and restaurants in {destination}",
        "hl": "en",
        "api_key": api_key
    }

    try:
        response = requests.get("https://serpapi.com/search", params=params)
        data = response.json()
        
        local_results = data.get("local_results", [])
        top_eats = []
        
        for place in local_results[:5]:
            top_eats.append({
                "name": place.get("title"),
                "rating": place.get("rating"),
                "type": place.get("type"),
                "address": place.get("address")
            })
        
        if top_eats:
            print(f"✅ Food Agent Found: {len(top_eats)} restaurants.")
        return {"food_recommendations": top_eats}

    except Exception as e:
        print(f"❌ Food API Error: {e}")
        return {"food_recommendations": []}