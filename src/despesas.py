
from datetime import datetime
from .dados import carregar, guardar, proximo_id


# Issue 1 

def adicionar_despesa():
    print("\nAdicionar Despesa")

    descricao = input("Descrição da despesa: ").strip()
    if descricao == "":
        print("Tens de escrever uma descrição")
        return

    try:
        valor = float(input("Valor da despesa: ").replace(",", "."))

        if valor <= 0:
            print("O valor tem de ser maior que zero")
            return

    except ValueError:
        print("O valor introduzido não e valido")
        return

    categoria = input("Categoria: ").strip()
    if categoria == "":
        print("Tens de indicar uma categoria")
        return

    data = input("Data (DD-MM-AAAA): ").strip()

    try:
        datetime.strptime(data, "%d-%m-%Y")
    except ValueError:
        print("A data não é válida")
        return

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
        print("Valor:", f"{despesa['valor']:.2f}", "€")
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

    try:
        id_despesa = int(input("\nID da despesa que queres editar: "))
    except ValueError:
        print("ID inválido")
        return

    for despesa in despesas:
        if despesa["id"] == id_despesa:

            print("\nDeixa vazio para manter o valor atual")

            descricao = input("Nova descrição: ").strip()

            valor_texto = input("Novo valor (€): ").replace(",", ".")

            if valor_texto != "":
                try:
                    valor = float(valor_texto)

                    if valor <= 0:
                        print("O numero tem de ser maior que zero")
                        return

                except ValueError:
                    print("Valor invalido")
                    return

            categoria = input("Nova categoria: ").strip()

            data = input("Nova data (DD-MM-AAAA): ").strip()

            if data != "":
                try:
                    datetime.strptime(data, "%d-%m-%Y")
                except ValueError:
                    print("A data é inválida")
                    return

            if descricao != "":
                despesa["descricao"] = descricao

            if valor_texto != "":
                despesa["valor"] = round(valor, 2)

            if categoria != "":
                despesa["categoria"] = categoria

            if data != "":
                despesa["data"] = data

            guardar(dados)

            print("\nDespesa editada com sucesso!")
            return

    print("Não existe nenhuma despesa com esse ID")
