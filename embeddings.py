from langchain_ollama import OllamaEmbeddings

MODEL_NAME = "nomic-embed-text-v2-moe"

_embeddings = OllamaEmbeddings(model=MODEL_NAME)

def get_embeddings():
    return _embeddings

