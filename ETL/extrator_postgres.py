import re
import time
from typing import List
from util.marcadores import marcador
from util.separador_blocos import cria_lista_de_linhas
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models_db.models import Processo

DATABASE_URL = "postgresql+psycopg2://postgres:postgrespw@localhost:15432/diarios_uf"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

class Extrator():
    def __init__(self):
        self.blocos_arquivo = []

    def run(self, arquivo: List[str], exibir: bool = False, salvar_db: bool = False, fonte: str = "") -> None:
        start_time = time.time()
        resumo = cria_lista_de_linhas(arquivo)
        self.procurar_itens(resumo)
        if exibir:
            self.exibe_blocos(self.blocos_arquivo)
        if salvar_db:
            self.salva_banco(self.blocos_arquivo, fonte)
        end_time = time.time()
        print(f"Tempo total de execução: {end_time - start_time:.2f} segundos")

    def procurar_itens(self, resumo: List[str]) -> None:
        for linha in resumo[1:]:
            for elemento in linha[:-1]:
                self.blocos_arquivo.append(elemento)
            for elemento in linha[-1:]:
                lista = elemento.split(')  NO ')
                for i in lista[:-1]:
                    self.blocos_arquivo.append(i)
                    nlista = i.split(')   - PARTE ')
                    for n in nlista[-1:]:
                        self.blocos_arquivo.append(n)

    def exibe_blocos(self, blocos: List[str]) -> None:
        for i, pedaco in enumerate(blocos):
            print(f'Pedaço {i + 1}')
            print(pedaco)
            print(len(pedaco))
            print()

    def matches_de_marcador(self, texto: str, lista_sentencas: List[tuple]) -> List[str]:
        marcadores = []
        if texto:
            for regex in lista_sentencas:
                if regex[1].search(texto):
                    marcadores.append(regex[0])
            marcadores = list(set(marcadores))
        if not marcadores:
            marcadores.append('NAO_CLASSIFICADO')
        return marcadores

    def salva_banco(self, blocos: List[str], fonte: str) -> None:
        lista_sentencas = marcador()
        for i, pedaco in enumerate(blocos):
            npus_bloco = re.findall(r'\d{7}\s*[\.\-]\s*?\d{2}\s*[\.\-]\s*\d{4}\s*[\.\-]\s*\d\s*[\.\-]\s*\d{2}\s*[\.\-]\s*\d{4}', pedaco)
            marcadores = self.matches_de_marcador(pedaco, lista_sentencas)
            try:
                novo_processo = Processo(
                    npu=', '.join(npus_bloco),
                    texto_pedaco=pedaco,
                    marcadores=','.join(marcadores),
                    fonte=fonte
                )
                session.add(novo_processo)
                session.commit()
            except Exception as e:
                print(f"Erro ao salvar no banco de dados: {e}")
                session.rollback()

if __name__ == '__main__':
    import glob

    ex = Extrator()
    caminhos = glob.glob(r"D:\diarios\SP\2021\01\*.txt")

    for caminho in caminhos:
        try:
            with open(caminho, 'r', encoding='utf-8') as f:
                arq = f.readlines()
            ex.run(arq, exibir=False, salvar_db=True, fonte=caminho)
        except Exception as e:
            print(f"Erro ao processar o arquivo {caminho}: {e}")