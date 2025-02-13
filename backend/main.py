from crawl4ai import AsyncWebCrawler
import asyncio
from pathlib import Path
import pdfplumber
import tempfile

async def crawl4ai_request(file_path: str) -> str:
    path = Path(file_path)
    
    # Permission conflict for crawl4ai so write file to a temporary text file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
        with pdfplumber.open(path) as pdf:
            text = ''
            for page in pdf.pages:
                text += page.extract_text() + '\n'
            # Write text to temporary file
            temp_file.write(text)
            temp_path = temp_file.name

    try:
        # Use file:// URL format with the temporary text file
        file_url = f"file://{temp_path}"
        async with AsyncWebCrawler() as crawler:
            result = await crawler.arun(file_url)
            return result.markdown
    finally:
        # Clean up temporary file
        Path(temp_path).unlink(missing_ok=True)
      
if __name__ == "__main__":
    # Example using relative path
    file_path = "relative/path/to/your/file.pdf"
    result = asyncio.run(crawl4ai_request(file_path))
    print(result)