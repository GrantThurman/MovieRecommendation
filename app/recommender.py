def verify_movie(movie_input, data):
    matches = data[data["clean_title"] == movie_input]
    if len(matches) == 0:
        return None
    elif len(matches) == 1:
        return matches.iloc[0]
    else:
        return matches.drop_duplicates(subset=["movie_id"])

def get_similar_movies(movie_id, data, annoy_index, movie_ids, amount):
    index_val = movie_ids.index(movie_id)
    similar_indices = annoy_index.get_nns_by_item(index_val, amount + 1)[1:]
    similar_indices = [i for i in similar_indices if movie_ids[i] != movie_id]
    return data.iloc[similar_indices]

def recommend_movies(movie_id, data, annoy_index, movie_ids, amount):
    recommended = get_similar_movies(movie_id, data, annoy_index, movie_ids, amount)
    return recommended[["title", "genres"]].reset_index(drop=True)