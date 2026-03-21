import os
import requests
from state import TravelState
from langchain_community.llms import Ollama

# 1. Connect to your local Gemma model
local_llm = Ollama(model="gemma:2b")

def get_city_from_code(airport_code: str) -> str:
    print(f"\n🧠 [Local AI] Translating: {airport_code}...")
    # New ultra-strict prompt
    prompt = f"Return ONLY the city name for airport code {airport_code}. One word only. No sentences. Example: BOM -> Mumbai. Now do: {airport_code} ->"
    
    try:
        city_name = local_llm.invoke(prompt).strip()
        # If Gemma still gives a sentence, we take only the last word
        city_name = city_name.split()[-1].replace('.', '') 
        print(f"🤖 [Local AI] Gemma result: {city_name}\n")
        return city_name
    except Exception as e:
        return airport_code

def search_node(state: TravelState):
    """Fetches LIVE hotel data scraping Google Hotels via SerpAPI."""
    destination_code = state.get("destination", "LHR")
    start_date = state.get("start_date", "2026-04-01")
    end_date = state.get("end_date", "2026-04-07")
    
    print(f"🔍 [Search Agent] Preparing hotel search for code: {destination_code}...")

    # 2. Translate the code to a full city name using Gemma!
    full_city_name = get_city_from_code(destination_code)

    # Securely grab the API key
    api_key = os.getenv("SERPAPI_API_KEY")
    if not api_key:
        print("❌ Missing SERPAPI_API_KEY in .env file.")
        return {"hotel_candidates": []}

    # Set up the API parameters for Google Hotels
    params = {
        "engine": "google_hotels",
        "q": full_city_name, # 3. Use the FULL CITY NAME here instead of the code!
        "check_in_date": start_date,
        "check_out_date": end_date,
        "currency": "USD",
        "hl": "en",
        "api_key": api_key
    }

    try:
        # Make the live API call
        print(f"🌍 [Search Agent] Sending query to Google Hotels: 'Hotels in {full_city_name}'")
        response = requests.get("https://serpapi.com/search", params=params)
        data = response.json()
        
        # --- NEW DEBUG LINES ---
        if "error" in data:
            print(f"🚨 SerpAPI HOTEL Error: {data['error']}")
        # -----------------------
        
        properties = data.get("properties", [])
        live_hotels = []
        
        # Grab the top 4 hotel deals
        for hotel in properties[:4]:
            name = hotel.get("name", "Unknown Hotel")
            # Google Hotels nests the price, so we safely extract it
            price = hotel.get("rate_per_night", {}).get("extracted_lowest", 200.0)
            rating = hotel.get("overall_rating", 0.0)
            url = hotel.get("link", "https://google.com/travel/hotels")
            
            live_hotels.append({
                "name": name,
                "price": float(price) if price else 0.0,
                "rating": float(rating) if rating else 0.0,
                "url": url
            })
        
        if live_hotels:
            print(f"✅ Live Hotels Found: {len(live_hotels)} options.")
        else:
            print("⚠️ No live hotels found for this route/date.")
            
        return {"hotel_candidates": live_hotels}

    except Exception as e:
        print(f"❌ API Error: {e}")
        return {"hotel_candidates": []}