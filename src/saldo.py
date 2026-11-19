"""Cálculos de saldo, totais mensais e histórico financeiro."""

from datetime import datetime
from src import dados
from src.poupanca import calcular_poupado

# Aceita os dois formatos usados no grupo, até se decidir um só.
FORMATOS_DATA = ("%Y-%m-%d", "%d-%m-%Y")


def mes_da_data(texto):
    """Extrai o mês (AAAA-MM) de uma data escrita num dos formatos aceites.

    Args:
        texto (str): Data, por exemplo '2026-11-05' ou '05-11-2026'.

    Returns:
        str | None: O mês no formato AAAA-MM, ou None se a data for inválida.
    """
    for formato in FORMATOS_DATA:
        try:
            return datetime.strptime(texto, formato).strftime("%Y-%m")
        except ValueError:
            continue
    return None


def total_por_mes(registos):
    """Soma os valores dos registos agrupados por mês.

    Registos com data inválida são ignorados.

    Args:
        registos (list[dict]): Registos com as chaves 'valor' e 'data'.

    Returns:
        dict[str, float]: Total por mês, por exemplo {'2026-11': 850.5}.
    """
    totais = {}
    for registo in registos:
        mes = mes_da_data(registo["data"])
        if mes is None:
            continue
        totais[mes] = totais.get(mes, 0.0) + float(registo["valor"])
    return totais


def resumo_mensal(rendimentos, despesas):
    """Calcula rendimentos, despesas e saldo de cada mês.

    Args:
        rendimentos (list[dict]): Lista de rendimentos.
        despesas (list[dict]): Lista de despesas.

    Returns:
        list[dict]: Um dicionário por mês, por ordem cronológica, com as
        chaves 'mes', 'rendimentos', 'despesas' e 'saldo'.
    """
    rend = total_por_mes(rendimentos)
    desp = total_por_mes(despesas)
    resumo = []
    for mes in sorted(set(rend) | set(desp)):
        r = rend.get(mes, 0.0)
        d = desp.get(mes, 0.0)
        resumo.append({"mes": mes, "rendimentos": r,
                       "despesas": d, "saldo": r - d})
    return resumo


def resumo_de_um_mes(rendimentos, despesas, mes):
    """Devolve o resumo de um mês específico.

    Args:
        rendimentos (list[dict]): Lista de rendimentos.
        despesas (list[dict]): Lista de despesas.
        mes (str): Mês no formato AAAA-MM.

    Returns:
        dict: Resumo do mês; com zeros se não houver registos.
    """
    for linha in resumo_mensal(rendimentos, despesas):
        if linha["mes"] == mes:
            return linha
    return {"mes": mes, "rendimentos": 0.0, "despesas": 0.0, "saldo": 0.0}


def consultar_resumo_mensal():
    """Pede um mês ao utilizador e mostra rendimentos, despesas e saldo.

    Enter sem escrever nada cancela a operação.
    """
    while True:
        mes = input("Mês (AAAA-MM, Enter para cancelar): ").strip()
        if not mes:
            print("Operação cancelada.")
            return
        try:
            datetime.strptime(mes, "%Y-%m")
            break
        except ValueError:
            print("Formato inválido. Exemplo: 2026-11")

    base = dados.carregar()
    linha = resumo_de_um_mes(base["rendimentos"], base["despesas"], mes)
    print(f"\nResumo de {mes}")
    print(f"Rendimentos: {linha['rendimentos']:.2f}€")
    print(f"Despesas:    {linha['despesas']:.2f}€")
    print(f"Saldo:       {linha['saldo']:.2f}€")
    if linha["saldo"] < 0:
        print("Atenção: o saldo deste mês é negativo.")


def mostrar_saldo_total():
    """Mostra o saldo total (rendimentos menos despesas de todos os meses).

    Usa poupanca.calcular_poupado para não duplicar o cálculo.
    """
    base = dados.carregar()
    saldo = calcular_poupado(base)
    print(f"\nSaldo disponível: {saldo:.2f}€")
    if saldo < 0:
        print("Atenção: gastaste mais do que recebeste.")


def mostrar_historico():
    """Mostra uma linha por mês com rendimentos, despesas e saldo."""
    base = dados.carregar()
    resumo = resumo_mensal(base["rendimentos"], base["despesas"])
    if not resumo:
        print("Ainda não existem registos para mostrar.")
        return

    print(f"\n{'Mês':<9}{'Rendimentos':>13}{'Despesas':>11}{'Saldo':>11}")
    print("-" * 44)
    for linha in resumo:
        print(f"{linha['mes']:<9}{linha['rendimentos']:>12.2f}€"
              f"{linha['despesas']:>10.2f}€{linha['saldo']:>10.2f}€")


def menu_saldo():
    """Mostra o submenu de saldo e histórico e executa a opção escolhida."""
    while True:
        print("\n*** SALDO E HISTÓRICO ***")
        print("1. Saldo total")
        print("2. Resumo de um mês")
        print("3. Histórico mês a mês")
        print("0. Voltar")

        opcao = input("Escolhe uma opção: ").strip()

        if opcao == "1":
            mostrar_saldo_total()
        elif opcao == "2":
            consultar_resumo_mensal()
        elif opcao == "3":
            mostrar_historico()
        elif opcao == "0":
            break
        else:
            print("Opção inválida. Escolhe 1, 2, 3 ou 0.")