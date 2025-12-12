from typing import List
from PyPDF2 import PdfReader
from kion_pgvectorstore.file_loader import FileLoader
from kion_pgvectorstore.document import Document

class KionPDFFileLoader(FileLoader):
    # Constructor to pass PDF file_path
    def __init__(self, file_path, chunk_size, chunk_overlap):
        super().__init__(file_path, chunk_size, chunk_overlap)
        print(f"Initialized KionPDFFileLoader with file_path: {file_path}, chunk_size: {chunk_size}, chunk_overlap: {chunk_overlap}")

    def _normalize_pdf_text(self, text: str) -> str:
        """Best-effort cleanup of PDF-extracted text to improve chunk quality.

        - Remove soft hyphen characters (\xad) used for line wrapping in PDFs
        - Merge hyphenated line breaks: e.g. 'configu-\nration' -> 'configuration'
        - Collapse excessive internal spaces caused by PDF extraction
        """
        try:
            import re
            if not text:
                return text or ""
            # Remove soft hyphen
            text = text.replace("\xad", "")
            # Merge hyphenated breaks across lines
            text = re.sub(r"(\w)-\n(\w)", r"\1\2", text)
            # Replace isolated line breaks that split words without spaces: 'abc\ndef' -> 'abc def'
            text = re.sub(r"(\w)\n(\w)", r"\1 \2", text)
            # Collapse runs of spaces
            text = re.sub(r"[ \t]{2,}", " ", text)
            return text
        except Exception:
            return text

    # Load PDF File
    def load_file(self) -> List[Document]:
        reader = PdfReader(self.file_path)
        documents: List[Document] = []
        for i, page in enumerate(reader.pages, start=1):
            try:
                text = self._normalize_pdf_text(page.extract_text() or "")
            except Exception:
                text = ""
            documents.append(Document(page_content=text, metadata={'source': self.file_path, 'page': i}))
        print(f"Number of PDF Documents loaded = {len(documents)}")
        return documents