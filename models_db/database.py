from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from models_db.models import Processo

DATABASE_URL = "postgresql+psycopg://postgres:postgrespw@localhost:15432/diarios_uf"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

def executar_query_sql(sql_query: str):
    print(sql_query)
    try:
        result = session.execute(text(sql_query))
        rows = result.fetchall()
        return [row for row in rows]
    except Exception as e:
        return f"Erro ao executar a consulta: {e}"