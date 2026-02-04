import os
import json
from PIL import Image
from dotenv import load_dotenv
from google import genai

load_dotenv()

PROMPT = """
Analyze the PDF form image.
Focus ONLY on the **Right Column** (the empty fillable side).

Task:
Identify the **Inner Safe Content Area** for each field.
- The box should NOT touch the black grid lines.
- **Shrink your selection slightly** inwards to exclude borders.
- The left edge (xmin) must be clearly inside the white space, to the right of the vertical divider.

Return JSON:
{
  "fields": [
    {
      "type": "string",  // e.g. "date", "time", "name", "location", "purpose_description", "signature"
      "box_2d": [ymin, xmin, ymax, xmax] // 0-1000 scale
    }
  ]
}
"""

def detect_fields(image_path):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY not found in .env")

    client = genai.Client(api_key=api_key)
    img = Image.open(image_path)

    response = client.models.generate_content(
        model="gemini-2.5-flash", 
        contents=[PROMPT, img],
        config={
            "response_mime_type": "application/json",
            "temperature": 0
        }
    )

    try:
        return json.loads(response.text)
    except json.JSONDecodeError:
        print("Raw response:", response.text)
        raise RuntimeError("Gemini returned invalid JSON")