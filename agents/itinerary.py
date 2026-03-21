import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from state import TravelState

def itinerary_node(state: TravelState):
    """Generates the final day-by-day itinerary using Groq (Llama 3)."""
    print("📝 [Itinerary Agent] Compiling the final day-by-day travel plan...")

    # Grab the API key to ensure it exists
    if not os.getenv("GROQ_API_KEY"):
        print("❌ Missing GROQ_API_KEY in .env file.")
        return {"final_itinerary": "Error: Missing Groq API Key."}

    # Initialize the ultra-fast Groq LLM
    try:
        llm = ChatGroq(
            model="llama-3.3-70b-versatile", # <--- UPDATED TO THE NEWEST MODEL
            temperature=0.7
        )
    except Exception as e:
        print(f"❌ Groq Initialization Error: {e}")
        return {"final_itinerary": "Error initializing AI Brain."}

    # Extract our gathered data
    destination = state.get("destination", "Unknown")
    start_date = state.get("start_date", "Unknown")
    end_date = state.get("end_date", "Unknown")
    weather = state.get("weather_summary", "No weather data.")
    flights = state.get("flight_candidates", [])
    hotels = state.get("hotel_candidates", [])

    # Format the data so the LLM can read it easily
    flight_text = "\n".join([f"- {f['airline']}: ${f['price']}" for f in flights]) if flights else "No flights booked."
    hotel_text = "\n".join([f"- {h['name']}: ${h['price']}/night (Rating: {h['rating']})" for h in hotels]) if hotels else "No hotels booked."

    # The Master Prompt
    template = """
    You are an expert, high-end travel concierge. Create a day-by-day itinerary for a trip to {destination} from {start_date} to {end_date}.

    Here is the live data you must incorporate:
    - Expected Weather: {weather}
    - Chosen Flights: {flights}
    - Chosen Hotels: {hotels}

    Your Output Requirements:
    1. Introduction: Briefly welcome them to {destination} and mention how to pack for the {weather}.
    2. Local Transit Hack: Explicitly tell the user the best way to get around (e.g., "Do not use Uber here, use Grab" or "The Metro is the best option").
    3. Day-by-Day Plan: Provide a realistic morning, afternoon, and evening schedule. 
    4. Local Food: Suggest a famous local dish they MUST try while they are there.

    Format this beautifully using Markdown. Keep it engaging but highly practical.
    """

    prompt = PromptTemplate(
        input_variables=["destination", "start_date", "end_date", "weather", "flights", "hotels"],
        template=template
    )

    chain = prompt | llm

    try:
        # Generate the final response
        # Update this part inside itinerary_node:
        response = chain.invoke({
            "destination": destination,
            "start_date": start_date,
            "end_date": end_date,
            "weather": weather,
            "flights": flight_text,
            "hotels": hotel_text,
            "food": state.get("food_recommendations", []),      # <--- ADD THIS
            "sights": state.get("attraction_candidates", [])   # <--- ADD THIS
        })
        
        print("✅ Final Itinerary Generated Successfully!")
        return {"final_itinerary": response.content}

    except Exception as e:
        print(f"❌ LLM Generation Error: {e}")
        return {"final_itinerary": "Error generating itinerary due to AI provider limits."}