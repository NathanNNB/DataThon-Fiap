import { useState } from "react";
import UploadForm from "./components/UploadForm";
import "./App.css";

function App() {
  const [questions, setQuestions] = useState([]);

  return (
    <div className="app-container">
      <div className="left-pane">
        <h1>Upload de JSON</h1>
        <UploadForm onQuestionsReceived={setQuestions} />
      </div>

      <div className="right-pane">
        <h2>Questões recebidas</h2>
        {questions?.length === 0 ? (
          <p className="placeholder">Nenhuma questão ainda</p>
        ) : (
          <ul className="questions-list">
            {questions?.map((q, idx) => (
              <li key={idx} className="question-item">
                {q}
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}

export default App;
