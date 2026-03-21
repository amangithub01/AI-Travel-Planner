from langgraph.graph import StateGraph, START, END
from state import TravelState

# Import all 10 of your agents!
from agents.weather import weather_node
from agents.database_agent import cache_node
from agents.search import search_node
from agents.flight import flight_node
from agents.store import store_node
from agents.recommend import recommend_hotels_node, recommend_flights_node
from agents.itinerary import itinerary_node 
from agents.food import food_node          # <--- NEW IMPORT
from agents.attractions import attractions_node # <--- NEW IMPORT

# 1. Initialize the Graph
workflow = StateGraph(TravelState)

# 2. Add all the worker nodes
workflow.add_node("weather_agent", weather_node)
workflow.add_node("cache_agent", cache_node)
workflow.add_node("search_agent", search_node)
workflow.add_node("flight_agent", flight_node)
workflow.add_node("store_agent", store_node)
workflow.add_node("recommend_hotels", recommend_hotels_node)
workflow.add_node("recommend_flights", recommend_flights_node)
workflow.add_node("food_agent", food_node)             # <--- NEW NODE
workflow.add_node("attractions_agent", attractions_node) # <--- NEW NODE
workflow.add_node("itinerary_agent", itinerary_node) 

# 3. The Smart Router (Conditional Logic)
def route_after_cache(state: TravelState):
    """If cache hits, jump straight to recommendations. Else, run the live AI agents."""
    if state.get("cached_results", False):
        print("⚡ [Router] Cache hit! Bypassing live LLM and API searches.")
        return "recommend_hotels"
    else:
        print("🚦 [Router] Cache miss. Initiating live web extraction.")
        return "search_agent"

# 4. Wire the Edges (The Flowchart)
workflow.add_edge(START, "weather_agent")
workflow.add_edge("weather_agent", "cache_agent")

# Add the crossroad
workflow.add_conditional_edges("cache_agent", route_after_cache)

# Path A: The Live Search Route (Cache Miss)
workflow.add_edge("search_agent", "flight_agent")
workflow.add_edge("flight_agent", "store_agent")
workflow.add_edge("store_agent", "recommend_hotels")

# Path B: The Final Presentation (Both routes converge here)
workflow.add_edge("recommend_hotels", "recommend_flights")
workflow.add_edge("recommend_flights", "food_agent")        # <--- UPDATED FLOW
workflow.add_edge("food_agent", "attractions_agent")       # <--- NEW FLOW
workflow.add_edge("attractions_agent", "itinerary_agent")  # <--- NEW FLOW
workflow.add_edge("itinerary_agent", END) 

# 5. Compile the application
app = workflow.compile()