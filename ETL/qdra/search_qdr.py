import warnings

from qdrant_client import models, QdrantClient
from sentence_transformers import SentenceTransformer

warnings.filterwarnings("ignore")

embedd = SentenceTransformer('all-MiniLM-L6-v2')
cliente = QdrantClient(url="http://localhost:6333")

def search_qdr(query):
    hits = cliente.search(
        collection_name="vinhos_for_rag",
        query_vector=embedd.encode(query).tolist(),
        limit=4
    )

    for h in hits:
        print(h.payload['metadata']['title'], "score:", h.score)

def search_qdr2(query,pais,valorMin,valorMax,pointMin,pointMax):
    hits = cliente.search(
        collection_name="vinhos_for_rag",
        query_vector=embedd.encode(query).tolist(),
        query_filter=models.Filter(
            must=[
                models.FieldCondition(key="metadata.country", match=models.MatchValue(value=pais)),
                models.FieldCondition(key="metadata.price", range=models.Range(gte=valorMin, lte=valorMax)),
                models.FieldCondition(key="metadata.points", range=models.Range(gte=pointMin, lte=pointMax)),
            ]
        ),
        limit=4
    )
    for h in hits:
        print(h.payload['metadata']['title'],
              "\nprice",h.payload['metadata']['price'],
              "\npoints",h.payload['metadata']['points'],
              "score:", h.score)

search_qdr("Quinta dos Avidagos 2011")
search_qdr2("Night Sky", "us", 15.0, 30.0, 90, 100)

