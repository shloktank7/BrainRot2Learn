# BrainRot2Learn: Notes → Short Study Videos

**What it is:** Turn a PDF (or .txt) of class notes into short, vertical (1080×1920) “study snippet” videos with auto‑summarized bullet captions. Built for Gen Z attention spans; perfect for quick review.

**No API keys. Local only.** Uses simple sentence selection + MoviePy to render a vertical MP4. This version avoids ImageMagick by drawing text with Pillow (so only FFmpeg is needed for writing the video).

## Why it matters (Creativity + Future of Learning)
- **Engagement:** Converts dense notes into fast, digestible micro‑lessons.
- **Accessibility:** Visual captions; add TTS later for audio learners.
- **Innovation:** Bridges study workflows and short‑form video culture.

## Quickstart

```bash
# 1) create and activate a virtual env (recommended)
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 2) install requirements
pip install --upgrade pip
pip install -r requirements.txt

# 3) put your notes into ./input as a PDF or TXT file
#    example included: input/sample_notes.txt

# 4) generate bullets (optional preview)
python summarize.py --src input/sample_notes.txt

# 5) make the vertical video (1080x1920)
python make_video.py --src input/sample_notes.txt --out output/brainrot_snippets.mp4
```

> If you use a **PDF**, the tool extracts text with `pypdf`. If the PDF is scanned images (no embedded text), use OCR first or paste text into a `.txt` file.

## Options

```
python make_video.py --src <path> --out <mp4 path> --bullets 7 --maxlen 120 --dur 3.5
```

- `--bullets`: max bullet slides
- `--maxlen`: max characters per bullet
- `--dur`: seconds per slide

## Roadmap (Future Work)
- Add TTS voiceover (e.g., `pyttsx3`) and background music
- Support background stock clips behind captions
- Streamlit/Gradio web UI for drag‑and‑drop PDFs
- Smarter summarization (e.g., keyphrase scoring, embeddings/LLMs)

## Tech
- Python, MoviePy, Pillow, NLTK, PyPDF
