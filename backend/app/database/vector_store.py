import os
import faiss
import pickle
import numpy as np

from app.config import settings


class VectorStore:
    """
    Handles FAISS vector storage
    and similarity search.
    """

    def __init__(self):

        self.index_path = os.path.join(
            settings.VECTOR_STORE_DIR,
            "faiss_index.index"
        )

        self.metadata_path = os.path.join(
            settings.VECTOR_STORE_DIR,
            "metadata.pkl"
        )

        self.index = None
        self.metadata = []

        # Create directory if missing
        os.makedirs(
            settings.VECTOR_STORE_DIR,
            exist_ok=True
        )

    def create_index(self, embeddings, chunks):

        """
        Create FAISS index.
        """

        embedding_dim = len(embeddings[0])

        self.index = faiss.IndexFlatL2(
            embedding_dim
        )

        vectors = np.array(
            embeddings
        ).astype("float32")

        self.index.add(vectors)

        self.metadata = chunks

        self.save_index()

    def save_index(self):

        """
        Save FAISS index to disk.
        """

        faiss.write_index(
            self.index,
            self.index_path
        )

        with open(
            self.metadata_path,
            "wb"
        ) as f:

            pickle.dump(
                self.metadata,
                f
            )

    def load_index(self):

        """
        Load saved FAISS index.
        """

        if not os.path.exists(
            self.index_path
        ):
            return False

        self.index = faiss.read_index(
            self.index_path
        )

        with open(
            self.metadata_path,
            "rb"
        ) as f:

            self.metadata = pickle.load(f)

        return True

    def search(self, query_embedding, k=3):

        """
        Perform similarity search.
        """

        query_vector = np.array(
            [query_embedding]
        ).astype("float32")

        distances, indices = self.index.search(
            query_vector,
            k
        )

        results = []

        for idx in indices[0]:

            results.append(
                self.metadata[idx]
            )

        return results