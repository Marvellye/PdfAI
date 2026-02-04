# coord_utils.py
def image_to_pdf(box, img_size, page_rect):
    img_w, img_h = img_size
    pdf_w, pdf_h = page_rect.width, page_rect.height

    x = box["x"] / img_w * pdf_w
    y = pdf_h - (box["y"] / img_h * pdf_h)
    w = box["width"] / img_w * pdf_w
    h = box["height"] / img_h * pdf_h

    return x, y, w, h
