from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.config import settings


class DocumentChunker:
    """
    Splits large documents into smaller chunks.
    """

    def __init__(self):

        self.chunk_size = settings.CHUNK_SIZE
        self.chunk_overlap = settings.CHUNK_OVERLAP

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap
        )

    def chunk_document(self, document):

        """
        Split a single document into chunks.
        """

        text = document["content"]

        chunks = self.text_splitter.split_text(text)

        chunked_docs = []

        for i, chunk in enumerate(chunks):

            chunked_docs.append({
                "file_name": document["file_name"],
                "chunk_id": i,
                "content": chunk
            })

        return chunked_docs

    def chunk_documents(self, documents):

        """
        Split multiple documents into chunks.
        """

        all_chunks = []

        for document in documents:

            chunks = self.chunk_document(document)

            all_chunks.extend(chunks)

        return all_chunks