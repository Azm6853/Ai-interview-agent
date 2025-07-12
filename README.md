# 🧠 AI Interview Agent

A personalized, intelligent interview agent that simulates dynamic job interviews tailored to the candidate’s resume, job role, and real-time responses.

Built using LangChain, OpenAI, FastAPI, and React — this system adapts to the user's background and evaluates their responses using a scoring rubric, making it a next-gen solution for mock interviews, hiring tests, or talent assessments.

---

## 🚀 Features

- 📄 **Resume Parsing**: Extracts skills, education, and experience from uploaded resumes
- 🧩 **Role Matching**: Determines the candidate’s likely job role and selects appropriate question sets
- 💬 **Adaptive Interviewing**: Generates icebreakers, technical, and behavioral questions based on real-time conversation
- 🧠 **LLM-Powered Scoring**: Uses GPT to evaluate candidate responses and generate structured feedback
- 📊 **Feedback Report**: Provides scores for communication, depth, clarity, and confidence
- 🧵 **Memory**: Remembers past answers to ask better follow-ups
- 🎤 (Optional) Voice support using Whisper & ElevenLabs (planned)

---

## 🛠️ Tech Stack

| Area       | Tech |
|------------|------|
| Backend    | FastAPI, Python, LangChain, OpenAI API |
| Frontend   | React, Tailwind CSS |
| Parsing    | PyMuPDF, spaCy |
| Scoring    | OpenAI GPT-4 (LLM) |
| Optional   | Whisper (STT), ElevenLabs (TTS), Pinecone (vector memory) |

---

## 📂 Project Structure

```
ai-interview-agent/
│
├── backend/
│   ├── main.py                # FastAPI API routes
│   ├── resume_parser.py       # Resume extraction logic
│   ├── agent_engine.py        # LangChain agent for generating questions
│   ├── question_templates.py  # Stores prompt templates
│   ├── scoring.py             # Evaluates answers using GPT
│   ├── models/
│   │   └── user_session.py    # Data structures
│   └── utils/
│       └── role_matcher.py    # Matches candidate to job type
│
├── prompts/                   # Text prompt files for LLM use
│   ├── icebreaker.txt
│   ├── technical.txt
│   ├── behavioral.txt
│   └── rubric.txt
│
├── data/sample_resumes/       # Example resumes for testing
├── frontend/                  # (In Progress) React UI
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md
```

---

## ⚙️ Getting Started

### 🔧 Backend (FastAPI)

```bash
# Install dependencies
pip install -r requirements.txt

# Run the API
uvicorn backend.main:app --reload
```

### 📦 Requirements

```bash
python -m spacy download en_core_web_sm
```

---

### 🧪 Test Resume Parser

```bash
python backend/resume_parser.py
```

---

## 🧪 Example API Routes

| Route | Description |
|-------|-------------|
| `POST /upload_resume` | Upload resume and extract structured info |
| `POST /start_interview` | Start personalized interview session |
| `POST /ask_question` | Send response, receive next question and feedback |

---

## 💡 Future Improvements

- 🎤 Voice support (Whisper + ElevenLabs)
- 🧠 Long-term memory for multi-session interviews (Pinecone)
- 📅 Calendar and scheduling integration
- 🧑‍💼 Recruiter dashboard for multi-candidate review

---

## 📜 License

This project is licensed under the **MIT License** — free to use and modify.

---

## 👤 Author

**Anirban Maity**  
[LinkedIn](https://www.linkedin.com/in/ani-psu) | Penn State University | Class of 2025
