from typing import TypedDict, List, Optional, Annotated
from operator import add

class TravelState(TypedDict):
    # Core User Inputs
    origin: str
    destination: str
    start_date: str
    end_date: str
    bedrooms: int
    max_price: float
    min_rating: float
    
    # Routing Flags
    cached_results: bool
    
    # Agent Outputs
    weather_summary: Optional[str]
    
    # Using Annotated[List[dict], add] ensures results are appended 
    # and not overwritten as the graph moves between nodes.
    hotel_candidates: Annotated[List[dict], add]
    flight_candidates: Annotated[List[dict], add]
    
    # --- NEW DISCOVERY FIELDS ---
    food_recommendations: Annotated[List[dict], add]    # For SerpAPI Food results
    attraction_candidates: Annotated[List[dict], add]  # For Foursquare Attraction results
    
    # Final Presentation
    final_itinerary: Optional[str]