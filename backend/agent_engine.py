import os
from dotenv import load_dotenv
from openai import AzureOpenAI

# Load environment variables from .env file
load_dotenv()

# Initialize Azure OpenAI client
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_version=os.getenv("AZURE_OPENAI_VERSION")
)

def ask_openai(prompt: str) -> str:
    try:
        response = client.chat.completions.create(
            model=os.getenv("AZURE_OPENAI_ENGINE"),
            messages=[
                {"role": "system", "content": "You are a helpful, adaptive AI interview agent."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1024
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

def generate_question(role: str, stage: str) -> str:
    """
    Creates a prompt and queries the AI to generate a role-specific interview question.
    """
    prompt = f"Generate a {stage} interview question for a candidate applying for the role of {role}."
    return ask_openai(prompt)
