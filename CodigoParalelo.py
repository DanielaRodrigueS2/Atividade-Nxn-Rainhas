import random
import time
import concurrent.futures
import threading

#Marco do início da execução do programa
start_time = time.time()

#Bloqueio de acesso para múltiplas threads em determinada parte do código
lock = threading.Lock()


#Função para criar a matriz com todas as posições com o número 0
def criaMatriz(tamanho):
    matriz = []
    for x in range(tamanho):
        linha = []
        for y in range(tamanho):
            linha.append(0)
        matriz.append(linha)
    return matriz


#Função para apresentar a matriz
def imprimeMatriz(matriz ,tamanho):
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
def posicionaRainha(matriz, lin, linOcupada, colOcupada, tamanho):
    tentativas = 0
    #Nesse looping a coluna a ser posicionada a nova Rainha será decidida de forma randomica e terá um limite de tentivas
    #que informará caso a forma como as outras Rainhas foram dispostas não permita a resolução do problema
    while tentativas < tamanho * 10:
        #Define uma coluna para posicionar a Rainha excluindo as colunas já ocupadas por outras Rainhas
        col = random.choice([num for num in range(0, tamanho) if num not in colOcupada])
        #Chama a função verificaDisp para verificar se a Rainha entrará em xeque pela diagonal por alguma outra Rainha já posicionada
        if verificaDisp(lin, col, linOcupada, colOcupada):
            # Caso a coluna selecionada esteja disponível aloca as posições de linha e coluna ocupadas e a Rainha no tabuleiro encerrando o looping
            #Como multiplas threads estarão executando simultaneamente e acessando as mesmas variáveis, para não ocorrer sobrescrição de informação
            #é realizado um bloqueio nessas variáveis para que as threads não as alterem de forma simultânea, acarretando em erro
            with lock:
                linOcupada.append(lin)
                colOcupada.append(col)
                matriz[lin][col] = 1
            return False
        #Variável que irá controlar a quantidade de tentativas realizadas
        tentativas+=1
    #Caso o limite de tentativas seja atinjido, será informado que houve erro, o que fará que a resolução do problema se reinicie
    return True


def resolveNRainhas(tamanho):
    #Cria o tabuleiro e posiciona a primeira rainha para iniciar o processo de resolução
    matriz = criaMatriz(tamanho)
    linOcupada = [0]
    colOcupada = [random.randint(0, tamanho - 1)]
    matriz[linOcupada[0]][colOcupada[0]] = 1

    #Criação de uma ThreadPool para execução da tarefa de posicionamento das Rainhas de forma paralela
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for i in range(1, tamanho):
            #Futures recebera os retornos de erro de posicionamento das threads
            futures.append(executor.submit(posicionaRainha, matriz, i, linOcupada, colOcupada, tamanho))

        #Caso algum posicionamento de Rainha tenha apontado erro o processo de resolução é totalmente reiniciado
        #A verificação também ocorre de forma paralela conforme as threads são encerradas
        for future in concurrent.futures.as_completed(futures):
            erro = future.result()
            if erro:
                return None

    #Caso nenhum erro de posicionamento tenha sido identificado o tabuleiro montado é transmitido para apresentação
    return matriz


def main():
    tamanho = int(input("Digite o tamanho da matriz de NxN rainhas: "))
    matriz = None

    #Inicia o processo de resolução da matriz tendo ela mesma como indicativo de resolução
    while matriz is None:
        matriz = resolveNRainhas(tamanho)

    #Realiza a impressão do problema resolvido
    imprimeMatriz(matriz, tamanho)



main()

#Informa o tempo de execução
execution_time = time.time() - start_time
print("--- %s segundos ---" % execution_time)