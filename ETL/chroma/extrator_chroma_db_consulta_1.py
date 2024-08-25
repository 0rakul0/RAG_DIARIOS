from typing import List
from sentence_transformers import SentenceTransformer
import nest_asyncio
import chromadb as db

# Aplicar nest_asyncio
nest_asyncio.apply()

# Função para embutir o texto
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

def embed_text(text: str) -> List[float]:
    embedding = model.encode([text], convert_to_tensor=True)
    return embedding.cpu().numpy()[0].tolist()

query = input("escreva o que está buscando: ").upper()
query_embedding = embed_text(query)

chrma_cliente = db.Client()
chrma_cliente = db.PersistentClient(path="../db_banco_1")
collection = chrma_cliente.get_or_create_collection(name="diario")

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

results_embedding = collection.query(query_embeddings=query_embedding, n_results=20)

for i in results_embedding['documents']:
    for j in i:
        print(j)
        print()

