"""Módulo de pesquisa: procurar, filtrar e resumir despesas."""

from src import dados

def pesquisar_por_descricao(despesas, texto):
    """Devolve as despesas cuja descrição contém o texto indicado.
    A pesquisa não distingue maiúsculas de minúsculas.

    Args:
        despesas: Lista de despesas.
        texto: Texto a procurar na descrição.

    Devolve:
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

    Devolve:
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
