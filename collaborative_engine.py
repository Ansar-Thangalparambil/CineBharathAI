import pandas as pd
from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split
from surprise import accuracy

# 1. Load Data
ratings = pd.read_csv("ratings.csv")
movies = pd.read_csv("movies.csv")

# 2. Format the data for the Surprise library
# Surprise needs to know the scale of our ratings (1 to 5)
reader = Reader(rating_scale=(1, 5))
data = Dataset.load_from_df(ratings[['userId', 'movieId', 'rating']], reader)

# 3. Split the data (The Golden Rule of Machine Learning)
# We train the AI on 80% of the data, and test it on the remaining 20% to see if it's accurate
trainset, testset = train_test_split(data, test_size=0.20)

# 4. Initialize and Train the SVD Model (The Netflix Algorithm)
algo = SVD()
print("Training the AI on the matrix... (This might take a few seconds)")
algo.fit(trainset)

# 5. Test the AI's Accuracy
# We ask the AI to predict the ratings for the 20% of data we hid from it
predictions = algo.test(testset)

# RMSE = Root Mean Square Error (How far off the AI's guesses are on a 5-star scale)
error = accuracy.rmse(predictions)
print(f"--- AI Training Complete ---")
print(f"The AI can predict user ratings with an average error of: {error:.2f} stars.")

# 6. Let's make a real prediction!
# We know User #1 gave 'The Matrix' (Movie ID 2571) a 5.0. 
# Let's ask the AI to predict how User #1 would rate 'The Matrix Revolutions' (Movie ID 6934)
prediction = algo.predict(uid=1, iid=6934)
print(f"\nAI Prediction: User 1 will rate 'Matrix Revolutions' a {prediction.est:.2f} out of 5")