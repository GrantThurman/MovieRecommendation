## Imports
import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from annoy import AnnoyIndex
import os
from app.data_loader import load_netflix_data
from app.recommender import verify_title, recommend_movies
from app.utils import setup_annoy_index


# Load data and index
netflix_data, netflix_ids = load_netflix_data()
annoy_index = setup_annoy_index(netflix_data, "models/netflix_index.ann", "text_features")

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

st.markdown("<h1 color: 18230F> Netflix Recommendation System </h1>", unsafe_allow_html=True)
st.markdown("Enter a title to get recommendations!")

title_input = st.text_input("Title: ").lower().strip()
title_id = verify_title(title_input, netflix_data, "clean_title")

recommendations = recommend_movies(title_id,netflix_data, annoy_index, netflix_ids, amount=5)
st.table(recommendations)