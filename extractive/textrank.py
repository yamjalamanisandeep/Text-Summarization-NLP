from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import networkx as nx
import re



def is_valid_sentence(sent):
    sent = sent.strip()

    
    sent = re.sub(r"^[\-\*\d\.\)]+", "", sent).strip()

    words = sent.split()

    # Reject short lines
    if len(words) < 10:
        return False

    # Simple verb check
    if not re.search(
        r"\b(is|are|was|were|has|have|had|will|can|may|provides|includes|shows|explains)\b",
        sent.lower()
    ):
        return False

    return True


# ---------------- TEXTRANK ----------------
def extractive_summary(original_sentences, cleaned_sentences, top_n=5):

    valid_original = []
    valid_cleaned = []

    # Filter valid sentences
    for i, sent in enumerate(original_sentences):
        if is_valid_sentence(sent):
            valid_original.append(original_sentences[i])
            valid_cleaned.append(cleaned_sentences[i])

    # Fallback if too few sentences
    if len(valid_cleaned) < top_n:
        valid_original = original_sentences
        valid_cleaned = cleaned_sentences

    # ---------------- TF-IDF ----------------
    vectorizer = TfidfVectorizer(
        max_features=5000,
        stop_words="english",
        ngram_range=(1, 2)
    )

    tfidf_matrix = vectorizer.fit_transform(valid_cleaned)

    # ---------------- SIMILARITY MATRIX ----------------
    similarity_matrix = cosine_similarity(tfidf_matrix)

    # ---------------- GRAPH (TextRank) ----------------
    graph = nx.from_numpy_array(similarity_matrix)

    scores = nx.pagerank(graph)

    # Rank sentences
    ranked_sentences = sorted(
        ((scores[i], s, i) for i, s in enumerate(valid_original)),
        reverse=True
    )

    # Select top sentences
    selected = sorted(ranked_sentences[:top_n], key=lambda x: x[2])

    summary = [item[1] for item in selected]

    return summary




# from sklearn.feature_extraction.text import TfidfVectorizer
# import numpy as np
# import re

# def is_valid_sentence(sent):
#     sent = sent.strip()

#     # Remove bullet/list patterns
#     sent = re.sub(r"^[\-\*\d\.\)]+", "", sent).strip()

#     words = sent.split()

#     # Reject very short lines (headings)
#     if len(words) < 12:
#         return False

#     # Reject lines without verbs (likely headings)
#     if not re.search(r"\b(is|are|was|were|has|have|offers|provides|known|focus|includes|places|emphasizes)\b", sent.lower()):
#         return False

#     return True


# def extractive_summary(original_sentences, cleaned_sentences, top_n=5):
#     valid_original = []
#     valid_cleaned = []

#     for i, sent in enumerate(original_sentences):
#         if is_valid_sentence(sent):
#             valid_original.append(original_sentences[i])
#             valid_cleaned.append(cleaned_sentences[i])

#     # Fallback safety
#     if len(valid_cleaned) < top_n:
#         valid_original = original_sentences
#         valid_cleaned = cleaned_sentences

#     vectorizer = TfidfVectorizer(
#         max_features=8000,
#         stop_words="english",
#         ngram_range=(1, 2)
#     )

#     tfidf_matrix = vectorizer.fit_transform(valid_cleaned)
#     scores = np.asarray(tfidf_matrix.sum(axis=1)).ravel()

#     top_indices = np.argpartition(scores, -top_n)[-top_n:]
#     top_indices = sorted(top_indices)

#     summary = [valid_original[i] for i in top_indices]

#     return summary
