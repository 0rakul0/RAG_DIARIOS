from crewai import Agent, Task, Crew
from langchain_community.llms import Ollama
from sentence_transformers import SentenceTransformer
from models_db.v.view import executar_query_sql
from models_db.m.models import Processo


llm = Ollama(
    model="llama3",
    base_url="http://localhost:11434"
)


class CustomAgent(Agent):

    def generate_sql_query(self, user_query: str):
        prompt = f"""
         use o pedido do usuário: '{user_query.upper()}' para gerar uma query de SQL.
         Use a seguinte estrutura da tabela {Processo.table_structure} para converter o pedido.
         exemplo de consulta: SELECT * FROM diarios.blocos_processos where <coluna_solicitada> LIKE '%<npu_solicitada>%';
         só responda com a query sugerida
         """
        response = self.llm(prompt)
        query = str(response).replace('\n', ' ')
        return query

    def handle_query(self, query: str):
        sql_query = self.generate_sql_query(query)
        resultado = executar_query_sql(sql_query)
        return resultado

agent = CustomAgent(
    role="Você é um especialista em consultas de banco de dados processuais.",
    goal="Responda com a query pedida e a quantidade de respostas achadas, caso o tipo da coluna seja STRING use LIKE",
    backstory="Você é um excelente pesquisador que traz informações dos processos.",
    allow_delegation=False,
    verbose=False,
    llm=llm,
)

def create_task(agent, query):
    description = (f"""Realizar consulta no banco de dados processuais com o termo: {query}. Caso seja um NPU, não altere a estrutura do NPU, pois no banco está salvo sem estar formatado.""")
    resposta = agent.handle_query(query)
    expected_output = f"Resultado da consulta: {resposta}"
    return Task(description=description, agent=agent, expected_output=expected_output)

if __name__ == '__main__':
    query_usuario = input("Digite a consulta: ")
    task = create_task(agent, query_usuario)
    crew = Crew(
        agents=[agent],
        tools=[],
        tasks=[task],
        verbose=2,
    )
    result = crew.kickoff()
    print(result)
