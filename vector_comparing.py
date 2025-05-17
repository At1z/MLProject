from langchain_huggingface import HuggingFaceEmbeddings
from sklearn.metrics.pairwise import cosine_similarity


embedding_model = HuggingFaceEmbeddings(model_name="thenlper/gte-large")

def vector_compare(content, answer):
    contentVector = embedding_model.embed_query(content)
    answerVector = embedding_model.embed_query(answer)
    similarity = cosine_similarity([contentVector], [answerVector])[0][0]
    return similarity
