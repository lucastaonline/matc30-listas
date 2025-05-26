# Tranquilo tbm
import random

def activityNotifications(expenditure, d):
    numero_notificacoes = 0
    for i in range(d, len(expenditure)):
        ultimos_d_dias = sorted(expenditure[i - d:i])
        gasto_do_dia = expenditure[i]
        
        # O tamanho do array ultimos_d_dias sempre vai ser d
        if d % 2 == 0:
            mediana = (ultimos_d_dias[d // 2 - 1] + ultimos_d_dias[d // 2]) / 2
        else:
            mediana = ultimos_d_dias[d // 2]

        if gasto_do_dia >= 2 * mediana:
            numero_notificacoes += 1
    
    return numero_notificacoes

def gerar_dados(n, max_val=200):
    return [random.randint(0, max_val) for _ in range(n)]

def main():
    n, d = 10, 5
    gastos = gerar_dados(n)

    # n, d = map(int, input().split())
    # gastos = list(map(int, input().split()))

    # while len(gastos) != n:
    #     print(f"Tamanho do array deve ser {n}")

    #     gastos = list(map(int, input().split()))
    
    # resultado = activityNotifications(gastos, d)

    # Caso de teste 1
    # n, d = 9, 5
    # gastos = [2, 3, 4, 2, 3, 6, 8, 4, 5]

    print(f"n = {n}, d = {d}")
    print("Gastos:", gastos)

    resultado = activityNotifications(gastos, d)
    print("Notificações:", resultado)

if __name__ == '__main__':
    main()