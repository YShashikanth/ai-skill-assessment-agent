# 🚀 AI-Powered Skill Assessment & Personalized Learning Agent

## 📌 Overview

Traditional resume screening only checks keywords — not actual skill depth.

This project builds an **AI-powered hiring assistant** that:

* Evaluates real skill proficiency
* Compares Resume vs Job Description
* Identifies skill gaps
* Generates interview questions
* Creates a personalized learning roadmap
* Provides hiring recommendation

---

## 🧠 Key Features

### 🎯 Skill Scoring

Evaluates proficiency (not just presence):

* Strong → 7–9/10
* Moderate → 5–6/10
* Basic → 3–4/10

---

### 📊 Match Score

Measures alignment between resume and job role.

---

### ⚠️ Skill Gap Analysis

Identifies missing skills with priority:

* High
* Medium
* Low

---

### 💬 Interview Questions

* Role-specific
* Skill-based
* Practical scenarios

---

### 📚 Learning Plan

For each gap:

* Reason
* Time estimate
* Resources

---

### 🧾 Hiring Decision

* Recommend / Reject
* With reasoning

---

## 🏗️ Architecture

```
Frontend (React + Vite)
        ↓
FastAPI Backend
        ↓
OpenRouter LLM API
        ↓
Structured JSON Output
        ↓
Frontend Visualization
```

---

## 🛠️ Tech Stack

### Frontend

* React (Vite)
* CSS

### Backend

* FastAPI
* Python

### AI

* OpenRouter API

### PDF Parsing

* PyMuPDF
* pdfplumber

---

## 📂 Project Structure

```
ai-skill-assessment-agent/
│
├── backend/
│   ├── main.py
│   ├── agent.py
│   ├── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │
│   ├── package.json
│
└── README.md
```

---

# ⚙️ Setup Instructions

---

## 🔹 1. Clone Repository

```
git clone https://github.com/YShashikanth/ai-skill-assessment-agent.git
cd ai-skill-assessment-agent
```

---

## 🔹 2. Backend Setup

```
cd backend
python -m venv venv
```

### Activate

**Windows**

```
venv\Scripts\activate
```

**Mac/Linux**

```
source venv/bin/activate
```

---

## 🔹 3. Install Dependencies

```
pip install -r requirements.txt
```

---

## 🔹 4. Add API Key

Create `.env` inside backend:

```
OPENROUTER_API_KEY=your_api_key_here
```

---

## 🔹 5. Run Backend

```
uvicorn main:app --reload
```

Backend runs at:

```
http://127.0.0.1:8000
```

---

## 🔹 6. Frontend Setup

```
cd ../frontend
npm install
npm run dev
```

Frontend runs at:

```
http://localhost:5173
```

---

# 🔄 How It Works

1. Upload Resume (PDF or text)
2. Upload Job Description
3. Backend:

   * Extracts text
   * Cleans data
   * Sends to AI
4. AI:

   * Scores skills
   * Finds gaps
   * Generates questions
   * Builds learning plan
5. Results displayed in UI

---

# 📊 Example Output

```
Match Score: 65%

Summary:
Strong technical candidate with backend skills.

Decision:
Recommend with learning plan.

Skill Gaps:
Agile (High)
Jira (Medium)

Learning Plan:
Agile → 2 weeks
Jira → 1 week
```

---

# ⚠️ Common Issues

### Backend not working

* Ensure server is running

### API errors

* Check API key

### PDF not extracting

* Use paste option

---

# 🔐 Security Note

* Do NOT commit `.env`
* Keep API key private

---

# 🚀 Future Improvements

* Conversational interview mode
* PDF report download
* Candidate comparison
* Dashboard analytics

---

# 👨‍💻 Author

**Y Shashikanth**

---

# 🏁 Final Note

This project demonstrates how AI can move beyond automation into
👉 intelligent hiring decision systems.
