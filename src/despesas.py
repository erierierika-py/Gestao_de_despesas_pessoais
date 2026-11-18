# Issue 1 
import json
from pathlib import Path
from datetime import datetime


def adicionar_despesa():
    print("\n--- Adicionar Despesa --")

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
        print("A data nao e valida")
        return

    caminho = Path(__file__).resolve().parent.parent / "data" / "despesas.json"

    if caminho.exists():
        with open(caminho, "r", encoding="utf-8") as ficheiro:
            despesas = json.load(ficheiro)
    else:
        despesas = []

    nova_despesa = {
        "id": max((d["id"] for d in despesas), default=0) + 1,
        "descricao": descricao,
        "valor": round(valor, 2),
        "categoria": categoria,
        "data": data
    }

    despesas.append(nova_despesa)

    caminho.parent.mkdir(exist_ok=True)

    with open(caminho, "w", encoding="utf-8") as ficheiro:
        json.dump(despesas, ficheiro, indent=4, ensure_ascii=False)

    print("\nRegisto adicionado!")


if __name__ == "__main__":
    adicionar_despesa()
