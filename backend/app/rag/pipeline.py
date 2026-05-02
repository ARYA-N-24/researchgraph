import os
import fitz  # PyMuPDF

from app.config import settings

# =========================
# Graph Imports
# =========================

from app.graph.entities import EntityExtractor
from app.graph.relationships import RelationshipExtractor
from app.graph.builder import GraphBuilder
from app.database.graph_store import GraphStore

# =========================
# Core Modules
# =========================

from app.document.loader import DocumentLoader
from app.document.chunker import DocumentChunker
from app.document.table_parser import TableParser

from app.rag.embeddings import EmbeddingModel
from app.database.pinecone_store import PineconeStore
from app.rag.retriever import Retriever
from app.models.llm import LLMModel

from app.multimodal.image_processor import ImageProcessor
from app.multimodal.clip_embeddings import CLIPEmbedding

from app.multimodal.audio_processor import AudioProcessor
from app.multimodal.audio_embeddings import AudioEmbedding


# =========================
# PDF IMAGE EXTRACTION
# =========================

def extract_images_from_pdf(pdf_path, output_folder):

    doc = fitz.open(pdf_path)

    image_count = 0

    for page_index in range(len(doc)):

        page = doc[page_index]

        images = page.get_images(full=True)

        for img_index, img in enumerate(images):

            xref = img[0]

            base_image = doc.extract_image(xref)

            image_bytes = base_image["image"]

            image_ext = base_image["ext"]

            image_name = (
                f"page_{page_index+1}_img_{img_index+1}.{image_ext}"
            )

            image_path = os.path.join(
                output_folder,
                image_name
            )

            with open(image_path, "wb") as f:

                f.write(image_bytes)

            image_count += 1

    print(f"🖼️ Extracted {image_count} images from PDF")


# =========================
# MAIN PIPELINE
# =========================

class RAGPipeline:

    def __init__(self):

        print("🚀 Initializing RAG Pipeline...")

        self.loader = DocumentLoader()

        self.chunker = DocumentChunker()

        self.table_parser = TableParser()

        self.embedder = EmbeddingModel()

        self.vector_store = PineconeStore()

        self.retriever = Retriever()

        self.llm = LLMModel()

        self.image_processor = ImageProcessor()

        self.clip_embedder = CLIPEmbedding()

        self.audio_processor = AudioProcessor()

        self.audio_embedder = AudioEmbedding()

        # Graph components

        self.entity_extractor = EntityExtractor()

        self.relationship_extractor = RelationshipExtractor()

        self.graph_builder = GraphBuilder()

        self.graph_store = GraphStore()

        print("✅ Pipeline initialized successfully")


    # =========================
    # BUILD INDEX
    # =========================

    def build_index(self):

        print("\n🚀 Starting multimodal index build...")

        # STEP 1 — LOAD DOCUMENTS

        print("\n📄 Loading documents...")

        documents = self.loader.load_all_documents()

        print(f"✅ Loaded {len(documents)} documents")


        # STEP 2 — EXTRACT PDF IMAGES

        print("\n🖼️ Extracting images from PDFs...")

        for file in os.listdir(settings.DOCUMENTS_DIR):

            if file.endswith(".pdf"):

                pdf_path = os.path.join(
                    settings.DOCUMENTS_DIR,
                    file
                )

                extract_images_from_pdf(
                    pdf_path,
                    settings.IMAGES_DIR
                )


        # STEP 3 — CHUNK TEXT

        print("\n✂️ Chunking text...")

        all_chunks = self.chunker.chunk_documents(documents)

        print(f"📚 Created {len(all_chunks)} text chunks")


        # STEP 4 — TABLE EXTRACTION

        print("\n📊 Extracting tables...")

        table_chunks = []

        try:

            table_chunks = self.table_parser.extract_all_tables()

            print(f"📊 Extracted {len(table_chunks)} tables")

        except Exception as e:

            print(f"⚠️ Table extraction failed: {e}")


        # STEP 5 — IMAGE PROCESSING

        print("\n🖼️ Processing images...")

        image_explanations = self.image_processor.explain_all_images()

        print(f"🖼️ Processed {len(image_explanations)} images")


        # STEP 6 — AUDIO PROCESSING

        print("\n🎵 Processing audio files...")

        extracted_audio = self.audio_processor.process_audio_files()

        audio_chunks = []

        for audio in extracted_audio:

            audio_chunks.append({

                "content":
                f"Audio content from {audio['source']}",

                "metadata": {
                    "source": audio["source"],
                    "type": "audio"
                }

            })


        # STEP 7 — TEXT EMBEDDINGS

        print("\n🧠 Generating text embeddings...")

        combined_text_chunks = all_chunks + table_chunks

        text_list = [

            chunk["content"]

            for chunk in combined_text_chunks

        ]

        text_embeddings = self.embedder.embed_documents(text_list)

        print(f"✅ Generated {len(text_embeddings)} text embeddings")


        # STEP 8 — IMAGE EMBEDDINGS

        print("\n🧠 Generating CLIP embeddings...")

        clip_data = self.clip_embedder.embed_all_images()

        clip_chunks = []
        clip_vectors = []

        for item in clip_data:

            clip_chunks.append({

                "content":
                f"Image content from {item['source']}",

                "metadata": {
                    "source": item["source"],
                    "type": "image"
                }

            })

            clip_vectors.append(item["embedding"])


        # STEP 9 — AUDIO EMBEDDINGS

        print("\n🧠 Generating audio embeddings...")

        audio_vectors = []

        for audio in extracted_audio:

            emb = self.audio_embedder.embed_audio(audio["path"])

            audio_vectors.append(emb)


        # STEP 10 — COMBINE ALL

        print("\n🔗 Combining embeddings...")

        combined_embeddings = []
        combined_chunks = []

        combined_embeddings.extend(text_embeddings)
        combined_chunks.extend(combined_text_chunks)

        combined_embeddings.extend(clip_vectors)
        combined_chunks.extend(clip_chunks)

        combined_embeddings.extend(audio_vectors)
        combined_chunks.extend(audio_chunks)

        print(f"📦 Total vectors: {len(combined_embeddings)}")


        # STEP 11 — STORE

        print("\n📡 Uploading to Pinecone...")

        self.vector_store.upsert_embeddings(
            combined_embeddings,
            combined_chunks
        )

        print("✅ Pinecone upload complete")


        # STEP 12 — GRAPH BUILD

        print("\n🧠 Building Knowledge Graph...")

        entities = self.entity_extractor.extract_from_chunks(
            combined_chunks
        )

        relationships = self.relationship_extractor.create_relationships(
            entities
        )

        self.graph_builder.add_entities(entities)

        self.graph_builder.add_relationships(relationships)

        graph = self.graph_builder.get_graph()

        self.graph_store.save_graph(graph)

        print("🧠 Knowledge graph saved successfully")

        print("\n✅ FULL INDEX BUILD COMPLETE")


    # =========================
    # QUERY FUNCTION
    # =========================

    def query(self, user_query):

        print("\n🔍 Running Graph-aware Query...")

        graph = self.graph_store.load_graph()

        graph_context = []

        expanded_query = user_query

        final_context = []


        # =========================
        # GRAPH EXPANSION
        # =========================

        if graph is not None:

            print("🧠 Graph loaded")

            query_entities = (

                self.entity_extractor
                .extract_entities(user_query)

            )

            print(
                f"🔎 Query entities: {query_entities}"
            )

            related_nodes = set()

            for entity in query_entities:

                if entity in graph:

                    neighbors = list(
                        graph.neighbors(entity)
                    )[:5]

                    related_nodes.update(
                        neighbors
                    )

            if related_nodes:

                graph_context = list(
                    related_nodes
                )

                expanded_query += (

                    " Related concepts: "
                    + ", ".join(graph_context)

                )

                print(
                    f"🔗 Graph context added: {graph_context}"
                )


        # =========================
        # VECTOR RETRIEVAL
        # =========================

        retrieved_chunks = (

            self.retriever.retrieve(
                expanded_query
            )

        )

        formatted_chunks = []

        for chunk in retrieved_chunks:

            if isinstance(chunk, dict):

                formatted_chunks.append(chunk)

            else:

                formatted_chunks.append({

                    "content": str(chunk)

                })


        # =========================
        # ADD GRAPH CONTEXT
        # =========================

        if graph_context:

            final_context.append({

                "content":
                "Related concepts: "
                + ", ".join(graph_context)

            })


        final_context.extend(
            formatted_chunks
        )


        # =========================
        # GENERATE ANSWER
        # =========================

        answer = (

            self.llm.generate_answer(

                user_query,

                final_context

            )

        )


        # ✅ FIXED RETURN FORMAT

        return {

            "answer": answer,

            "graph_nodes": graph_context

        }