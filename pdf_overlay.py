# pdf_overlay.py
from reportlab.pdfgen import canvas

def create_overlay(page_rect, layout, values, output_pdf):
    c = canvas.Canvas(output_pdf, pagesize=(page_rect.width, page_rect.height))
    c.setFont("Helvetica", 9)

    for entry_layout, entry_data in zip(layout["entries"], values):
        for field, box in entry_layout.items():
            x, y, _, _ = box
            c.drawString(x + 2, y - 10, entry_data.get(field, ""))

    c.save()
