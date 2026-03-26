from preprocessing.preprocess import preprocess_text
from extractive.textrank import extractive_summary
from abstractive.bart_summary import abstractive_summary
from evaluation.rouge_eval import evaluate_summaries
import time
import os


def run_summarization_pipeline(text, top_n=4, run_evaluation=True):
    start_time = time.time()

    # Step 1: Preprocessing
    original_sentences, cleaned_sentences = preprocess_text(text)

    # Step 2: Extractive Summarization (TextRank)
    extractive_sentences = extractive_summary(
        original_sentences,
        cleaned_sentences,
        top_n=top_n
    )
    extractive_paragraph = " ".join(extractive_sentences)

    # Step 3: Abstractive Summarization (BART)
    abstractive = abstractive_summary(extractive_paragraph)

    end_time = time.time()
    exec_time = round(end_time - start_time, 2)

    rouge_scores = None

    # Step 4: Evaluation (ROUGE)
    if run_evaluation:
        os.makedirs("evaluation", exist_ok=True)

        gen_path = "evaluation/generated.txt"
        ref_path = "evaluation/reference.txt"

        with open(gen_path, "w", encoding="utf-8") as f:
            f.write(abstractive)

        if os.path.exists(ref_path):
            rouge_scores = evaluate_summaries(
                generated_path=gen_path,
                reference_path=ref_path
            )
        else:
            print("Reference summary not found. Skipping ROUGE evaluation.")

    return {
        "extractive": extractive_paragraph,
        "abstractive": abstractive,
        "execution_time": exec_time,
        "rouge": rouge_scores
    }


# ------------------ CLI Testing ------------------
if __name__ == "__main__":
    sample_path = "data/sample.txt"

    if not os.path.exists(sample_path):
        print("sample.txt not found in data/ folder")
        exit(0)

    with open(sample_path, "r", encoding="utf-8") as file:
        text = file.read()

    results = run_summarization_pipeline(text, top_n=4, run_evaluation=True)

    print("\nExtractive Summary:\n")
    print(results["extractive"])

    print("\nAbstractive Summary:\n")
    print(results["abstractive"])

    print(f"\nTotal Execution Time: {results['execution_time']} seconds")

    if results["rouge"]:
        print("\nROUGE Scores:")
        for k, v in results["rouge"].items():
            print(f"{k}: Precision={v.precision:.4f}, Recall={v.recall:.4f}, F1={v.fmeasure:.4f}")
















































































































# # from preprocessing.preprocess import preprocess_text
# # from extractive.textrank import extractive_summary
# # from abstractive.bart_summary import abstractive_summary
# # import time

# # # Read input text
# # with open("data/sample.txt", "r", encoding="utf-8") as file:
# #     text = file.read()

# # start_time = time.time()

# # # Step 1: Preprocessing
# # original_sentences, cleaned_sentences = preprocess_text(text)

# # # Step 2: Extractive Summarization
# # extractive_sentences = extractive_summary(
# #     original_sentences,
# #     cleaned_sentences,
# #     top_n=4
# # )

# # extractive_paragraph = " ".join(extractive_sentences)

# # print("\nExtractive Summary:\n")
# # print(extractive_paragraph)

# # # Step 3: Abstractive Summarization (on extractive output)
# # abstractive = abstractive_summary(extractive_paragraph)

# # print("\nAbstractive Summary:\n")
# # print(abstractive)

# # end_time = time.time()
# # print(f"\nTotal Execution Time: {round(end_time - start_time, 2)} seconds")

# # # Save generated summary for evaluation
# # with open("evaluation/generated.txt", "w", encoding="utf-8") as f:
# #     f.write(abstractive)



# from preprocessing.preprocess import preprocess_text
# from extractive.textrank import extractive_summary
# from abstractive.bart_summary import abstractive_summary
# from evaluation.rouge_eval import evaluate_summaries
# import time
# import os

# # Read input text
# with open("data/sample.txt", "r", encoding="utf-8") as file:
#     text = file.read()

# start_time = time.time()

# # Step 1: Preprocessing
# original_sentences, cleaned_sentences = preprocess_text(text)

# # Step 2: Extractive Summarization
# extractive_sentences = extractive_summary(
#     original_sentences,
#     cleaned_sentences,
#     top_n=4
# )

# extractive_paragraph = " ".join(extractive_sentences)

# print("\nExtractive Summary:\n")
# print(extractive_paragraph)

# # Step 3: Abstractive Summarization (on extractive output)
# abstractive = abstractive_summary(extractive_paragraph)

# print("\nAbstractive Summary:\n")
# print(abstractive)

# end_time = time.time()
# print(f"\nTotal Execution Time: {round(end_time - start_time, 2)} seconds")

# # Step 4: Save generated summary for evaluation
# os.makedirs("evaluation", exist_ok=True)
# with open("evaluation/generated.txt", "w", encoding="utf-8") as f:
#     f.write(abstractive)

# # Step 5: Run ROUGE + BLEU Evaluation
# print("\nRunning Evaluation ROUGE ...")
# evaluate_summaries(
#     generated_path="evaluation/generated.txt",
#     reference_path="evaluation/reference.txt"
# )



# app.py  (BACKEND CORE LOGIC)

# from preprocessing.preprocess import preprocess_text
# from extractive.textrank import extractive_summary
# from abstractive.bart_summary import abstractive_summary
# from evaluation.rouge_eval import evaluate_summaries
# import time
# import os


# def run_summarization_pipeline(text, top_n=4, run_evaluation=True):
    

#     start_time = time.time()

#     # Step 1: Preprocessing
#     original_sentences, cleaned_sentences = preprocess_text(text)

#     # Step 2: Extractive Summarization
#     extractive_sentences = extractive_summary(
#         original_sentences,
#         cleaned_sentences,
#         top_n=top_n
#     )
#     extractive_paragraph = " ".join(extractive_sentences)

#     # Step 3: Abstractive Summarization
#     abstractive = abstractive_summary(extractive_paragraph)

#     end_time = time.time()
#     exec_time = round(end_time - start_time, 2)

#     rouge_scores = None

#     # Step 4: Evaluation (ROUGE)
#     if run_evaluation:
#         os.makedirs("evaluation", exist_ok=True)
#         with open("evaluation/generated.txt", "w", encoding="utf-8") as f:
#             f.write(abstractive)

#         rouge_scores = evaluate_summaries(
#             generated_path="evaluation/generated.txt",
#             reference_path="evaluation/reference.txt"
#         )

#     return {
#         "extractive": extractive_paragraph,
#         "abstractive": abstractive,
#         "execution_time": exec_time,
#         "rouge": rouge_scores
#     }


# # ------------------ CLI Testing ------------------
# if __name__ == "__main__":
#     with open("data/sample.txt", "r", encoding="utf-8") as file:
#         text = file.read()

#     results = run_summarization_pipeline(text, top_n=4, run_evaluation=True)

#     print("\nExtractive Summary:\n")
#     print(results["extractive"])

#     print("\nAbstractive Summary:\n")
#     print(results["abstractive"])

#     print(f"\nTotal Execution Time: {results['execution_time']} seconds")

#     if results["rouge"]:
#         print("\nROUGE Scores:")
#         for k, v in results["rouge"].items():
#             print(f"{k}: F1 = {v.fmeasure:.4f}")

















# from preprocessing.preprocess import preprocess_text
# from extractive.textrank import extractive_summary
# from abstractive.bart_summary import abstractive_summary
# from evaluation.rouge_eval import evaluate_summaries
# import time
# import os


# def run_summarization_pipeline(text, top_n=4, run_evaluation=True):
#     start_time = time.time()

#     # Step 1: Preprocessing
#     original_sentences, cleaned_sentences = preprocess_text(text)

#     # Step 2: Extractive Summarization
#     extractive_sentences = extractive_summary(
#         original_sentences,
#         cleaned_sentences,
#         top_n=top_n
#     )
#     extractive_paragraph = " ".join(extractive_sentences)

#     # Step 3: Abstractive Summarization
#     abstractive = abstractive_summary(extractive_paragraph)

#     exec_time = round(time.time() - start_time, 2)

#     rouge_scores = None

#     # Step 4: Evaluation (ROUGE)
#     if run_evaluation:
#         try:
#             os.makedirs("evaluation", exist_ok=True)
#             with open("evaluation/generated.txt", "w", encoding="utf-8") as f:
#                 f.write(abstractive)

#             rouge_scores = evaluate_summaries(
#                 generated_path="evaluation/generated.txt",
#                 reference_path="evaluation/reference.txt"
#             )
#         except Exception as e:
#             print("ROUGE evaluation failed:", e)
#             rouge_scores = None

#     return {
#         "extractive": extractive_paragraph,
#         "abstractive": abstractive,
#         "execution_time": exec_time,
#         "rouge": rouge_scores
#     }


# # ------------------ CLI Testing ------------------
# if __name__ == "__main__":
#     with open("data/sample1.txt", "r", encoding="utf-8") as file:
#         text = file.read()

#     results = run_summarization_pipeline(text, top_n=4, run_evaluation=True)

#     print("\nExtractive Summary:\n")
#     print(results["extractive"])

#     print("\nAbstractive Summary:\n")
#     print(results["abstractive"])

#     print(f"\nTotal Execution Time: {results['execution_time']} seconds")

#     if results["rouge"]:
#         print("\nROUGE Scores:")
#         for k, v in results["rouge"].items():
#             print(f"{k}: F1 = {v.fmeasure:.4f}")





