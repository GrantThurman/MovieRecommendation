def verify_title(title_input, data):
    matches = data[data["clean_title"] == title_input]
    if len(matches) == 0:
        return None
    elif len(matches) == 1:
        return matches.iloc[0]
    else:
        return matches.drop_duplicates(subset=["title_id"])

# def get_similar_movies(title_id, data, annoy_index, title_ids, amount):
#     index_val = title_ids.index(title_id)
#     similar_indices = annoy_index.get_nns_by_item(index_val, amount + 1)[1:]
#     similar_indices = [i for i in similar_indices if title_ids[i] != title_id]
#     return data.iloc[similar_indices]

def get_similar_titles(title_id, data, annoy_index, title_ids, n=5):
    # Ensure title_id is in the title_ids list
    try:
        index_val = title_ids.index(title_id)
    except ValueError:
        return "Title ID not found in index."

    similar_indices = annoy_index.get_nns_by_item(index_val, n + 1)[1:]  # skip input
    similar_indices = [i for i in similar_indices if title_ids[i] != title_id]

    return data.iloc[similar_indices]

def recommend_movies(title_id, data, annoy_index, title_ids, amount):
    recommended = get_similar_titles(title_id, data, annoy_index, title_ids, amount)
    return recommended[["title", "genres"]].reset_index(drop=True)