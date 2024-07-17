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
import os

# Aplicar nest_asyncio
nest_asyncio.apply()

# Função para embutir o texto
def embed_text(model, text: str) -> List[float]:
    embedding = model.encode([text], convert_to_tensor=True)
    return embedding.cpu().numpy()[0].tolist()

def main():
    # Inicializar modelos
    embed_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    llm = Ollama(model="llama3:latest", request_timeout=420)
    LlamaSettings.llm = llm

    # Inicializar cliente ChromaDB
    chrma_cliente = db.PersistentClient(path="D:\github\pySparkProject\ETL\db_banco_1")
    collection = chrma_cliente.get_or_create_collection(name="diario")

    # FERRAMENTA DO AGENTE
    def procura_bloco_similar(query: str, top_k: int = 3) -> List[str]:
        try:
            query_embedding = embed_text(embed_model, query)
            results_embedding = collection.query(query_embeddings=query_embedding, n_results=top_k)
            similar_cases = [doc for document in results_embedding['documents'] for doc in document]
            return similar_cases
        except Exception as e:
            st.error(f"Erro ao buscar casos similares: {e}")
            return []

    # TAREFA DO AGENTE
    def gerar_pesquisa(novo_caso: str, casos_similares: List[str]) -> str:
        input_text = f"Informações providas: {novo_caso}\n\nProcessos similares: {' '.join(casos_similares)}"
        messages = [
            ChatMessage(
                role="system", content="Você é um especialista em pesquisa no diario oficial e fornece dados processuais de acordo com as informações fornecidas."
            ),
            ChatMessage(role="user", content=input_text),
            ChatMessage(role="user", content="Você só deve fornecer dados do processo com extidão ao que está sendo solicitado, "
                                             "verifique se caso for um ADV (advogado) seu codigo do OAB é igual ao fornecido pelo usuario,"
                                             "um numero processal pode ser pesquisado por regex usando \d{7}\-\d{2}\.\d{4}.\d.\d{2}\.\d{4},"
                                             "caso for um numero processual só informe dados do processo solicitado,"
                                             "se não for um numero processual ou um advogado, traga todos os dados relacionados ao que está sendo pedido,"
                                             "não adicione nenhum texto adicional ao texto do dado."
                                             "Sua resposta deve conter somente a lista dos processo similares e informar do que se trata o processo.")
        ]
        try:
            resp = llm.chat(messages=messages)
            return resp
        except Exception as e:
            st.error(f"Erro ao gerar informações do processo: {e}")
            return ""


    # Criar ferramentas do agente
    procura_bloco_similar_tool = FunctionTool.from_defaults(fn=procura_bloco_similar)
    gerar_pesquisa_tool = FunctionTool.from_defaults(fn=gerar_pesquisa)
    agent = ReActAgent.from_tools(
        [procura_bloco_similar_tool, gerar_pesquisa_tool],
        llm=llm,
        verbose=True,
    )

    # Interface do Streamlit
    st.title("Assistente de Processos")

    novo_caso = st.text_area("Insira os dados ou outras informações do diário")
    if st.button("Buscar casos similares e gerar relatório"):
        if novo_caso:
            with st.spinner("Buscando blocos de processo..."):
                casos_similares = procura_bloco_similar(query=novo_caso)
                if casos_similares:
                    for i in casos_similares:
                        st.write(i)
                    st.subheader("Processos Similares Encontrados")
                    informacoes_do_processo = agent.chat(f"procure pelos processo mais similar a esse novo processo {novo_caso} visando usá-los para obter o processo mais semelhante")
                    st.subheader("Informações do Processo")
                    st.write(informacoes_do_processo)
                else:
                    st.error("Nenhum processo similar encontrado.")
        else:
            st.error("Por favor, informe o Processo e informações necessárias.")

if __name__ == "__main__":
    main()
    """
    para rodar o modelo
    streamlit run .\ETL\extrator_chroma_db_consulta_2.py
    """