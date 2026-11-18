"""Módulo de ajuda: mostra instruções de utilização da aplicação."""

largura = 70

seccoes = {
    "Despesas": [
        "Registar despesa: pede descrição, valor, categoria e data.",
        "Editar/apagar despesa: escolhido pelo id; para ser apagado pede confirmação.",
        "Pesquisar: procura pela descrição (não distingue maiúsculas).",
        "Filtrar: mostra só as despesas de uma categoria.",
        "Gasto por categoria: total e percentagem de cada categoria.",
    ],
    "Rendimentos e saldo": [
        "Registar/alterar/eliminar rendimentos.",
        "Saldo: diferença entre rendimentos e despesas, por mês.",
        "Histórico: resumo mês a mês.",
    ],
    "Orçamento e poupança": [
        "Limite mensal: define o máximo que queres gastar por mês.",
        "Avisos: a aplicação avisa quando estás perto do limite.",
        "Objetivo de poupança: define uma meta e vê o progresso.",
        "Subscrições: pagamentos regulares (Netflix, ginásio...).",
    ],
    "Dados": [
        "Exportar: gera um resumo em ficheiro CSV.",
        "Backup: guarda uma cópia dos dados na pasta backups/.",
        "Restaurar: volta a uma cópia anterior (pede confirmação).",
    ],
    "Formatos aceites": [
        "Data: AAAA-MM-DD (exemplo: 2026-11-18).",
        "Valor: número maior que 0, com ponto ou vírgula (12.50 ou 12,50).",
        "Para cancelar uma operação, carrega em Enter sem escrever nada.",
    ],
}


def _linha_separadora(caracter="-"):
    """Devolve uma linha de separação com a largura definida."""
    return caracter * largura


def mostrar_ajuda():
    """Mostra na consola as instruções de utilização, por secções."""
    print(_linha_separadora("="))
    print(" *** AJUDA - GESTOR DE DESPESAS *** ".center(largura))
    print(_linha_separadora("="))

    for titulo, linhas in seccoes.items():
        print(f"\n{titulo.upper()}")
        print(_linha_separadora())
        for linha in linhas:
            print(f"  - {linha}")

    print()
    input("Carrega em Enter para voltar ao menu...")
