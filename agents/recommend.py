from state import TravelState

def recommend_hotels_node(state: TravelState):
    """Filters and ranks hotels based on user constraints."""
    print("⭐ [Hotel Recommender] Filtering hotels by budget...")
    candidates = state.get("hotel_candidates", [])
    max_price = state.get("max_price", 1000)

    # Keep only hotels under budget
    filtered_hotels = [h for h in candidates if h["price"] <= max_price]
    
    # Sort by rating (highest first)
    filtered_hotels.sort(key=lambda x: x.get("rating", 0), reverse=True)
    
    return {"hotel_candidates": filtered_hotels}

def recommend_flights_node(state: TravelState):
    """Filters and ranks flights based on price."""
    print("⭐ [Flight Recommender] Finding the best flight deals...")
    candidates = state.get("flight_candidates", [])
    
    # Sort by price (lowest first)
    sorted_flights = sorted(candidates, key=lambda x: x["price"])
    
    return {"flight_candidates": sorted_flights}