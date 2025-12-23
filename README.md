# PDF Letterhead Overlay Tool

This project automates the process of applying a company letterhead to a batch of PDF documents. It scrapes a web directory for PDF files, downloads them, shifts the content down to make space for a header, applies the letterhead as a background, and saves the final files locally.

## Features
* **Auto-Discovery:** Scrapes a given URL to find all linked PDF files.
* **Smart Overlay:** Places the content *on top* of your letterhead (watermark style).
* **Content Shifting:** Automatically moves original text down (configurable) to prevent overlapping with the letterhead header.
* **Environment Config:** All settings (URLs, paths) are managed via a simple `.env` file.

## Prerequisites
* Python 3.6+ (Recommended: 3.12)

## Installation

1.  **Clone or download** this repository.

2.  **Create and activate a virtual environment** (Recommended):
    * **Windows:**
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```
    * **Mac/Linux:**
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```

3.  **Install dependencies** using pip:
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

Create a file named `.env` in the root directory and add the following settings:

```env
# The URL containing the list of PDFs to download
PDF_INDEX_URL=[http://example.com/documents/](http://example.com/documents/)

# The local path to your letterhead PDF (Single page background)
LETTERHEAD_PATH=letterhead.pdf

# The folder where processed files will be saved
OUTPUT_DIR=processed_pdfs

# How far to move the original text down (in points)
# 20 points is approx 7mm. Increase this if text overlaps your header.
SHIFT_DOWN_AMOUNT=20
```

## Usage

1. Ensure your `letterhead.pdf` is in the project folder (or update the path in `.env`).
2. Run the script:
```bash
python main.py

```
3. Check the `processed_pdfs` folder for your results.

## Troubleshooting

* **Header blocked?** Ensure your original content PDFs have a transparent background. If they are scanned images with white backgrounds, the letterhead will be hidden behind them.
* **Overlapping text?** Increase the `SHIFT_DOWN_AMOUNT` in your `.env` file.

```

```
