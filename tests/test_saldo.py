"""Testes dos cálculos de saldo."""

import io
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from datetime import datetime
from unittest.mock import patch

from src import dados, saldo
from src.saldo import mes_da_data, resumo_mensal, resumo_de_um_mes, estado_saldo

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

    def test_estado_saldo(self):
        self.assertEqual(estado_saldo(1000, -5), "negativo")
        self.assertEqual(estado_saldo(1000, 150), "baixo")
        self.assertEqual(estado_saldo(1000, 500), "ok")
        self.assertEqual(estado_saldo(0, 0), "ok")

class TestLimiteMensal(unittest.TestCase):
    """Testes do limite de gastos mensal (com um ficheiro temporário)."""

    def setUp(self):
        self.pasta = tempfile.TemporaryDirectory()
        caminho = os.path.join(self.pasta.name, "dados.json")
        self.patcher = patch.object(dados, "ficheiro", caminho)
        self.patcher.start()

    def tearDown(self):
        self.patcher.stop()
        self.pasta.cleanup()

    def definir(self, respostas):
        """Corre definir_limite_mensal com respostas simuladas."""
        with patch("builtins.input", side_effect=respostas), \
                redirect_stdout(io.StringIO()):
            saldo.definir_limite_mensal()

    def test_definir_limite(self):
        self.definir(["500,50"])
        self.assertEqual(dados.carregar()["orcamento"]["limite_mensal"], 500.5)

    def test_valores_invalidos_repetem_a_pergunta(self):
        self.definir(["abc", "nan", "inf", "-5", "0", "300"])
        self.assertEqual(dados.carregar()["orcamento"]["limite_mensal"], 300.0)

    def test_enter_cancela(self):
        self.definir([""])
        self.assertEqual(dados.carregar()["orcamento"]["limite_mensal"], 0)

    def test_aviso_quando_ultrapassa(self):
        hoje = datetime.now().strftime("%Y-%m-%d")
        d = dados.carregar()
        d["orcamento"]["limite_mensal"] = 100
        d["despesas"].append({"id": 1, "descricao": "x", "valor": 120,
                              "categoria": "y", "data": hoje})
        dados.guardar(d)
        with redirect_stdout(io.StringIO()) as saida:
            saldo.mostrar_limite_restante()
        self.assertIn("Atingiste ou ultrapassaste", saida.getvalue())

if __name__ == "__main__":
    unittest.main()