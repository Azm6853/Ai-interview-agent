# backend/scoring.py

import os
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()

# Init Azure client
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_version=os.getenv("AZURE_OPENAI_VERSION")
)

def load_rubric_prompt():
    with open("prompts/rubric.txt", "r") as f:
        return f.read()

def score_answer(answer: str, question: str) -> dict:
    prompt = load_rubric_prompt()
    try:
        response = client.chat.completions.create(
            model=os.getenv("AZURE_OPENAI_ENGINE"),
            messages=[
                {"role": "system", "content": "You are an expert interview evaluator."},
                {"role": "user", "content": f"{prompt}\n\nQuestion: {question}\n\nAnswer: {answer}"}
            ],
            temperature=0.3
        )
        return eval(response.choices[0].message.content)
    except Exception as e:
        return {
            "clarity": 0,
            "depth": 0,
            "relevance": 0,
            "confidence": 0,
            "feedback": f"Could not parse evaluation. Error: {e}"
        }
