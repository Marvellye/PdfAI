# gemini_vision.py
import os
import json
from PIL import Image
from dotenv import load_dotenv
from google import genai

load_dotenv()  # 👈 loads .env automatically

PROMPT = """
Analyze this logbook page.

The page contains exactly 5 repeated log entries.
Each entry has these fields:
- date
- time
- description
- signature

Return bounding boxes for each field.

Output JSON ONLY in this schema:
{
  "entries": [
    {
      "date": {"x": number, "y": number, "width": number, "height": number},
      "time": {"x": number, "y": number, "width": number, "width": number},
      "description": {"x": number, "y": number, "width": number, "height": number},
      "signature": {"x": number, "y": number, "width": number, "height": number}
    }
  ]
}

Coordinates are IMAGE PIXELS.
Top-left origin.
"""

def detect_layout(image_path):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY not found in .env")

    client = genai.Client(api_key=api_key)
    img = Image.open(image_path)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[img, PROMPT],
        config={
            "response_mime_type": "application/json",
            "temperature": 0
        }
    )

    return json.loads(response.text)
