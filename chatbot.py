import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def is_vague_query(query):
    query = query.lower()

    vague_patterns = [
        "what's going on",
        "whats going on",
        "what is going on",
        "tell me about",
        "what happened with",
        "what's happening with",
        "whats happening with"
    ]

    return any(pattern in query for pattern in vague_patterns)


def get_clarification_response(query):
    return (
    "Your question is a little broad. Do you want:\n\n"
    "- recent news updates\n"
    "- background information\n"
    "- policy decisions\n"
    "- political analysis"
)


def get_general_response(query):
    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": query}
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Error: {str(e)}"