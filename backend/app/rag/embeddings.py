from langchain_ollama import OllamaEmbeddings


class EmbeddingModel:
    """
    Text embedding model.

    Fix:
    Model outputs 1024-d vectors
    Pinecone expects 512
    → We truncate to 512
    """

    def __init__(self):

        print("🧠 Loading text embedding model...")

        self.embedding_model = OllamaEmbeddings(
            model="mxbai-embed-large"
        )

        # Target dimension
        self.target_dimension = 512

        print("✅ Text embedding model ready")


    def embed_documents(self, documents):

        texts = []

        for doc in documents:

            if isinstance(doc, dict):

                texts.append(
                    doc.get("content", "")
                )

            else:

                texts.append(str(doc))


        raw_embeddings = (
            self.embedding_model
            .embed_documents(texts)
        )


        # =========================
        # TRUNCATE TO 512
        # =========================

        fixed_embeddings = []

        for emb in raw_embeddings:

            if len(emb) > self.target_dimension:

                emb = emb[:self.target_dimension]

            fixed_embeddings.append(emb)


        return fixed_embeddings