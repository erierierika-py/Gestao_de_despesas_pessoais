"""Testes do módulo login."""

import unittest

from src import login


class TestLogin(unittest.TestCase):
    """Testes das funções de cálculo do login."""

    def test_mesmo_hash(self):
        # mesma palavra-passe e mesmo salt dão o mesmo hash
        self.assertEqual(login.gerar_hash("1234", "abc"), login.gerar_hash("1234", "abc"))

    def test_hash_diferente(self):
        # palavra-passe diferente dá hash diferente
        self.assertNotEqual(login.gerar_hash("1234", "abc"), login.gerar_hash("1235", "abc"))

    def test_palavra_passe_certa(self):
        salt = "abc"
        d = {"login": {"salt": salt, "hash": login.gerar_hash("1234", salt)}}
        self.assertTrue(login.verificar_palavra_passe("1234", d))

    def test_palavra_passe_errada(self):
        salt = "abc"
        d = {"login": {"salt": salt, "hash": login.gerar_hash("1234", salt)}}
        self.assertFalse(login.verificar_palavra_passe("9999", d))

    def test_sem_login_guardado(self):
        self.assertFalse(login.verificar_palavra_passe("1234", {}))


if __name__ == "__main__":
    unittest.main()