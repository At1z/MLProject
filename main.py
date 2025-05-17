from ollama import ask_ollama
from OpenAiApi import ask_openai


def main():
    prompt = "How can my code discover the name of an object?"
    
    print("Question: ", prompt)
    [answer, vector_similarity, semantic_similarity] = ask_openai(prompt)
    print("OpenAI answer:", answer)
    print(f"Cosine similarity: {vector_similarity:.4f}")
    print(f"Semantic similarity: {semantic_similarity}")    

    print("Question: ", prompt)
    [answer, vector_similarity, semantic_similarity] = ask_ollama(prompt)
    print("Ollama answer:", answer)
    print(f"Cosine similarity: {vector_similarity:.4f}")
    print(f"Semantic similarity: {semantic_similarity}")
    

if __name__ == "__main__":
    main()


# How to run
# ollama run DeepSeek-R1
# python main.py