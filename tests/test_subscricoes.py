"""Testes do módulo subscricoes."""

import unittest

from src import subscricoes


class TestTotalMensal(unittest.TestCase):
    """Testes de total_mensal."""

    def test_varias_subscricoes(self):
        lista = [
            {"nome": "Netflix", "valor": 12.99},
            {"nome": "Ginásio", "valor": 30},
            {"nome": "Spotify", "valor": 6.99},
        ]
        self.assertAlmostEqual(subscricoes.total_mensal(lista), 49.98)

    def test_uma_subscricao(self):
        lista = [{"nome": "Netflix", "valor": 12.99}]
        self.assertAlmostEqual(subscricoes.total_mensal(lista), 12.99)

    def test_lista_vazia(self):
        self.assertEqual(subscricoes.total_mensal([]), 0)

    def test_valores_inteiros(self):
        lista = [{"valor": 10}, {"valor": 20}]
        self.assertEqual(subscricoes.total_mensal(lista), 30)


if __name__ == "__main__":
    unittest.main()
    