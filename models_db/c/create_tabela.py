from sqlalchemy import create_engine
from models_db.m.models import Base

DATABASE_URL = "postgresql+psycopg2://postgres:postgrespw@localhost:15432/diarios_uf"
engine = create_engine(DATABASE_URL)

# Cria todas as tabelas definidas nos modelos
Base.metadata.create_all(engine)

print("Tabelas criadas com sucesso.")
