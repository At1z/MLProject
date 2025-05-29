import requests
import os
from dotenv import load_dotenv

load_dotenv()

def semantic_match_openai(context: str, answer: str, model="gpt-4o"):
    """
    Checks whether the given answer matches the meaning of the context using OpenAI.
    Returns an integer score from 1 to 5 based on the MOSE scale.
    """
    prompt = f"""
You are a semantic evaluator.
Your task is to compare a context and an answer.
Score how well the answer matches the meaning and intent of the context.
Use the MOSE scale from 1 to 5:
1 = completely irrelevant,
2 = mostly irrelevant,
3 = somewhat related but lacking detail,
4 = mostly relevant,
5 = perfect match.

Respond only with a number from 1 to 5.

Context:
\"\"\"{context}\"\"\"

Answer:
\"\"\"{answer}\"\"\"

Score:
"""

    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You evaluate the semantic similarity of answers."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0,
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        reply = response.json()["choices"][0]["message"]["content"].strip()
        return float(reply)
    except Exception as e:
        print("Failed to parse score:", e)
        return None
