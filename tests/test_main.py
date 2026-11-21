"""Testes da saída do menu principal."""

import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

import main

DADOS_VAZIOS = {"despesas": [], "rendimentos": []}


class TestSair(unittest.TestCase):
    def executar(self, respostas):
        """Corre main.main() com respostas simuladas e devolve o texto mostrado."""
        with patch("main.login.fazer_login", return_value=True), \
                patch("main.dados.carregar", return_value=DADOS_VAZIOS), \
                patch("builtins.input", side_effect=respostas), \
                redirect_stdout(io.StringIO()) as saida:
            main.main()
        return saida.getvalue()
        
    def test_sair_confirmado(self):
        texto = self.executar(["0", "s"])
        self.assertIn("Até à próxima", texto)

    def test_sair_nao_confirmado_volta_ao_menu(self):
        texto = self.executar(["0", "n", "0", "s"])
        self.assertEqual(texto.count("GESTÃO DE DESPESAS PESSOAIS"), 2)

    def test_opcao_com_espacos(self):
        texto = self.executar([" 0 ", "s"])
        self.assertIn("Até à próxima", texto)

    def test_confirmar_saida(self):
        with patch("builtins.input", return_value="s"):
            self.assertTrue(main.confirmar_saida())
        with patch("builtins.input", return_value="n"):
            self.assertFalse(main.confirmar_saida())


if __name__ == "__main__":
    unittest.main()