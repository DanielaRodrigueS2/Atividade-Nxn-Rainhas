import random
import time

start_time = time.time()

#Varíaveis globais
tamanho = 0
erro = True

#Função para criar a matriz com todas as posições com o número 0
def criaMatriz():
    matriz = []
    for x in range(tamanho):
        linha = []
        for y in range(tamanho):
            linha.append(0)
        matriz.append(linha)
    return matriz

#Função para apresentar a matriz
def imprimeMatriz(matriz):
    for i in range(tamanho):
        print(matriz[i])

#Função para verificar se a nova Rainha a ser posicionada está em xeque na diagonal por alguma outra Rainha já posicionada
def verificaDisp(lin, col, linOcupada, colOcupada):
    #Teste realizado com todas as Rainhas já posicionadas
    for i in range(len(linOcupada)):
        if abs(lin - linOcupada[i]) == abs(col - colOcupada[i]):
            return False
    return True

#Função responsável por posicionar a Rainha no tabuleiro
def posicionaRainha(matriz, linOcupada, colOcupada):
    global erro
    tentativas = 0
    #Nesse looping a coluna a ser posicionada a nova Rainha será decidida de forma randomica e terá um limite de tentivas
    #que informará caso a forma como as outras Rainhas foram dispostas não permita a resolução do problema
    while tentativas < tamanho * 10:
        lin = len(linOcupada)
        col = random.choice([num for num in range(0, tamanho) if num not in colOcupada])
        if verificaDisp(lin, col, linOcupada, colOcupada):
            linOcupada.append(lin)
            colOcupada.append(col)
            matriz[lin][col] = 1
            break
        tentativas+=1
    #Caso o limite de tentativas seja atinjido, será informado que houve erro, o que fará que a resolução do problema se reinicie
    if tentativas == tamanho * 10:
        erro = True

def main():
    global tamanho, erro
    tamanho = int(input("Digite o tamanho da matriz de NxN rainhas: "))

    while erro:
        erro = False
        matriz = criaMatriz()
        linOcupada = []
        linOcupada.append(0)
        colOcupada = []
        colOcupada.append(random.randint(0, tamanho - 1))
        matriz[linOcupada[0]][colOcupada[0]] = 1
        for i in range (1, tamanho):
            posicionaRainha(matriz, linOcupada, colOcupada)
            if erro:
                break

    imprimeMatriz(matriz)

main()

execution_time = time.time() - start_time
print("--- %s segundos ---" % execution_time)