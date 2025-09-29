import { useState } from "react";
import UploadForm from "./components/UploadForm"; // ou UploadForm real
import StarRating from "./components/StarRating";
import "./App.css";

function App() {
  const [questions, setQuestions] = useState([]);
  const [candidateSummary, setCandidateSummary] = useState("");
  const [jobSummary, setJobSummary] = useState("");
  const [rating, setRating] = useState(0);
  const [submitted, setSubmitted] = useState(false);

  const handleDataReceived = ({ questions, candidateSummary, jobSummary }) => {
    setQuestions(questions || []);
    setCandidateSummary(candidateSummary || "");
    setJobSummary(jobSummary || "");
    setRating(0);
    setSubmitted(false);
  };

  const hasData = questions.length > 0 || candidateSummary || jobSummary;

  const submitEvaluation = async () => {
    if (!rating) return alert("Escolha uma avaliação antes de enviar!");

    const payload = {
      json_sent: {
        questions,
        candidateSummary,
        jobSummary
      },
      json_received: {
        questions,
        candidateSummary,
        jobSummary
      },
      rating
    };

    try {
      const baseURL = import.meta.env.VITE_FLASK_API_URL;
      const res = await fetch(`${baseURL}/submit_evaluation`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload)
      });
      const data = await res.json();
      if (res.ok) {
        alert("Avaliação enviada com sucesso!");
        setSubmitted(true);
      } else {
        console.error(data);
        alert("Erro ao enviar avaliação. Veja o console.");
      }
    } catch (err) {
      console.error(err);
      alert("Erro ao conectar com o servidor.");
    }
  };

  return (
    <div className="app-container">
      <div className="left-pane">
        <h1>Upload de JSON</h1>
        <UploadForm onDataReceived={handleDataReceived} />
      </div>

      <div className="right-pane">
        <h2>Resumo do Candidato</h2>
        {candidateSummary ? (
          <p className="summary">{candidateSummary}</p>
        ) : (
          <p className="placeholder">Nenhum resumo do candidato</p>
        )}

        <h2>Resumo da Vaga</h2>
        {jobSummary ? (
          <p className="summary">{jobSummary}</p>
        ) : (
          <p className="placeholder">Nenhum resumo da vaga</p>
        )}

        <h2>Questões Recebidas</h2>
        {questions.length === 0 ? (
          <p className="placeholder">Nenhuma questão ainda</p>
        ) : (
          <ul className="questions-list">
            {questions.map((q, idx) => (
              <li key={idx} className="question-item">
                {q}
              </li>
            ))}
          </ul>
        )}

        {/* Avaliação só aparece quando houver dados */}
        {hasData && !submitted && (
          <div className="rating-section">
            <h2>Avalie a qualidade das perguntas</h2>
            <StarRating rating={rating} onChange={setRating} />
            {rating > 0 && (
              <p>Você avaliou: {rating} estrela{rating > 1 ? "s" : ""}</p>
            )}
            <button 
              className="submit-btn" 
              onClick={submitEvaluation}
              disabled={rating === 0} // desabilitado até escolher nota
            >
              Enviar Avaliação
            </button>
          </div>
        )}

        {submitted && <p>✅ Avaliação enviada!</p>}
      </div>
    </div>
  );
}

export default App;
