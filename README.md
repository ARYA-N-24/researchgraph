# 🧠 ResearchGraph  
## Multi-Modal Graph RAG System for Research Intelligence

ResearchGraph is a **Multi-Modal Retrieval-Augmented Generation (RAG) system** enhanced with a **Knowledge Graph** for improved reasoning and contextual retrieval.

It supports **text, images, audio, and structured relationships**, enabling intelligent analysis of research papers and technical content.

---

# 🚀 Features

## 📄 Text Processing
- PDF ingestion
- Text chunking
- Semantic embeddings
- Vector search

## 🖼 Image Understanding
- Image extraction
- CLIP embeddings
- Visual reasoning

## 🎵 Audio Processing
- Whisper transcription
- Audio embeddings
- Speech understanding

## 🧠 Knowledge Graph (Graph RAG)
- Entity extraction
- Relationship modeling
- Graph-based reasoning
- Query expansion

## 🔎 Retrieval-Augmented Generation
- Pinecone vector database
- Top-K semantic retrieval
- Context-aware responses

## 📊 Graph Visualization
- Interactive knowledge graph
- Highlight active nodes
- Graph-aware reasoning

---

# 🧱 System Architecture


User Input
│
├── Text (PDF / Manual Input)
├── Images
├── Audio
│
▼
Multimodal Processing Layer
│
├── Text Embeddings
├── CLIP Image Embeddings
├── Audio Embeddings
│
▼
Vector Database (Pinecone)
│
▼
Knowledge Graph Builder
│
▼
Graph RAG Retrieval
│
▼
LLM Response Generation


---

# 🧰 Tech Stack

## Backend

- FastAPI
- LangChain
- Ollama (LLM + embeddings)
- Pinecone (Vector Database)
- NetworkX (Graph Processing)

## AI Models

- LLM → phi3 / llama3
- Text Embedding → nomic-embed-text
- Image Embedding → CLIP (ViT-B-32)
- Audio → Whisper

## Frontend

- React
- Axios
- ForceGraph2D
- Vite

---

# 📂 Project Structure


researchgraph/

backend/
│
├── app/
│ ├── api/
│ ├── rag/
│ ├── graph/
│ ├── database/
│ ├── document/
│ ├── multimodal/
│ └── models/
│
frontend/
│
data/
│ ├── documents/
│ ├── images/
│ ├── audio/
│ └── graph/
│
requirements.txt
README.md
.gitignore


---

# ⚙️ Installation

## Step 1 — Clone Repository
```bash
git clone https://github.com/ARYA-N-24/researchgraph.git
cd researchgraph

Step 2 — Backend Setup
cd backend
pip install -r requirements.txt

Step 3 — Install Ollama Models
ollama pull phi3
ollama pull nomic-embed-text
ollama pull llava

Step 4 — Run Backend
uvicorn app.main:app --reload

Step 5 — Frontend Setup
cd frontend
npm install
npm run dev

📥 Supported Inputs

Users can upload:

✔ PDF documents
✔ Images (.png, .jpg)
✔ Audio (.mp3, .wav, .ogg)
✔ Manual text

🔎 Example Queries
Explain CNN

Summarize transfer learning

What does Figure 3 represent?

Compare results in Table 2

Explain concepts mentioned in audio
📊 Knowledge Graph Output

The system builds:

Entity Nodes
Concept Relationships
Query-Aware Graph Context

Graph highlights:

Query Nodes → Highlighted
Related Concepts → Connected
🧪 Example Workflow
Upload PDF
Upload Audio
Upload Image
Upload Text

Build Index

Ask Query

View Graph Relationships
🎯 Use Cases
Research Paper Understanding
Literature Review Assistance
Educational Content Analysis
Scientific Knowledge Mapping
Multi-modal Learning Systems
🔐 Environment Variables

Create:

.env

Add:

PINECONE_API_KEY=your_key
PINECONE_INDEX_NAME=researchgraph

Arya N
Bharath S

GitHub:
https://github.com/ARYA-N-24

⭐ Project Status
✔ Multi-modal ingestion
✔ Pinecone vector storage
✔ CLIP image embeddings
✔ Whisper audio processing
✔ Knowledge graph generation
✔ Graph-aware retrieval
✔ Frontend visualization

Status: COMPLETE

---

# 🚀 After Adding README

Run:

```bash
git add README.md
git commit -m "Added professional README"
git push
