import streamlit as st
# Import the functions we just wrote in recommender.py
from recommender import load_and_clean_data, compute_similarity_matrix, get_content_recommendations

st.title("🎬 Modular Movie Recommendation Hub")

# 1. Load data using cached functions from recommender file
movies = load_and_clean_data()
cosine_sim = compute_similarity_matrix(movies)

# 2. Setup the Dropdown
selected_movie = st.selectbox(
    "Select a movie you like:",
    movies['title'].values
)

# 3. Handle Button Click
if st.button("Get Recommendations"):
    # Call the recommendation logic engine from our other file
    results = get_content_recommendations(selected_movie, movies, cosine_sim)
    
    if results:
        st.subheader("You might also enjoy:")
        for idx, movie in enumerate(results, 1):
            st.write(f"🍿 **{idx}.** {movie}")
    else:
        st.error("Movie not found or error calculating results.")
        