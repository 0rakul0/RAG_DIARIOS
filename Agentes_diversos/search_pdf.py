from crewai import Agent, Task, Crew, Process
from crewai_tools import PDFSearchTool
from typing import List
from langchain_community.llms import Ollama
from dotenv import load_dotenv
import os

load_dotenv()
os.environ["OLLAMA_HOST"] = "http://localhost:11434"

# --- ferramenta para extrair e add no banco vetorial---
"""
se não tiver uma chave da OPENAI para usar a ferramenta usar uma alternativa
por exemplo um sistema proprio de pesquisa de banco e embbedings para pesquisar no arquivo.

para mais informações de customização e config:
- https://docs.embedchain.ai/components/llms
- https://docs.embedchain.ai/components/embedding-models
- https://docs.crewai.com/tools/PDFSearchTool/#custom-model-and-embeddings

"""

pdf_search_tool = PDFSearchTool(
    pdf=r"C:\Users\jeffe\OneDrive\Área de Trabalho\IPEA\Apostila Completa ELT 574.pdf",
    config=dict(
        llm=dict(provider="ollama", config=dict(model='llama3', base_url='http://localhost:11434')),
        embedder=dict(provider="ollama", config=dict(model="all-minilm", base_url='http://localhost:11434')),
    ),
)  # pdf com a apostila de ML com config para usar o llama

# --- agente que usa a ferramenta para extrair informações ---
re_searcher = Agent(
    role="Procura",
    goal="pesquisa e procura informações relevantes",
    backstory=(
        """
        A pesquisa é encontrar e extrair informações de várias fontes
        """
    ),
    allow_delegation=False,
    verbose=True,
    tools=[pdf_search_tool]  # pode por mais de uma ferramenta aqui
)

# --- agente que usa as informações extraídas para ter respostas ---
profissional_de_respostas = Agent(
    role="Responder perguntas do pdf",
    goal="Responde as perguntas baseadas no que foi extraído dos pdf",
    backstory=(
        """
        Você é um excelente cientista de dados que responde todas as perguntas com base no que foi extraído dos pdf
        """
    ),
    allow_delegation=False,
    verbose=True,
    tools=[]
)

# --- tarefas do agente de pesquisa do PDF ---
perguntas = Task(
    description="""
    Responda à pergunta do cliente com base no PDF da instalação inicial.
    O agente de pesquisa irá pesquisar através do PDF para encontrar o relevante do PDF de inspeção casa.

    Aqui está a pergunta do cliente
    {pergunta_do_user}
    """,
    expected_output="""
    Forneça respostas claras e precisas à pergunta do cliente com base no conteúdo do PDF de inspeção.
    Se não souber, responda que não sabe do assunto
    """,
    tools=[pdf_search_tool],
    agent=re_searcher
)

respostas = Task(
    description="""
    - Escreva um resumo das respostas para o usuário com base nas descobertas do agente de pesquisa.
    - O resumo deve indicar claramente como solucionar as questões encontradas na seção especificada
    """,
    expected_output="""
    Escreva um resumo claro e conciso que possa ser enviado ao usuário para resolver os problemas encontrados na pergunta
    """,
    tools=[],
    agent=profissional_de_respostas
)

# --- juntando os agentes ---
crew = Crew(
    agents=[re_searcher, profissional_de_respostas],
    tasks=[perguntas, respostas],
    process=Process.sequential,
)

# --- pergunta do usuário ---
user_question = input("Informe o que gostaria de resumir do PDF de instrução da pós?\n ")
result = crew.kickoff(inputs={"pergunta_do_user": user_question})
print(result)
