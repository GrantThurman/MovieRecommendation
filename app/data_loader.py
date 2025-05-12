import pandas as pd

def load_movie_data():
    movies = pd.read_csv("data/movies.csv")
    ratings = pd.read_csv("data/ratings.csv")

    movies["year"] = movies["title"].str.extract(r"\((\d{4})\)\s*$")
    movies["year"] = pd.to_numeric(movies["year"], errors="coerce")
    movies["clean_title"] = movies.title.str.lower().str.split("(", n=1).str[0].str.strip()
    movies.genres = movies.genres.str.replace("|", ", ")

    avg_ratings = ratings.groupby("movieId")["rating"].mean().reset_index()
    movies = movies.merge(avg_ratings, how="left", on="movieId")[movies["year"] > 1950]
    movies.rename(columns={"rating": "average_rating", "movieId": "movie_id"}, inplace=True)

    # Casting to smaller types
    movies["movie_id"] = movies["movie_id"].astype("int32")
    movies["year"] = movies["year"].astype("int32")
    movies["genres"] = movies["genres"].astype("category")
    movies["average_rating"] = pd.to_numeric(movies["average_rating"], downcast="float")

    movie_ids = movies["movie_id"].tolist()
    
    return movies, movie_ids


def load_netflix_data():
    netflix = pd.read_csv("data/netflix_titles.csv", encoding="ISO-8859-1")
    ## Clean
    netflix = netflix.iloc[:, 0:12]  # Keep relevant columns
    # Rename columns to match previous dataset
    netflix = netflix.rename(columns={"listed_in": "genres", "release_year": "year"})
    # Ensure proper formatting
    netflix["year"] = pd.to_numeric(netflix["year"], errors="coerce")  # Convert to numeric
    netflix["genres"] = netflix["genres"].str.lower().str.replace(" ", "_")  # Normalize genre formatting
    netflix["show_id"] = netflix["show_id"].str[1:].astype(int) # Convert IDs to integers
    # Create a combined text feature column
    netflix["text_features"] = netflix["title"] + " " + netflix["genres"] + " " + netflix["description"]

    netflix_ids = netflix["show_id"].tolist()

    return netflix, netflix_ids