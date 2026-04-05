# from transformers import BartTokenizer, BartForConditionalGeneration
# import torch

# MODEL_NAME = "sshleifer/distilbart-cnn-12-6"  # Fast, public model

# tokenizer = BartTokenizer.from_pretrained(MODEL_NAME)
# model = BartForConditionalGeneration.from_pretrained(MODEL_NAME)

# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# model.to(device)

# def abstractive_summary(text, max_length=120, min_length=50):
#     inputs = tokenizer(
#         text,
#         return_tensors="pt",
#         max_length=512,
#         truncation=True
#     ).to(device)

#     summary_ids = model.generate(
#         inputs["input_ids"],
#         max_length=max_length,
#         min_length=min_length,
#         num_beams=4,
#         no_repeat_ngram_size=3,
#         early_stopping=True
#     )

#     return tokenizer.decode(summary_ids[0], skip_special_tokens=True)






from transformers import BartTokenizer, BartForConditionalGeneration
import torch
from functools import lru_cache

MODEL_NAME = "sshleifer/distilbart-cnn-12-6"  # fast & lightweight

# ---------------- LOAD MODEL (CACHED) ----------------
@lru_cache(maxsize=1)
def load_model():
    tokenizer = BartTokenizer.from_pretrained(MODEL_NAME)
    model = BartForConditionalGeneration.from_pretrained(MODEL_NAME)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    model.eval()  # 🔥 important for faster inference

    return tokenizer, model, device


# ---------------- SUMMARIZATION FUNCTION ----------------
def abstractive_summary(text, max_length=120, min_length=40):
    tokenizer, model, device = load_model()

    # 🔥 TOKENIZATION (optimized)
    inputs = tokenizer(
        text,
        return_tensors="pt",
        max_length=512,
        truncation=True,
        padding="longest"
    ).to(device)

    # 🔥 NO GRADIENT → faster inference
    with torch.no_grad():
        summary_ids = model.generate(
            inputs["input_ids"],
            max_length=max_length,
            min_length=min_length,
            num_beams=3,                 # reduced from 4 → faster
            no_repeat_ngram_size=2,      # balanced quality + speed
            early_stopping=True
        )

    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    return summary