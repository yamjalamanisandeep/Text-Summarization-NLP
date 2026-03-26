# from sklearn.feature_extraction.text import TfidfVectorizer
# import numpy as np

# def extractive_summary(original_sentences, cleaned_sentences, top_n=4):
#     if len(cleaned_sentences) <= top_n:
#         return original_sentences

#     vectorizer = TfidfVectorizer(
#         max_features=5000,
#         stop_words="english",
#         ngram_range=(1, 2)
#     )

#     tfidf_matrix = vectorizer.fit_transform(cleaned_sentences)

#     scores = np.asarray(tfidf_matrix.sum(axis=1)).ravel()

#     # Fast top-N selection
#     top_indices = np.argpartition(scores, -top_n)[-top_n:]
#     top_indices = sorted(top_indices)

#     summary = [original_sentences[i] for i in top_indices]
#     return summary


# from sklearn.feature_extraction.text import TfidfVectorizer
# import numpy as np

# def extractive_summary(original_sentences, cleaned_sentences, top_n=4):
#     if len(cleaned_sentences) <= top_n:
#         return original_sentences

#     vectorizer = TfidfVectorizer(
#         max_features=8000,
#         stop_words="english",
#         ngram_range=(1, 2)
#     )

#     tfidf_matrix = vectorizer.fit_transform(cleaned_sentences)
#     scores = np.asarray(tfidf_matrix.sum(axis=1)).ravel()

#     # boost longer informative sentences
#     for i, sent in enumerate(original_sentences):
#         length_bonus = min(len(sent.split()) / 25, 1.5)
#         scores[i] *= length_bonus

#     top_indices = np.argpartition(scores, -top_n)[-top_n:]
#     top_indices = sorted(top_indices)

#     return [original_sentences[i] for i in top_indices]

from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import re

def is_valid_sentence(sent):
    sent = sent.strip()

    # Remove bullet/list patterns
    sent = re.sub(r"^[\-\*\d\.\)]+", "", sent).strip()

    words = sent.split()

    # Reject very short lines (headings)
    if len(words) < 12:
        return False

    # Reject lines without verbs (likely headings)
    if not re.search(r"\b(is|are|was|were|has|have|offers|provides|known|focus|includes|places|emphasizes)\b", sent.lower()):
        return False

    return True


def extractive_summary(original_sentences, cleaned_sentences, top_n=5):
    valid_original = []
    valid_cleaned = []

    for i, sent in enumerate(original_sentences):
        if is_valid_sentence(sent):
            valid_original.append(original_sentences[i])
            valid_cleaned.append(cleaned_sentences[i])

    # Fallback safety
    if len(valid_cleaned) < top_n:
        valid_original = original_sentences
        valid_cleaned = cleaned_sentences

    vectorizer = TfidfVectorizer(
        max_features=8000,
        stop_words="english",
        ngram_range=(1, 2)
    )

    tfidf_matrix = vectorizer.fit_transform(valid_cleaned)
    scores = np.asarray(tfidf_matrix.sum(axis=1)).ravel()

    top_indices = np.argpartition(scores, -top_n)[-top_n:]
    top_indices = sorted(top_indices)

    summary = [valid_original[i] for i in top_indices]

    return summary
