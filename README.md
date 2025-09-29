# DataThon-Fiap


Back
https://flask-service-1092765354740.us-central1.run.app/

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