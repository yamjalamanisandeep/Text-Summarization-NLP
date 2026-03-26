
# from rouge_score import rouge_scorer

# def evaluate_summaries(generated_path, reference_path):
#     # Read generated summary
#     with open(generated_path, "r", encoding="utf-8") as f:
#         generated_text = f.read()

#     # Read reference summary
#     with open(reference_path, "r", encoding="utf-8") as f:
#         reference_text = f.read()

#     # -------- ROUGE Evaluation --------
#     scorer = rouge_scorer.RougeScorer(["rouge1", "rouge2", "rougeL"], use_stemmer=True)
#     rouge_scores = scorer.score(reference_text, generated_text)

#     print("\nROUGE Scores:")
#     for key, value in rouge_scores.items():
#         print(f"{key}: Precision={value.precision:.4f}, Recall={value.recall:.4f}, F1={value.fmeasure:.4f}")

#     # ✅ IMPORTANT: return the scores
#     return rouge_scores











from rouge_score import rouge_scorer

def evaluate_summaries(generated_path, reference_path):
    
    with open(generated_path, "r", encoding="utf-8") as f:
        generated_text = f.read()

    with open(reference_path, "r", encoding="utf-8") as f:
        reference_text = f.read()

   
    scorer = rouge_scorer.RougeScorer(["rouge1", "rouge2", "rougeL"], use_stemmer=True)
    rouge_scores = scorer.score(reference_text, generated_text)


    return rouge_scores
