from transformers import BartTokenizer, BartForConditionalGeneration
import torch

MODEL_NAME = "sshleifer/distilbart-cnn-12-6"  # Fast, public model

tokenizer = BartTokenizer.from_pretrained(MODEL_NAME)
model = BartForConditionalGeneration.from_pretrained(MODEL_NAME)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

def abstractive_summary(text, max_length=120, min_length=50):
    inputs = tokenizer(
        text,
        return_tensors="pt",
        max_length=512,
        truncation=True
    ).to(device)

    summary_ids = model.generate(
        inputs["input_ids"],
        max_length=max_length,
        min_length=min_length,
        num_beams=4,
        no_repeat_ngram_size=3,
        early_stopping=True
    )

    return tokenizer.decode(summary_ids[0], skip_special_tokens=True)
