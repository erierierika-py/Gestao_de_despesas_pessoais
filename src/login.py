"""Módulo de login: criar e verificar a palavra-passe da aplicação."""

import hashlib
import secrets #secrets e n random por segurança

from src import dados


def gerar_salt():
    """Gera um salt aleatório (texto) para juntar à palavra-passe.

    Devolve:
        str: Salt com 32 caracteres hexadecimais.
    """
    return secrets.token_hex(16)


def gerar_hash(palavra_passe, salt):
    """Calcula o hash SHA-256 da palavra-passe junto com o salt.

    Args:
        palavra_passe (str): Palavra-passe em texto.
        salt (str): Texto aleatório que torna o hash único.

    Returns:
        str: Hash em hexadecimal (64 caracteres).
    """
    texto = salt + palavra_passe
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()
# hashlib transforma qualquer texto num código de 64 caract.