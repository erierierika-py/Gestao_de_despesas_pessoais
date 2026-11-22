"""Módulo de despesas: adicionar, consultar, editar e eliminar despesas."""

import math
from datetime import datetime

from .dados import carregar, guardar, proximo_id
from .saldo import mostrar_limite_restante
from .utilitarios import confirmar

FORMATO_DATA = "%Y-%m-%d"

def adicionar_despesa():
    print("\nAdicionar Despesa")

    while True:
        descricao = input("Descrição da despesa: ").strip()

        if descricao == "":
            print("Erro: Falta uma descrição")
        else:
            break

    while True:
        try:
            valor = float(input("Valor da despesa (€): ").replace(",", "."))

            if not math.isfinite(valor) or valor <= 0:
                print("Erro: O numero tem de ser maior que zero")
            else:
                break

        except ValueError:
            print("Erro: Valor invalido, tenta novamente")

    while True:
        categoria = input("Categoria: ").strip()

        if categoria == "":
            print("Erro: Indica uma categoria")
        else:
            break

    while True:
        data = input("Data (AAAA-MM-DD): ").strip()

        try:
            datetime.strptime(data, FORMATO_DATA)
            break

        except ValueError:
            print("Erro: A data não é válida, tenta novamente")

    dados = carregar()

    nova_despesa = {
        "id": proximo_id(dados["despesas"]),
        "descricao": descricao,
        "valor": round(valor, 2),
        "categoria": categoria,
        "data": data
    }

    dados["despesas"].append(nova_despesa)
    guardar(dados)

    print("\nRegisto adicionado!")

    mostrar_limite_restante()


def consultar_despesas():
    dados = carregar()
    despesas = dados["despesas"]

    print("\nConsultar Despesas")

    if len(despesas) == 0:
        print("Ainda não existem despesas")
        return

    for despesa in despesas:
        print("\nID:", despesa["id"])
        print("Descrição:", despesa["descricao"])
        print("Valor:", f"{float(despesa['valor']):.2f}", "€")
        print("Categoria:", despesa["categoria"])
        print("Data:", despesa["data"])


def editar_despesa():
    dados = carregar()
    despesas = dados["despesas"]

    print("\nEditar Despesa")

    if len(despesas) == 0:
        print("Ainda não existem despesas")
        return

    for despesa in despesas:
        print("ID:", despesa["id"], "-", despesa["descricao"])

    while True:
        try:
            id_despesa = int(input("\nID da despesa que queres editar: "))

        except ValueError:
            print("Erro: ID invalido, tenta novamente")
            continue

        encontrada = None

        for despesa in despesas:
            if despesa["id"] == id_despesa:
                encontrada = despesa
                break

        if encontrada is not None:
            break
        else:
            print("Erro: Não existe nenhuma despesa com esse ID")

    print("\nDeixa vazio para manter o valor atual")

    descricao = input("Nova descrição: ").strip()

    while True:
        valor_texto = input("Novo valor (€): ").replace(",", ".")

        if valor_texto == "":
            break

        try:
            valor = float(valor_texto)

            if not math.isfinite(valor) or valor <= 0:
                print("Erro: O numero tem de ser maior que zero")
            else:
                break

        except ValueError:
            print("Erro: Valor invalido, tenta novamente")

    categoria = input("Nova categoria: ").strip()

    data = input("Nova data (DD-MM-AAAA): ").strip()

    if descricao != "":
        encontrada["descricao"] = descricao

    if valor_texto != "":
        encontrada["valor"] = round(valor, 2)

    if categoria != "":
        encontrada["categoria"] = categoria

    if data != "":
        encontrada["data"] = data

    guardar(dados)

    print("\nDespesa editada com sucesso!")


def eliminar_despesa():
    dados = carregar()
    despesas = dados["despesas"]

    print("\nEliminar Despesa")

    if len(despesas) == 0:
        print("Ainda não existem despesas")
        return

    for despesa in despesas:
        print("ID:", despesa["id"], "-", despesa["descricao"])

    while True:
        try:
            id_despesa = int(input("\nID da despesa que queres eliminar: "))

        except ValueError:
            print("Erro: ID invalido, tenta novamente")
            continue

        for despesa in despesas:
            if despesa["id"] == id_despesa:

                print("\nDescrição:", despesa["descricao"])
                print("Valor:", despesa["valor"], "€")

                if not confirmar("Eliminar esta despesa?"):
                    print("Operação cancelada.")
                    return

                despesas.remove(despesa)
                guardar(dados)

                print("\nDespesa eliminada")
                return

        print("Erro: Essa despesa não existe, tenta novamente")
