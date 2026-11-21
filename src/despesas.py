
from datetime import datetime
from .dados import carregar, guardar, proximo_id


# Issue 1

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

            if valor <= 0:
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
        data = input("Data (DD-MM-AAAA): ").strip()

        try:
            datetime.strptime(data, "%d-%m-%Y")
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


# Issue 2

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


# Issue 3

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
            print("Erro: ID inválido, tenta novamente")
            continue

        encontrada = None

        for despesa in despesas:
            if despesa["id"] == id_despesa:
                encontrada = despesa
                break

        if encontrada != None:
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

            if valor <= 0:
                print("Erro: O numero tem de ser maior que zero")
            else:
                break

        except ValueError:
            print("Erro: Valor invalido, tenta novamente")

    categoria = input("Nova categoria: ").strip()

    while True:
        data = input("Nova data (DD-MM-AAAA): ").strip()

        if data == "":
            break

        try:
            datetime.strptime(data, "%d-%m-%Y")
            break

        except ValueError:
            print("Erro: A data é inválida, tenta novamente")

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


# Issue 4

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

                despesas.remove(despesa)
                guardar(dados)

                print("\nDespesa eliminada")
                return

        print("Erro: Essa despesa não existe, tenta novamente")
