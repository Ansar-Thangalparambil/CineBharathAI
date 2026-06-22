import random
import streamlit as st
from recommender import get_movies_by_language_and_genres, GENRE_MAP, get_credential_status

# 1. Fetch centralized environment credentials and diagnostic state from recommender.py
config = get_credential_status()
credential = config["credential"]
has_valid_credential = config["has_valid_credential"]

st.set_page_config(page_title="CineBharat AI", page_icon="🎬", layout="wide")

# Premium Apple-style dark layout with CSS glassmorphism
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght=300;400;500;600;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] { 
        font-family: 'Inter', sans-serif; 
        background-color: #0b0f19; 
    }
    
    .app-title { 
        font-size: 3rem !important; 
        font-weight: 700; 
        letter-spacing: -1.5px;
        background: linear-gradient(135deg, #ffffff 30%, #a5b4fc 100%); 
        -webkit-background-clip: text; 
        -webkit-text-fill-color: transparent; 
        margin-bottom: 0.2rem; 
    }
    
    .subtitle {
        color: #64748b;
        font-size: 1.1rem;
        margin-bottom: 2.5rem;
    }
    
    .movie-card { 
        background: rgba(30, 41, 59, 0.4); 
        border: 1px solid rgba(255, 255, 255, 0.05); 
        border-radius: 16px; 
        padding: 24px; 
        margin-bottom: 20px; 
        backdrop-filter: blur(12px); 
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }
    
    .movie-card:hover { 
        transform: translateY(-4px); 
        border-color: rgba(99, 102, 241, 0.4); 
        box-shadow: 0 12px 20px -10px rgba(99, 102, 241, 0.15);
    }
    
    .movie-header { 
        display: flex; 
        justify-content: space-between; 
        align-items: center; 
        margin-bottom: 12px; 
    }
    
    .movie-title { 
        font-size: 1.4rem; 
        font-weight: 600; 
        color: #ffffff; 
        letter-spacing: -0.5px;
    }
    
    .rating-badge { 
        background: linear-gradient(135deg, #4f46e5 0%, #06b6d4 100%); 
        color: white; 
        padding: 5px 12px; 
        border-radius: 20px; 
        font-size: 0.85rem; 
        font-weight: 600; 
    }
    
    .movie-meta {
        color: #94a3b8;
        font-size: 0.85rem;
        margin-bottom: 12px;
    }
    
    .movie-overview { 
        color: #cbd5e1; 
        font-size: 0.95rem; 
        line-height: 1.6; 
    }
    </style>
""", unsafe_allow_html=True)

# Main Title Header Section
st.markdown('<h1 class="app-title">🎬 CineBharat AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Industry, Decades & Dynamic Multi-Genre Discovery Engine</p>', unsafe_allow_html=True)

# Step 1, 2 & 3: Interactive Layout columns
col1, col2, col3 = st.columns(3)

with col1:
    industry = st.selectbox(
        "Step 1: Choose Industry",
        ["Mollywood(Malayalam)", "Hindi (Bollywood)", "Tamil", "Telugu", "Hollywood"]
    )

with col2:
    genre_options = list(GENRE_MAP.keys())
    selected_genres = st.multiselect(
        "Step 2: Choose Genre vibe(s)", 
        genre_options, 
        default=["Comedy"]
    )

with col3:
    selected_era = st.selectbox(
        "Step 3: Choose Timeline vibe",
        [
            "✨ Evergreen (All-Time Masterpieces)",
            "📼 Retro 80s (1980 - 1989)",
            "📟 Golden 90s (1990 - 1999)",
            "💿 Millennium 00s (2000 - 2009)",
            "📱 Digital 10s (2010 - 2019)",
            "🚀 Modern 20s (2020s onward)"
        ]
    )

lang_codes = {
    "Mollywood(Malayalam)": "ml", 
    "Hindi (Bollywood)": "hi", 
    "Tamil": "ta", 
    "Telugu": "te", 
    "Hollywood": "en"
}

# Live Environmental Variable Warnings (Using clean, native Streamlit layout containers)
if not has_valid_credential:
    with st.container():
        st.markdown("### ⚠️ Environment Configuration Diagnostics")
        st.info(f"**Detected Key Source:** {config['key_source']}")
        st.info(f"**Loaded Key Length:** {config['key_length']} characters")
        st.error(f"**System Flag:** {config['diagnostic_reason']}")
        
        st.markdown("**How to resolve this in 3 quick steps:**")
        st.markdown(
            "1. Make sure your **.env** file is in the same directory as `app.py` and contains no spaces around the `=` sign.\n"
            "2. If you are using the v3 Key, replace the temporary placeholders in your key so that it is exactly **32 characters long**.\n"
            "3. **CRITICAL:** Stop your terminal by pressing `Ctrl + C` and restart it with `streamlit run app.py` to force Streamlit to flush its cache and load the new file variables."
        )

# Step 4: Fetch Live Recommendations
genre_label = " & ".join(selected_genres) if selected_genres else "Any"
era_short_name = selected_era.split(" ")[1] if len(selected_era.split(" ")) > 1 else "Masterpiece"

if st.button(f"Find {industry} {genre_label} {era_short_name} Movies", type="primary"):
    if not selected_genres:
        st.warning("Please select at least one genre to begin discovery!")
    elif not has_valid_credential:
        st.error("Cannot query TMDB: Please follow the diagnostic steps above to configure your active .env variables, then reload your Streamlit session!")
    else:
        # Innovative, Zomato/Swiggy-style fun cinema status generators
        fun_loading_lines = [
            f"🍿 Grabbing the warm popcorn & queueing up {genre_label} blockbusters...",
            f"🎬 Rolling the cameras for your handpicked {industry} matches...",
            f"🎟️ Printing your VIP front-row tickets to some timeless {genre_label} cinema...",
            f"📽️ Feeding your favorite cinematic flavors into the vintage projector...",
            f"✨ Curating the ultimate {genre_label} masterpieces just for you...",
            f"📦 Sifting through history's highest rated films to deliver the perfect platter..."
        ]
        chosen_message = random.choice(fun_loading_lines)
        
        with st.spinner(chosen_message):
            recommended_data = get_movies_by_language_and_genres(
                credential, 
                lang_codes[industry], 
                selected_genres, 
                era=selected_era
            )
            
            if not recommended_data.empty:
                first_title = recommended_data.iloc[0]['Title']
                if any(err_word in first_title for err_word in ["Failed", "Error", "Diagnostic", "Validation"]):
                    st.write("### 🔍 System Diagnostics")
                else:
                    st.write(f"### 🍿 Recommended **{industry}** Matchups ({selected_era.split(' ')[1]} vibe)")
                
                # Render results elegantly
                for _, row in recommended_data.iterrows():
                    st.markdown(f"""
                        <div class="movie-card">
                            <div class="movie-header">
                                <div class="movie-title">{row['Title']}</div>
                                <div class="rating-badge">★ {row['Rating']:.1f}</div>
                            </div>
                            <div class="movie-meta">📅 Released: {row['Release Date']}</div>
                            <div class="movie-overview">{row['Overview']}</div>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No matching movies found for this exact genre blend and decade. Try selecting standard genres or a different timeline vibe!")