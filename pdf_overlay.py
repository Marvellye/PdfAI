# pdf_overlay.py
from reportlab.pdfgen import canvas
from reportlab.lib.colors import red

def create_overlay(page_rect, fields, output_pdf):
    c = canvas.Canvas(output_pdf, pagesize=(page_rect.width, page_rect.height))
    
    for f in fields:
        box = f["bounding_box"]
        value = f.get("value", "")
        
        x = box["x"]
        y = box["y"]
        w = box["width"]
        h = box["height"]

        # --- DEBUG: Uncomment to see the boxes ---
        # c.setStrokeColor(red)
        # c.rect(x, y, w, h, stroke=1, fill=0)
        # -----------------------------------------

        c.setFont("Helvetica", 12)
        
        # Calculate vertical center
        # PDF draws text from the baseline. 
        # We start at y (bottom) + half height - approx half font height (4)
        text_y = y + (h / 2) - 4 
        text_x = x + 5 # Padding from left

        c.drawString(text_x, text_y, str(value))

    c.save()