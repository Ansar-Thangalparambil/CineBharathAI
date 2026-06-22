import pandas as pd

# Load the datasets
movies = pd.read_csv("movies.csv")
ratings = pd.read_csv("ratings.csv")

# 1. Group by movieId and calculate the average rating AND the total number of ratings
movie_stats = ratings.groupby('movieId').agg(
    avg_rating=('rating', 'mean'),
    num_ratings=('rating', 'count')
).reset_index()

# 2. Merge our new stats table with the movies table so we can see the titles
popular_movies = pd.merge(movie_stats, movies[['movieId', 'title']], on='movieId')

# 3. The "One-Hit Wonder" Filter
# A movie with one 5-star rating isn't better than a movie with 10,000 4.8-star ratings.
# Let's only look at movies that have been rated at least 50 times.
popular_movies = popular_movies[popular_movies['num_ratings'] >= 50]

# 4. Sort the movies by the highest average rating and grab the top 10
top_10_movies = popular_movies.sort_values(by='avg_rating', ascending=False).head(10)

print("\n--- Top 10 Movies (Our Cold Start Baseline) ---")
print(top_10_movies[['title', 'avg_rating', 'num_ratings']])