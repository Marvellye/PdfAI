# gemini_vision.py
import os
import json
from PIL import Image
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

PROMPT = """
Analyze this form image. Identify the **empty fillable areas** corresponding to the labels (e.g., the empty box next to 'Name:', 'Date:', etc.).

Return JSON in this format:
{
  "fields": [
    {
      "type": "string",  // e.g., "name", "date", "time", "location", "purpose_description", "signature"
      "box_2d": [ymin, xmin, ymax, xmax] // Integer coordinates on a 0-1000 scale
    }
  ]
}

Rules:
1. "box_2d" must be [ymin, xmin, ymax, xmax] integers (0-1000).
2. Do not detect the label text itself; detect the empty space to the right or below the label where handwriting would go.
"""

def detect_fields(image_path):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY not found in .env")

    client = genai.Client(api_key=api_key)
    img = Image.open(image_path)

    response = client.models.generate_content(
        model="gemini-2.5-flash", # Use 2.0 or 1.5 Pro for better spatial reasoning
        contents=[PROMPT, img],
        config={
            "response_mime_type": "application/json",
            "temperature": 0
        }
    )

    try:
        data = json.loads(response.text)
        return data
    except json.JSONDecodeError:
        print("Raw response:", response.text)
        raise RuntimeError("Gemini returned invalid JSON")