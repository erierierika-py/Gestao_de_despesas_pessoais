"""Módulo de poupança: objetivo, valor poupado e progresso."""

from src import dados

def definir_objetivo():
    """Pede um valor ao utilizador e guarda-o como objetivo de poupança.

    O valor tem de ser um número maior que 0. Se o utilizador carregar
    em Enter sem escrever nada, a operação é cancelada.
    """
    d = dados.carregar()
    atual = d["poupanca"]["objetivo"]
    if atual > 0:
        print(f"Objetivo atual: {atual:.2f}€")

    while True:
        objetivo = input("Novo objetivo em € (Enter para cancelar): ").strip().replace(",", ".")
        if not objetivo:
            print("Operação cancelada.")
            return
        try:
            valor = float(objetivo)
        except ValueError:
            print("Valor inválido. Escreve um número.")
            continue
        if valor <= 0:
            print("O objetivo tem de ser maior que 0.")
            continue
        break

    d["poupanca"]["objetivo"] = valor
    dados.guardar(d)
    print(f"Objetivo definido: {valor:.2f}€")


def calcular_poupado(d):
    """Calcula o valor poupado: total de rendimentos menos total de despesas.

    Args:
        d: Dicionário completo de dados (resultado de dados.carregar()).

    Devolve:
        float: Valor poupado. Pode ser negativo se gastaste mais do que recebeste.
    """
    total_rendimentos = sum(r["valor"] for r in d["rendimentos"])
    total_despesas = sum(x["valor"] for x in d["despesas"])
    return total_rendimentos - total_despesas

