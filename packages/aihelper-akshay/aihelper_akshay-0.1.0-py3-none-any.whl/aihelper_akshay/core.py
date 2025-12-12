import openai
from aihelper_akshay.utils import format_response

# Set API key from environment variable
# export OPENAI_API_KEY="your_key"
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_response(prompt: str) -> str:
    """Send a prompt to an AI model and return the result."""
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    text = response["choices"][0]["message"]["content"]
    return format_response(text)


def summarize_text(text: str) -> str:
    """Summarize input text using the AI API."""
    prompt = f"Summarize this text: {text}"
    return get_response(prompt)
