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


def verificar_palavra_passe(palavra_passe, d):
    """Verifica se a palavra-passe corresponde à que está guardada.

    Args:
        palavra_passe (str): Palavra-passe escrita pelo utilizador.
        d (dict): Dicionário completo de dados (resultado de dados.carregar()).

    Returns:
        bool: True se corresponder, False se não corresponder ou se
            ainda não existir palavra-passe guardada.
    """
    guardado = d.get("login")
    if not guardado or "salt" not in guardado or "hash" not in guardado:
        return False

    hash_escrito = gerar_hash(palavra_passe, guardado["salt"])
    return secrets.compare_digest(hash_escrito, guardado["hash"])