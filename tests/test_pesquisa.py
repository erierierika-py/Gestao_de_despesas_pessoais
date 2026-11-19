"""Testes do módulo pesquisa."""

import unittest

from src import pesquisa


class TestPesquisarPorDescricao(unittest.TestCase):
    """Testes de pesquisar_por_descricao."""

    def setUp(self):
        """Cria despesas de exemplo antes de cada teste."""
        self.despesas = [
            {"id": 1, "descricao": "Pingo Doce", "valor": 23.5,
             "categoria": "Alimentação", "data": "2026-11-10"},
            {"id": 2, "descricao": "Passe", "valor": 40,
             "categoria": "Transportes", "data": "2026-11-12"},
            {"id": 3, "descricao": "Pingo Doce", "valor": 15.2,
             "categoria": "Alimentação", "data": "2026-11-15"},
        ]

    def test_encontra_varias(self):
        resultado = pesquisa.pesquisar_por_descricao(self.despesas, "pingo")
        self.assertEqual(len(resultado), 2)

    def test_ignora_maiusculas(self):
        resultado = pesquisa.pesquisar_por_descricao(self.despesas, "PINGO")
        self.assertEqual(len(resultado), 2)

    def test_procura_em_qualquer_parte(self):
        resultado = pesquisa.pesquisar_por_descricao(self.despesas, "doce")
        self.assertEqual(len(resultado), 2)

    def test_ignora_espacos_nas_pontas(self):
        resultado = pesquisa.pesquisar_por_descricao(self.despesas, "  passe  ")
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0]["id"], 2)

    def test_sem_resultados(self):
        resultado = pesquisa.pesquisar_por_descricao(self.despesas, "xyz")
        self.assertEqual(resultado, [])

    def test_lista_vazia(self):
        resultado = pesquisa.pesquisar_por_descricao([], "pingo")
        self.assertEqual(resultado, [])


class TestFiltrarPorCategoria(unittest.TestCase):
    """Testes de filtrar_por_categoria."""

    def setUp(self):
        """Cria despesas de exemplo antes de cada teste."""
        self.despesas = [
            {"id": 1, "descricao": "Pingo Doce", "valor": 23.5,
             "categoria": "Alimentação", "data": "2026-11-10"},
            {"id": 2, "descricao": "Passe", "valor": 40,
             "categoria": "Transportes", "data": "2026-11-12"},
            {"id": 3, "descricao": "Pingo Doce", "valor": 15.2,
             "categoria": "Alimentação", "data": "2026-11-15"},
            {"id": 4, "descricao": "Cinema", "valor": 8.5,
             "categoria": "Lazer", "data": "2026-10-16"},
        ]

    def test_filtra_varias(self):
        resultado = pesquisa.filtrar_por_categoria(self.despesas, "Alimentação")
        self.assertEqual(len(resultado), 2)

    def test_so_devolve_a_categoria_pedida(self):
        resultado = pesquisa.filtrar_por_categoria(self.despesas, "Lazer")
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0]["id"], 4)

    def test_ignora_maiusculas(self):
        resultado = pesquisa.filtrar_por_categoria(self.despesas, "alimentação")
        self.assertEqual(len(resultado), 2)

    def test_ignora_espacos_nas_pontas(self):
        resultado = pesquisa.filtrar_por_categoria(self.despesas, "  Lazer  ")
        self.assertEqual(len(resultado), 1)

    def test_igualdade_exata_nao_parcial(self):
        # "Aliment" não deve apanhar "Alimentação" (é igualdade, não "contém")
        resultado = pesquisa.filtrar_por_categoria(self.despesas, "Aliment")
        self.assertEqual(resultado, [])

    def test_categoria_sem_despesas(self):
        resultado = pesquisa.filtrar_por_categoria(self.despesas, "Saúde")
        self.assertEqual(resultado, [])

    def test_lista_vazia(self):
        resultado = pesquisa.filtrar_por_categoria([], "Lazer")
        self.assertEqual(resultado, [])


if __name__ == "__main__":
    unittest.main()

