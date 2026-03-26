import os
from datetime import datetime
from state import TravelState
from langchain_community.llms import Ollama


def budget_node(state: TravelState):
    """Checks if the user's budget is realistic before scraping APIs."""
    print("💰 [Budget Agent] Evaluating financial constraints...")

    destination = state.get("destination", "Unknown")
    start_date_str = state.get("start_date", "")
    end_date_str = state.get("end_date", "")
    budget = state.get("max_price", 0)

    # 1. Calculate the total days of the trip
    try:
        start = datetime.strptime(start_date_str, "%Y-%m-%d")
        end = datetime.strptime(end_date_str, "%Y-%m-%d")
        days = (end - start).days
        if days <= 0:
            days = 1
    except:
        days = 5  # Fallback if dates are weird

    # 2. Set our baseline constraint ($100 per day minimum)
    min_required = days * 100

    if budget >= min_required:
        print("✅ [Budget Agent] Budget is sufficient.")
        return {"error": None}  # All good, continue the graph!

    # 3. If budget is too low, wake up Gemma to generate a custom warning
    print(
        f"⚠️ [Budget Agent] Budget ${budget} is too low for {days} days. Asking Gemma for advice..."
    )

    local_llm = Ollama(model="gemma:2b")

    prompt = f"""
    A user wants to travel to {destination} for {days} days with a total budget of ${budget} USD. 
    This is mathematically impossible. 
    
    Task: Write a ONE SENTENCE warning telling them this budget is too low, and suggest they need at least ${min_required} USD for a {days}-day trip to {destination}.
    """

    try:
        warning_msg = local_llm.invoke(prompt).strip()
        print(f"🤖 [Local AI] {warning_msg}")

        # We return this as an 'error' in the state so the frontend can catch it
        return {"error": warning_msg}

    except Exception as e:
        return {
            "error": f"Budget too low. Please increase your budget to at least ${min_required} for a {days}-day trip."
        }
