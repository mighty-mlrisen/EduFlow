from transformers import AutoTokenizer
from transformers import AutoModelForSeq2SeqLM

MODEL_NAME = "cointegrated/rut5-base"

print("Loading model...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

model = AutoModelForSeq2SeqLM.from_pretrained(
    MODEL_NAME
)

print("Model loaded")


def summarize(text: str):

    prompt = (
        "Напиши краткое содержание статьи:\n\n"
        + text
    )

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=512
    )

    outputs = model.generate(
        **inputs,
        max_new_tokens=80,
        num_beams=5,
        no_repeat_ngram_size=3,
        early_stopping=True
    )

    summary = tokenizer.decode(
        outputs[0],
        skip_special_tokens=True
    )

    return summary


with open(
    "article.txt",
    "r",
    encoding="utf-8"
) as f:

    article = f.read()

result = summarize(article)

print("\nSUMMARY:")
print(result)