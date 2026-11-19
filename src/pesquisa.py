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