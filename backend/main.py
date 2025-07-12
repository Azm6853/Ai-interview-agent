# backend/main.py

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import os
import uuid

from resume_parser import parse_resume
from utils.role_matcher import match_role

app = FastAPI()

# Allow CORS (Cross-Origin Requests) for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Folder to store uploaded files
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.get("/")
def read_root():
    return {"message": "AI Interview Agent API is running."}

@app.post("/upload_resume")
async def upload_resume(file: UploadFile = File(...)):
    # Save uploaded resume with a unique name
    file_ext = file.filename.split('.')[-1]
    file_id = f"{uuid.uuid4()}.{file_ext}"
    file_path = os.path.join(UPLOAD_FOLDER, file_id)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Parse the resume
    parsed_resume = parse_resume(file_path)

    # Match the role using extracted skills
    matched_role = match_role(parsed_resume.get("skills", []))

    return {
        "status": "success",
        "parsed_resume": parsed_resume,
        "matched_role": matched_role
    }

from fastapi import Body
from agent_engine import generate_question

# In-memory mock state (replace with real session store later)
session_state = {
    "stage": "icebreaker",  # or "technical", "behavioral"
    "asked_questions": [],
    "role": "Software Engineer"  # default or from role matcher
}


@app.post("/start_interview")
def start_interview(role: str = Body(..., embed=True)):
    """
    Starts the interview with an icebreaker question for the given role.
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
    Accepts the user's answer and returns the next question.
    Rotates through stages: icebreaker → technical → behavioral → end
    """
    current_stage = session_state["stage"]

    # Progress logic: switch stage after first answer
    if current_stage == "icebreaker":
        session_state["stage"] = "technical"
    elif current_stage == "technical":
        session_state["stage"] = "behavioral"
    elif current_stage == "behavioral":
        return {
            "stage": "complete",
            "message": "Interview complete. Thank you for participating!"
        }

    next_stage = session_state["stage"]
    question = generate_question(role=session_state["role"], stage=next_stage)
    session_state["asked_questions"].append(question)

    return {
        "stage": next_stage,
        "question": question
    }

