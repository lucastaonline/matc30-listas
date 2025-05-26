# bora ajudar esse sapo miserável
# Quero deixar claro uma coisa aqui
# Não irei usar o GPT para fazer o código pra mim.
# Com certeza irei usar para tirar dúvidas básicas da linguagem python e pra me ensinar algumas estratégias que posso utilizar
# na resolução das respostas, até pq eu quero aprender mais né kkk, mas o código vai ser meu. Tamo junto e bora vitória

# Pra esse problema vou usar a resolução da Cadeia de Markov
# Cada célula do labirinto acessível vai ser um estado. Vou montar uma matriz de probabilidade (Matriz de Transição) pra armazenar a probabildiade de
# o sacana do sapo ir de um estado pra o outro.

# Com a matriz de transição eu calculo a matriz fundamental e depois a probabilidade com a matriz de absorção.

# Update:
# Isso é complexo como a porra, mas eu to aqui me fudendo pra fazer, to escrevendo pra provar q sou eu mesmo, pode até me pergunta se duvidar, tamo junto mano gibas.

# Update 2:
# Depois de horas acabei. Se isso não estiver certo eu me mato na sua frente tmj (brincadeira)

import random

class Estado:
    def __init__(self, coordenadas, absorvente, eh_inicio, eh_mina, eh_saida):
        self.coordenadas = coordenadas
        self.absorvente = absorvente
        self.eh_inicio = eh_inicio
        self.eh_mina = eh_mina
        self.eh_saida = eh_saida
        self.eh_tunel = False
        self.coordenada_destino_tunel = None
        
def obter_informacoes_tunel(estado, tunnels):
    for tuneis in tunnels:
        if estado.coordenadas[0] == tuneis[0] - 1  and estado.coordenadas[1] == tuneis[1] - 1:
            estado.eh_tunel = True
            estado.coordenada_destino_tunel = (tuneis[2], tuneis[3])
        elif estado.coordenadas[0] == tuneis[2] - 1 and estado.coordenadas[1] == tuneis[3] - 1:
            estado.eh_tunel = True
            estado.coordenada_destino_tunel = (tuneis[0], tuneis[1])
    
def montar_array_estados(n, m, maze):
    estados_absorventes = ['%', '*']
    estados_nao_absorventes = ['O', 'A']
    array_estados = []
    
    for linha in range(n):
        for coluna in range(m):
            if maze[linha][coluna] in estados_absorventes:
                array_estados.append(Estado((linha, coluna), True, 
                                            maze[linha][coluna] == 'A', 
                                            maze[linha][coluna] == '*', 
                                            maze[linha][coluna] == '%'))
            elif maze[linha][coluna] in estados_nao_absorventes:
                array_estados.append(Estado((linha,coluna), False, 
                                            maze[linha][coluna] == 'A', 
                                            maze[linha][coluna] == '*', 
                                            maze[linha][coluna] == '%'))
                
    return array_estados

def retorna_celula(coordenadas, direcao):
    celulas = {
        'cima': (coordenadas[0] - 1, coordenadas[1]),
        'baixo': (coordenadas[0] + 1, coordenadas[1]),
        'esquerda': (coordenadas[0], coordenadas[1] - 1),
        'direita': (coordenadas[0], coordenadas[1] + 1)
    }
    return celulas[direcao]
    
def verificar_celula_acessivel(n, m, estado, maze, direcao):
    coordenadas = estado.coordenadas

    if estado.eh_tunel:
        coordenadas = estado.coordenada_destino_tunel

    coordenadas_celula = retorna_celula(coordenadas, direcao)

    if coordenadas_celula[0] < 0 or coordenadas_celula[0] >= n:
        return False
    
    if coordenadas_celula[1] < 0 or coordenadas_celula[1] >= m:
        return False
    
    if maze[coordenadas_celula[0]][coordenadas_celula[1]] == '#':
        return False
    
    return True
                
def montar_matriz_transicao(n, m, estados, maze):
    matriz_transicao = []
    for estado in estados:
        linha_matriz = [0.0] * len(estados)

        if estado.absorvente:
            linha_matriz[estados.index(estado)] = 1.0
            matriz_transicao.append(linha_matriz)
            continue

        if estado.eh_tunel:
            estado_destino = next((e for e in estados if e.coordenadas == estado.coordenada_destino_tunel), None)
            
            if estado_destino is None:
                matriz_transicao.append(linha_matriz)
                continue
            elif estado_destino.absorvente:
                linha_matriz[estados.index(estado_destino)] = 1.0
                matriz_transicao.append(linha_matriz)
                continue

        quantidade_celulas_acessiveis = 0

        direcoes_acessiveis = []

        if verificar_celula_acessivel(n, m, estado, maze, 'cima'):
            quantidade_celulas_acessiveis+= 1
            direcoes_acessiveis.append('cima')

        if verificar_celula_acessivel(n, m, estado, maze, 'baixo'):
            quantidade_celulas_acessiveis+= 1
            direcoes_acessiveis.append('baixo')

        if verificar_celula_acessivel(n, m, estado, maze, 'esquerda'):
            quantidade_celulas_acessiveis+= 1
            direcoes_acessiveis.append('esquerda')

        if verificar_celula_acessivel(n, m, estado, maze, 'direita'):
            quantidade_celulas_acessiveis+= 1
            direcoes_acessiveis.append('direita')

        if quantidade_celulas_acessiveis == 0:
            matriz_transicao.append(linha_matriz)
            continue

        probabilidade = 1.0 / quantidade_celulas_acessiveis

        for direcao in direcoes_acessiveis:
            coordenadas = estado.coordenadas

            if estado.eh_tunel:
                coordenadas = estado.coordenada_destino_tunel

            coordenadas_celula_acessivel = retorna_celula(coordenadas, direcao)

            for i, estado_acessivel in enumerate(estados):
                if estado_acessivel.coordenadas == coordenadas_celula_acessivel:
                    linha_matriz[i] = probabilidade
                    break

        matriz_transicao.append(linha_matriz)

    return matriz_transicao

def montar_submatriz_transicao_estados_transientes(matriz_transicao, estados):
    submatriz_transicao_estados_transientes = []
    estados_transientes = [estado for estado in estados if not estado.absorvente]
    estado_inicial_index = next((i for i, e in enumerate(estados_transientes) if e.eh_inicio))

    for i in range(len(estados_transientes)):
        linha = []
        for j in range(len(estados_transientes)):
            linha.append(matriz_transicao[estados.index(estados_transientes[i])][estados.index(estados_transientes[j])])
        submatriz_transicao_estados_transientes.append(linha)

    return submatriz_transicao_estados_transientes, estado_inicial_index

def montar_submatriz_absorcao(matriz_transicao, estados):
    submatriz_absorcao = []
    estados_transientes = [estado for estado in estados if not estado.absorvente]
    estados_absorventes = [estado for estado in estados if estado.absorvente]

    estados_absorventes_indexes = [estados_absorventes.index(e) for e in estados_absorventes if e.eh_saida]

    for i in range(len(estados_transientes)):
        linha = []
        for j in range(len(estados_absorventes)):
            linha.append(matriz_transicao[estados.index(estados_transientes[i])][estados.index(estados_absorventes[j])])
        submatriz_absorcao.append(linha)

    return submatriz_absorcao, estados_absorventes_indexes

def montar_matriz_identidade(tamanho):
    matriz_identidade = []
    for i in range(tamanho):
        linha = []
        for j in range(tamanho):
            if i == j:
                linha.append(1.0)
            else:
                linha.append(0.0)
        matriz_identidade.append(linha)
    return matriz_identidade

# Essa função eu usei o GPT pra fazer pq não sabia se podia usar o numpy e porra... sacanagem eu ter q fazer isso aqui do zero
def inverter_matriz(matriz):
    n = len(matriz)

    # Verifica se é quadrada
    if any(len(linha) != n for linha in matriz):
        raise ValueError("A matriz deve ser quadrada.")

    # Cria a matriz aumentada [A | I]
    identidade = [[float(i == j) for j in range(n)] for i in range(n)]
    aumentada = [linha[:] + identidade[i] for i, linha in enumerate(matriz)]

    # Aplica o método de Gauss-Jordan
    for i in range(n):
        # Pivô deve ser diferente de zero
        if aumentada[i][i] == 0:
            for j in range(i + 1, n):
                if aumentada[j][i] != 0:
                    aumentada[i], aumentada[j] = aumentada[j], aumentada[i]
                    break
            else:
                raise ValueError("A matriz não é invertível (determinante zero).")

        # Normaliza a linha do pivô
        pivô = aumentada[i][i]
        aumentada[i] = [x / pivô for x in aumentada[i]]

        # Zera a coluna nos outros lugares
        for j in range(n):
            if j != i:
                fator = aumentada[j][i]
                aumentada[j] = [
                    a - fator * b for a, b in zip(aumentada[j], aumentada[i])
                ]

    # Extrai a inversa (lado direito)
    inversa = [linha[n:] for linha in aumentada]
    return inversa

def subtrair_matrizes(matriz_a, matriz_b):
    resultado = []
    for i in range(len(matriz_a)):
        linha = []
        for j in range(len(matriz_a[0])):
            linha.append(matriz_a[i][j] - matriz_b[i][j])
        resultado.append(linha)
    
    return resultado

def multiplicar_matrizes(matriz_a, matriz_b):
    resultado = []
    for i in range(len(matriz_a)):
        linha = []
        for j in range(len(matriz_b[0])):
            soma = 0
            for k in range(len(matriz_b)):
                soma += matriz_a[i][k] * matriz_b[k][j]
            linha.append(soma)
        resultado.append(linha)
    
    return resultado

def montar_matriz_fundamental(submatriz_transicao_estados_transientes):
    matriz_identidade = montar_matriz_identidade(len(submatriz_transicao_estados_transientes))

    matriz_identidade_menos_submatriz = subtrair_matrizes(matriz_identidade, submatriz_transicao_estados_transientes)

    matriz_fundamental = inverter_matriz(matriz_identidade_menos_submatriz)

    return matriz_fundamental

def resolver_labirinto(n, m, k, maze, tunnels):
    estados = montar_array_estados(n, m, maze)
    
    for estado in estados:
        obter_informacoes_tunel(estado, tunnels)
    
    matriz_transicao = montar_matriz_transicao(n, m, estados, maze)
    submatriz_transicao_estados_transientes_estado_inicial_index = montar_submatriz_transicao_estados_transientes(matriz_transicao, estados)
    submatriz_absorcao_e_saida_indexes = montar_submatriz_absorcao(matriz_transicao, estados)
    
    matriz_fundamental = montar_matriz_fundamental(submatriz_transicao_estados_transientes_estado_inicial_index[0])

    matriz_absorcao = multiplicar_matrizes(matriz_fundamental, submatriz_absorcao_e_saida_indexes[0])

    probabilidade_fuga = 0.0
    estado_inicial_index = submatriz_transicao_estados_transientes_estado_inicial_index[1]
    estados_saida_indexes = submatriz_absorcao_e_saida_indexes[1]

    probabilidade_fuga = sum(matriz_absorcao[estado_inicial_index][index] for index in estados_saida_indexes)
    
    return probabilidade_fuga

def gerar_labirinto(n, m):
    elementos = ['O'] * 5 + ['#','*', '%']
    labirinto = [''.join(random.choice(elementos) for _ in range(m)) for _ in range(n)]
    i, j = random.randint(0, n-1), random.randint(0, m-1)
    linha = list(labirinto[i])
    linha[j] = 'A'
    labirinto[i] = ''.join(linha)
    return labirinto
    
def gerar_tuneis(k, n, m):
    tuneis = set()
    while len(tuneis) < k:
        i1, j1 = random.randint(0, n-1), random.randint(0, m-1)
        i2, j2 = random.randint(0, n-1), random.randint(0, m-1)
        if (i1 != i2 or j1 != j2):
            tuneis.add((i1, j1, i2, j2))
    return list(tuneis)

def main():
    n, m, k = 3, 3, 1
    maze = gerar_labirinto(n, m)
    tunnels = gerar_tuneis(k, n, m)

    # Não tenho certeza se você quer que eu faça a leitura da entrada ou se você quer deixar o código gerado então tá aí
    # n, m, k = map(int, input().split())
    # maze = []
    # for _ in range(n):
    #     linha = input().strip()
    #     while len(linha) != m:
    #         print(f"Tamanho da linha deve ser {m}")
    #         linha = input().strip()

    #     maze.append(linha)

    # tunnels = []
    # for _ in range(k):
    #     tuneis = input().split()
    #     while len(tuneis) != 4:
    #         print("Tamanho dos túneis deve ser 4")
    #         tuneis = input().split()
    #         i1, j1, i2, j2 = map(int, tuneis)
    #         if not (0 <= i1 <= n and 0 <= j1 <= m and 0 <= i2 <= n and 0 <= j2 <= m):
    #             print("Coordenadas dos túneis fora do range da matriz")
    #             tuneis = input().split()
    #             continue

    #     i1, j1, i2, j2 = map(int, tuneis)
    #     tunnels.append((i1, j1, i2, j2))

    # resultado = resolver_labirinto(n, m, k, maze, tunnels)
    # print(resultado)
    
    # Caso de teste fornecido
    # n, m, k = 3, 6, 1
    # maze = [
    #     "###*OO",
    #     "O#OA%O",
    #     "###*OO"
    # ]
    # tunnels = [(2, 3, 2, 1)]

    print("Maze:")
    for linha in maze:
        print(linha)
    print("Tunnels:", tunnels)
    
    resultado = resolver_labirinto(n, m, k, maze, tunnels)
    print("Probabilidade de fuga:", resultado)

if __name__ == '__main__':
    main()