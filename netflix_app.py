## Imports
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from annoy import AnnoyIndex
import os
from app.data_loader import load_netflix_data
from app.recommender import verify_movie, recommend_movies
from app.utils import setup_annoy_index


# Load data and index
netflix_data, netflix_ids = load_netflix_data()
annoy_index = setup_annoy_index(netflix_data, "models/netflix_index.ann", "text_features")


# # Find similar shows/movies
# def get_similar_titles(title, n=5):
#         idx = netflix_data[netflix_data["title"].str.lower() == input.lower()].index[0]
#         similar_idxs = annoy_index.get_nns_by_item(idx, n + 1)[1:]  # Skip the query item
#         return netflix_data.loc[similar_idxs, "title"].tolist()
        
    
    

title_input = input("Enter a movie/show title: ")
recommendations = recommend_movies(verify_title(title_input, netflix_data), netflix_data, annoy_index, netflix_ids, amount=5)
print("Recommended Titles:", recommendations)