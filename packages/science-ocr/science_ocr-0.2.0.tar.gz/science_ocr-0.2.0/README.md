# Science-OCR

**Science-OCR** is a lightweight, ready-to-use Python package designed to extract clean, structured text from scientific papers in PDF format. It wraps a simple interface around Surya-OCR's `layout`, `text_detection`, and `text_recognition` models, while using PyMuPDF (fitz) to rasterize PDF pages into images for processing.

This tool is ideal for researchers, data scientists, and developers who want reliable OCR extraction from research papers—without dealing with complicated pipelines.

## ✨ Features

* 📄 Optimized for scientific PDFs
* 🔍 High-accuracy OCR with Surya-OCR (layout + detection + recognition)
* 🧩 Minimal API — only one method to use
* 🐍 Easy installation via `pip`
* 🚀 Zero setup — works out-of-the-box

## 📦 Installation

```bash
pip install science-ocr
```

No additional configuration required — models load automatically.

## 🚀 Quick Start

```python
from science_ocr import ScienceOCR

ocr = ScienceOCR()

text = ocr.parse_text(
    path="path/to/paper.pdf",
    first_page=0,      # optional
    last_page=None,    # optional
    dpi=300            # optional
)

print(text)
```

## 📘 API Reference

### `parse_text(self, path, first_page=0, last_page=None, dpi=300)`

Extracts OCR text from a PDF.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| path | str | — | Path to the PDF file. |
| first_page | int | 0 | 0-indexed first page to process. |
| last_page | int \| None | None | Last page index (inclusive). If `None`, processes until the final page. |
| dpi | int | 300 | Rasterization DPI for PyMuPDF before OCR. |

**Returns:** A single string containing the concatenated OCR text from the selected page range.

## 🧠 How It Works (Behind the Scenes)

1. PyMuPDF (fitz) loads the PDF and renders each page at the specified DPI.
2. Each rendered page image is passed through Surya-OCR:
   * `layout` model to detect structure
   * `text_detection` model to find text regions
   * `text_recognition` model to extract text
3. Results are merged and returned as clean, readable text.

This hybrid pipeline is optimized for the complex layouts of scientific literature (equations, tables, multi-column layouts, etc.).

## 📦 Model Weights

This package uses Surya-OCR models that are mirrored on HuggingFace for reliability:
- Mirror: `https://huggingface.co/TomasGD/surya-ocr-mirror-models-2025_05_07`

Models are subject to Surya's licensing terms (see [MODEL_LICENSE](MODEL_LICENSE)).

## 🤝 Contributing

Pull requests and suggestions are welcome! If you encounter any issues, please open an issue on the project's repository.

## 📄 License

**Science-OCR** is licensed under AGPL-3.0, but depends on:

- **PyMuPDF**: AGPL-3.0
- **Surya-OCR**: Code is GPL-3.0 & Models are AI Pubs Open Rail-M license (free for research, personal use, and startups under $2M funding/revenue)

**For commercial use exceeding $2M funding/revenue, you must obtain commercial licenses for the dependencies.**

## Disclaimer

The maintainers of Science-OCR are not responsible for ensuring your compliance with third-party licenses. It is your responsibility to review and comply with all applicable licenses for dependencies used in this project.
