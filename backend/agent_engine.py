# backend/agent_engine.py

import openai
import os

# Set your OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# Map prompt stage to file
PROMPT_PATHS = {
    "icebreaker": "prompts/icebreaker.txt",
    "technical": "prompts/technical.txt",
    "behavioral": "prompts/behavioral.txt"
}

def load_prompt(file_path):
    """Loads the prompt template from a file."""
    with open(file_path, "r") as f:
        return f.read()

def generate_question(role="Software Engineer", stage="technical"):
    """
    Generate an interview question using GPT-4.

    Args:
        role (str): The matched job role (e.g. "Software Engineer")
        stage (str): Type of question - "icebreaker", "technical", "behavioral"

    Returns:
        str: The AI-generated question
    """
    # Pick correct prompt file or fallback to technical
    prompt_file = PROMPT_PATHS.get(stage, PROMPT_PATHS["technical"])
    prompt = load_prompt(prompt_file)

    # GPT call
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": f"You are an AI interviewer for a {role} role."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    return response["choices"][0]["message"]["content"]


# Test run from terminal
if __name__ == "__main__":
    q1 = generate_question(role="Software Engineer", stage="icebreaker")
    print("Icebreaker Question:\n", q1)

    q2 = generate_question(role="Software Engineer", stage="technical")
    print("\nTechnical Question:\n", q2)

    q3 = generate_question(role="Software Engineer", stage="behavioral")
    print("\nBehavioral Question:\n", q3)
