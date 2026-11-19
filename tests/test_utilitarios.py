"""Testes da função confirmar."""

import unittest
from unittest.mock import patch

from src.utilitarios import confirmar


class TestConfirmar(unittest.TestCase):
    def test_sim(self):
        with patch("builtins.input", return_value="s"):
            self.assertTrue(confirmar("Apagar?"))

    def test_maiuscula(self):
        with patch("builtins.input", return_value="S"):
            self.assertTrue(confirmar("Apagar?"))

    def test_nao(self):
        with patch("builtins.input", return_value="n"):
            self.assertFalse(confirmar("Apagar?"))

    def test_vazio(self):
        with patch("builtins.input", return_value=""):
            self.assertFalse(confirmar("Apagar?"))


if __name__ == "__main__":
    unittest.main()