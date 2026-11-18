
from datetime import datetime
from .dados import carregar, guardar, proximo_id


# Issue 1 

def adicionar_despesa():
    print("\n Adicionar Despesa")

    descricao = input("Descrição da despesa: ").strip()
    if descricao == "":
        print("Falta uma descrição")
        return

    try:
        valor = float(input("Valor da despesa (€): ").replace(",", "."))

        if valor <= 0:
            print("O numero tem de ser maior que zero")
            return


    except ValueError:
        print("Valor invalido")
        return

    

    categoria = input("Categoria: ").strip()
    if categoria == "":
        print("Indica uma categoria")
        return

    data = input("Data (DD-MM-AAAA): ").strip()
    try:
        datetime.strptime(data, "%d-%m-%Y")
    except ValueError:
        print("A data invalida")
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

    print("\nRegisto adicionado")


# Issue 2 

def consultar_despesas():
    dados = carregar()
    despesas = dados["despesas"]

    print("\nConsultar Despesas")

    if len(despesas) == 0:
        print("Ainda não tem despesas ")
        return

    for despesa in despesas:
        print("ID:", despesa["id"])
        print("Descrição:", despesa["descricao"])
        print("Valor:", f"{float(despesa['valor']):.2f}", "€")
        print("Categoria:", despesa["categoria"])
        print("Data:", despesa["data"])
