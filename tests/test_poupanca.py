"""Testes do módulo poupanca."""

import unittest

from src import poupanca


class TestCalcularPoupado(unittest.TestCase):
    """Testes de calcular_poupado."""

    def test_rendimentos_maiores_que_despesas(self):
        d = {
            "rendimentos": [{"valor": 900}],
            "despesas": [{"valor": 23.5}, {"valor": 40}],
        }
        self.assertAlmostEqual(poupanca.calcular_poupado(d), 836.5)

    def test_varios_rendimentos(self):
        d = {
            "rendimentos": [{"valor": 900}, {"valor": 100}],
            "despesas": [{"valor": 250}],
        }
        self.assertAlmostEqual(poupanca.calcular_poupado(d), 750)

    def test_despesas_maiores_que_rendimentos(self):
        # o resultado pode ser negativo (gastou mais do que recebeu)
        d = {
            "rendimentos": [{"valor": 100}],
            "despesas": [{"valor": 150.5}],
        }
        self.assertAlmostEqual(poupanca.calcular_poupado(d), -50.5)

    def test_sem_despesas(self):
        d = {"rendimentos": [{"valor": 500}], "despesas": []}
        self.assertAlmostEqual(poupanca.calcular_poupado(d), 500)

    def test_sem_rendimentos(self):
        d = {"rendimentos": [], "despesas": [{"valor": 30}]}
        self.assertAlmostEqual(poupanca.calcular_poupado(d), -30)

    def test_tudo_vazio(self):
        d = {"rendimentos": [], "despesas": []}
        self.assertEqual(poupanca.calcular_poupado(d), 0)


if __name__ == "__main__":
    unittest.main()
    