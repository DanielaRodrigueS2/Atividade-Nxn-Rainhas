import time

#Código utilizado na apresentação "A" para comparações com código "B"

start_time = time.time()

# Função responsável por gerar a matriz de um tamanho x usando listas dentro de listas
def criaMatriz(tam):
    matriz = []
    for x in range(tam):
        linha = []
        for y in range(tam):
            linha.append(0)
        matriz.append(linha)
    return matriz

# Função que imprime a matriz linha por linha
def imprimeMatriz(matriz, tam):
    for i in range(tam):
        print(matriz[i])

# Função que verifica se é seguro colocar uma rainha na posição (linha, coluna)
def esta_seguro(tabuleiro, linha, coluna, n):
    # Verifica se há alguma rainha na mesma coluna
    for i in range(linha):
        if tabuleiro[i][coluna] == 1:
            return False

    # Verifica a diagonal superior à esquerda
    for i, j in zip(range(linha, -1, -1), range(coluna, -1, -1)):
        if tabuleiro[i][j] == 1:
            return False

    # Verifica a diagonal superior à direita
    for i, j in zip(range(linha, -1, -1), range(coluna, n)):
        if tabuleiro[i][j] == 1:
            return False

    return True

# Função recursiva para resolver o problema de N rainhas
def resolve_n_rainhas(tabuleiro, linha, n):
    if linha >= n:
        return True

    for i in range(n):
        if esta_seguro(tabuleiro, linha, i, n):
            tabuleiro[linha][i] = 1
            if resolve_n_rainhas(tabuleiro, linha + 1, n):
                return True
            tabuleiro[linha][i] = 0  # backtracking

    return False

# Função principal que executa o programa
def main():
    n = int(input("Digite o tamanho do tabuleiro (n x n): "))# Tamanho do tabuleiro NxN
    tabuleiro = criaMatriz(n)

    # Solicita ao usuário para escolher a coluna da primeira rainha na linha 1
    coluna = int(input(f"Escolha a coluna (0 a {n-1}) para a primeira rainha na linha 1: "))

    # Coloca a primeira rainha na posição escolhida
    tabuleiro[0][coluna] = 1

    # Resolve o problema para as rainhas restantes
    if resolve_n_rainhas(tabuleiro, 1, n):
        print("Solução encontrada:")
        imprimeMatriz(tabuleiro, n)
    else:
        print("Nenhuma solução existe.")


main()

execution_time = time.time() - start_time
print("--- %s segundos ---" % execution_time)