# pdf_overlay.py
from reportlab.pdfgen import canvas
from reportlab.lib.colors import red, black

def create_overlay(page_rect, fields, output_pdf):
    c = canvas.Canvas(output_pdf, pagesize=(page_rect.width, page_rect.height))
    
    # --- CALIBRATION KNOBS ---
    FONT_SIZE = 10
    X_PADDING = 25      # Increased from 15 to 25 to clear the vertical line
    Y_OFFSET = -2       # Keep vertical alignment
    # -------------------------

    c.setFont("Helvetica", FONT_SIZE)
    c.setFillColor(black)

    for f in fields:
        box = f["bounding_box"]
        value = f.get("value", "")
        
        x, y, w, h = box["x"], box["y"], box["width"], box["height"]

        # --- DEBUG: Red Boxes (Disabled for final output) ---
        # c.setStrokeColor(red)
        # c.setLineWidth(0.5)
        # c.rect(x, y, w, h, stroke=1, fill=0)
        # ----------------------------------------------------

        # Draw Text with the new Safe Margin
        text_x = x + X_PADDING
        text_y = y + (h / 2) + Y_OFFSET

        c.drawString(text_x, text_y, str(value))

    c.save()