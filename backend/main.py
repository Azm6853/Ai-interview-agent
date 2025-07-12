from fastapi import FastAPI, File, UploadFile, Body
from fastapi.middleware.cors import CORSMiddleware
import os
import uuid

from backend.resume_parser import parse_resume

from utils.role_matcher import match_role
from agent_engine import generate_question
from scoring import score_answer

app = FastAPI()

# Enable CORS for frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For dev only — restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# In-memory session state (will be replaced by DB or Redis later)
session_state = {
    "stage": "icebreaker",  # "icebreaker" → "technical" → "behavioral"
    "asked_questions": [],
    "role": "Software Engineer"
}


@app.get("/")
def read_root():
    return {"message": "AI Interview Agent API is running."}


@app.post("/upload_resume")
async def upload_resume(file: UploadFile = File(...)):
    # Save uploaded file
    file_ext = file.filename.split('.')[-1]
    file_id = f"{uuid.uuid4()}.{file_ext}"
    file_path = os.path.join(UPLOAD_FOLDER, file_id)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Parse resume
    parsed_resume = parse_resume(file_path)

    # Match role
    matched_role = match_role(parsed_resume.get("skills", []))

    # Save to session
    session_state["role"] = matched_role["matched_role"]

    return {
        "status": "success",
        "parsed_resume": parsed_resume,
        "matched_role": matched_role
    }


@app.post("/start_interview")
def start_interview(role: str = Body(..., embed=True)):
    """
    Starts the interview with an icebreaker question.
    """
    session_state["stage"] = "icebreaker"
    session_state["asked_questions"] = []
    session_state["role"] = role

    question = generate_question(role=role, stage="icebreaker")
    session_state["asked_questions"].append(question)

    return {
        "stage": session_state["stage"],
        "question": question
    }


@app.post("/ask_question")
def ask_question(answer: str = Body(..., embed=True)):
    """
    Accepts the user's answer, scores it, and returns the next question.
    """

    current_stage = session_state["stage"]
    current_role = session_state["role"]
    last_question = session_state["asked_questions"][-1] if session_state["asked_questions"] else ""

    # Evaluate user's answer using GPT rubric
    evaluation = score_answer(answer=answer, question=last_question)

    # Determine next stage
    if current_stage == "icebreaker":
        session_state["stage"] = "technical"
    elif current_stage == "technical":
        session_state["stage"] = "behavioral"
    elif current_stage == "behavioral":
        session_state["stage"] = "complete"
        return {
            "stage": "complete",
            "message": "Interview complete. Thank you!",
            "last_question_feedback": evaluation
        }

    next_stage = session_state["stage"]
    next_question = generate_question(role=current_role, stage=next_stage)
    session_state["asked_questions"].append(next_question)

    return {
        "stage": next_stage,
        "question": next_question,
        "last_question_feedback": evaluation
    }
