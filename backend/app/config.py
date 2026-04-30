import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Settings:
    """
    Central configuration class.
    All system-wide settings go here.
    """

    # Base paths
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    DATA_DIR = os.path.join(BASE_DIR, "../../data")

    DOCUMENTS_DIR = os.path.join(DATA_DIR, "documents")
    IMAGES_DIR = os.path.join(DATA_DIR, "images")
    TABLES_DIR = os.path.join(DATA_DIR, "tables")
    AUDIO_DIR = os.path.join(DATA_DIR, "audio")

    VECTOR_STORE_DIR = os.path.join(DATA_DIR, "vector_store")
    GRAPH_STORE_DIR = os.path.join(DATA_DIR, "graph")

    # Model settings
    EMBEDDING_MODEL = "text-embedding-3-small"

    LLM_MODEL = "gpt-4.1-mini"

    # Chunking settings
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200

    # OpenAI API key
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


# Create singleton settings object
settings = Settings()