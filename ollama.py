import requests
from searching_example import searching
import json

# Modele do testu: 
# DeepSeek-R1 -> gubi się trochę, ale odpowiada
# deepseek-r1:14b - komputer mi umiera -> spoko odpowiedź 
# gemma3:12b - podobno mega boss :) - komputer mi umiera -> freeze kompa xD
# llama3:8b -> w sumie git
# gemma:7b


def ask_ollama(prompt, model="llama3:8b"):

    docs_scores = searching(prompt)

    context = "\n\n".join([doc.page_content for doc, _ in docs_scores])
    print("Content from Ollama: ", context)
    
    # #Reszta
    # chat_history = [
    #     {"role": "system", "content": "You are a helpful chatbot. Try to answer in few sentences using the following information to answer the user's questions excally like in documents. These documents contain the knowledge you need to assist the user:"},
    #     {"role": "system", "content": f"Contextual documents:\n{context}"},
    #     {"role": "user", "content": prompt}
    # ]
    # url = "http://localhost:11434/api/chat"
    # payload = {
    #     "model": model,
    #      "messages": chat_history,
    #      "stream": False
    #  }
    # try:
    #     response = requests.post(url, json=payload)
    #     response.raise_for_status()
    #     reply = response.json()["message"]["content"]
    #     return reply
    # except Exception as e:
    #     return f"Błąd podczas zapytania do Ollamy: {e}"
    
    
    # Llama3:8B
    final_prompt = (
        "You are a helpful assistant. Using the context below, answer the question in a few sentences.\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {prompt}\n"
        "Answer:"
    )
    url = "http://localhost:11434/api/generate" 

    payload = {
        "model": model,
        "prompt":final_prompt,
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        response_text = response.text
        json_lines = [json.loads(line) for line in response_text.strip().split("\n") if line.strip()]
        reply = "".join(chunk.get("response", "") for chunk in json_lines)

        return reply

    except Exception as e:
        return f"Błąd podczas zapytania do Ollamy: {e}\nRaw response:\n{response.text}"
