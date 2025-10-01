# DataThon-Fiap


Back
https://flask-service-1092765354740.us-central1.run.app/




# Backend DataThon-FIAP

Este backend foi desenvolvido em Python utilizando Flask para servir rotas REST e Google BigQuery para persistência dos dados de avaliação. A arquitetura está organizada para facilitar a escalabilidade e manutenção.

## Estrutura de Pastas

```
## Estrutura de Pastas

```
backend/
├── app/
│   ├── __init__.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── questions.py
│   │   └── submit_evaluation.py
│   └── utils/
│       ├── __init__.py
│       ├── call_model.py
│       ├── create_table.py
│       ├── model_rag.py
│       ├── preprocessing.py
│       ├── questions_example.json
│       └── settings.py
├── tests/
│   ├── test_question.py
│   └── test_submit_evaluation.py
├── main.py
├── requirements.txt
├── Dockerfile
├── deploy.ps1
├── pytest.ini
├── .gitignore
```

## Como Rodar o Projeto

1. **Pré-requisitos**
   - Python 3.8+
   - Conta e projeto no Google Cloud com BigQuery habilitado
   - Credencial de serviço (`gcp_key.json`)

2. **Instale as dependências:**
   ```powershell
   pip install -r requirements.txt
   ```

3. **Configure a autenticação do Google Cloud:**
   - Coloque o arquivo `gcp_key.json` na raiz do backend.
   - Defina a variável de ambiente:
     ```powershell
     $env:GOOGLE_APPLICATION_CREDENTIALS="caminho\para\gcp_key.json"
     ```

4. **Execute o servidor Flask:**
   ```powershell
   python main.py
   ```
   O servidor estará disponível em `http://localhost:5000`.

## Rotas Disponíveis

### POST `/questions`
- **Descrição:** Recebe dados para geração de perguntas.
- **Payload esperado:**
  ```json
  {
    "candidate": {...},
    "job": {...}
  }
  ```
- **Resposta:**
  ```json
  {
    "questions": ["Pergunta 1", "Pergunta 2", ...]
  }
  ```

### POST `/submit_evaluation`
- **Descrição:** Registra uma avaliação no BigQuery.
- **Payload esperado:**
  ```json
  {
    "json_sent": {...},
    "json_received": {...},
    "rating": 1-5
  }
  ```
- **Resposta:**
  ```json
  {
    "message": "Avaliação registrada com sucesso!",
    "evaluation_id": "<uuid>"
  }
  ```

## Testes

Os testes unitários estão na pasta `tests/` e podem ser executados com:
```powershell
pytest
```

## Observações
- O projeto utiliza o Google BigQuery, portanto é necessário ter uma conta e projeto configurados.
- O arquivo `requirements.txt` lista todas as dependências necessárias.
- Para deploy, utilize o `Dockerfile` ou o script `deploy.ps1` conforme sua necessidade.

---

Para dúvidas ou sugestões, entre em contato com o mantenedor.


# Frontend

The **frontend** of the application was built with **React + Vite**.  
It allows the user to select a **JSON file** containing résumé and job description data, and send this file to the backend through the `/questions` endpoint.  
The API responds with a list of **customized questions** based on the provided résumé and job description.

---

## 🚀 Deployment
The frontend is hosted on a **Google Cloud Storage bucket** and can be accessed at:

👉 [https://storage.googleapis.com/datathon-fiap/index.html](https://storage.googleapis.com/datathon-fiap/index.html)

---


## ⚙️ Running Locally

### 1. Clone the repository

You will need to clone the repo: [Datathon-Fiap](https://github.com/NathanNNB/DataThon-Fiap)
```
cd frontend
```
### 2. Install dependencies
```bash
yarn install
# or
npm install
```

### 3. Start in development mode
```bash
yarn dev
# or
npm run dev
```

### 4. Configure the environment variables

Create a `.env` file in the root of the `frontend` folder (if it doesn't exist) and add the following variable:

```env
VITE_FLASK_API_URL=http://127.0.0.1:5000
```