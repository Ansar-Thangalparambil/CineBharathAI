import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# 1. Load Data
movies = pd.read_csv("movies.csv")
movies['genres'] = movies['genres'].fillna('')

# 2. Build the Matrix
tfv = TfidfVectorizer(stop_words='english')
tfv_matrix = tfv.fit_transform(movies['genres'])
cosine_sim = cosine_similarity(tfv_matrix, tfv_matrix)

# We need a way to look up a movie's index number based on its title
# This creates a pandas Series where the index is the title, and the value is the ID
indices = pd.Series(movies.index, index=movies['title']).drop_duplicates()

# 3. The Recommendation Engine Function
def get_recommendations(title, cosine_sim=cosine_sim):
    # Check if the movie is actually in our database
    if title not in indices:
        return "Movie not found in database. Check your spelling!"
    
    # Get the index of the movie that matches the title
    idx = indices[title]

    # Get the pairwise similarity scores of all movies with that movie
    # This turns a row of the matrix into a list of (index, score) tuples
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort the movies based on the similarity scores in descending order (highest first)
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the scores of the 5 most similar movies (ignoring the 1st one, which is the movie itself)
    sim_scores = sim_scores[1:6]

    # Get the movie indices
    movie_indices = [i[0] for i in sim_scores]

    # Return the top 5 most similar movies
    return movies['title'].iloc[movie_indices]

# Let's test it out!
print("--- Recommendations for 'Toy Story (1995)' ---")
print(get_recommendations('Toy Story (1995)'))

print("\n--- Recommendations for 'Dark Knight, The (2008)' ---")
print(get_recommendations('Dark Knight, The (2008)'))