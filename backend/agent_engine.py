from openai import OpenAI
import os

# Load prompt from file
def load_prompt(file_path):
    with open(file_path, "r") as f:
        return f.read()

# Get next question using GPT
def generate_question(role="Software Engineer", stage="technical"):
    if stage == "icebreaker":
        prompt = load_prompt("prompts/icebreaker.txt")
    elif stage == "technical":
        prompt = load_prompt("prompts/technical.txt")
    elif stage == "behavioral":
        prompt = load_prompt("prompts/behavioral.txt")
    else:
        prompt = "Ask a follow-up question related to the previous answer."

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": f"You are an AI interviewer for a {role} role."},
            {"role": "user", "content": prompt}
        ]
    )
    return response["choices"][0]["message"]["content"]
