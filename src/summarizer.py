# src/summarizer.py

from transformers import pipeline
import os

def summarize_transcript(input_txt_path, output_summary_path, max_length=130, min_length=30):
    if not os.path.exists(input_txt_path):
        print("❌ Transcript file not found!")
        return

    with open(input_txt_path, "r", encoding="utf-8") as f:
        text = f.read()

    # Limit input for testing (models may not handle huge input at once)
    if len(text) > 2000:
        text = text[:2000]

    summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

    summary = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)[0]["summary_text"]

    with open(output_summary_path, "w", encoding="utf-8") as f:
        f.write(summary)

    print(f"✅ Summary saved to: {output_summary_path}")
    return summary
