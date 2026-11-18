"""Módulo de backup: criar, listar e restaurar cópias do ficheiro de dados."""

import os
import shutil
from datetime import datetime

from src import dados

pasta_backups = "backups"


def criar_backup():
    """Cria uma cópia do ficheiro de dados na pasta backups/.
    O nome do file inclui a data e a hora.
    Se ainda não existirem dados, mostra mensagem e não faz nada.
    """
    if not os.path.exists(dados.FICHEIRO):
        print("Ainda não existem dados para guardar. Registe algo primeiro.")
        return

    os.makedirs(pasta_backups, exist_ok=True)
    nome = datetime.now().strftime("backup_%Y-%m-%d_%H-%M-%S.json")
    destino = os.path.join(pasta_backups, nome)
    shutil.copy(dados.FICHEIRO, destino)
    print(f"Backup criado em: {destino}")


def listar_backups():
    """Devolve a lista de backups existentes, do mais recente para o mais antigo.
    Devolve:
        list[str]: Nomes dos ficheiros de backup.
    """
    if not os.path.isdir(pasta_backups):
        return []
    ficheiros = [f for f in os.listdir(pasta_backups) if f.endswith(".json")]
    return sorted(ficheiros, reverse=True)


def mostrar_backups():
    """Mostra na consola os backups existentes, numerados."""
    backups = listar_backups()
    if not backups:
        print("Não existem backups.")
        return
    print("Backups existentes:")
    for i, nome in enumerate(backups, start=1):
        print(f"  {i}. {nome}")