from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # <-- NEW IMPORT
from pydantic import BaseModel
from graph import app as travel_graph
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize the FastAPI app
app = FastAPI(title="AI Travel Planner API")

# --- CORS MIDDLEWARE BLOCK ---
# This allows your Next.js frontend to talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (perfect for development)
    allow_credentials=True,
    allow_methods=["*"],  # Allows GET, POST, etc.
    allow_headers=["*"],
)
# ------------------------------


# Define the data structure we expect from the user
class TripRequest(BaseModel):
    origin: str
    destination: str
    start_date: str = "2026-04-01"
    end_date: str = "2026-04-07"
    max_price: float = 20000.0


@app.post("/plan-trip")
async def plan_trip(request: TripRequest):
    print(f"🚀 Received API request for {request.destination} from {request.origin}")

    # Set up the initial state for LangGraph
    initial_state = {
        "origin": request.origin,
        "destination": request.destination,
        "start_date": request.start_date,
        "end_date": request.end_date,
        "bedrooms": 1,
        "max_price": request.max_price,
        "min_rating": 4.0,
        "cached_results": False,
        "weather_summary": None,
        "hotel_candidates": [],
        "flight_candidates": [],
        "food_recommendations": [],  # <-- Added to state
        "attraction_candidates": [],  # <-- Added to state
        "final_itinerary": None,
    }

    # Run the graph
    final_state = travel_graph.invoke(initial_state)

    # --- NEW: CHECK FOR BUDGET ERROR BEFORE RETURNING DATA ---
    if final_state.get("error"):
        print(f"⚠️ Sending budget warning to frontend: {final_state.get('error')}")
        return {
            "status": "error",
            "message": final_state.get("error"),  # This sends Gemma's warning to the UI
        }

    # Return a clean JSON response to the browser/frontend
    return {
        "status": "success",
        "weather": final_state.get("weather_summary", "No weather data found."),
        "flights": final_state.get("flight_candidates", []),
        "hotels": final_state.get("hotel_candidates", []),
        "food": final_state.get("food_recommendations", []),  # <-- NEW
        "attractions": final_state.get("attraction_candidates", []),  # <-- NEW
        "itinerary": final_state.get("final_itinerary", "No itinerary generated."),
    }
