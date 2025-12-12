from abc import ABC, abstractmethod

class VectorDatabase(ABC):
    @abstractmethod
    def list_collections(self):
        pass

    @abstractmethod
    def list_files(self, collection_name):
        pass

    @abstractmethod
    def add_documents(self, documents, collection_name, metadata=None):
        pass

    @abstractmethod
    def delete_file(self, collection_name, file_name):
        pass

    @abstractmethod
    def delete_collection(self, collection_name):
        pass

    @abstractmethod
    def similarity_search_with_scores(self, collection_name, query, k=5):
        pass