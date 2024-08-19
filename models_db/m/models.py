from sqlalchemy import Column, Integer, String, Text, MetaData
from sqlalchemy.ext.declarative import declarative_base

metadata = MetaData(schema="diarios")
Base = declarative_base(metadata=metadata)

class Processo(Base):
    __tablename__ = 'blocos_processos'

    id = Column(Integer, primary_key=True)
    texto_pedaco = Column(Text)
    marcadores = Column(String)
    fonte = Column(String)

    table_structure = """
            - nome_da_tabela: diarios.blocos_processos
            - id: INTERGER
            - texto_pedaco: TEXT
            - marcadores: STRING
            - fonte: STRING
            """