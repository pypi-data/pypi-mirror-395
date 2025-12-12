"""
The Converter - Makes EVERYTHING into JSON
"""
import json
from bs4 import BeautifulSoup
import csv
from io import StringIO

def to_json(content, content_type="text/plain"):
    """
    Convert ANY content to JSON format
    
    Args:
        content: The raw content (string or bytes)
        content_type: What type of content it is
        
    Returns:
        dict: Always returns a Python dict (JSON-ready)
    """
    
    # If already JSON, just parse it
    if 'json' in content_type.lower():
        if isinstance(content, bytes):
            content = content.decode('utf-8')
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return {
                "error": True,
                "message": "Invalid JSON received",
                "raw_content": content[:500]
            }
    
    # If HTML, extract text and structure
    if 'html' in content_type.lower():
        if isinstance(content, bytes):
            content = content.decode('utf-8')
        try:
            soup = BeautifulSoup(content, 'lxml')
            return {
                "title": soup.title.string if soup.title else "No title",
                "text": soup.get_text(strip=True, separator=' ')[:1000],
                "links": [a.get('href') for a in soup.find_all('a', href=True)][:50],
                "images": [img.get('src') for img in soup.find_all('img', src=True)][:20],
                "content_type": "html"
            }
        except Exception as e:
            return {
                "error": True,
                "message": f"Failed to parse HTML: {str(e)}",
                "raw_content": content[:500]
            }
    
    # If CSV, convert to list of dicts
    if 'csv' in content_type.lower():
        if isinstance(content, bytes):
            content = content.decode('utf-8')
        try:
            reader = csv.DictReader(StringIO(content))
            return {
                "data": list(reader),
                "content_type": "csv"
            }
        except Exception as e:
            return {
                "error": True,
                "message": f"Failed to parse CSV: {str(e)}",
                "raw_content": content[:500]
            }
    
    # If plain text or anything else, wrap it in JSON
    if isinstance(content, bytes):
        try:
            content = content.decode('utf-8')
        except UnicodeDecodeError:
            content = content.decode('utf-8', errors='ignore')
    
    return {
        "content": content,
        "content_type": content_type
    }
