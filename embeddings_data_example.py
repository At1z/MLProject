from transformers import AutoTokenizer
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings


EMBEDDING_MODEL = "all-MiniLM-L6-v2"

def get_embeddings(data):
    tokenizer = AutoTokenizer.from_pretrained(EMBEDDING_MODEL)
    text_splitter = RecursiveCharacterTextSplitter.from_huggingface_tokenizer(
        tokenizer,
        separators=["\n \n", "\n\n", "\n", " ", ""],
        chunk_size=512,
        chunk_overlap=0,
    )

    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

    all_docs = []
    for item in data:
        text = f"Q: {item['question']} A: {item['answer']}"
        docs = text_splitter.split_text(text)
        all_docs.extend(docs)

    return all_docs, embeddings
