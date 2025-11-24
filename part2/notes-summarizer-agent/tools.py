import json
from pypdf import PdfReader
from datetime import datetime

def extract_text_from_pdf(file) -> str:
    """Extract text from uploaded PDF file."""
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def save_to_memory(filename: str, metadata: dict):
    """Save file metadata to memory.json."""
    try:
        memory = load_memory()
    except FileNotFoundError:
        memory = []
    
    entry = {
        "filename": filename,
        "timestamp": datetime.now().isoformat(),
        **metadata
    }
    memory.append(entry)
    
    with open("memory.json", "w") as f:
        json.dump(memory, f, indent=2)

def load_memory() -> list:
    """Load memory entries from memory.json."""
    try:
        with open("memory.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
