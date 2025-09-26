import { useState } from "react";
import "./UploadForm.css";

function UploadForm({ onQuestionsReceived }) {
  const [file, setFile] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) return alert("Selecione um arquivo JSON!");

    const text = await file.text();
    const jsonData = JSON.parse(text);

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
      onQuestionsReceived(data.questions);
    } catch (err) {
      console.error("Erro ao enviar arquivo:", err);
    }
  };

  return (
    <div className="upload-container">
      <label className="custom-file-upload">
        <input type="file" accept="application/json" onChange={handleFileChange} />
        Escolher arquivo
      </label>
      <span className="file-name">{file ? file.name : "Nenhum arquivo selecionado"}</span>

      <button type="button" className="upload-btn" onClick={handleUpload}>
        Enviar
      </button>
    </div>
  );
}

export default UploadForm;
