import argparse
import re
from typing import List
from pypdf import PdfReader

# NLTK sentence tokenizer
import nltk
nltk.download('punkt', quiet=True)
from nltk.tokenize import sent_tokenize

def extract_pdf_text(path: str) -> str:
    reader = PdfReader(path)
    texts = []
    for page in reader.pages:
        t = page.extract_text() or ""
        texts.append(t)
    return "\n".join(texts)

def extract_text(path: str) -> str:
    if path.lower().endswith(".pdf"):
        return extract_pdf_text(path)
    else:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()

def clean_text(t: str) -> str:
    t = re.sub(r"\s+", " ", t)
    return t.strip()

def naive_summary_bullets(text: str, max_bullets: int = 7, max_len: int = 120) -> List[str]:
    sents = [s.strip() for s in sent_tokenize(text)]
    bullets = []
    for s in sents:
        s = re.sub(r"\s+", " ", s)
        if len(s) < 25:
            continue
        s = s[:max_len].rstrip()
        bullets.append(s)
        if len(bullets) >= max_bullets:
            break
    if not bullets:
        bullets = ["Key ideas not detected. Add clearer notes or increase summary length."]
    return bullets

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True, help="Path to notes file (.pdf or .txt)")
    ap.add_argument("--bullets", type=int, default=7, help="Max number of bullets")
    ap.add_argument("--maxlen", type=int, default=120, help="Max characters per bullet")
    args = ap.parse_args()

    raw = extract_text(args.src)
    text = clean_text(raw)
    bullets = naive_summary_bullets(text, max_bullets=args.bullets, max_len=args.maxlen)
    for b in bullets:
        print(f"- {b}")

if __name__ == "__main__":
    main()
