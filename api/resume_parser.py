import io
import fitz  # PyMuPDF
from docx import Document

def extract_resume_text(content_type: str, file_data: bytes, filename: str) -> str:
    content_type = content_type.lower()
    filename = filename.lower()

    if "pdf" in content_type or filename.endswith(".pdf"):
        doc = fitz.open(stream=file_data, filetype="pdf")
        return " ".join(page.get_text() for page in doc)

    elif "word" in content_type or filename.endswith(".docx"):
        doc = Document(io.BytesIO(file_data))
        return "\n".join(p.text for p in doc.paragraphs if p.text.strip())

    else:
        raise ValueError("Unsupported file format")
