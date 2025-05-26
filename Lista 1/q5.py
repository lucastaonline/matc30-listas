import random

class Node:
    def __init__(self, value, children):
        self.value = value
        self.children = children
        self.parent = None

def similar_pair(n, k, edges):
    quantidade__pares_similares = 0
    nos = {}

    for edge in edges:
        if edge[0] not in nos:
            nos[edge[0]] = Node(edge[0], [])

        if edge[1] not in nos:
            nos[edge[1]] = Node(edge[1], [])
            
        nos[edge[0]].children.append(nos[edge[1]])
        nos[edge[1]].parent = nos[edge[0]]

    for no in nos.values():
        if no.parent is None:
            continue

        parent = no.parent

        while parent is not None:
            if abs(parent.value - no.value) <= k:
                quantidade__pares_similares += 1
            
            parent = parent.parent

    return quantidade__pares_similares

def generateTestCases():
    return [
        (5, 2, [(3, 2), (3, 1), (1, 4), (1, 5)]),
        (6, 3, [(1, 2), (1, 3), (2, 4), (3, 5), (3, 6)]),
        (4, 1, [(1, 2), (2, 3), (3, 4)]),
        (7, 4, [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (6, 7)]),
        (3, 0, [(1, 2), (2, 3)])
    ]
def main():
    # Já te provei que sei ler entradas né... esse aqui eu vou deixar a que você me deu
    testCases = generateTestCases()
    for idx, (n, k, edges) in enumerate(testCases, 1):
        print(f"🧪 Teste {idx}")
        print(f"n = {n}, k = {k}, edges = {edges}")
        result = similar_pair(n, k, edges)
        print(f"➡️ Resultado: {result}\n")

if __name__ == "__main__":
 main()