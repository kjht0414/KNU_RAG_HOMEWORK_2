from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import CSVLoader
from langchain_core.documents import Document
from typing import List
from embeddings import get_embeddings
import os

def load_documents() -> List[Document]:
    loader = CSVLoader(
        file_path=r'./topic1/dataset.csv', 
        encoding='utf-8',
        content_columns=["title", "content"],
        metadata_columns=["type", "author", "created_at"]
        )

    loaded_docs = loader.load()

    return loaded_docs


def embedding(docs:List[Document]):
    embeddings = get_embeddings()
    vectorstore = FAISS.from_documents(
        documents=docs, 
        embedding=embeddings)
    return vectorstore

path_str = r'./exp-faiss'
def save_vector_to_local(vectorstore):
    vectorstore.save_local(path_str)

def load_vector_from_local():
    return FAISS.load_local(
        path_str, 
        embeddings=get_embeddings(), 
        allow_dangerous_deserialization=True)

def init_vectorstore():
    if os.path.exists(path_str):
        print('불러오는 중')    
        return load_vector_from_local()
    print('임베딩 중')
    docs = load_documents()
    vectorstore = embedding(docs)
    save_vector_to_local(vectorstore)
    return vectorstore