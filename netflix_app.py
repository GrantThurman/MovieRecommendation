## Imports
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from annoy import AnnoyIndex
import os
from app.data_loader import load_netflix_data
from app.utils import setup_annoy_index


# Load data and index
netflix_data, netflix_ids = load_netflix_data()
annoy_index = setup_annoy_index(netflix_data, "models/netflix_index.ann", "text_features")

# Find similar shows/movies
def get_similar_titles(title, n=5):
    # Find the index of the given title
    title_row = netflix_data[netflix_data["title"].str.lower() == title.lower()]

    if title_row.empty:
        return "Title not found in dataset."

    title_index = title_row.index[0]  # Get the row index

    # Get similar movie/show indices from Annoy
    similar_indices = annoy_index.get_nns_by_item(title_index, n + 1)  # Get more to exclude input

    # Get recommended movies/shows
    recommended_titles = netflix_data.iloc[similar_indices[1:]]["title"].tolist()  # Exclude input title

    return recommended_titles

title_input = input("Enter a movie/show title: ")
recommendations = get_similar_titles(title_input, n=5)
print("Recommended Titles:", recommendations)