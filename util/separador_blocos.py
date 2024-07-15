
import re
from util.utilString import remove_acentos, remove_varios_espacos
from functools import reduce,partial

def cria_lista_de_linhas_mantendo_separador(arquivo, lista_expressoes_ignoradas, separador):
    # lista_expressoes_ignoradas = []
    linhas = arquivo[1:]
    nome_arquivo = arquivo[0]
    if linhas != []:

        linhas = ''.join(linhas).split('\n')
        linhas = list(map(lambda linha: remove_acentos(linha).upper(), linhas))
        linhas = list(filter(lambda linha: linha != '',
                             list(map(lambda linha: remove_varios_espacos(re.sub('\s*\n|\t', '', linha)), linhas))))
        linhas = list(map(lambda linha: linha + ' SEPARADOR ', linhas))

        linhas_concatenadas = ''
        fatia = 10000
        for i in range(0, int(len(linhas) / fatia) + 1):
            if i * fatia < len(linhas):
                linhas_concatenadas += (remove_acentos(
                    reduce(lambda x, y: x + ' ' + y if not x.endswith('-') else x[:-1] + y,
                           linhas[i * fatia:i * fatia + fatia]))).upper()

        for expressao_ignorada in lista_expressoes_ignoradas:
            linhas_concatenadas = expressao_ignorada.sub('', linhas_concatenadas)

        lista_de_linhas = re.split(separador, linhas_concatenadas)
        lista_de_linhas = list(map(lambda linha: re.sub('\sSEPARADOR\s', ' ', linha),
                                   list(filter(lambda linha: linha is not None, lista_de_linhas))))[1:]
        lista_de_linhas = list(filter(lambda linha: linha != ' ', lista_de_linhas))
        lista_de_linhas = list(filter(lambda linha: linha != ' (', lista_de_linhas))
        lista_de_linhas = list(filter(
            lambda linha: linha != re.search('\A\/\d{2}\s*\(\s*$', linha).group(0) if re.search('\A\/\d{2}\s*\(\s*$',
                                                                                                linha) else ' ',
            lista_de_linhas))
        lista_de_linhas = list(filter(lambda linha: len(linha) > 3, lista_de_linhas))

        regex_npu = re.compile(
            '^(\\b\d{7}\s*[\.\-]\s*?\d{2}\s*[\.\-]\s*\d{4}\s*[\.\-]\s*\d\s*[\.\-]\s*\d{2}\s*[\.\-]\s*\d{4}|\\b\d{7}\s*[\.\-]\s*?\d{2}\s*[\.\-]\s*\d{4}\s*[\.\-]\s*\d{3}\s*[\.\-]\s*\d{4}|\\b\d{3}\s*[\.\-]\s*\d{2}\s*[\.\-]\s*\d{6}\s*[\.\-]\s*\d|\\b\d{4}\s*[\.\-]\s*\d{2}\s*[\.\-]\s*\d{4}\s*[\.\-]\s*\d\s*[\.\-]\s*\d{2}\s*[\.\-]\s*\d{4}|\\b\d{4}\s*[\.\-]\s*\d{2}\s*[\.\-]\s*\d{2}\s*[\.\-]\s*\d{6}\s*[\.\-]\s*\d|\\b\d{3}\s*[\.\-]\s*\d{2}\s*[\.\-]\s*\d{4}\s*[\.\-]\s*\d\s*[\.\-]\s*\d{2}\s*[\.\-]\s*\d{4}|\\b\d{5}\s*[\.\-]\s*\d{2}\s*[\.\-]\s*\d{4}\s*[\.\-]\s*\d\s*[\.\-]\s*\d{2}\s*[\.\-]\s*\d{4}|\\b\d{7}\s*[\.\-]\s*\d\/\d|\\b\d{3}\s*[\.\-]\s*\d{2}\s*[\.\-]\s*\d{4}\s*[\.\-]\s*\d{6}\s*[\.\-]\s*\d|\\b\d{3}\s*[\.\-]\s*\d{3}\s*[\.\-]\s*\d\/\d|\\b\d{6,7}\s*[\.\-]\s*\d{2}\s*[\.\-]\s*\d{4}\s*[\.\-]\s*\d\s*[\.\-]\s*\d{2}\s*[\.\-]\s*\d{4}|\\b\d{3}\s*[\.\-]\s*\d{2}\s*[\.\-]\s*\d{4}\s*[\.\-]\s*\d{6}(\s*[\.\-]\s*\d\/\d{6}\s*[\.\-]\s*\d{3})?|\\b\d{3}\.\d{2,4}\.\d{6}\-?\d?)$')

        for pos, linha in enumerate(lista_de_linhas):
            npu = True
            while npu:
                if re.search(regex_npu, lista_de_linhas[pos]) and re.search(regex_npu, lista_de_linhas[pos + 1]):
                    lista_de_linhas.pop(pos + 1)
                else:
                    npu = False

        novas_linhas = []
        for pos, linha in enumerate(lista_de_linhas):
            if pos % 2 == 0:
                try:
                    novas_linhas.append(f'{linha} {lista_de_linhas[pos + 1]}')
                except:
                    continue

        return (nome_arquivo, novas_linhas)

    return ('', '')


def cria_lista_de_linhas(arquivo):
    lista_expressoes_ignoradas = []

    expressao_cabecalho = re.compile(
        '(DISPONIBILIZACAO\s*:?\s*.{0,9}?-?FEIRA\s*,?\s*)(\d{1,2}\s*DE\s*.{4,9}\s*DE\s*\d{4})', re.IGNORECASE)
    lista_expressoes_ignoradas.append(expressao_cabecalho)

    expressao_diario = re.compile(r'DIARIO.{0,100}\s*-?\s*CADERNO\s*JUDICIAL\s*-?\s*2.\s*', re.IGNORECASE)
    lista_expressoes_ignoradas.append(expressao_diario)

    expressao_caderno = re.compile(r'CADERNO\s*\d{1,2}\n?', re.IGNORECASE)
    lista_expressoes_ignoradas.append(expressao_caderno)

    expressao_site = re.compile(r'WWW.DJE.TJSP.JUS.BR', re.IGNORECASE)
    lista_expressoes_ignoradas.append(expressao_site)

    expressao_edicao = re.compile(r'SAO\s*PAULO\s*,?\s*ANO\s*\w*\s*-?\s*EDICAO\s*(\d+\s)*', re.IGNORECASE)
    lista_expressoes_ignoradas.append(expressao_edicao)

    expressao_rodape = re.compile(
        r'F\s*E\s*D\s*E\s*R\s*A\s*L.{0,100}?1\s*1\s*\.\s*4\s*1\s*9\s*\/0\s*6\s*,?\s*A\s*R\s*T\s*\.\s*4', re.IGNORECASE)
    lista_expressoes_ignoradas.append(expressao_rodape)

    expressao_rodape2 = re.compile(
        r'((?:PUBLICACAO\s*O\s*F\s*I\s*C\s*I\s*A\s*L\s*)?DO\s*TRIBUNAL\s*DE\s*JUSTICA\s*DO\s*ESTADO\s*DE\s*SAO\s*PAULO\s*-?\s*LEI\s*O\s*(?:DISPONIBILIZACAO\s*:?\s*.{0,9}?\s*-?FEIRA\s*,?\s*\d+\s*DE\s*.{1,10}\s*DE\s*\d{4})?\s*DIARIO\s*.*?CADERNO.*?(?:SAO\s*PAULO\s*,?\s*ANO\s*.*?EDICAO\s*(?:\d+\s*)*|PARTE\s*\w+\s*(?:\d+)?\s*))',
        re.IGNORECASE)
    lista_expressoes_ignoradas.append(expressao_rodape2)

    expressao_cabecalho2 = re.compile(
        r'(PUBLICACAO\s*O\s*F\s*I\s*C\s*I\s*A\s*L\s*DO\s*TRIBUNAL\s*DE\s*JUSTICA\s*DO\s*ESTADO\s*DE\s*SAO\s*PAULO.{0,40}LEI FEDERAL\s*N.?\s*\d*\.?\d*\/\d*.?\s*ART.?\s*\d*.?\s*DISPONIBILIZACAO\s*:\s*.{0,9}?\-?FEIRA\s*\,?\s*\d+\s*DE\s*.{0,50}\s*DIARIO\s*DA\s*JUSTICA\s*.{0,100}\s*PARTE\s*\w+\s*.{0,60}\s*EDICAO(?:\s*\d+)+)',
        re.IGNORECASE)
    lista_expressoes_ignoradas.append(expressao_cabecalho2)

    expressao_cabecalho3 = re.compile(
        r'PUBLICACAO\s*.{1,30}?\s*DO\s*TRIBUNAL\s*.{1,150}?\s*CADERNO\s*JUD\s*.{1,50}?\s*(?:CAPITAL|INTERIOR)',
        re.IGNORECASE)
    lista_expressoes_ignoradas.append(expressao_cabecalho3)

    expressao_cabecalho4 = re.compile(r'PUBLICACAO\s*.{1,20}?\s*DO\s*TRIBUNAL\s*.{1,150}?\s*LEI\s*O', re.IGNORECASE)
    lista_expressoes_ignoradas.append(expressao_cabecalho4)

    expressao_cabecalho5 = re.compile(r'DIARIO\s*.{1,50}?\s*CADERNO\s*JUD\s*.{1,100}?\s*CAPITAL\s*', re.IGNORECASE)
    lista_expressoes_ignoradas.append(expressao_cabecalho5)

    expressao_cabecalho6 = re.compile(
        r'(?:(?:\s*\d+\s*))?\s*D.?O.?E.?\s*\;?\s*PODER\s*.{1,50}?\s*SAO\s*PAULO\s*.{1,50}?\s*DE\s*.{1,15}?\s*DE\s*\d{4}\s*.{0,50}\s*\—?\s*.{0,20}?\s*(?:(?:\s*\d+\s*))?',
        re.IGNORECASE)
    lista_expressoes_ignoradas.append(expressao_cabecalho6)

    expressao_cabecalho7 = re.compile(
        r'DIARIO\W*OFI\W*CIAL\W*PODER\W*JUD\w*\W*CAD\w*\W*JUD\w*.{1,80}?\W*(?:CAPITAL|INTERIOR)\W*(?:\d+|\W*(?:PARTE|P\w*)\W*\w*)',
        re.IGNORECASE)
    lista_expressoes_ignoradas.append(expressao_cabecalho7)

    # cadernos antigos
    expressao_cabecalho8 = re.compile(
        r'\w*\-?FEIRA\W*\d+.{0,50}?\W*S.O\W*PAULO\W*.{0,50}?\W*(?:\d+)?\W*DI.RIO\W*OFI\w*.{0,50}?(?:PARTE|PRT)\W*I+\W*(?:\d+\/?\d+)?',
        re.IGNORECASE)
    lista_expressoes_ignoradas.append(expressao_cabecalho8)

    expressao_cabecalho9 = re.compile(
        r'\w*\W*\—?\W*D.O.E.\W*.{0,50}?\W*S.O\W*PAULO\W*.{0,50}?\w+\-FEIRA\W*\d+\W*.{0,20}\W*DE\W*\d{4}\W*(?:CADERNO\W*\d+\W*\d*)?',
        re.IGNORECASE)
    lista_expressoes_ignoradas.append(expressao_cabecalho9)

    expressao_cabecalho10 = re.compile(
        r'PUBLICACAO\W*OFICIAL\W*DO\W*TRIBUNAL\W*DE\W*JUSTICA\W*DO\W*ESTADO\W*DE\W*S.O\W*PAULO\W*LEI\W*O\W*DI.RIO\W*DA\W*JUSTI.A\W*ELETR.NICO\W*CADERNO\W*JUDICIAL\W*1A\W*INST.NCIA\W*(?:INTERIOR|CAPITAL)\W*(?:PARTE\W*\w*)?\W*\W*\d+',
        re.IGNORECASE)
    lista_expressoes_ignoradas.append(expressao_cabecalho10)

    separador = '(?:\s+SEPARADOR\s+(?:PROC\s*\.?\s*?(?:ESSO)?(?:[ \:\s*\-\s*]*))?(\\b\d{7}\s*[\.\-]\s*?\d{2}\s*[\.\-]\s*\d{4}\s*[\.\-]\s*\d\s*[\.\-]\s*\d{2}\s*[\.\-]\s*\d{4}|\\b\d{7}\s*[\.\-]\s*?\d{2}\s*[\.\-]\s*\d{4}\s*[\.\-]\s*\d{3}\s*[\.\-]\s*\d{4}|\\b\d{3}\s*[\.\-]\s*\d{2}\s*[\.\-]\s*\d{6}\s*[\.\-]\s*\d|\\b\d{4}\s*[\.\-]\s*\d{2}\s*[\.\-]\s*\d{4}\s*[\.\-]\s*\d\s*[\.\-]\s*\d{2}\s*[\.\-]\s*\d{4}|\\b\d{4}\s*[\.\-]\s*\d{2}\s*[\.\-]\s*\d{2}\s*[\.\-]\s*\d{6}\s*[\.\-]\s*\d|\\b\d{3}\s*[\.\-]\s*\d{2}\s*[\.\-]\s*\d{4}\s*[\.\-]\s*\d\s*[\.\-]\s*\d{2}\s*[\.\-]\s*\d{4}|\\b\d{5}\s*[\.\-]\s*\d{2}\s*[\.\-]\s*\d{4}\s*[\.\-]\s*\d\s*[\.\-]\s*\d{2}\s*[\.\-]\s*\d{4}|\\b\d{7}\s*[\.\-]\s*\d\/\d|\\b\d{3}\s*[\.\-]\s*\d{2}\s*[\.\-]\s*\d{4}\s*[\.\-]\s*\d{6}\s*[\.\-]\s*\d|\\b\d{3}\s*[\.\-]\s*\d{3}\s*[\.\-]\s*\d\/\d|\\b\d{6,7}\s*[\.\-]\s*\d{2}\s*[\.\-]\s*\d{4}\s*[\.\-]\s*\d\s*[\.\-]\s*\d{2}\s*[\.\-]\s*\d{4}|\\b\d{3}\s*[\.\-]\s*\d{2}\s*[\.\-]\s*\d{4}\s*[\.\-]\s*\d{6}(\s*[\.\-]\s*\d\/\d{6}\s*[\.\-]\s*\d{3})?|\\b\d{3}\.\d{2,4}\.\d{6}\-?\d?))'

    lista_de_linhas = cria_lista_de_linhas_mantendo_separador(arquivo, lista_expressoes_ignoradas, separador)
    return lista_de_linhas
