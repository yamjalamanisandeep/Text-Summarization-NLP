# import streamlit as st
# import time
# import os

# from preprocessing.preprocess import preprocess_text
# from extractive.textrank import extractive_summary
# from abstractive.bart_summary import abstractive_summary
# from evaluation.rouge_eval import evaluate_summaries

# st.set_page_config(page_title="Text Summarization NLP", layout="centered")

# st.title("📝 Text Summarization using NLP")
# st.caption("Generate Extractive & Abstractive summaries with ROUGE evaluation")

# # --------- Caching for Speed ----------
# @st.cache_data(show_spinner=False)
# def run_preprocess(text):
#     return preprocess_text(text)

# @st.cache_data(show_spinner=False)
# def run_extractive(original_sentences, cleaned_sentences, top_n):
#     return extractive_summary(original_sentences, cleaned_sentences, top_n)

# @st.cache_resource(show_spinner=False)
# def load_bart():
#     return abstractive_summary

# bart_model = load_bart()
# # -------------------------------------

# input_text = st.text_area("📌 Input Text", height=220, placeholder="Paste your article or paragraph here...")

# top_n = st.slider("🔢 Number of sentences in Extractive Summary", 3, 6, 4)

# if st.button("🚀 Summarize"):
#     if not input_text.strip():
#         st.warning("Please enter some text.")
#     else:
#         with st.spinner("Processing text..."):
#             start_time = time.time()

#             # Step 1: Preprocessing
#             original_sentences, cleaned_sentences = run_preprocess(input_text)

#             # Step 2: Extractive Summary
#             extractive_sentences = run_extractive(original_sentences, cleaned_sentences, top_n)
#             extractive_paragraph = " ".join(extractive_sentences)

#             # Step 3: Abstractive Summary
#             abstractive = bart_model(extractive_paragraph)

#             end_time = time.time()

#         col1, col2 = st.columns(2)

#         with col1:
#             st.subheader("📄 Extractive Summary")
#             st.write(extractive_paragraph)

#         with col2:
#             st.subheader("✨ Abstractive Summary")
#             st.write(abstractive)

#         st.success(f"⏱️ Execution Time: {round(end_time - start_time, 2)} seconds")

#         # Save generated summary for evaluation
#         os.makedirs("evaluation", exist_ok=True)
#         with open("evaluation/generated.txt", "w", encoding="utf-8") as f:
#             f.write(abstractive)

#         with st.expander("📊 ROUGE Evaluation"):
#             rouge_scores = evaluate_summaries(
#                 generated_path="evaluation/generated.txt",
#                 reference_path="evaluation/reference.txt"
#             )

#             st.write(f"ROUGE-1 F1: {rouge_scores['rouge1'].fmeasure:.3f}")
#             st.write(f"ROUGE-2 F1: {rouge_scores['rouge2'].fmeasure:.3f}")
#             st.write(f"ROUGE-L F1: {rouge_scores['rougeL'].fmeasure:.3f}")




# streamlit_app.py  (FRONTEND / UI ONLY)

# import streamlit as st
# from app import run_summarization_pipeline

# st.set_page_config(page_title="Text Summarization NLP", layout="centered")

# st.title("📝 Text Summarization using NLP")
# st.caption("Frontend UI for Text Summarization System")

# input_text = st.text_area(
#     "📌 Input Text",
#     height=220,
#     placeholder="Paste your article or paragraph here..."
# )

# top_n = st.slider("🔢 Number of sentences in Extractive Summary", 3, 6, 4)

# if st.button("🚀 Summarize"):
#     if not input_text.strip():
#         st.warning("Please enter some text.")
#     else:
#         with st.spinner("Summarizing..."):
#             results = run_summarization_pipeline(
#                 text=input_text,
#                 top_n=top_n,
#                 run_evaluation=True
#             )

#         col1, col2 = st.columns(2)

#         with col1:
#             st.subheader("📄 Extractive Summary")
#             st.write(results["extractive"])

#         with col2:
#             st.subheader("✨ Abstractive Summary")
#             st.write(results["abstractive"])

#         st.success(f"⏱️ Execution Time: {results['execution_time']} seconds")

#         if results["rouge"]:
#             with st.expander("📊 ROUGE Evaluation"):
#                 st.write(f"ROUGE-1 F1: {results['rouge']['rouge1'].fmeasure:.3f}")
#                 st.write(f"ROUGE-2 F1: {results['rouge']['rouge2'].fmeasure:.3f}")
#                 st.write(f"ROUGE-L F1: {results['rouge']['rougeL'].fmeasure:.3f}")




import streamlit as st
import pandas as pd
from app import run_summarization_pipeline

st.set_page_config(page_title="Text Summarization NLP", layout="centered")

st.title("📝 Text Summarization using NLP")
st.caption("AI-based Extractive + Abstractive Summarization System")

# -------------------------------
# MODE SELECTION
# -------------------------------
mode = st.radio(
    "Choose Input Type:",
    ["✍️ Manual Input", "📰 Use Dataset"]
)

input_text = ""

# -------------------------------
# OPTION 1: MANUAL INPUT
# -------------------------------
if mode == "✍️ Manual Input":
    input_text = st.text_area(
        "📌 Enter Text",
        height=220,
        placeholder="Paste your article or paragraph here..."
    )

# -------------------------------
# OPTION 2: DATASET INPUT
# -------------------------------
elif mode == "📰 Use Dataset":
    try:
        df = pd.read_csv("data/news.csv", on_bad_lines='skip')

        index = st.number_input(
            "Select Article Index",
            min_value=0,
            max_value=min(len(df)-1, 100),
            value=0
        )

        input_text = str(df.iloc[index]["article"])
        reference = str(df.iloc[index]["highlights"])

        st.subheader("📄 Selected Article")
        st.write(input_text[:500] + "...")

        # st.subheader("🟢 Reference Summary")
        # st.write(reference)

    except:
        st.error("Dataset not found or invalid format")

# -------------------------------
# PARAMETERS
# -------------------------------
top_n = st.slider(
    "🔢 Number of sentences (Extractive)",
    3, 6, 4
)

# -------------------------------
# RUN BUTTON
# -------------------------------
if st.button("🚀 Summarize"):
    if not input_text.strip():
        st.warning("Please enter some text.")
    else:
        with st.spinner("Summarizing..."):
            results = run_summarization_pipeline(
                text=input_text,
                top_n=top_n,
                run_evaluation=True
            )

        # -------------------------------
        # OUTPUT
        # -------------------------------
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📄 Extractive Summary")
            st.write(results["extractive"])

        with col2:
            st.subheader("✨ Abstractive Summary")
            st.write(results["abstractive"])

        st.success(f"⏱️ Execution Time: {results['execution_time']} seconds")

        # -------------------------------
        # ROUGE
        # -------------------------------
        if results["rouge"]:
            with st.expander("📊 ROUGE Evaluation"):
                st.write(f"ROUGE-1 F1: {results['rouge']['rouge1'].fmeasure:.3f}")
                st.write(f"ROUGE-2 F1: {results['rouge']['rouge2'].fmeasure:.3f}")
                st.write(f"ROUGE-L F1: {results['rouge']['rougeL'].fmeasure:.3f}")