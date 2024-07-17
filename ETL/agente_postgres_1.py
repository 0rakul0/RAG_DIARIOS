from crewai import Agent, Task, Crew
from langchain_community.llms import Ollama
from models_db.database import executar_query_sql
from util.utilString import remove_acentos

llm = Ollama(
    model="llama3",
    base_url="http://localhost:11434"
)

table_structure = """
Estrutura da tabela blocos_processos:
- npu: STRING
- texto_pedaco: TEXT
- marcadores: STRING
- data_created: TIMESTAMP
- fonte: STRING
"""

class CustomAgent(Agent):

    def generate_sql_query(self, user_query: str):
        prompt = f"""
        Use a seguinte estrutura da tabela {table_structure} para converter o pedido do usuário em uma consulta SQL:       
        Pedido do usuário: '{remove_acentos(user_query)}'
        """
        response = self.llm(prompt)
        return response.strip()

    def handle_query(self, query: str):
        sql_query = self.generate_sql_query(query)
        print(sql_query)
        return executar_query_sql(sql_query)

agent = CustomAgent(
    role="Você é um especialista em consultas de banco de dados processuais.",
    goal="Forneça dados processuais de acordo com a consulta fornecida.",
    backstory="Você é um excelente pesquisador que traz informações dos processos.",
    allow_delegation=False,
    verbose=True,
    llm=llm,
)

def create_task(agent, query):
    description = f"Realizar consulta no banco de dados processuais com o termo: {query}"
    expected_output = agent.handle_query(query)
    return Task(description=description, agent=agent, expected_output=expected_output)

if __name__ == '__main__':
    query_usuario = input("Digite a consulta: ")
    task = create_task(agent, query_usuario)
    crew = Crew(
        agents=[agent],
        tasks=[task],
        verbose=2,
    )
    result = crew.kickoff()
    print(result)
