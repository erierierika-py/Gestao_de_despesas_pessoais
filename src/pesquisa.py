"""Módulo de pesquisa: procurar, filtrar e resumir despesas."""

from datetime import datetime

from src import dados
from src.saldo import mes_da_data

def pesquisar_por_descricao(despesas, texto):
    """Devolve as despesas cuja descrição contém o texto indicado.
    A pesquisa não distingue maiúsculas de minúsculas.

    Args:
        despesas: Lista de despesas.
        texto: Texto a procurar na descrição.

    Returns:
        list: Despesas que contêm o texto (pode ser uma lista vazia).
    """
    texto = texto.strip().lower()
    return [x for x in despesas if texto in x["descricao"].lower()]


def mostrar_despesas(lista):
    """Mostra uma tabela com as despesas recebidas.

    Args:
        lista: Despesas a mostrar (cada uma com id, descricao,
            valor, categoria e data).
    """
    if not lista:
        print("Não há despesas para mostrar.")
        return

    print(f"{'ID':<4}{'Descrição':<22}{'Valor':>9}  {'Categoria':<15}{'Data':<10}")
    print("-" * 60)
    for x in lista:
        print(
            f"{x['id']:<4}{x['descricao']:<22}{x['valor']:>8.2f}€  "
            f"{x['categoria']:<15}{x['data']:<10}"
        )
    print("-" * 60)

def menu_pesquisar():
    """Pede um texto ao utilizador e mostra as despesas que o contêm na descrição.

    Se o texto estiver vazio, a operação é cancelada. Se não houver
    resultados, avisa o utilizador.
    """
    d = dados.carregar()

    if not d["despesas"]:
        print("Ainda não existem despesas registadas.")
        return

    texto = input("Pesquisar na descrição (Enter para cancelar): ").strip()
    if not texto:
        print("Pesquisa cancelada.")
        return

    resultados = pesquisar_por_descricao(d["despesas"], texto)

    if not resultados:
        print(f"Nenhuma despesa encontrada com '{texto}'.")
        return

    print(f"\n{len(resultados)} resultado(s) para '{texto}':")

    mostrar_despesas(resultados)


def filtrar_por_categoria(despesas, categoria):
    """Devolve as despesas que pertencem à categoria indicada.

    A comparação não distingue maiúsculas de minúsculas.

    Args:
        despesas (list[dict]): Lista de despesas.
        categoria (str): Nome da categoria a filtrar.

    Returns:
        list[dict]: Despesas dessa categoria (pode ser uma lista vazia).
    """
    categoria = categoria.strip().lower()
    return [x for x in despesas if x["categoria"].lower() == categoria]


def menu_filtrar():
    """Mostra as categorias, pede uma escolha e lista as despesas dessa categoria.

    No fim mostra o total gasto na categoria. Se a escolha for inválida
    ou a categoria não tiver despesas, avisa o utilizador.
    """
    d = dados.carregar()

    if not d["categorias"]:
        print("Ainda não existem categorias registadas.")
        return

    print("Categorias:")
    for i, nome in enumerate(d["categorias"], start=1):
        print(f"  {i}. {nome}")

    escolha = input("Número da categoria (Enter para cancelar): ").strip()
    if not escolha:
        print("Operação cancelada.")
        return
    if not escolha.isdigit() or not (1 <= int(escolha) <= len(d["categorias"])):
        print("Escolha inválida.")
        return

    categoria = d["categorias"][int(escolha) - 1]
    resultados = filtrar_por_categoria(d["despesas"], categoria)

    if not resultados:
        print(f"Não há despesas na categoria '{categoria}'.")
        return

    print(f"\nDespesas em '{categoria}':")
    mostrar_despesas(resultados)
    total = sum(x["valor"] for x in resultados)
    print(f"Total gasto em '{categoria}': {total:.2f}€")


def gasto_por_categoria(despesas):
    """Soma as despesas de cada categoria.

    Args:
        despesas (list[dict]): Lista de despesas.

    Returns:
        dict: Categoria -> total gasto, ordenado da categoria com mais
            gastos para a com menos.
    """
    totais = {}
    for x in despesas:
        categoria = x["categoria"]
        totais[categoria] = totais.get(categoria, 0) + x["valor"]

    def total_do_par(par):
        """Devolve o total de um par (categoria, total), para ordenar."""
        return par[1]

    ordenado = sorted(totais.items(), key=total_do_par, reverse=True)
    return dict(ordenado)

def filtrar_por_mes(despesas, mes):
    """Devolve as despesas de um mês, aceitando os dois formatos de data.

    Args:
        despesas (list[dict]): Lista de despesas.
        mes (str): Mês no formato AAAA-MM.

    Returns:
        list[dict]: Despesas desse mês (pode ser uma lista vazia).
    """
    return [x for x in despesas if mes_da_data(x["data"]) == mes]


def categorias_disponiveis(d):
    """Junta as categorias registadas com as usadas nas despesas.

    Não repete categorias que só diferem nas maiúsculas.

    Args:
        d (dict): Dicionário completo de dados.

    Returns:
        list[str]: Categorias por ordem alfabética.
    """
    vistas = {}
    nomes = list(d["categorias"]) + [x["categoria"] for x in d["despesas"]]
    for nome in nomes:
        vistas.setdefault(nome.strip().lower(), nome.strip())
    return sorted(vistas.values(), key=str.lower)

def menu_gasto_categoria():
    """Mostra o gasto por categoria, com valor e percentagem do total.

    Pergunta ao utilizador se quer ver um mês específico (AAAA-MM)
    ou todos. Se não houver despesas, avisa.
    """
    d = dados.carregar()

    if not d["despesas"]:
        print("Ainda não existem despesas registadas.")
        return

    mes = input("Mês (AAAA-MM) ou Enter para ver todos: ").strip()

    if mes:
        despesas = [x for x in d["despesas"] if x["data"].startswith(mes)]
        titulo = f"Gasto por categoria em {mes}"
    else:
        despesas = d["despesas"]
        titulo = "Gasto por categoria (todos os meses)"

    if not despesas:
        print(f"Não há despesas para '{mes}'.")
        return

    totais = gasto_por_categoria(despesas)
    total_geral = sum(totais.values())

    print(f"\n{titulo}")
    print("-" * 44)
    for categoria, valor in totais.items():
        percentagem = valor / total_geral * 100
        print(f"{categoria:<18}{valor:>9.2f}€  {percentagem:>6.1f}%")
    print("-" * 44)
    print(f"{'Total':<18}{total_geral:>9.2f}€")