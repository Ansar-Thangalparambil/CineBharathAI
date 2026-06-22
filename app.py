import streamlit as st
from recommender import fetch_live_trending_movies

st.set_page_config(page_title="CineBharat AI", layout="wide")

st.title("🇮🇳 CineBharat AI: Real-Time Discovery Engine")

# Your API key is added directly here so you don't have to type it on screen
api_key = "39f7844eaa2a8a841f841249fb5989a7"

# Setup the UI Controls
language = st.selectbox(
    "Select Regional Cinema:",
    ["Malayalam", "Hindi (Bollywood)", "Tamil", "Telugu"]
)

# A dictionary to translate English names to TMDB language codes
lang_codes = {
    "Malayalam": "ml",
    "Hindi (Bollywood)": "hi",
    "Tamil": "ta",
    "Telugu": "te"
}

# The Live Fetch Button
if st.button(f"Fetch Live Trending {language} Movies"):
    with st.spinner('Connecting to live database...'):
        
        # Call our API function from recommender.py
        live_data = fetch_live_trending_movies(api_key, lang_codes[language])
        
        if not live_data.empty:
            st.subheader(f"🔥 Top Trending {language} Movies Right Now")
            
            # Display the data in a beautiful interactive table
            st.dataframe(
                live_data[['Title', 'Rating', 'Release Date', 'Overview']], 
                use_container_width=True,
                hide_index=True
            )
        else:
            st.error("Could not fetch data. Please check your internet connection or API key.")