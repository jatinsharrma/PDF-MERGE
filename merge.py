import os
import requests
import io
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from dotenv import load_dotenv
from pypdf import PdfReader, PdfWriter, Transformation

# 1. Load environment variables
load_dotenv()

# Read config from .env (with defaults as backup)
INDEX_URL = os.getenv("PDF_INDEX_URL")
LETTERHEAD_PATH = os.getenv("LETTERHEAD_PATH", "letterhead.pdf")
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "processed_pdfs")
# Convert string '20' to integer 20. Default to 20 if missing.
SHIFT_DOWN = int(os.getenv("SHIFT_DOWN_AMOUNT", 20))

def process_pdfs():
    # Validation
    if not INDEX_URL:
        print("Error: PDF_INDEX_URL is missing in .env file")
        return
    
    # 2. Setup Output Directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 3. Load Letterhead
    try:
        letterhead_reader = PdfReader(LETTERHEAD_PATH)
        letterhead_page = letterhead_reader.pages[0] 
        print(f"Loaded letterhead from: {LETTERHEAD_PATH}")
    except FileNotFoundError:
        print(f"Error: Letterhead file not found at '{LETTERHEAD_PATH}'")
        return

    # 4. Scrape the URL
    print(f"Scanning {INDEX_URL}...")
    try:
        response = requests.get(INDEX_URL)
        response.raise_for_status()
    except Exception as e:
        print(f"Failed to fetch URL: {e}")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    
    # Find links ending in .pdf (case insensitive)
    pdf_links = [a['href'] for a in soup.find_all('a', href=True) 
                 if a['href'].lower().endswith('.pdf')]

    print(f"Found {len(pdf_links)} PDFs. Starting processing...")

    # 5. Loop through and process
    for link in pdf_links:
        full_url = urljoin(INDEX_URL, link)
        filename = os.path.basename(link)
        save_path = os.path.join(OUTPUT_DIR, filename)

        try:
            print(f"Processing: {filename}...")
            
            # Download into memory
            pdf_response = requests.get(full_url)
            pdf_response.raise_for_status()
            content_stream = io.BytesIO(pdf_response.content)

            # Process
            writer = PdfWriter()
            content_reader = PdfReader(content_stream)

            for content_page in content_reader.pages:
                # A. Shift Content Down
                # tx=0 (no horizontal move), ty=-SHIFT_DOWN (move down)
                content_page.add_transformation(
                    Transformation().translate(tx=0, ty=-SHIFT_DOWN)
                )
                
                # B. Merge Letterhead (Background)
                # over=False puts letterhead behind the content
                content_page.merge_page(letterhead_page, over=False)
                
                writer.add_page(content_page)

            # Save
            with open(save_path, "wb") as f_out:
                writer.write(f_out)
                
        except Exception as e:
            print(f"  -> Failed to process {filename}: {e}")

    print("\nAll tasks completed.")

if __name__ == "__main__":
    process_pdfs()
