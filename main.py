import os
import json
from PIL import Image
from pypdf import PdfReader, PdfWriter

# Import your helper modules
from pdf_render import render_page
from gemini_vision import detect_fields
from coord_utils import image_to_pdf
from pdf_overlay import create_overlay

PDF_PATH = "input/logbook.pdf"
CACHE_PATH = "cache/layout.json"

# Values to fill into the form
FILL_VALUES = {
    "name": "John Doe",
    "date": "2026-02-04",
    "time": "14:30",
    "location": "Lab A",
    "purpose_description": "Routine check completed",
    "signature": "JD"
}

def main():
    # 1. Render PDF page to image for AI analysis
    image_path, page_rect = render_page(PDF_PATH, dpi=300)

    layout = None
    
    # 2. Check Cache
    if os.path.exists(CACHE_PATH):
        try:
            with open(CACHE_PATH, "r") as f:
                layout = json.load(f)
                print("[+] Loaded layout from cache")
        except json.JSONDecodeError:
            print("[!] Cache exists but is invalid. Rebuilding...")

    # 3. If no cache, run AI detection
    if layout is None:
        print("[*] Running Gemini free-form field detection...")
        
        # Get raw data from Gemini (contains "box_2d" in 0-1000 scale)
        raw_layout = detect_fields(image_path)
        
        processed_fields = []
        
        # Convert Gemini coordinates to PDF coordinates
        for field in raw_layout.get("fields", []):
            if "box_2d" in field:
                # Convert [ymin, xmin, ymax, xmax] -> {x, y, width, height}
                pdf_box = image_to_pdf(field["box_2d"], page_rect)
                
                processed_fields.append({
                    "type": field.get("type", "unknown"),
                    "bounding_box": pdf_box  # Store the converted box
                })
        
        layout = {"fields": processed_fields}

        # Save to cache
        os.makedirs("cache", exist_ok=True)
        with open(CACHE_PATH, "w") as f:
            json.dump(layout, f, indent=2)

        print("[+] Layout cached")

    # 4. Prepare data for Overlay
    overlay_fields = []
    
    for f in layout["fields"]:
        field_type = f.get("type", "unknown")
        
        # Simple fuzzy matching (e.g., "Signature" -> "signature")
        field_key = field_type.lower().replace(" ", "_")
        value = ""
        
        # Find matching value in FILL_VALUES
        for k, v in FILL_VALUES.items():
            if k in field_key or field_key in k:
                value = v
                break
        
        if value and "bounding_box" in f:
            overlay_fields.append({
                "bounding_box": f["bounding_box"],
                "value": value
            })

    # 5. Generate PDF
    base = PdfReader(PDF_PATH)
    writer = PdfWriter()
    
    # We are skipping form filling for now to force the overlay method
    print("[*] Generating text overlay...")
    overlay_pdf = "cache/overlay.pdf"
    
    # Create the overlay PDF with the text
    create_overlay(page_rect, overlay_fields, overlay_pdf)
    
    # Merge overlay
    overlay = PdfReader(overlay_pdf)
    writer.append(base)
    page = writer.pages[0]
    page.merge_page(overlay.pages[0])

    os.makedirs("output", exist_ok=True)
    with open("output/filled.pdf", "wb") as f:
        writer.write(f)

    print("[✓] Done → output/filled.pdf")

if __name__ == "__main__":
    main()