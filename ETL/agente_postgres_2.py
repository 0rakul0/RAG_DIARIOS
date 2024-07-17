from typing import List
from llama_index.llms.ollama import Ollama
from llama_index.core.llms import ChatMessage
from llama_index.core.tools import FunctionTool
from llama_index.core.agent import ReActAgent
from llama_index.core import Settings as LlamaSettings
from models_db.database import executar_query_sql
from models_db.models import Processo
from util.utilString import remove_acentos
import streamlit as st

llm = Ollama(model="llama3:latest", request_timeout=420)
LlamaSettings.llm = llm

def consultor_banco(query: str) -> List[str]:
    query = remove_acentos(query)
    df = executar_query_sql(query)
    return df

def gerador_de_query(pedido: str) -> List[str]:
    input_text = f"transforme a solicitação do {pedido} em uma query de SQL para o postgres"
    messages = [
        ChatMessage(
            role="system",
            content="Você é um especialista em consulta de SQL ao banco de dados do postgres"
        ),
        ChatMessage(role="user", content=input_text),
        ChatMessage(role="user",
                    content="Você só deve fornecer uma query de SQL que seja utilizavel no banco de dados postgres\n"
                            f"use a estrutura {Processo.table_structure} para realizar consulta ao banco de diarios na tabela blocos_processos\n"
                            "caso o pedido seja em uma coluna tipo string, não esqueça de por ''."
                            "Não adicione nenhum texto a mais na consulta"
                            "Na sua resposta deve somente constar a lista da consulta realizada.")
    ]
    try:
        resp = llm.chat(messages=messages)
        return resp
    except Exception as e:
        st.error(f"Erro ao gerar a query: {e}")
        return ""

def validar_resposta(resposta: str) -> str:
    input_text = f"verifique se {resposta} em uma query de SQL para o postgres"
    messages = [
        ChatMessage(
            role="system",
            content="Você é um especialista em consulta de SQL ao banco de dados do postgres"
        ),
        ChatMessage(role="user", content=input_text),
        ChatMessage(role="user",
                    content="Você só deve fornecer uma query de SQL que seja utilizavel no banco de dados postgres\n"
                            f"use a estrutura {Processo.table_structure} para realizar a validação da query ao banco de diarios na tabela blocos_processos\n"
                            "caso o pedido seja em uma coluna tipo string, não esqueça de por ''."
                            "Não adicione nenhum texto a mais na consulta"
                            "Na sua resposta deve somente constar a lista da consulta realizada.")
    ]
    try:
        resp = llm.chat(messages=messages)
        return resp
    except Exception as e:
        st.error(f"Erro ao gerar a query: {e}")
        return ""

consulta_query = FunctionTool.from_defaults(fn=consultor_banco)
validar_resposta = FunctionTool.from_defaults(fn=validar_resposta)
gerar_query = FunctionTool.from_defaults(fn=gerador_de_query)

agent_consulta = ReActAgent.from_tools([consulta_query,validar_resposta], llm=llm, verbose=True)
agent_gerador = ReActAgent.from_tools([validar_resposta,gerar_query], llm=llm, verbose=True)

if __name__ == "__main__":
    tabela = 'blocos_processos'
    descricao = Processo.table_structure
    cons = input("digite sua solicitação: ")

    # Primeiro agente para gerar a resposta
    resposta = agent_consulta.chat(remove_acentos(cons))
    consulta = agent_gerador.chat(resposta.response)

    # Exibir resultados
    print(f"Resposta gerada e validada: {resposta.response}")
    print(f"Resultado da consulta ao banco de dados: {consulta.response}")