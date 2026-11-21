"""Módulo de login: criar e verificar a palavra-passe da aplicação."""

import getpass
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


def criar_palavra_passe():
    """Pede ao utilizador para criar uma palavra-passe e guarda-a (só o hash).

    A palavra-passe tem de ter pelo menos 4 caracteres e tem de ser
    confirmada. Se o utilizador carregar em Enter sem escrever nada,
    a operação é cancelada.

    Returns:
        bool: True se a palavra-passe foi criada, False se foi cancelada.
    """
    print("Ainda não existe palavra-passe. Vamos criar uma.")

    while True:
        nova_pw = getpass.getpass("Nova palavra-passe (Enter para cancelar): ")
        if not nova_pw:
            print("Operação cancelada.")
            return False
        if len(nova_pw) < 4:
            print("A palavra-passe tem de ter pelo menos 4 caracteres.")
            continue

# getpass funciona como o input, mas não mostra o que é escrito no ecrã
        confirmacao = getpass.getpass("Confirma a palavra-passe: ")
        if confirmacao != nova_pw:
            print("As palavras-passe não coincidem. Tenta outra vez.")
            continue
        break

    d = dados.carregar()
    salt = gerar_salt()
    d["login"] = {"salt": salt, "hash": gerar_hash(nova_pw, salt)}
    dados.guardar(d)
    print("Palavra-passe criada com sucesso.")
    return True


max_tentativas = 3

def fazer_login():
    """Faz o login do utilizador no arranque da aplicação.

    Na primeira execução (sem palavra-passe guardada), pede para criar uma.
    Nas seguintes, pede a palavra-passe com um máximo de 3 tentativas.

    Returns:
        bool: True se o utilizador pode entrar, False caso contrário.
    """
    d = dados.carregar()
    guardado = d.get("login")

    if not guardado or "hash" not in guardado:
        return criar_palavra_passe()

    for tentativa in range(1, max_tentativas + 1):
        escrita = getpass.getpass("Palavra-passe: ")
        if verificar_palavra_passe(escrita, d):
            print("Login efetuado com sucesso.")
            return True
        restantes = max_tentativas - tentativa
        if restantes > 0:
            print(f"Palavra-passe incorreta. Restam {restantes} tentativa(s).")

    print("Demasiadas tentativas falhadas. A aplicação vai fechar.")
    return False