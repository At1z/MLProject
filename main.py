from ollama import ask_ollama
from OpenAiApi import ask_openai


def main():
    prompt = "How can my code discover the name of an object?"
    
    # print("Question: ", prompt)
    # [answer, vector_similarity, semantic_similarity, scoreBleu, scoreRouge] = ask_openai(prompt)
    # print("OpenAI answer:", answer)
    # print(f"Cosine similarity: {vector_similarity:.4f}")
    # print(f"Semantic similarity: {semantic_similarity}") 
    # print(f"Bleu similarity: {scoreBleu}")
    # print(f"Rouge similarity: {scoreRouge}")   

    print("Question: ", prompt)
    [answer, vector_similarity, semantic_similarity, scoreBleu, scoreRouge] = ask_ollama(prompt)
    print("Ollama answer:", answer)
    print(f"Cosine similarity: {vector_similarity:.4f}")
    print(f"Semantic similarity: {semantic_similarity}")
    print(f"Bleu similarity: {scoreBleu}")
    print(f"Rouge similarity: {scoreRouge}")

if __name__ == "__main__":
    main()


# How to run
# ollama run DeepSeek-R1
# python main.py