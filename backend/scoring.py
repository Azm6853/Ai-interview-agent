# backend/scoring.py

import openai
import os

# Load OpenAI API Key from environment
openai.api_key = os.getenv("OPENAI_API_KEY")


def load_rubric_prompt():
    """Load the evaluation rubric from a text file."""
    with open("prompts/rubric.txt", "r") as f:
        return f.read()


def score_answer(answer: str, question: str) -> dict:
    """
    Uses OpenAI to score a candidate's answer based on the rubric.

    Args:
        answer (str): The user's response to the interview question.
        question (str): The question that was asked.

    Returns:
        dict: A JSON-like dictionary of scores and feedback.
    """
    prompt = load_rubric_prompt()

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert interview evaluator."},
            {"role": "user", "content": f"{prompt}\n\nQuestion: {question}\n\nAnswer: {answer}"}
        ],
        temperature=0.3
    )

    try:
        # Attempt to parse GPT's JSON-like response
        return eval(response["choices"][0]["message"]["content"])
    except Exception:
        return {
            "clarity": 0,
            "depth": 0,
            "relevance": 0,
            "confidence": 0,
            "feedback": "Could not parse evaluation. Please try again."
        }


# Example usage
if __name__ == "__main__":
    question = "Explain how a hash table works."
    answer = "A hash table maps keys to values using a hash function. It allows average constant time lookups."
    result = score_answer(answer, question)
    print("Evaluation Result:", result)
