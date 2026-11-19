"""Módulo de rendimentos: registar e listar rendimentos (salários e outros)."""

from src import dados
from src.utilitarios import confirmar 

FORMATO_DATA = "%Y-%m-%d"
TEXTO_FORMATO_DATA = "AAAA-MM-DD"

TIPOS = {"1": "Salário", "2": "Outro"}


def _pedir_valor():
    """Pede um valor maior que 0 ao utilizador.

    Returns:
        float | None: O valor, ou None se o utilizador cancelar com Enter.
    """
    while True:
        texto = input("Valor (Enter para cancelar): ").strip().replace(",", ".")
        if not texto:
            return None
        try:
            valor = float(texto)
        except ValueError:
            print("Valor inválido. Escreve um número (ex.: 850.50).")
            continue
        if valor <= 0 or valor != valor or valor == float("inf"):
            print("O valor tem de ser um número maior que 0.")
            continue
        return round(valor, 2)


def _pedir_data():
    """Pede uma data válida ao utilizador.

    Returns:
        str | None: A data no formato definido em FORMATO_DATA,
        ou None se o utilizador cancelar com Enter.
    """
    from datetime import datetime

    while True:
        texto = input(f"Data ({TEXTO_FORMATO_DATA}, Enter para cancelar): ").strip()
        if not texto:
            return None
        try:
            datetime.strptime(texto, FORMATO_DATA)
        except ValueError:
            print(f"Data inválida. Usa o formato {TEXTO_FORMATO_DATA}.")
            continue
        return texto


def _pedir_tipo():
    """Pede o tipo de rendimento (Salário ou Outro).

    Returns:
        str | None: O tipo escolhido, ou None se o utilizador cancelar com Enter.
    """
    while True:
        escolha = input("Tipo (1 - Salário, 2 - Outro, Enter para cancelar): ").strip()
        if not escolha:
            return None
        if escolha in TIPOS:
            return TIPOS[escolha]
        print("Opção inválida. Escreve 1 ou 2.")


def registar_rendimento():
    """Pede os dados ao utilizador e regista um novo rendimento.

    Guarda o rendimento na chave "rendimentos" do ficheiro de dados, com os
    campos id, descricao, valor, data e tipo. Em qualquer pergunta, Enter
    sem escrever nada cancela a operação.
    """
    descricao = input("Descrição (ex.: Salário de novembro, Enter para cancelar): ").strip()
    if not descricao:
        print("Operação cancelada.")
        return

    valor = _pedir_valor()
    if valor is None:
        print("Operação cancelada.")
        return

    data = _pedir_data()
    if data is None:
        print("Operação cancelada.")
        return

    tipo = _pedir_tipo()
    if tipo is None:
        print("Operação cancelada.")
        return

    d = dados.carregar()
    d["rendimentos"].append({
        "id": dados.proximo_id(d["rendimentos"]),
        "descricao": descricao,
        "valor": valor,
        "data": data,
        "tipo": tipo,
    })
    dados.guardar(d)
    print(f"Rendimento '{descricao}' registado com sucesso.")


def listar_rendimentos():
    """Mostra na consola todos os rendimentos registados."""
    lista = dados.carregar()["rendimentos"]
    if not lista:
        print("Ainda não existem rendimentos registados.")
        return

    print(f"{'ID':<4}{'Data':<12}{'Descrição':<25}{'Tipo':<9}{'Valor':>10}")
    print("-" * 60)
    for r in lista:
        print(f"{r['id']:<4}{r['data']:<12}{r['descricao']:<25}{r['tipo']:<9}{r['valor']:>9.2f}€")



def _escolher_rendimento(d):
    """Pede um id ao utilizador e devolve o rendimento correspondente.

    Args:
        d (dict): Dicionário completo de dados.

    Returns:
        dict | None: O rendimento escolhido, ou None se o utilizador
        cancelar ou o id não existir.
    """
    texto = input("Id do rendimento (Enter para cancelar): ").strip()
    if not texto:
        print("Operação cancelada.")
        return None
    if not texto.isdigit():
        print("Id inválido.")
        return None
    for r in d["rendimentos"]:
        if r["id"] == int(texto):
            return r
    print("Não existe nenhum rendimento com esse id.")
    return None


def alterar_rendimento():
    """Altera a descrição, o valor, a data ou o tipo de um rendimento.

    O utilizador escolhe o rendimento pelo id e depois o campo a alterar.
    Enter sem escrever nada cancela a alteração.
    """
    d = dados.carregar()
    if not d["rendimentos"]:
        print("Ainda não existem rendimentos registados.")
        return

    listar_rendimentos()
    r = _escolher_rendimento(d)
    if r is None:
        return

    print("\nO que queres alterar?")
    print("1 - Descrição")
    print("2 - Valor")
    print("3 - Data")
    print("4 - Tipo")
    print("0 - Cancelar")
    campo = input("Escolhe uma opção: ").strip()

    if campo == "1":
        chave = "descricao"
        novo = input(f"Nova descrição (atual: {r['descricao']}, Enter para cancelar): ").strip()
    elif campo == "2":
        chave = "valor"
        novo = _pedir_valor()
    elif campo == "3":
        chave = "data"
        novo = _pedir_data()
    elif campo == "4":
        chave = "tipo"
        novo = _pedir_tipo()
    elif campo == "0":
        print("Operação cancelada.")
        return
    else:
        print("Opção inválida.")
        return

    if not novo:
        print("Operação cancelada.")
        return

    r[chave] = novo
    dados.guardar(d)
    print("Rendimento alterado com sucesso.")


def eliminar_rendimento():
    """Elimina um rendimento escolhido pelo id, depois de pedir confirmação."""
    d = dados.carregar()
    if not d["rendimentos"]:
        print("Ainda não existem rendimentos registados.")
        return

    listar_rendimentos()
    r = _escolher_rendimento(d)
    if r is None:
        return

    if not confirmar(f"Eliminar '{r['descricao']}' ({r['valor']:.2f}€)?"):
        print("Operação cancelada.")
        return

    d["rendimentos"].remove(r)
    dados.guardar(d)
    print("Rendimento eliminado.")


def menu_rendimentos():
    """Mostra o submenu de rendimentos e executa a opção escolhida."""
    while True:
        print("\n*** RENDIMENTOS ***")
        print("1. Registar rendimento")
        print("2. Listar rendimentos")
        print("3. Alterar rendimento")
        print("4. Eliminar rendimento")
        print("0. Voltar")

        opcao = input("Escolhe uma opção: ").strip()

        if opcao == "1":
            registar_rendimento()
        elif opcao == "2":
            listar_rendimentos()
        elif opcao == "3":
            alterar_rendimento()
        elif opcao == "4":
            eliminar_rendimento()
        elif opcao == "0":
            break
        else:
            print("Opção inválida. Escolhe 1, 2, 3, 4 ou 0.")