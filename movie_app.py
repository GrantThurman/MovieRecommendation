"""
This app recommends movies to a user based on a movie entered by the user.
(Contains movies from 1950 to 2019)
Author: Grant Thurman
Date: 2025-4-12
"""

# Imports
import streamlit as st
import pandas as pd

from app.data_loader import load_movie_data
from app.recommender import verify_title, recommend_movies
from app.utils import setup_annoy_index

# Load data and index
movie_data, movie_ids = load_movie_data()
annoy_index = setup_annoy_index(movie_data, "models/movie_index.ann", "genres")

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

st.markdown("<h1 color: 18230F> 🎬 Movie Recommendation System </h1>", unsafe_allow_html=True)
st.markdown("Enter a movie title to get recommendations!")

movie_input = st.text_input("Movie Title: ").lower().strip()
if movie_input:
    movie_matches = verify_title(movie_input, movie_data, "clean_title")

    if movie_matches is None:
        st.write("Movie not found!")
    elif isinstance(movie_matches, pd.Series):  # Single match
        recommendations = recommend_movies(movie_matches["movie_id"], movie_data, annoy_index, movie_ids, amount=10)
        st.write("Movies similar to", movie_matches["title"], ":")
        recommendations = recommendations[["title", "genres"]].reset_index(drop=True)
        recommendations.columns = [col.capitalize() for col in recommendations.columns]
        recommendations.index += 1  # start numbering at 1
        st.table(recommendations)
    else:  # Multiple matches
        selected_movie = st.selectbox(
            "Multiple movies found. Please choose one:",
            movie_matches["title"].tolist(),
            index=0
        )
        selected_movie_data = movie_matches[movie_matches["title"] == selected_movie].iloc[0]
        recommendations = recommend_movies(selected_movie_data["movie_id"], movie_data, annoy_index, movie_ids, amount=10)
        st.write("Movies similar to", selected_movie, ":")
        recommendations = recommendations[["title", "genres"]].reset_index(drop=True)
        recommendations.columns = [col.capitalize() for col in recommendations.columns]
        recommendations.index += 1  # start numbering at 1
        st.table(recommendations)
