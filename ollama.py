import requests
from searching_example import searching

def ask_ollama(prompt, model="DeepSeek-R1"):
    docs_scores = searching(prompt)
    context = "\n\n".join([doc.page_content for doc, _ in docs_scores])
    chat_history = [
        {"role": "system", "content": f"Contextual documents:\n{context}"},
        {"role": "user", "content": prompt}
    ]

    url = "http://localhost:11434/api/chat"
    payload = {
        "model": model,
        "messages": chat_history,
        "stream": False
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        reply = response.json()["message"]["content"]
        return reply
    except Exception as e:
        return f"Błąd podczas zapytania do Ollamy: {e}"
