"""Módulo partilhado para ler e guardar os dados da aplicação em JSON."""

import json
import os

ficheiro = os.path.join("data", "dados.json")

dados_iniciais = {
    "categorias": [],
    "despesas": [],
    "rendimentos": [],
    "orcamento": {"limite_mensal": 0},
    "poupanca": {"objetivo": 0},
    "subscricoes": [],
    "login": {},
}


def carregar():
    """Lê os dados do ficheiro JSON.

    Se o ficheiro não existir ou estiver corrompido, devolve a estrutura inicial vazia.

    Returns:
        dict: Todos os dados da aplicação.
    """
    if not os.path.exists(ficheiro):
        return json.loads(json.dumps(dados_iniciais))
    try:
        with open(ficheiro, "r", encoding="utf-8") as f:
            dados = json.load(f)
    except (json.JSONDecodeError, OSError):
        return json.loads(json.dumps(dados_iniciais))
    # garante que todas as chaves existem
    for chave, valor in dados_iniciais.items():
        dados.setdefault(chave, valor)
    return dados


def guardar(dados):
    """Guarda os dados no ficheiro JSON.

    Args:
        dados (dict): Estrutura completa a guardar.
    """
    os.makedirs(os.path.dirname(ficheiro), exist_ok=True)
    with open(ficheiro, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)


def proximo_id(lista):
    """Devolve o próximo id livre para uma lista de dicionários com campo 'id'."""
    return max((item["id"] for item in lista), default=0) + 1