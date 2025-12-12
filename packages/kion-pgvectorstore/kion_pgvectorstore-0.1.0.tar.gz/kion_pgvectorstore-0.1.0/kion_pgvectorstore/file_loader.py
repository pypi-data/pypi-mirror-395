# from abc import ABC#, abstractmethod
import os
from typing import List, Any
from kion_pgvectorstore.document import Document
from kion_pgvectorstore.recursive_text_splitter import RecursiveCharacterTextSplitter

class FileLoader:
    # Constructor to pass a File path
    def __init__(self, file_path: str, chunk_size: int, chunk_overlap: int):
        self.file_path = file_path
        self.chunk_size = int(chunk_size)
        self.chunk_overlap = int(chunk_overlap)

    # Create a method that will call the correct loader
    def call_file_loader(self) -> List[Document]:
        print(f"working directory: {os.getcwd()} - file_path: {self.file_path} ")
        print(f"Calling file loader for: {self.file_path}")
        return self.load_file()
    
    # Split Documents into chunks
    def split_data(self, loaded_documents, collection_name):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
            is_separator_regex=False
        )
        chunks = text_splitter.split_documents(loaded_documents)

        file_name = os.path.basename(self.file_path)  # Extract file name from path
        print(f"File name for metadata: {file_name}")

        for chunk in chunks:
            custom_metadata = {
                'file_name': os.path.basename(self.file_path),
                'collection_name': collection_name
            }
            chunk.metadata.update(custom_metadata)

        print("Chunking done")
        return chunks


    def embed_chunks(self, chunks: List[Document]) -> List[Any]:
        raise NotImplementedError("Use PGVectorPlugin to handle embeddings and storage.")

    # Mutator methods for file_path, chunk_size, and chunk_overlap
    def set_file_path(self, file_path: str):
        self.file_path = file_path

    def set_chunk_size(self, chunk_size: int):
        self.chunk_size = int(chunk_size)

    def set_chunk_overlap(self, chunk_overlap: int):
        self.chunk_overlap = int(chunk_overlap)