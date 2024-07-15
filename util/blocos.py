import re

def quebra_blocos(texto, chunck, sobrepor):
    if chunck <= sobrepor:
        raise ValueError("O tamanho do bloco deve ser maior do que a sobreposição")

    pedacos = []
    inicio = 0

    while inicio < len(texto):
        final = inicio + chunck
        pedacos.append(texto[inicio:final])
        if final >= len(texto):
            inicio = len(texto)
        else:
            inicio += chunck - sobrepor

    return pedacos


if __name__ == '__main__':
    local = r"D:\diarios\SP\2021\01\DJSP_Caderno15_2021_01_21.txt"

    with open(local, 'r', encoding='utf-8') as file:
        texto = file.read()

    print(len(texto))
    pedacos = quebra_blocos(texto, chunck=1000, sobrepor=200)

    for i, pedaco in enumerate(pedacos):
        print(f'Pedaço {i+1}')
        print(pedaco)
        print(len(pedaco))
        print()
