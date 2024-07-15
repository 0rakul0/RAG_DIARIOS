from typing import List
import streamlit as st
from sentence_transformers import SentenceTransformer
from llama_index.llms.ollama import Ollama
from llama_index.core.llms import ChatMessage
from llama_index.core.tools import FunctionTool
from llama_index.core.agent import ReActAgent
from llama_index.core import Settings as LlamaSettings
import nest_asyncio
import chromadb as db
from chromadb.config import Settings as ChromaSettings
import os
# Aplicar nest_asyncio
nest_asyncio.apply()


# Função para embutir o texto
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

def embed_text(text: str) -> List[float]:
    embedding = model.encode([text], convert_to_tensor=True)
    return embedding.cpu().numpy()[0].tolist()

query = input("escreva o que está buscando: ")
q_embbeding = embed_text(query)

chrma_cliente = db.Client()
chrma_cliente = db.PersistentClient(path="db_banco_1")
collection = chrma_cliente.get_or_create_collection(name="diario")

llm = Ollama(model="llama3:latest", request_timeout=420)
LlamaSettings.llm = llm

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

results = collection.query(query_texts=query, n_results=5)
results_embedding = collection.query(query_embeddings=q_embbeding, n_results=5)

print(results_embedding)
print()

for i in results['documents']:
    for j in i:
        print(j)
        print()

for i in results_embedding['documents']:
    for j in i:
        print(j)
        print()