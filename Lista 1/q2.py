# Esse aqui foi de boa
import random

def insertionSort(arr):
    quantidade_deslocamentos = 0

    for i in range(1, len(arr)):
        for j in range(i, 0, -1):
            if arr[j] < arr[j - 1]:
                arr[j], arr[j - 1] = arr[j - 1], arr[j]
                quantidade_deslocamentos += 1
            else:
                break

    return quantidade_deslocamentos

def generate_random_array(size, min_val=1, max_val=100):
    return [random.randint(min_val, max_val) for _ in range(size)]

def main():
    arr = generate_random_array(10)

    # Não tenho certeza se você quer que eu faça a leitura da entrada ou se você quer deixar o código gerado então tá aí
    # numero_casos_teste = int(input())
    # for _ in range(numero_casos_teste):
    #     tamanho_array = int(input())
    #     arr = []
        

    #     arr = input().split()
    #     while len(arr) != tamanho_array:
    #         print("Tamanho do array deve ser", tamanho_array)
    #         arr = input().split()
            
    #     arr = [int(x) for x in arr]
    #     result = insertionSort(arr)
    #     print(result)

    # Caso de teste 1
    # arr = [1 ,1, 1, 2, 2]
    # Caso de teste 2
    # arr = [2, 1, 3, 1, 2]

    print("Array de entrada:", arr)
    result = insertionSort(arr)
    print("Deslocamentos realizados:", result)

if __name__ == '__main__':
    main()
