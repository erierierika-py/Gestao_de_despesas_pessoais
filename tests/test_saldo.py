"""Testes dos cálculos de saldo."""

import unittest

from src.saldo import mes_da_data, resumo_mensal, resumo_de_um_mes

RENDIMENTOS = [{"valor": 1200, "data": "2026-10-05"},
               {"valor": 1200, "data": "2026-11-05"}]
DESPESAS = [{"valor": 50, "data": "10-10-2026"},
            {"valor": 100, "data": "20-10-2026"},
            {"valor": 30, "data": "02-11-2026"}]


class TestSaldo(unittest.TestCase):
    def test_mes_da_data_dois_formatos(self):
        self.assertEqual(mes_da_data("2026-11-05"), "2026-11")
        self.assertEqual(mes_da_data("05-11-2026"), "2026-11")

    def test_mes_da_data_invalida(self):
        self.assertIsNone(mes_da_data("abc"))

    def test_resumo_mensal(self):
        resumo = resumo_mensal(RENDIMENTOS, DESPESAS)
        self.assertEqual(len(resumo), 2)
        self.assertEqual(resumo[0]["mes"], "2026-10")
        self.assertEqual(resumo[0]["saldo"], 1050)
        self.assertEqual(resumo[1]["saldo"], 1170)

    def test_mes_sem_registos(self):
        linha = resumo_de_um_mes(RENDIMENTOS, DESPESAS, "2025-01")
        self.assertEqual(linha["saldo"], 0.0)

    def test_formato_dd_mm_aaaa(self):
        despesas = [{"valor": 10, "data": "05-11-2026"}]
        resumo = resumo_mensal([], despesas)
        self.assertEqual(resumo[0]["mes"], "2026-11")


if __name__ == "__main__":
    unittest.main()