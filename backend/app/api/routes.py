from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel
import os
import shutil

from app.rag.pipeline import RAGPipeline
from app.config import settings


# =========================
# Create Router
# =========================

router = APIRouter()

# Initialize pipeline
pipeline = RAGPipeline()


# =========================
# Request Models
# =========================

class QueryRequest(BaseModel):
    query: str


class TextUploadRequest(BaseModel):
    text: str


# =========================
# Upload PDF
# =========================

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):

    save_path = os.path.join(
        settings.DOCUMENTS_DIR,
        file.filename
    )

    with open(save_path, "wb") as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )

    return {
        "message":
        f"{file.filename} uploaded successfully"
    }


# =========================
# Upload Audio
# =========================

@router.post("/upload-audio")
async def upload_audio(file: UploadFile = File(...)):

    save_path = os.path.join(
        settings.AUDIO_DIR,
        file.filename
    )

    with open(save_path, "wb") as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )

    return {
        "message":
        f"Audio uploaded: {file.filename}"
    }


# =========================
# Upload Image
# =========================

@router.post("/upload-image")
async def upload_image(file: UploadFile = File(...)):

    save_path = os.path.join(
        settings.IMAGES_DIR,
        file.filename
    )

    with open(save_path, "wb") as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )

    return {
        "message":
        f"Image uploaded: {file.filename}"
    }


# =========================
# Upload Manual Text
# FIXED VERSION
# =========================

@router.post("/upload-text")
async def upload_text(
    request: TextUploadRequest
):

    file_path = os.path.join(
        settings.DOCUMENTS_DIR,
        "manual_input.txt"
    )

    # Append text instead of overwrite
    with open(
        file_path,
        "a",
        encoding="utf-8"
    ) as f:

        f.write(request.text)
        f.write("\n\n")

    return {
        "message":
        "Text uploaded successfully"
    }


# =========================
# Build Index
# =========================

@router.post("/build-index")
def build_index():

    pipeline.build_index()

    return {
        "message":
        "Index built successfully"
    }


# =========================
# Query RAG
# =========================

@router.post("/query")
def query_rag(request: QueryRequest):

    result = pipeline.query(
        request.query
    )

    return {

        "query": request.query,

        "answer": result["answer"],

        "graph_nodes":
        result["graph_nodes"]

    }


# =========================
# Get Graph Data (LIMITED)
# =========================

@router.get("/graph")
def get_graph():

    graph = pipeline.graph_store.load_graph()

    if graph is None:

        return {
            "nodes": [],
            "edges": []
        }

    MAX_NODES = 50

    nodes = list(
        graph.nodes()
    )[:MAX_NODES]

    edges = []

    for edge in graph.edges():

        if (
            edge[0] in nodes and
            edge[1] in nodes
        ):

            edges.append({

                "source": edge[0],
                "target": edge[1]

            })

    return {

        "nodes": nodes,
        "edges": edges

    }