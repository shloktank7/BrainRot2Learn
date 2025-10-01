import argparse
from typing import List, Tuple
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import ImageClip, concatenate_videoclips
import numpy as np
import os

from summarize import extract_text, clean_text, naive_summary_bullets

# Video settings
W, H = 1080, 1920
BG_COLOR = (20, 20, 30)       # dark bg
TITLE_COLOR = (142, 202, 230) # light blue
TEXT_COLOR = (255, 255, 255)  # white
FOOT_COLOR  = (173, 181, 189) # gray
TITLE = "Study Snippets"
FOOTER = "@brainrot2learn"

def load_font(size: int, bold: bool=False):
    # Tries a few common fonts; falls back to default
    candidates = [
        "Arial.ttf",
        "Arial Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/Library/Fonts/Arial.ttf",
        "/Library/Fonts/Arial Bold.ttf",
    ]
    for c in candidates:
        try:
            return ImageFont.truetype(c, size=size)
        except Exception:
            continue
    return ImageFont.load_default()

def draw_multiline(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont, box: Tuple[int,int,int,int], fill=(255,255,255), line_spacing=10):
    x0, y0, x1, y1 = box
    max_width = x1 - x0
    words = text.split()
    lines = []
    line = ""
    for w in words:
        test = f"{line} {w}".strip()
        if draw.textlength(test, font=font) <= max_width:
            line = test
        else:
            lines.append(line)
            line = w
    if line:
        lines.append(line)

    y = y0
    for l in lines:
        draw.text((x0, y), l, font=font, fill=fill)
        y += font.getbbox(l)[3] - font.getbbox(l)[1] + line_spacing

def make_slide(text: str, dur: float = 3.5) -> ImageClip:
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)

    title_font = load_font(72, bold=True)
    body_font  = load_font(52, bold=False)
    foot_font  = load_font(38, bold=False)

    # Title
    tw = draw.textlength(TITLE, font=title_font)
    draw.text(((W - tw)//2, 120), TITLE, font=title_font, fill=TITLE_COLOR)

    # Body (centered box)
    margin = 80
    box = (margin, 400, W - margin, H - 350)
    draw_multiline(draw, text, font=body_font, box=box, fill=TEXT_COLOR, line_spacing=12)

    # Footer
    fw = draw.textlength(FOOTER, font=foot_font)
    draw.text(((W - fw)//2, H - 140), FOOTER, font=foot_font, fill=FOOT_COLOR)

    frame = np.array(img)
    return ImageClip(frame).set_duration(dur)

def build_video(bullets: List[str], out_path: str, dur: float):
    clips = [make_slide(b, dur=dur) for b in bullets]
    video = concatenate_videoclips(clips, method="compose")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    video.write_videofile(out_path, fps=24, codec="libx264", audio=False)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True, help="Path to notes file (.pdf or .txt)")
    ap.add_argument("--out", default="output/brainrot_snippets.mp4", help="Output mp4 path")
    ap.add_argument("--bullets", type=int, default=7, help="Max number of bullets")
    ap.add_argument("--maxlen", type=int, default=120, help="Max characters per bullet")
    ap.add_argument("--dur", type=float, default=3.5, help="Seconds per slide")
    args = ap.parse_args()

    raw = extract_text(args.src)
    text = clean_text(raw)
    bullets = naive_summary_bullets(text, max_bullets=args.bullets, max_len=args.maxlen)
    build_video(bullets, args.out, dur=args.dur)
    print(f"Saved video to {args.out}")

if __name__ == "__main__":
    main()
