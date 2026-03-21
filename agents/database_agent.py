import sqlite3
from state import TravelState

def cache_node(state: TravelState):
    """Checks the local database for both hotels AND flights."""
    destination = state.get("destination", "").lower()
    print(f"🗄️ [Cache Agent] Checking database for '{destination}'...")

    conn = sqlite3.connect('travel_cache.db')
    cursor = conn.cursor()

    # --- 🌟 NEW SAFETY CODE: Create tables if they don't exist yet ---
    cursor.execute('''CREATE TABLE IF NOT EXISTS accommodations (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        name TEXT, 
        location_city TEXT, 
        price_per_night REAL, 
        rating REAL, 
        url TEXT
    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS flights (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        airline TEXT, 
        origin TEXT, 
        destination TEXT, 
        price REAL, 
        url TEXT
    )''')
    conn.commit()
    # ----------------------------------------------------------------

    # 1. Grab the Hotels
    cursor.execute("SELECT name, price_per_night, rating, url FROM accommodations WHERE LOWER(location_city) = ?", (destination,))
    hotel_rows = cursor.fetchall()
    cached_hotels = [{"name": row[0], "price": row[1], "rating": row[2], "url": row[3]} for row in hotel_rows]
    
    # 2. Grab the Flights
    cursor.execute("SELECT airline, price, url FROM flights WHERE LOWER(destination) = ?", (destination,))
    flight_rows = cursor.fetchall()
    cached_flights = [{"airline": row[0], "price": row[1], "url": row[2]} for row in flight_rows]

    conn.close()

    if cached_hotels or cached_flights:
        print(f"✅ Cache Hit! Found {len(cached_hotels)} hotels and {len(cached_flights)} flights.")
        return {
            "hotel_candidates": cached_hotels, 
            "flight_candidates": cached_flights, # Now we are passing the flights to the state!
            "cached_results": True
        }
    else:
        print("❌ Cache Miss. Will need live search.")
        return {"cached_results": False}