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