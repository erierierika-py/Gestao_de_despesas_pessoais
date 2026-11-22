
"""Cálculos de saldo, totais mensais e histórico financeiro."""

from datetime import datetime
from src import dados
from src.poupanca import calcular_poupado

# Aceita os dois formatos usados no grupo
FORMATOS_DATA = ("%Y-%m-%d", "%d-%m-%Y")
LIMITE_AVISO = 0.20  # avisa quando resta menos de 20% do que se recebeu
PERTO_DO_LIMITE = 0.8  # avisa quando já se gastou 80% do limite mensal

def mes_da_data(texto):
    """Extrai o mês de uma data válida."""

    for formato in FORMATOS_DATA:
        try:
            return datetime.strptime(texto, formato).strftime("%Y-%m")
        except ValueError:
            continue
    return None


def total_por_mes(registos):
    """Calcula o total de registos por mês."""
    totais = {}

    for registo in registos:
        mes = mes_da_data(registo["data"])

        if mes is None:
            continue

        totais[mes] = totais.get(mes, 0.0) + float(registo["valor"])

    return totais


def resumo_mensal(rendimentos, despesas):
    """Calcula rendimentos, despesas e saldo de cada mês."""
    rend = total_por_mes(rendimentos)
    desp = total_por_mes(despesas)
    resumo = []

    for mes in sorted(set(rend) | set(desp)):
        r = rend.get(mes, 0.0)
        d = desp.get(mes, 0.0)

        resumo.append({
            "mes": mes,
            "rendimentos": r,
            "despesas": d,
            "saldo": r - d
        })

    return resumo


def resumo_de_um_mes(rendimentos, despesas, mes):
    """Devolve o resumo de um mês específico."""
    for linha in resumo_mensal(rendimentos, despesas):
        if linha["mes"] == mes:
            return linha

    return {
        "mes": mes,
        "rendimentos": 0.0,
        "despesas": 0.0,
        "saldo": 0.0
    }


def consultar_resumo_mensal():
    """Pede um mês e mostra o respetivo resumo."""
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
    """Mostra o saldo total de todos os registos."""
    base = dados.carregar()
    saldo = calcular_poupado(base)

    print(f"\nSaldo disponível: {saldo:.2f}€")

    if saldo < 0:
        print("Atenção: gastaste mais do que recebeste.")


def mostrar_historico():
     """Mostra o histórico mensal de rendimentos, despesas e saldo."""
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


# Limite de gastos mensal

def definir_limite_mensal():
    """Define o limite mensal de gastos."""
    base = dados.carregar()

    print("\nDefinir Limite Mensal")
    print("Limite atual:", base["orcamento"]["limite_mensal"], "€")

    while True:
        try:
            limite = float(input("Novo limite mensal (€): ").replace(",", "."))

            if limite <= 0:
                print("Erro: O limite tem de ser maior que zero")
            else:
                break

        except ValueError:
            print("Erro: Valor invalido, tenta novamente")

    base["orcamento"]["limite_mensal"] = round(limite, 2)
    dados.guardar(base)

    print("\nLimite mensal guardado com sucesso!")


# Verificar dinheiro restante

def mostrar_limite_restante():
    """Mostra o limite de gastos restante do mês atual."""
    base = dados.carregar()

    limite = base["orcamento"]["limite_mensal"]

    if limite <= 0:
        print("\nAinda não definiste um limite mensal")
        return

    mes_atual = datetime.now().strftime("%Y-%m")

    gastos = total_por_mes(base["despesas"])
    total_gasto = gastos.get(mes_atual, 0)

    restante = limite - total_gasto

    print("\nOrçamento Mensal")
    print("Limite mensal:", f"{limite:.2f}", "€")
    print("Total gasto:", f"{total_gasto:.2f}", "€")
    print("Dinheiro disponível:", f"{restante:.2f}", "€")

    if restante <= 0:
        print("\nAtenção! Atingiste ou ultrapassaste o limite mensal!")

    elif total_gasto >= limite * 0.8:
        print("\nAviso! Estás perto de atingir o limite mensal")


def menu_saldo():
    """Mostra o menu de saldo, histórico e limite mensal."""
    while True:
        print("\n*** SALDO E HISTÓRICO ***")
        print("1. Saldo total")
        print("2. Resumo de um mês")
        print("3. Histórico mês a mês")
        print("4. Definir limite de gastos mensal")
        print("5. Consultar limite restante")
        print("0. Voltar")

        opcao = input("Escolhe uma opção: ").strip()

        if opcao == "1":
            mostrar_saldo_total()

        elif opcao == "2":
            consultar_resumo_mensal()

        elif opcao == "3":
            mostrar_historico()

        elif opcao == "4":
            definir_limite_mensal()

        elif opcao == "5":
            mostrar_limite_restante()

        elif opcao == "0":
            break

        
        else:
            print("Opção inválida. Escolhe 1, 2, 3, 4, 5 ou 0.")


def estado_saldo(total_rendimentos, saldo):
    """Classifica o estado do saldo."""

    if saldo < 0:
        return "negativo"

    if total_rendimentos > 0 and saldo < total_rendimentos * LIMITE_AVISO:
        return "baixo"

    return "ok"


def aviso_saldo_baixo(d):
    """Mostra um aviso se o dinheiro estiver a acabar."""

    saldo = calcular_poupado(d)
    total = sum(r["valor"] for r in d["rendimentos"])

    estado = estado_saldo(total, saldo)

    if estado == "negativo":
        print(f"AVISO: o saldo está negativo ({saldo:.2f}€)!")

    elif estado == "baixo":
        print(f"AVISO: o dinheiro está a acabar! Restam {saldo:.2f}€.")
