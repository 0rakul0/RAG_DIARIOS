import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

def generate_embeddings(sentences, model):
    if not sentences:
        return np.zeros(model.get_sentence_embedding_dimension())
    embeddings = model.encode([sentences])[0]
    return embeddings

texto = """
eu e meu cachorro fomos ao parque, era um dia ensolarado e nos divertimos muito.
"""

texto_embeddings = generate_embeddings(texto, model)

print(texto_embeddings)
