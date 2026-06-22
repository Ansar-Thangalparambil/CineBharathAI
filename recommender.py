import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def load_and_clean_data():
    """Loads raw dataset and injects custom Indian and Malayalam movies."""
    movies = pd.read_csv("movies.csv")
    
    indian_movies_data = {
        'movieId': [200001, 200002, 200003, 200004, 200005, 200006, 200007, 200008, 200009, 200010],
        'title': [
            '3 Idiots (2009)', 
            'Dangal (2016)', 
            'Sholay (1975)', 
            'RRR (2022)', 
            'Bahubali: The Beginning (2015)',
            'Dilwale Dulhania Le Jayenge (1995)',
            'Drishyam (2013)',            # Malayalam Mystery/Thriller
            'Kumbalangi Nights (2019)',   # Malayalam Comedy/Drama
            'Manichitrathazhu (1993)',    # Malayalam Horror/Psychological Thriller
            'Premam (2015)'               # Malayalam Romance/Comedy
        ],
        'genres': [
            'Comedy|Drama|Romance',
            'Drama|Action',
            'Action|Adventure|Comedy',
            'Action|Drama|Adventure',
            'Action|Adventure|Fantasy',
            'Comedy|Drama|Romance',
            'Crime|Drama|Mystery|Thriller',
            'Comedy|Drama|Romance',
            'Horror|Mystery|Thriller',
            'Comedy|Romance'
        ]
    }
    
    indian_movies_df = pd.DataFrame(indian_movies_data)
    combined_movies = pd.concat([movies, indian_movies_df], ignore_index=True)
    combined_movies['genres'] = combined_movies['genres'].fillna('')
    
    return combined_movies

def compute_similarity_matrix(df):
    """Turns movie genres into numerical vectors and calculates similarity."""
    tfv = TfidfVectorizer(stop_words='english')
    tfv_matrix = tfv.fit_transform(df['genres'])
    cosine_sim = cosine_similarity(tfv_matrix, tfv_matrix)
    return cosine_sim

def get_content_recommendations(title, df, cosine_sim):
    """Looks up a movie title and returns the top 5 closest matches."""
    indices = pd.Series(df.index, index=df['title']).drop_duplicates()
    
    if title not in indices:
        return []
        
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:6]
    movie_indices = [i[0] for i in sim_scores]
    return df['title'].iloc[movie_indices].tolist()