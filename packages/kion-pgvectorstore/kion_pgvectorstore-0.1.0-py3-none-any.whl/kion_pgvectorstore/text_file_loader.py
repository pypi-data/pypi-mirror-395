from typing import List
from kion_pgvectorstore.file_loader import FileLoader
from kion_pgvectorstore.document import Document

class KionTextFileLoader(FileLoader):
    # Constructor to pass TXT file_path
    def __init__(self, file_path, chunk_size, chunk_overlap):
        super().__init__(file_path, chunk_size, chunk_overlap)

    # Load Text File
    def load_file(self) -> List[Document]:
        with open(self.file_path, 'r', encoding='utf-8') as f:
            text = f.read()
        # TextLoader returning a list with one Document
        documents = [Document(page_content=text, metadata={'source': self.file_path})]
        return documents