import os
import docx
from langchain_community.embeddings import HuggingFaceEmbeddings
from llama_index.embeddings.langchain import LangchainEmbedding


lc_embed_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2"
)
embed_model = LangchainEmbedding(lc_embed_model)

###### dividindo em pedaços

doc_path = r"../data_teste/apostila-python-orientacao-a-objetos.docx"

text_chunks = []

doc = docx.Document(doc_path)
for p in doc.paragraphs:
    text_chunks.append(p.text)

# remove todos os chunks que tenham menos de 10 palavras
text_chunks = [string.strip().strip('\n') for string in text_chunks if len(string.split()) >= 10]

chunks_with_embeddings = []
for chunk in text_chunks:
    embedding = embed_model.get_text_embedding(chunk)
    chunks_with_embeddings.append({"text": chunk, "embedding": embedding})

print(chunks_with_embeddings)

import pinecone
#### gerando um index do documento

pinecone.init(
    api_key = 'a8f60821-b576-4ca6-9b83-c2c980d44658',
    environment="us-central1-gcp"
)

# create index
index_name = "livro-python"

if index_name not in pinecone.list_indexes():
    pinecone.create_index(index_name, dimension=1536)

# connect to index
index = pinecone.Index(index_name)

# process everything in batches of 64
batch_size = 64

for i in range(0, len(chunks_with_embeddings), batch_size):
    data_batch = chunks_with_embeddings[i: i + batch_size]
    # set end position of batch
    i_end = min(i + batch_size, len(chunks_with_embeddings))
    # get batch meta
    text_batch = [item["text"] for item in data_batch]
    # get ids
    ids_batch = [str(n) for n in range(i, i_end)]
    # get embeddings
    embeds = [item["embedding"] for item in data_batch]
    # prepare metadata and upsert batch
    meta = [{"text": text_batch} for text_batch in zip(text_batch)]
    to_upsert = zip(ids_batch, embeds, meta)
    # upsert to Pinecone
    index.upsert(vectors=list(to_upsert))
