import os
import json
from PIL import Image
from pypdf import PdfReader, PdfWriter

from pdf_render import render_page
from gemini_vision import detect_layout
from coord_utils import image_to_pdf
from pdf_overlay import create_overlay

PDF_PATH = "input/logbook.pdf"
CACHE_PATH = "cache/layout.json"

ENTRIES = [
    {
        "date": "2026-02-01",
        "time": "09:30",
        "description": "Routine system check",
        "signature": "JD"
    }
] * 5


def main():
    image_path, page_rect = render_page(PDF_PATH)

    layout = None  # 🔒 MUST exist before any checks

    # Try loading cache
    if os.path.exists(CACHE_PATH):
        try:
            with open(CACHE_PATH, "r") as f:
                layout = json.load(f)
                print("[+] Loaded layout from cache")
        except json.JSONDecodeError:
            print("[!] Cache exists but is invalid or empty. Rebuilding layout...")

    # Run Gemini if needed
    if layout is None:
        print("[*] Running Gemini layout detection...")
        raw_layout = detect_layout(image_path)
        img = Image.open(image_path)

        for entry in raw_layout["entries"]:
            for field in entry:
                entry[field] = image_to_pdf(
                    entry[field],
                    img.size,
                    page_rect
                )

        os.makedirs("cache", exist_ok=True)
        with open(CACHE_PATH, "w") as f:
            json.dump(raw_layout, f, indent=2)

        layout = raw_layout
        print("[+] Layout cached")

    overlay_pdf = "cache/overlay.pdf"
    create_overlay(page_rect, layout, ENTRIES, overlay_pdf)

    base = PdfReader(PDF_PATH)
    overlay = PdfReader(overlay_pdf)
    writer = PdfWriter()

    for i, page in enumerate(base.pages):
        if i == 0:
            page.merge_page(overlay.pages[0])
        writer.add_page(page)

    os.makedirs("output", exist_ok=True)
    with open("output/filled.pdf", "wb") as f:
        writer.write(f)

    print("[✓] Done → output/filled.pdf")


if __name__ == "__main__":
    main()