import unittest
from unittest.mock import patch
import cadastro

class TestCadastro(unittest.TestCase):

    @patch('cadastro._cadastros', [])
    def test_add_cadastro_sucesso(self):
        resultado = cadastro.add_cadastro("usuario1", "senha123", 1, "aluno")
        self.assertEqual(resultado, (0, None))

    @patch('cadastro._cadastros', [])
    def test_add_cadastro_acesso_invalido(self):
        resultado = cadastro.add_cadastro("usuario1", "senha123", 1, "invalido")
        self.assertEqual(resultado, (45, None))

    @patch('cadastro._cadastros', [{"login": "usuario1", "senha": "senha123", "id": 1, "tipo_acesso": "aluno"}])
    def test_add_cadastro_login_existente(self):
        resultado = cadastro.add_cadastro("usuario1", "senha123", 2, "aluno")
        self.assertEqual(resultado, (46, None))

    @patch('cadastro._cadastros', [{"login": "usuario2", "senha": "senha123", "id": 1, "tipo_acesso": "aluno"}])
    def test_add_cadastro_id_e_acesso_existente(self):
        resultado = cadastro.add_cadastro("usuario3", "senha123", 1, "aluno")
        self.assertEqual(resultado, (47, None))

    @patch('cadastro._cadastros', [{"login": "usuario1", "senha": "senha123", "id": 1, "tipo_acesso": "aluno"}])
    def test_del_cadastro_sucesso(self):
        resultado = cadastro.del_cadastro("usuario1")
        self.assertEqual(resultado, (0, None))

    @patch('cadastro._cadastros', [])
    def test_del_cadastro_login_nao_encontrado(self):
        resultado = cadastro.del_cadastro("usuario_inexistente")
        self.assertEqual(resultado, (49, None))

    @patch('cadastro._cadastros', [{"login": "usuario1", "senha": "senha123", "id": 1, "tipo_acesso": "aluno"}])
    def test_get_cadastro_by_login_sucesso(self):
        resultado, cadastro_encontrado = cadastro.get_cadastro_by_login("usuario1")
        self.assertEqual(resultado, 0)
        self.assertEqual(cadastro_encontrado["login"], "usuario1")

    @patch('cadastro._cadastros', [])
    def test_get_cadastro_by_login_nao_encontrado(self):
        resultado = cadastro.get_cadastro_by_login("usuario_inexistente")
        self.assertEqual(resultado, (49, None))

    @patch('cadastro._cadastros', [{"login": "usuario1", "senha": "senha123", "id": 1, "tipo_acesso": "aluno"}])
    def test_login_sucesso(self):
        resultado, id_usuario = cadastro.login("usuario1", "senha123")
        self.assertEqual(resultado, 0)
        self.assertEqual(id_usuario, 1)

    @patch('cadastro._cadastros', [{"login": "usuario1", "senha": "senha123", "id": 1, "tipo_acesso": "aluno"}])
    def test_login_senha_incorreta(self):
        resultado = cadastro.login("usuario1", "senha_incorreta")
        self.assertEqual(resultado, (50, None))

    @patch('cadastro._cadastros', [])
    def test_login_nao_encontrado(self):
        resultado = cadastro.login("usuario_inexistente", "senha123")
        self.assertEqual(resultado, (49, None))

    @patch('cadastro._cadastros', [{"login": "usuario1", "senha": "senha123", "id": 1, "tipo_acesso": "aluno"}])
    def test_is_aluno_sucesso(self):
        resultado, is_aluno = cadastro.is_aluno("usuario1")
        self.assertEqual(resultado, 0)
        self.assertTrue(is_aluno)

    @patch('cadastro._cadastros', [])
    def test_is_aluno_nao_encontrado(self):
        resultado = cadastro.is_aluno("usuario_inexistente")
        self.assertEqual(resultado, (49, None))

    @patch('cadastro._cadastros', [{"login": "professor1", "senha": "senha123", "id": 2, "tipo_acesso": "professor"}])
    def test_is_professor_sucesso(self):
        resultado, is_professor = cadastro.is_professor("professor1")
        self.assertEqual(resultado, 0)
        self.assertTrue(is_professor)

    @patch('cadastro._cadastros', [])
    def test_is_professor_nao_encontrado(self):
        resultado = cadastro.is_professor("usuario_inexistente")
        self.assertEqual(resultado, (49, None))

    @patch('cadastro._cadastros', [{"login": "admin1", "senha": "senha123", "id": 3, "tipo_acesso": "admin"}])
    def test_is_admin_sucesso(self):
        resultado, is_admin = cadastro.is_admin("admin1")
        self.assertEqual(resultado, 0)
        self.assertTrue(is_admin)

    @patch('cadastro._cadastros', [])
    def test_is_admin_nao_encontrado(self):
        resultado = cadastro.is_admin("usuario_inexistente")
        self.assertEqual(resultado, (49, None))

if __name__ == '__main__':
    unittest.main()