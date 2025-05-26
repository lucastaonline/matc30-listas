# Esse aqui é foda também...
# já saquei que vou ter q usar recursão...
# Já te digo que nunca conseguiria isso aqui se não fosse Google, StackOverflow e GPT

import random

MOD = 10**9 + 7

class Node:
    def __init__(self, tipo, valor=None, filho1=None, filho2=None):
        self.tipo = tipo
        self.valor = valor
        self.filho1 = filho1
        self.filho2 = filho2

# gpt me ajudou com esse
def construir_arvore(expr):
    operandos = []
    operadores = []

    def aplicar_operador():
        op = operadores.pop()
        if op == '|':
            right = operandos.pop()
            left = operandos.pop()
            operandos.append(Node("union", filho1=left, filho2=right))
        elif op == '.':
            right = operandos.pop()
            left = operandos.pop()
            operandos.append(Node("concat", filho1=left, filho2=right))

    i = 0
    while i < len(expr):
        char = expr[i]

        if char in 'ab':
            node = Node("char", valor=char)
            if i > 0 and expr[i - 1] in 'ab)*':
                operadores.append('.')  # concatenação implícita
            operandos.append(node)
            i += 1

        elif char == '*':
            filho = operandos.pop()
            operandos.append(Node("star", filho1=filho))
            i += 1

        elif char == '(':
            if i > 0 and expr[i - 1] in 'ab)*':
                operadores.append('.')  # concatenação implícita
            operadores.append('(')
            i += 1

        elif char == ')':
            while operadores and operadores[-1] != '(':
                aplicar_operador()
            operadores.pop()  # remove '('
            i += 1

        elif char == '|':
            while operadores and operadores[-1] == '.':
                aplicar_operador()
            operadores.append('|')
            i += 1

        else:
            i += 1  # ignora qualquer outro caractere inválido

    while operadores:
        aplicar_operador()

    return operandos[0]  # raiz da árvore sintática

def countRecognizedStrings(R, L):
    raiz_da_arvore = construir_arvore(R)
            
    def avalia_dp(node, L):
        dp = [0] * (L + 1)

        if node.tipo == "char":
            if L >= 1:
                dp[1] = 1
            return dp

        elif node.tipo == "concat":
            dp1 = avalia_dp(node.filho1, L)
            dp2 = avalia_dp(node.filho2, L)
            for i in range(L + 1):
                for j in range(i + 1):
                    dp[i] = (dp[i] + dp1[j] * dp2[i - j]) % MOD
            return dp

        elif node.tipo == "union":
            dp1 = avalia_dp(node.filho1, L)
            dp2 = avalia_dp(node.filho2, L)
            for i in range(L + 1):
                dp[i] = (dp1[i] + dp2[i]) % MOD
            return dp

        elif node.tipo == "star":
            base = avalia_dp(node.filho1, L)
            dp[0] = 1  # cadeia vazia
            for i in range(1, L + 1):
                for j in range(1, i + 1):
                    dp[i] = (dp[i] + base[j] * dp[i - j]) % MOD
            return dp

        return dp
    
    return avalia_dp(raiz_da_arvore, L)[L]

def gerar_expressao():
    # Simples gerador de expressões balanceadas
    bases = ["a", "b"]
    exp = random.choice(bases)
    for _ in range(random.randint(1, 3)):
        op = random.choice(["|", "", "*"])
        if op == "":
            exp = f"({exp}{random.choice(bases)})"
        elif op == "|":
            xp = f"({exp}|{random.choice(bases)})"
        elif op == "*":
            exp = f"({exp}*)"
    return exp

def main():
    T = 3
    casos = []
    for _ in range(T):
        R = gerar_expressao()
        L = random.randint(1, 6)
        casos.append((R, L))

    for R, L in casos:
        print(f"Expressão: {R}, Tamanho: {L}")
        resultado = countRecognizedStrings(R, L)
        print("Reconhecidas:", resultado)

if __name__ == '__main__':
    main()