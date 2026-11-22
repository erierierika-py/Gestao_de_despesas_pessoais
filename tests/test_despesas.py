"""Testes do módulo despesas."""

import io
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from src import dados, despesas


class TestDespesas(unittest.TestCase):
    def setUp(self):
        self.pasta = tempfile.TemporaryDirectory()
        caminho = os.path.join(self.pasta.name, "dados.json")
        self.patcher = patch.object(dados, "ficheiro", caminho)
        self.patcher.start()

    def tearDown(self):
        self.patcher.stop()
        self.pasta.cleanup()

    def correr(self, funcao, respostas):
        """Corre uma função com respostas simuladas, sem mostrar o texto."""
        with patch("builtins.input", side_effect=respostas), \
                redirect_stdout(io.StringIO()):
            funcao()

    def test_adicionar_valida(self):
        self.correr(despesas.adicionar_despesa,
                    ["Pingo Doce", "23,50", "Alimentação", "2026-11-10"])
        lista = dados.carregar()["despesas"]
        self.assertEqual(len(lista), 1)
        self.assertEqual(lista[0]["valor"], 23.5)

    def test_data_invalida_repete(self):
        self.correr(despesas.adicionar_despesa,
                    ["Cinema", "8", "Lazer", "abc", "", "2026-11-10"])
        self.assertEqual(dados.carregar()["despesas"][0]["data"], "2026-11-10")

    def test_valores_invalidos_repetem(self):
        self.correr(despesas.adicionar_despesa,
                    ["Passe", "abc", "nan", "inf", "-1", "40",
                     "Transportes", "2026-11-12"])
        self.assertEqual(dados.carregar()["despesas"][0]["valor"], 40.0)

    def test_eliminar_pede_confirmacao(self):
        self.correr(despesas.adicionar_despesa,
                    ["X", "5", "Y", "2026-11-10"])
        self.correr(despesas.eliminar_despesa, ["1", "n"])
        self.assertEqual(len(dados.carregar()["despesas"]), 1)
        self.correr(despesas.eliminar_despesa, ["1", "s"])
        self.assertEqual(dados.carregar()["despesas"], [])


if __name__ == "__main__":
    unittest.main()