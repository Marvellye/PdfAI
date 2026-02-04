# AI PDF Filler 🤖📄

An intelligent Python-based tool that uses Large Language Models (LLMs) to automatically map data to PDF form fields. Stop manually mapping JSON keys to PDF field names—let AI handle the context.

## 🚀 Features

- **Smart Mapping**: Uses AI to understand the relationship between your input data and PDF field names (e.g., mapping "home_address" to a PDF field named "ADDR_1").
- **Batch Processing**: Fill multiple PDFs or multiple records in one go.
- **Visual Verification**: Generates a preview of filled fields for review.
- **Support for Multiple LLMs**: Compatible with OpenAI (GPT-4), Anthropic (Claude), and local models via Ollama.
- **Preserves PDF Metadata**: Keeps the original PDF formatting and structure intact.

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Marvellye/pdfai.git
   cd pdfai
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your environment variables:**
   Create a `.env` file in the root directory:
   ```env
   GEMINI_API_KEY=your_api_key_here
   ```

## 📖 Usage


### How it Works
1. **Extraction**: The tool extracts all interactive field names from the target PDF.
2. **Reasoning**: It sends the field names and your data schema to the LLM to determine the best matches.
3. **Injection**: It uses `pypdf` or `pdfrw` to write the values into the PDF buffer.
4. **Flattening**: (Optional) Flattens the form so it is no longer editable.

## 📋 Requirements

- Python 3.8+
- `pypdf` or `fitz` (PyMuPDF)
- `python-dotenv`

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
*Note: This tool is intended to assist with form filling. Always verify the output for accuracy, especially for legal or medical documents.*