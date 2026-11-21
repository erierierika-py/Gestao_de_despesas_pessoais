"""Módulo de subscrições: pagamentos regulares (Netflix, ginásio, renda...)."""

from src import dados

def _pedir_valor():
    """Pede um valor > 0 ao utilizador. Devolve float ou None se cancelar."""
    while True:
        texto = input("Valor (Enter para cancelar): ").strip().replace(",", ".")
        if not texto:
            return None
        try:
            valor = float(texto)
        except ValueError:
            print("Valor inválido. Escreve um número (ex.: 12.50).")
            continue
        if valor <= 0:
            print("O valor tem de ser maior que 0.")
            continue
        return valor


def _pedir_dia():
    """Pede o dia do mês (1 a 31). Devolve int ou None se cancelar."""
    while True:
        texto = input("Dia do mês do pagamento (1-31, Enter para cancelar): ").strip()
        if not texto:
            return None
        if not texto.isdigit() or not (1 <= int(texto) <= 31):
            print("Dia inválido. Escreve um número entre 1 e 31.")
            continue
        return int(texto)


def adicionar_subscricao():
    """Pede os dados e adiciona uma subscrição ao ficheiro de dados."""
    d = dados.carregar()

    nome = input("Nome da subscrição (Enter para cancelar): ").strip()
    if not nome:
        print("Operação cancelada.")
        return

    valor = _pedir_valor()
    if valor is None:
        print("Operação cancelada.")
        return

    print("Categorias existentes:", ", ".join(d["categorias"]) or "(nenhuma)")
    categoria = input("Categoria: ").strip()
    if not categoria:
        categoria = "Outros"

    dia = _pedir_dia()
    if dia is None:
        print("Operação cancelada.")
        return

    subscricao = {
        "id": dados.proximo_id(d["subscricoes"]),
        "nome": nome,
        "valor": valor,
        "categoria": categoria,
        "dia": dia,
    }
    d["subscricoes"].append(subscricao)
    dados.guardar(d)
    print(f"Subscrição '{nome}' adicionada.")


def total_mensal(subscricoes):
    """Calcula o total mensal das subscrições.

    Args:
        subscricoes (list[dict]): Lista de subscrições.

    Returns:
        float: Soma dos valores.
    """
    return sum(s["valor"] for s in subscricoes)


def listar_subscricoes():
    """Mostra todas as subscrições e o total mensal."""
    d = dados.carregar()
    lista = d["subscricoes"]
    if not lista:
        print("Não existem subscrições registadas.")
        return

    print(f"{'ID':<4}{'Nome':<22}{'Valor':>9}  {'Categoria':<15}{'Dia':>4}")
    print("-" * 56)
    for s in lista:
        print(f"{s['id']:<4}{s['nome']:<22}{s['valor']:>8.2f}€  {s['categoria']:<15}{s['dia']:>4}")
    print("-" * 56)
    print(f"Total mensal: {total_mensal(lista):.2f}€")


def remover_subscricao():
    """Remove uma subscrição escolhida pelo id, com confirmação."""
    d = dados.carregar()
    if not d["subscricoes"]:
        print("Não existem subscrições para remover.")
        return

    listar_subscricoes()
    escolha = input("Id da subscrição a remover (Enter para cancelar): ").strip()
    if not escolha:
        print("Operação cancelada.")
        return
    if not escolha.isdigit():
        print("Id inválido.")
        return

    alvo = next((s for s in d["subscricoes"] if s["id"] == int(escolha)), None)
    if alvo is None:
        print("Não existe nenhuma subscrição com esse id.")
        return

    confirmacao = input(f"Remover '{alvo['nome']}'? (s/n): ").strip().lower()
    if confirmacao != "s":
        print("Operação cancelada.")
        return

    d["subscricoes"].remove(alvo)
    dados.guardar(d)
    print("Subscrição removida.")

