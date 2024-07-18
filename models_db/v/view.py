from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+psycopg://postgres:postgrespw@localhost:15432/diarios_uf"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

def executar_query_sql(sql_query: str):
    print(sql_query)
    session = Session()
    try:
        result = session.execute(text(sql_query))
        rows = result.fetchall()
        session.commit()
        return [row for row in rows]
    except Exception as e:
        session.rollback()
        return f"Erro ao executar a consulta: {e}"
    finally:
        session.close()

if __name__ =="__main__":
    # Exemplo de uso:
    nome_tabela = 'diarios.blocos_processos'
    sql_query =f"SELECT * FROM {nome_tabela} WHERE marcadores = 'NAO_CLASSIFICADO' LIMIT 10;"
    result = executar_query_sql(sql_query)
    print(result)