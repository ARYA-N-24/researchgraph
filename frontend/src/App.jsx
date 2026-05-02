import { useState } from "react";
import axios from "axios";
import GraphView from "./GraphView";

function App() {

  // =========================
  // State Variables
  // =========================

  const [query, setQuery] = useState("");
  const [answer, setAnswer] = useState("");

  const [file, setFile] = useState(null);
  const [audioFile, setAudioFile] = useState(null);
  const [imageFile, setImageFile] = useState(null);

  const [manualText, setManualText] = useState("");

  const [loading, setLoading] = useState(false);

  const [showGraph, setShowGraph] = useState(false);
  const [activeNodes, setActiveNodes] = useState([]);

  const API_URL = "http://127.0.0.1:8000";


  // =========================
  // Upload PDF
  // =========================

  const uploadFile = async () => {

    if (!file) {
      alert("Please select a PDF file.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {

      setLoading(true);

      const res = await axios.post(
        `${API_URL}/upload`,
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data"
          }
        }
      );

      alert(res.data.message);

    } catch (err) {

      console.error(err);
      alert("PDF upload failed.");

    } finally {

      setLoading(false);

    }

  };


  // =========================
  // Upload Audio
  // =========================

  const uploadAudio = async () => {

    if (!audioFile) {
      alert("Please select an audio file.");
      return;
    }

    const formData = new FormData();
    formData.append("file", audioFile);

    try {

      setLoading(true);

      const res = await axios.post(
        `${API_URL}/upload-audio`,
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data"
          }
        }
      );

      alert(res.data.message);

    } catch (err) {

      console.error(err);
      alert("Audio upload failed.");

    } finally {

      setLoading(false);

    }

  };


  // =========================
  // Upload Image
  // =========================

  const uploadImage = async () => {

    if (!imageFile) {
      alert("Please select an image.");
      return;
    }

    const formData = new FormData();
    formData.append("file", imageFile);

    try {

      setLoading(true);

      const res = await axios.post(
        `${API_URL}/upload-image`,
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data"
          }
        }
      );

      alert(res.data.message);

    } catch (err) {

      console.error(err);
      alert("Image upload failed.");

    } finally {

      setLoading(false);

    }

  };


  // =========================
  // Upload Manual Text
  // =========================

  const uploadText = async () => {

    if (!manualText) {
      alert("Enter text first.");
      return;
    }

    try {

      setLoading(true);

      const res = await axios.post(
        `${API_URL}/upload-text`,
        {
          text: manualText
        }
      );

      alert(res.data.message);

    } catch (err) {

      console.error(err);
      alert("Text upload failed.");

    } finally {

      setLoading(false);

    }

  };


  // =========================
  // Build Index
  // =========================

  const buildIndex = async () => {

    try {

      setLoading(true);

      const res = await axios.post(
        `${API_URL}/build-index`
      );

      alert(res.data.message);

    } catch (err) {

      console.error(err);
      alert("Index build failed.");

    } finally {

      setLoading(false);

    }

  };


  // =========================
  // Ask Question
  // =========================

  const askQuestion = async () => {

    if (!query) {
      alert("Please enter a question.");
      return;
    }

    try {

      setLoading(true);

      const res = await axios.post(
        `${API_URL}/query`,
        {
          query: query
        }
      );

      setAnswer(res.data.answer);

      setActiveNodes(
        res.data.graph_nodes || []
      );

    } catch (err) {

      console.error(err);
      alert("Error getting answer.");

    } finally {

      setLoading(false);

    }

  };


  // =========================
  // UI Layout
  // =========================

  return (

    <div style={{ padding: "40px", fontFamily: "Arial" }}>

      <h1>🧠 ResearchGraph</h1>

      <h3>
        Multi-Modal Research Paper Assistant
      </h3>

      <hr />


      {/* Upload PDF */}

      <h3>📂 Upload PDF</h3>

      <input
        type="file"
        accept=".pdf"
        onChange={(e) =>
          setFile(e.target.files[0])
        }
      />

      <br /><br />

      <button
        onClick={uploadFile}
        disabled={loading}
      >
        Upload PDF
      </button>

      <hr />


      {/* Upload Audio */}

      <h3>🎧 Upload Audio</h3>

      <input
        type="file"
        accept=".wav,.mp3,.ogg,.m4a"
        onChange={(e) =>
          setAudioFile(
            e.target.files[0]
          )
        }
      />

      <br /><br />

      <button
        onClick={uploadAudio}
        disabled={loading}
      >
        Upload Audio
      </button>

      <hr />


      {/* Upload Image */}

      <h3>🖼 Upload Image</h3>

      <input
        type="file"
        accept=".png,.jpg,.jpeg,.webp,.bmp"
        onChange={(e) =>
          setImageFile(
            e.target.files[0]
          )
        }
      />

      <br /><br />

      <button
        onClick={uploadImage}
        disabled={loading}
      >
        Upload Image
      </button>

      <hr />


      {/* Manual Text */}

      <h3>📝 Enter Text</h3>

      <textarea
        rows="6"
        cols="70"
        placeholder="Paste text content here..."
        value={manualText}
        onChange={(e) =>
          setManualText(e.target.value)
        }
      />

      <br /><br />

      <button
        onClick={uploadText}
        disabled={loading}
      >
        Upload Text
      </button>

      <hr />


      {/* Build Index */}

      <button
        onClick={buildIndex}
        disabled={loading}
      >
        📂 Build Index
      </button>

      <br /><br />


      {/* Query */}

      <input
        type="text"
        placeholder="Ask a question..."
        value={query}
        onChange={(e) =>
          setQuery(e.target.value)
        }
        style={{
          width: "400px",
          padding: "10px"
        }}
      />

      <br /><br />

      <button
        onClick={askQuestion}
        disabled={loading}
      >
        🔍 Get Answer
      </button>

      <hr />


      {/* ========================= */}
      {/* Knowledge Graph Section */}
      {/* ========================= */}

      <h3>📊 Knowledge Graph</h3>

      <button
        onClick={() =>
          setShowGraph(!showGraph)
        }
      >
        {showGraph ? "Hide Graph" : "Show Graph"}
      </button>

      <br /><br />

      {showGraph && (

        <GraphView
          activeNodes={activeNodes}
        />

        )}


      {/* Loading */}

      {loading && (
        <p>⏳ Processing...</p>
      )}


      {/* Answer */}

      <h3>📢 Answer:</h3>

      <div
        style={{
          border: "1px solid gray",
          padding: "15px",
          width: "600px",
          minHeight: "150px",
          backgroundColor: "#f9f9f9"
        }}
      >

        {answer}

      </div>

    </div>

  );

}

export default App;