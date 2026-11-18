"""Testes do registo de rendimentos."""

import unittest
from unittest.mock import patch

from src import rendimentos


class TestRegistarRendimento(unittest.TestCase):
    def test_registar_valido(self):
        base = {"rendimentos": []}
        respostas = ["Salário de novembro", "850,50", "2026-11-05", "1"]
        with patch("builtins.input", side_effect=respostas), \
                patch("src.rendimentos.dados.carregar", return_value=base), \
                patch("src.rendimentos.dados.guardar") as guardar:
            rendimentos.registar_rendimento()
        guardar.assert_called_once()
        r = base["rendimentos"][0]
        self.assertEqual(r["id"], 1)
        self.assertEqual(r["valor"], 850.50)
        self.assertEqual(r["tipo"], "Salário")

    def test_valor_invalido_repete_pergunta(self):
        base = {"rendimentos": []}
        respostas = ["Extra", "abc", "-5", "100", "2026-11-05", "2"]
        with patch("builtins.input", side_effect=respostas), \
                patch("src.rendimentos.dados.carregar", return_value=base), \
                patch("src.rendimentos.dados.guardar"):
            rendimentos.registar_rendimento()
        self.assertEqual(base["rendimentos"][0]["valor"], 100.0)

    def test_cancelar_nao_guarda(self):
        with patch("builtins.input", return_value=""), \
                patch("src.rendimentos.dados.guardar") as guardar:
            rendimentos.registar_rendimento()
        guardar.assert_not_called()


if __name__ == "__main__":
    unittest.main()