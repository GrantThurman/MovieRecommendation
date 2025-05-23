import pandas as pd
import gdown
import os

def download_file(url, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)  # ensure folder exists
    if not os.path.exists(output_path):
        gdown.download(url, output_path, quiet=False)

def load_movie_data():
    movies = pd.read_csv("data/movies.csv")

    movies.rename(columns={"movieId": "movie_id"}, inplace=True)
    movies["year"] = movies["title"].str.extract(r"\((\d{4})\)\s*$")
    movies["year"] = pd.to_numeric(movies["year"], errors="coerce")
    movies["clean_title"] = movies.title.str.lower().str.split("(", n=1).str[0].str.strip()
    movies.genres = movies.genres.str.replace("|", ", ")

    # Casting to smaller types
    movies["movie_id"] = movies["movie_id"].astype("int32")
    movies["genres"] = movies["genres"].astype("category")

    movie_ids = movies["movie_id"].tolist()
    return movies, movie_ids


def load_netflix_data():
    netflix_file_id = "1Qw5RhCshBus1qthFGdWCvF4JeZbT4jvr"
    url = f"https://drive.google.com/uc?id={netflix_file_id}"
    output_path = "data/netflix_titles.csv"
    download_file(url, output_path)

    netflix = pd.read_csv(output_path, on_bad_lines='skip', encoding="ISO-8859-1")
    ## Clean
    netflix = netflix.iloc[:, 0:12]  # Keep relevant columns
    # Rename columns to match previous dataset
    netflix = netflix.rename(columns={"listed_in": "genres", "release_year": "year"})
    # Ensure proper formatting
    netflix["year"] = pd.to_numeric(netflix["year"], errors="coerce")  # Convert to numeric
    netflix["clean_genres"] = netflix["genres"].str.lower().str.replace(" ", "_")  # Normalize genre formatting
    netflix["show_id"] = netflix["show_id"].str[1:].astype(int) # Convert IDs to integers
    netflix["clean_title"] = netflix.title.str.lower().str.strip()
    # Create a combined text feature column
    netflix["text_features"] = netflix["title"] + " " + netflix["clean_genres"] + " " + netflix["description"]

    netflix_ids = netflix["show_id"].tolist()

    return netflix, netflix_ids