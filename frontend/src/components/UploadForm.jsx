import { useState } from "react";
import "./UploadForm.css";

function UploadForm({ onDataReceived }) {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) return alert("Selecione um arquivo JSON!");

    const text = await file.text();
    const jsonData = JSON.parse(text);

    setLoading(true);
    try {
      const baseURL = import.meta.env.VITE_FLASK_API_URL;
      const res = await fetch(`${baseURL}/questions`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(jsonData),
      });

      const data = await res.json();

      // Esperando que o backend retorne algo como:
      // { questions: [...], candidateSummary: "...", jobSummary: "..." }
      onDataReceived({
        questions: data.questions,
        candidateSummary: data.candidateSummary,
        jobSummary: data.jobSummary,
      });
    } catch (err) {
      console.error("Erro ao enviar arquivo:", err);
      alert("Erro ao enviar arquivo. Veja o console para mais detalhes.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="upload-container">
      <label className="custom-file-upload">
        <input type="file" accept="application/json" onChange={handleFileChange} />
        Escolher arquivo
      </label>
      <span className="file-name">{file ? file.name : "Nenhum arquivo selecionado"}</span>

      <button 
        type="button" 
        className="upload-btn" 
        onClick={handleUpload}
        disabled={loading}
      >
        Enviar
      </button>

      {loading && (
        <div className="loading-overlay">
          <div className="spinner"></div>
          <span> Processando...</span>
        </div>
      )}
    </div>
  );
}

export default UploadForm;
