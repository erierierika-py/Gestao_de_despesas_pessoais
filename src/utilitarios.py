"""Funções utilitárias partilhadas por toda a aplicação."""


def confirmar(pergunta):
    """Pede confirmação ao utilizador antes de uma ação irreversível.

    Args:
        pergunta (str): Texto da pergunta a apresentar.

    Returns:
        bool: True se o utilizador responder 's' ou 'sim' (em maiúsculas
        ou minúsculas); False em qualquer outro caso.

    Exemplo:
        >>> if confirmar("Apagar este registo?"):
        ...     apagar()
    """
    resposta = input(f"{pergunta} (s/n): ").strip().lower()
    return resposta in ("s", "sim")