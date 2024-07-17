from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Processo(Base):
    __tablename__ = 'blocos_processos'
    __table_args__ = {'schema': 'diarios'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    npu = Column(String, nullable=False)
    texto_pedaco = Column(Text, nullable=False)
    marcadores = Column(Text, nullable=False)
    data_created = Column(DateTime, server_default=func.now(), nullable=False)
    fonte = Column(String, nullable=False)

    table_structure = """
        - id: INTERGER
        - npu: STRING
        - texto_pedaco: TEXT
        - marcadores: STRING
        - data_created: TIMESTAMP
        - fonte: STRING
        """