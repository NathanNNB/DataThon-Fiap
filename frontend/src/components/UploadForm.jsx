import { useState } from "react";
import "./UploadForm.css";

function UploadForm({ onQuestionsReceived }) {
  const [file, setFile] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) return alert("Selecione um arquivo JSON!");

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("http://localhost:5000/questions", {
        method: "POST",
        body: formData,
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

      <button className="upload-btn" onClick={handleUpload}>
        Enviar
      </button>
    </div>
  );
}

export default UploadForm;
