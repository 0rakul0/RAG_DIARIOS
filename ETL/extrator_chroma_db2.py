import re
import time
from typing import List
from util.marcadores import marcador
from util.separador_blocos import cria_lista_de_linhas
import chromadb as db
from sentence_transformers import SentenceTransformer


chrma_cliente = db.Client()
chrma_cliente = db.PersistentClient(path="db_banco_2")
collection = chrma_cliente.get_or_create_collection(name="diario")

class Extrator():
    def __init__(self):
        self.blocos_arquivo = []
        # self.model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

    def run(self, arquivo: List[str], exibir: bool = False, salvar_db: bool = False) -> None:
        start_time = time.time()  # Início da medição de tempo
        resumo = cria_lista_de_linhas(arquivo)

        procurar_itens_start_time = time.time()
        self.procurar_itens(resumo)
        procurar_itens_end_time = time.time()

        if exibir:
            self.exibe_blocos(self.blocos_arquivo)
        if salvar_db:
            salvar_db_start_time = time.time()
            self.salva_banco(self.blocos_arquivo)
            salvar_db_end_time = time.time()

        end_time = time.time()  # Fim da medição de tempo

        print(f"Tempo total de execução: {end_time - start_time:.2f} segundos")
        print(f"Tempo para procurar itens: {procurar_itens_end_time - procurar_itens_start_time:.2f} segundos")
        if salvar_db:
            print(f"Tempo para salvar no banco de dados: {salvar_db_end_time - salvar_db_start_time:.2f} segundos")


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
            if 'RECONVENCAO_PROCEDENTE' in marcadores:
                if 'PROCEDENTE' in marcadores:
                    marcadores.remove('PROCEDENTE')
            if 'RECONVENCAO_IMPROCEDENTE' in marcadores:
                if 'IMPROCEDENTE' in marcadores:
                    marcadores.remove('IMPROCEDENTE')
            if 'RECONVENCAO_PROCEDENTE_PARCIAL' in marcadores:
                if 'PROCEDENTE_EM_PARTE' in marcadores:
                    marcadores.remove('PROCEDENTE_EM_PARTE')
        if not marcadores:
            marcadores.append('NAO_CLASSIFICADO')
        return marcadores
    def salva_banco(self, blocos: List[str]) -> None:
        for i, pedaco in enumerate(blocos):
            try:
                collection.add(documents=pedaco, ids=[str(i)])
            except Exception as e:
                print(f"Erro ao salvar no banco de dados: {e}")

if __name__ == '__main__':
    ex = Extrator()
    caminho = r"D:\diarios\SP\2021\01\DJSP_Caderno15_2021_01_21.txt"
    try:
        with open(caminho, 'r', encoding='utf-8') as f:
            arq = f.readlines()
        ex.run(arq, exibir=False, salvar_db=True)
    except Exception as e:
        print(f"Erro ao processar o arquivo: {e}")

        """
        Tempo total de execução: 1687.68 segundos
        Tempo para procurar itens: 0.00 segundos
        Tempo para salvar no banco de dados: 1623.57 segundos
        """