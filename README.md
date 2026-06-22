🎬 CineBharat AI: Real-Time Discovery Engine

An exquisite, Apple-inspired dark glassmorphic movie discovery system tailored for regional Indian cinema (Malayalam, Hindi, Tamil, Telugu) and Hollywood. Moving away from static lookup systems, CineBharat AI utilizes advanced Natural Language Processing (NLP) to map user mood vibes to premium cinema.

📌 Project Overview

CineBharat AI is a highly optimized recommender system designed to deliver personalized movie matches. The architecture is split cleanly into a reactive, high-performance Streamlit frontend and a mathematically-grounded Vector Space Model backend.

By processing textual movie descriptions and metadata profiles through term-frequency vectors, the engine bypasses arbitrary keyword match limits to capture true thematic similarity.

✨ Core Engine Architecture & Algorithms

1. TF-IDF & Cosine Similarity Engine

At the heart of the discovery logic is a Content-Based Filtering algorithm powered by Scikit-Learn:

Vector Space Conversion: The engine concatenates descriptive summaries (overviews) and genre lists into a dense text corpus.

TF-IDF Weighting: A TfidfVectorizer isolates and down-weights common English stop-words while accentuating rare, thematic keywords.

Vector Overlap Mapping: When you select genres or timelines, the system translates your configuration into a search query vector, running cosine_similarity() across the database to rank movies based on mathematical angular proximity.

       [ User Query Vector ]
                │
                ▼
  [ Cosine Similarity Mapping ] ──► Rank Outputs by Angular Score
                ▲
                │
   [ Movie Candidate Vectors ]


2. Smart Shuffling & Fatigue Prevention

To replicate the fresh, changing feed of modern premium streaming apps, CineBharat AI implements a dynamic state-tracking shuffler:

Lookup State Mapping: Every user search query is mapped to a unique state lookup key:
(language_code, tuple(sorted(genre_names)), era)

Active Session Partitioning: The engine separates the top matching candidates into unseen and seen pools based on your current session history.

Reservoir Sampling: It pulls a random subset from the unseen candidates first. If you keep clicking search, it continuously shuffles the carousel. Once the entire catalog has been shown, it resets the lookup history automatically to prevent deadlocks.

3. Evergreen & Heuristic Filtering

Decade Mapping: Dynamically translates era vibes (e.g., Retro 80s, Millennium 00s) into precise chronological sorting rules.

Critically Acclaimed Skew (Evergreen): Prioritizes highly-rated, historically significant releases by enforcing a user score weighting factor ((Rating - 7.0) * 0.5), keeping timeless masterpieces at the top of your feed.

🎨 Premium UI Design System

The layout replicates the sleek, immersive interface of hardware media players and high-end streaming apps.

1. Color Palette & Visual Tokens

Element

Hex Color

Description

Deep Background

#0b0f19

Deep Obsidian Blue minimizing eye strain.

Gradients

#ffffff → #a5b4fc

Linear gradient masks for crisp header headers.

Borders

rgba(255, 255, 255, 0.05)

Micro-thin translucent borders mimicking etched glass.

Accent Glow

rgba(99, 102, 241, 0.4)

Royal Indigo highlight activated during hover states.

2. Typography

Enforces Google's geometric sans-serif font 'Inter' across all native Streamlit components and raw markdown blocks to provide highly legible, elegant screen presentations.

3. Glassmorphic Movie Cards

The results are loaded into floating, glassmorphic cards configured with subtle visual feedback:

Backdrop Filter: Softens behind-card layers using backdrop-filter: blur(12px).

Neon Hover Lift: Smooth CSS transition curves (transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1)) lift the cards slightly and cast an active indigo drop shadow when hovered over.

.movie-card:hover {
    transform: translateY(-4px);
    border-color: rgba(99, 102, 241, 0.4);
    box-shadow: 0 12px 20px -10px rgba(99, 102, 241, 0.15);
}


4. Playful Micro-Interactions

To elevate the loading transition experience, the interface displays random, cinema-themed status descriptors instead of generic system loaders:

🍿 Grabbing the warm popcorn & running offline TF-IDF similarity vectors on classics...

🎬 Initiating movie matrix transformations for your handpicked matches...

🎟️ Printing your virtual VIP tickets to some incredible masterpieces...

📂 Project Structure

📦 CineBharat-AI
 ┣ 📂 .venv                # Virtual environment packages
 ┣ 📜 .env                 # Root-level credential parameters
 ┣ 📜 app.py               # Streamlit application layout & UI design declarations
 ┣ 📜 recommender.py       # ML vector pipelines, dataset catalog, & state managers
 ┗ 📜 README.md            # Technical documentation


🚀 Local Installation & Setup

Follow these steps to set up and run CineBharat AI locally.

1. Clone the Directory

git clone [https://github.com/yourusername/CineBharat-AI.git](https://github.com/yourusername/CineBharat-AI.git)
cd CineBharat-AI


2. Configure Environment Variables

Create a .env file in the root folder (side-by-side with app.py) to hold your secure connection keys:

[!NOTE]
Make sure to place the .env file exactly in the root folder. Do not place it inside subdirectories or package folders like .venv.

# Root-level configuration file (.env)
API_KEY=your_32_character_api_key_here
READ_TOKEN=your_long_read_access_token_here


3. Set Up Virtual Environment

# Initialize Python virtual environment
python -m venv .venv

# Activate on Windows:
.\.venv\Scripts\Activate

# Activate on macOS/Linux:
source .venv/bin/activate


4. Install Dependencies

pip install -r requirements.txt


5. Launch the Application

streamlit run app.py


🛠️ Technology Stack

Language: Python 3.8+

Framework: Streamlit

Libraries: Scikit-Learn (TF-IDF Vectorization, Cosine Similarity), Pandas, Numpy, Dotenv

Design Elements: HTML5, CSS3, Google Fonts ('Inter')

Built by Ansar ❤️ - Data Scientist & Engineer