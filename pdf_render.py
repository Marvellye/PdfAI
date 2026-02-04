# pdf_render.py
import fitz

def render_page(pdf_path, page_num=0, dpi=200):
    doc = fitz.open(pdf_path)
    page = doc[page_num]
    mat = fitz.Matrix(dpi / 72, dpi / 72)
    pix = page.get_pixmap(matrix=mat)
    image_path = f"cache/page_{page_num}.png"
    pix.save(image_path)
    return image_path, page.rect
