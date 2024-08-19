import pandas as pd
import numpy as np
from langchain_community.embeddings import HuggingFaceEmbeddings
from llama_index.embeddings.langchain import LangchainEmbedding


lc_embed_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2"
)
embed_model = LangchainEmbedding(lc_embed_model)

df = pd.read_csv("../data_teste/words.csv")

df['embedding'] = df['text'].apply(lambda x: embed_model.get_text_embedding(x))

df.to_csv("../data_teste/word_embeddings.csv", index=False)

import ast

def list_of_float64(value):
    return np.array(ast.literal_eval(value), dtype=np.float64)

df = pd.read_csv("../data_teste/word_embeddings.csv", converters={"embedding": list_of_float64})
# print(df)

def cosine_similarity(vec1, vec2):
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    similarity = dot_product / (norm_vec1 * norm_vec2)
    return similarity

cappuccino = embed_model.get_text_embedding("cappuccino")

df["similaridade"] = df["embedding"].apply(lambda x: cosine_similarity(x, cappuccino))
res = df.sort_values("similaridade", ascending=False)
print(res)