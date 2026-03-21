# 🌍 AI Agentic Travel Planner

### *Smart itineraries, live weather, and curated stays powered by Local AI Agents.*

![Project Status](https://img.shields.io/badge/Status-Completed-success)
![Tech Stack](https://img.shields.io/badge/Stack-LangGraph%20|%20Next.js%20|%20Ollama-blue)

An advanced Multi-Agent Travel Architect that automates the entire vacation planning process. Built with **LangGraph** for orchestration and **Ollama (Gemma:2b)** for local intelligent reasoning.

---

## 🚀 The Multi-Agent Architecture
This project uses a decentralized agentic workflow to handle complex travel constraints:

* **🧠 Local AI Translator (Gemma:2b):** Acts as the bridge between human-readable city names and strict 3-letter IATA airport codes.
* **🌤️ Weather Agent:** Fetches real-time climate data for the destination.
* **✈️ Flight Agent:** Scrapes live Google Flights data for the best deals.
* **🏨 Hotel Agent:** Filters and recommends stays based on user ratings and budget.
* **📝 Itinerary Agent:** Compiles a day-by-day travel guide with "Must-Eat" local food and transit hacks.
* **🗄️ Cache Agent:** A persistent SQLite layer that optimizes repeat searches and reduces API latency.

---

## 🛠️ Tech Stack
| Category | Tools |
| :--- | :--- |
| **Backend** | Python, FastAPI, LangGraph, LangChain |
| **Local LLM** | Ollama (Gemma:2b) |
| **Frontend** | Next.js 15, Tailwind CSS, Lucide Icons |
| **Database** | SQLite3 |
| **APIs** | SerpAPI (Google Search), OpenWeather |

---

## 📸 Project Showcase
> **[INSERT LINK TO YOUR VIDEO DEMO OR GIF HERE]**
> *Watch the video to see Gemma:2b translating codes in the terminal while the UI updates in real-time!*

### Key Features:
* **Real-time Processing:** Watch the terminal logs to see agents collaborating.
* **Budget-Aware Recommendations:** Intelligent filtering for hotels.
* **Export to PDF:** Take your AI-generated plan with you instantly.
* **Local-First AI:** Privacy-focused reasoning using Ollama.

---

## 🏃 Setup & Installation

### 1. Prerequisite: Install Ollama
Download Ollama and pull the Gemma model:
```bash
ollama pull gemma:2b

Backend Setup
cd AI-Travel-Planner
python -m venv venv
source venv/bin/activate  # Or venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn main:app --reload

Frontend Setup
cd travel-frontend
npm install
npm run dev


🛡️ Security Note
This project requires a .env file for SerpAPI and Weather keys. Never commit your .env file to GitHub. A template .env.example is provided for reference.

Built with ❤️ by Aman Kumar 3rd Year B.Tech CSE Student | Backend & AI Enthusiast


