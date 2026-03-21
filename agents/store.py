import sqlite3
from state import TravelState

def store_node(state: TravelState):
    """
    Store Node: Writes fresh results to the database when a cache miss occurs.
    """
    # If we already used the cache, we don't need to save anything new!
    if state.get("cached_results", False):
        return {}

    print("💾 [Store Node] Saving new results to database cache...")
    destination = state.get("destination", "Unknown")
    origin = state.get("origin", "Unknown")
    hotels = state.get("hotel_candidates", [])
    flights = state.get("flight_candidates", [])

    conn = sqlite3.connect('travel_cache.db')
    cursor = conn.cursor()

    # Save new hotels
    for hotel in hotels:
        cursor.execute(
            "INSERT INTO accommodations (name, location_city, price_per_night, rating, url) VALUES (?, ?, ?, ?, ?)",
            (hotel.get("name"), destination, hotel.get("price"), hotel.get("rating"), hotel.get("url"))
        )
    
    # Save new flights
    for flight in flights:
        cursor.execute(
            "INSERT INTO flights (airline, origin, destination, price, url) VALUES (?, ?, ?, ?, ?)",
            (flight.get("airline"), origin, destination, flight.get("price"), flight.get("url"))
        )

    conn.commit()
    conn.close()
    
    return {} # We don't need to update the state here, just the external database