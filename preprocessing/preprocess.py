# from nltk.tokenize import sent_tokenize
# from nltk.corpus import stopwords
# import string

# def preprocess_text(text):
#     sentences = sent_tokenize(text)
#     cleaned_sentences = []

#     stop_words = set(stopwords.words("english"))

#     for sent in sentences:
#         sent_clean = sent.lower()
#         sent_clean = sent_clean.translate(str.maketrans("", "", string.punctuation))
#         words = sent_clean.split()
#         words = [w for w in words if w not in stop_words]
#         cleaned_sentences.append(" ".join(words))

#     return sentences, cleaned_sentences




from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
import string
import re

def preprocess_text(text):
    # Remove bullet/list-like standalone lines before sentence tokenization
    lines = text.split("\n")
    filtered_lines = []

    for line in lines:
        line = line.strip()

        # Skip empty lines
        if not line:
            continue

        # Skip list headings or short category lines
        if len(line.split()) <= 4:
            continue

        # Skip lines that look like section headers
        if line.isupper():
            continue

        filtered_lines.append(line)

    filtered_text = " ".join(filtered_lines)

    sentences = sent_tokenize(filtered_text)
    cleaned_sentences = []

    stop_words = set(stopwords.words("english"))

    for sent in sentences:
        sent_clean = sent.lower()
        sent_clean = sent_clean.translate(str.maketrans("", "", string.punctuation))
        words = sent_clean.split()
        words = [w for w in words if w not in stop_words]
        cleaned_sentences.append(" ".join(words))

    return sentences, cleaned_sentences
