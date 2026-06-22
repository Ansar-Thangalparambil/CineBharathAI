🎬 CineBharat AI: Real-Time Discovery Engine

📌 Project Overview

CineBharat AI is an advanced, full-stack real-time movie discovery engine tailored specifically for Indian Regional Cinema (Malayalam, Hindi, Tamil, Telugu) and Hollywood. Moving away from static datasets, this platform interacts directly with live cloud movie registry endpoints. It features an exquisite, Apple-inspired dark glassmorphism UI built entirely in Python, accompanied by a resilient backend logic layer.

This system is engineered to solve core API challenges, such as ISP censorship blockages, caching rate-limits, and content repetition fatigue.

✨ Key Features & Architectural Algorithms

1. Smart Shuffling & Impression Fatigue Prevention

Tired of seeing the exact same 10 movies on every search refresh? CineBharat AI resolves this using a State-Tracking Recommendation Shuffler in the backend:

Lookup State Mapping: Every user search query is mapped to a unique state tuple: (language_code, tuple(sorted(genre_names)), era).

State Partitioning: The engine dynamically separates the incoming film API candidates into two matrices: unseen and seen movies relative to the active session.

Non-overlapping Extraction: The application draws randomly from the unseen list. This mathematically guarantees 0% duplication on successive clicks, cycling through the entire candidate pool before resetting the history cache cleanly.

2. Multi-Proxy Failover & Alternate Domain Routing

To guarantee 100% service uptime against regional ISP firewalls (such as Jio/Airtel censorship blocks) and network hiccups:

Alternate Domain Flipping: If the connection to the primary film database server is blocked or fails, the engine seamlessly redirects calls to the official alternate global database endpoint with zero user interruption.

Multi-Proxy Chain: Fallback routing processes requests through five secure public CORS proxy strategies (Direct, CorsProxy, AllOrigins, CodeTabs, and ThingProxy).

Cache-Buster Appender: Appends a dynamic randomized integer (_cb) specifically to the proxy structures. This forces intermediate proxy nodes to bypass local caches and fetch fresh live payloads without corrupting query parameters.

3. Highly Granular Movie Vibes

Decade Partitioning: Seamlessly query specific cinematic eras (80s, 90s, 00s, 10s, 20s) with automated ISO date boundary parameters.

Separated Genres: Unlike typical engines, "Feel-Good" (mapped to lighthearted, mood-boosting releases) and "Romance" (mapped to standard romance) are separated into individual genres for more precise recommendation targeting.

Evergreen Masterpieces: Employs an index-ranking query filter that isolates obscure releases by enforcing a vote threshold (vote_count.gte=50) and sorting exclusively by maximum user score.

4. High-End Glassmorphic Frontend

Designed with a premium dark cinematic aesthetic matching an Apple TV or Netflix look:

Implements dynamic custom CSS injected seamlessly inside Streamlit.

Glassmorphic elements with translucent borders, subtle box shadows, and responsive floating hover transformations.

Playful, Zomato-style cinema-themed random status loading text (e.g., "🍿 Grabbing the warm popcorn...", "🎟️ Printing your VIP front-row tickets...") instead of dull, technical loading spinners.

📂 File Architecture

📦 CineBharat-AI
 ┣ 📂 .venv                # Virtual environment library (collapsed)
 ┣ 📜 .env                 # ROOT LEVEL environment variables (API Keys)
 ┣ 📜 app.py               # Clean Frontend presentation & layout styling (reaches to backend)
 ┣ 📜 recommender.py       # Centralized backend, credential auditing, and API pipelines
 ┗ 📜 README.md            # System documentation


🚀 Local Installation & Setup

1. Clone the workspace directory

git clone [https://github.com/yourusername/CineBharat-AI.git](https://github.com/yourusername/CineBharat-AI.git)
cd CineBharat-AI


2. Configure your environment variables
Create a file named .env in the root folder (side-by-side with app.py) and supply either your v3 API Key or v4 Read Access Token:

# Root-level configuration file (.env)
TMDB_API_KEY=your_32_character_v3_api_key_here
# OR
TMDB_READ_TOKEN=your_long_v4_read_access_token_here


3. Initialize your python environment

python -m venv .venv

# Activate on Windows:
.\.venv\Scripts\Activate
# Activate on macOS/Linux:
source .venv/bin/activate


4. Install necessary libraries

pip install -r requirements.txt


5. Start the engine

streamlit run app.py


🛠️ Technology Stack

Language: Python 3.8+

Framework: Streamlit

Libraries: Requests, Pandas, Dotenv

Design Elements: HTML5, Modern CSS3 Flexbox

Built by Ansar ❤️ - Data Scientist & Engineer