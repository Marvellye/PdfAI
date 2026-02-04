# coord_utils.py
def image_to_pdf(gemini_box, page_rect):
    """
    Converts Gemini 0-1000 scale coordinates to PDF Point coordinates.
    Gemini format: [ymin, xmin, ymax, xmax]
    PDF format: Bottom-Left Origin (x, y, width, height)
    """
    pdf_w = page_rect.width
    pdf_h = page_rect.height

    ymin, xmin, ymax, xmax = gemini_box

    # Normalize 0-1000 -> 0-1
    n_ymin = ymin / 1000.0
    n_xmin = xmin / 1000.0
    n_ymax = ymax / 1000.0
    n_xmax = xmax / 1000.0

    # Calculate Dimensions
    x = n_xmin * pdf_w
    width = (n_xmax - n_xmin) * pdf_w

    # Flip Y axis (PDF is bottom-left origin)
    pdf_top = pdf_h - (n_ymin * pdf_h)
    pdf_bottom = pdf_h - (n_ymax * pdf_h)
    
    height = pdf_top - pdf_bottom
    y = pdf_bottom 

    return { "x": x, "y": y, "width": width, "height": height }