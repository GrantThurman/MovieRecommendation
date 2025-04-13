import os

from sklearn.feature_extraction.text import TfidfVectorizer
from annoy import AnnoyIndex

def setup_annoy_index(data, index_path, feature): # "what to use for matrix"
    tfidf = TfidfVectorizer(stop_words="english")
    tfidf_matrix = tfidf.fit_transform(data[feature])
    tfidf_dense = tfidf_matrix.toarray()
    
    f = tfidf_dense.shape[1]
    annoy_index = AnnoyIndex(f, "angular")
    
    if os.path.exists(index_path):
        annoy_index.load(index_path)
    else:
        for i in range(len(data)):
            annoy_index.add_item(i, tfidf_dense[i])
        annoy_index.build(50)
        annoy_index.save(index_path)

    return annoy_index