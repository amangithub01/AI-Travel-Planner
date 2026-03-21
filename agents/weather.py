import requests
from state import TravelState

def weather_node(state: TravelState):
    """Fetches LIVE weather data using the free Open-Meteo API."""
    destination = state.get("destination", "London")
    print(f"🌤️ [Weather Agent] Fetching LIVE weather for {destination}...")

    try:
        # Step 1: Convert the city name into Latitude and Longitude
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={destination}&count=1"
        geo_response = requests.get(geo_url).json()
        
        if "results" not in geo_response:
            print("❌ Could not find city coordinates.")
            return {"weather_summary": f"Could not find weather for {destination}."}
            
        lat = geo_response["results"][0]["latitude"]
        lon = geo_response["results"][0]["longitude"]
        
        # Step 2: Use the coordinates to get the current live weather
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        weather_response = requests.get(weather_url).json()
        
        current = weather_response.get("current_weather", {})
        temp = current.get("temperature", "Unknown")
        wind = current.get("windspeed", "Unknown")
        
        summary = f"Currently {temp}°C with wind speeds of {wind} km/h."
        print(f"✅ Live Weather Found: {summary}")
        
        return {"weather_summary": summary}
        
    except Exception as e:
        print(f"❌ API Error: {e}")
        return {"weather_summary": "Weather service currently unavailable."}