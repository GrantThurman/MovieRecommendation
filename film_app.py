"""
This app recommends movies to a user based on a movie entered by the user.
(Contains movies from 1950 to 2019)
Author: Grant Thurman
Date: 2025-4-12
"""

# Imports
import streamlit as st
import pandas as pd

from app.data_loader import load_movie_data, load_netflix_data
from app.recommender import verify_title, recommend_movies
from app.utils import setup_annoy_index

# Load data and index
movie_data, movie_ids = load_movie_data()
movie_annoy_index = setup_annoy_index(movie_data, "models/movie_index.ann", "genres", rebuild=True)

netflix_data, netflix_ids = load_netflix_data()
netflix_annoy_index = setup_annoy_index(netflix_data, "models/netflix_index.ann", "text_features", rebuild=False)

# Streamlit UI
st.set_page_config(layout="wide")

# Background
st.markdown("""
    <style>
        .main {
            background-color: #f0f2f6;
        }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown("<h1 color: 18230F> 🎬 Film Recommendation System </h1>", unsafe_allow_html=True)

# Tabs
tab1, tab2 = st.tabs(["Movies", "Netflix"])

# Tab 1
tab1.markdown("Enter a movie title to get recommendations!")

movie_input = tab1.text_input("Movie Title: ").lower().strip()
if movie_input:
    movie_matches = verify_title(movie_input, movie_data, "clean_title")

    if movie_matches is None:
        tab1.write("Movie not found!")
    elif isinstance(movie_matches, pd.Series):  # Single match
        recommendations = recommend_movies(movie_matches["movie_id"], movie_data, movie_annoy_index, movie_ids, amount=10)
        #tab1.write("Movies similar to", movie_matches["title"], ":")
        recommendations = recommendations[["title", "genres"]].reset_index(drop=True)
        recommendations.columns = [col.capitalize() for col in recommendations.columns]
        recommendations.index += 1  # start numbering at 1
        tab1.table(recommendations)
    else:  # Multiple matches
        selected_movie = tab1.selectbox(
            "Multiple movies found. Please choose one:",
            movie_matches["title"].tolist(),
            index=0
        )
        selected_movie_data = movie_matches[movie_matches["title"] == selected_movie].iloc[0]
        recommendations = recommend_movies(selected_movie_data["movie_id"], movie_data, movie_annoy_index, movie_ids, amount=10)
        tab1.write("Movies similar to", selected_movie, ":")
        recommendations = recommendations[["title", "genres"]].reset_index(drop=True)
        recommendations.columns = [col.capitalize() for col in recommendations.columns]
        recommendations.index += 1  # start numbering at 1
        tab1.table(recommendations)

# Tab 2
tab2.markdown("Enter a Netflix title to get recommendations!")

netflix_input = tab2.text_input("Netflix Title: ").lower().strip()

# Checkboxes
include_movies = tab2.checkbox(label="Movies", value=True)
include_shows = tab2.checkbox(label="TV Shows", value=True)

if netflix_input:
    netflix_id = verify_title(netflix_input, netflix_data, "clean_title")

    if netflix_id is None:
        tab2.write("Title not found!")
    else:
        recommendations = recommend_movies(netflix_id["show_id"], netflix_data, netflix_annoy_index, netflix_ids, amount=10)
        recommendations = recommendations[["title", "genres", "type"]].reset_index(drop=True)
        # Filter the recommendations based on type
        if not include_movies:
            recommendations = recommendations[recommendations["type"] != "Movie"]
        if not include_shows:
            recommendations = recommendations[recommendations["type"] != "TV Show"]
        
        recommendations.columns = [col.capitalize() for col in recommendations.columns]
        recommendations.index += 1  # start numbering at 1
        tab2.table(recommendations)
