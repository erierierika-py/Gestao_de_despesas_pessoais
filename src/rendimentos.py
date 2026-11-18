"""Módulo de rendimentos: registar e listar rendimentos (salários e outros)."""

from src import dados

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