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