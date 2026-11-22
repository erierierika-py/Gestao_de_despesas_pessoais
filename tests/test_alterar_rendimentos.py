"""Testes de alterar e eliminar rendimentos."""

import os
import tempfile
import unittest
from unittest.mock import patch

from src import dados, rendimentos


class TestRendimentos(unittest.TestCase):
    def setUp(self):
        self.pasta = tempfile.TemporaryDirectory()
        caminho = os.path.join(self.pasta.name, "dados.json")
        self.patcher = patch.object(dados, "ficheiro", caminho)
        self.patcher.start()
        d = dados.carregar()
        d["rendimentos"].append({"id": 1, "descricao": "Salário", "valor": 850.0,
                                 "data": "2026-11-05", "tipo": "Salário"})
        dados.guardar(d)

    def tearDown(self):
        self.patcher.stop()
        self.pasta.cleanup()

    def test_alterar_valor(self):
        with patch("builtins.input", side_effect=["1", "2", "900"]):
            rendimentos.alterar_rendimento()
        self.assertEqual(dados.carregar()["rendimentos"][0]["valor"], 900.0)

    def test_eliminar_confirmado(self):
        with patch("builtins.input", side_effect=["1", "s"]):
            rendimentos.eliminar_rendimento()
        self.assertEqual(dados.carregar()["rendimentos"], [])

    def test_eliminar_nao_confirmado(self):
        with patch("builtins.input", side_effect=["1", "n"]):
            rendimentos.eliminar_rendimento()
        self.assertEqual(len(dados.carregar()["rendimentos"]), 1)

    def test_id_inexistente(self):
        with patch("builtins.input", side_effect=["99"]):
            rendimentos.eliminar_rendimento()
        self.assertEqual(len(dados.carregar()["rendimentos"]), 1)


if __name__ == "__main__":
    unittest.main()