import unittest
from ui import email_valido, clave_valida, validar_login_form


class TestEmailValido(unittest.TestCase):

    def test_email_correcto(self):
        self.assertTrue(email_valido("demo@fvncr.org"))

    def test_email_con_subdominio(self):
        self.assertTrue(email_valido("user@mail.co.cr"))

    def test_email_con_numeros(self):
        self.assertTrue(email_valido("user123@dominio.com"))

    def test_email_con_puntos_y_guiones(self):
        self.assertTrue(email_valido("nombre.apellido@mi-dominio.com"))

    def test_email_con_caracteres_especiales_validos(self):
        self.assertTrue(email_valido("user+tag@dominio.com"))

    def test_email_vacio(self):
        self.assertFalse(email_valido(""))

    def test_email_sin_arroba(self):
        self.assertFalse(email_valido("usuariodominio.com"))

    def test_email_sin_dominio(self):
        self.assertFalse(email_valido("usuario@"))

    def test_email_sin_usuario(self):
        self.assertFalse(email_valido("@dominio.com"))

    def test_email_sin_extension(self):
        self.assertFalse(email_valido("usuario@dominio"))

    def test_email_extension_una_letra(self):
        self.assertFalse(email_valido("usuario@dominio.c"))

    def test_email_con_espacios(self):
        self.assertFalse(email_valido("usuario @dominio.com"))

    def test_email_doble_arroba(self):
        self.assertFalse(email_valido("user@@dominio.com"))


class TestClaveValida(unittest.TestCase):

    def test_clave_solo_letras(self):
        self.assertTrue(clave_valida("abcDEF"))

    def test_clave_solo_numeros(self):
        self.assertTrue(clave_valida("123456"))

    def test_clave_alfanumerica(self):
        self.assertTrue(clave_valida("abc123"))

    def test_clave_con_numeral(self):
        self.assertTrue(clave_valida("clave#1"))

    def test_clave_solo_numeral(self):
        self.assertTrue(clave_valida("#"))

    def test_clave_vacia(self):
        self.assertFalse(clave_valida(""))

    def test_clave_con_espacio(self):
        self.assertFalse(clave_valida("clave 1"))

    def test_clave_con_arroba(self):
        self.assertFalse(clave_valida("clave@1"))

    def test_clave_con_signo_exclamacion(self):
        self.assertFalse(clave_valida("clave!"))

    def test_clave_con_guion(self):
        self.assertFalse(clave_valida("clave-1"))

    def test_clave_con_punto(self):
        self.assertFalse(clave_valida("clave.1"))

    def test_clave_con_tilde(self):
        self.assertFalse(clave_valida("contraseña"))


class TestValidarLoginForm(unittest.TestCase):

    def test_formulario_valido(self):
        valido, msg = validar_login_form("demo@fvncr.org", "demo")
        self.assertTrue(valido)
        self.assertEqual(msg, "")

    def test_email_vacio(self):
        valido, msg = validar_login_form("", "demo")
        self.assertFalse(valido)
        self.assertIn("email", msg.lower())

    def test_email_solo_espacios(self):
        valido, msg = validar_login_form("   ", "demo")
        self.assertFalse(valido)

    def test_clave_vacia(self):
        valido, msg = validar_login_form("demo@fvncr.org", "")
        self.assertFalse(valido)
        self.assertIn("clave", msg.lower())

    def test_clave_solo_espacios(self):
        valido, msg = validar_login_form("demo@fvncr.org", "   ")
        self.assertFalse(valido)

    def test_email_formato_invalido(self):
        valido, msg = validar_login_form("noesmail", "demo")
        self.assertFalse(valido)
        self.assertIn("email", msg.lower())

    def test_clave_caracteres_invalidos(self):
        valido, msg = validar_login_form("demo@fvncr.org", "cl@ve!")
        self.assertFalse(valido)
        self.assertIn("clave", msg.lower())

    def test_ambos_vacios(self):
        valido, msg = validar_login_form("", "")
        self.assertFalse(valido)

    def test_email_invalido_y_clave_invalida(self):
        valido, msg = validar_login_form("noesmail", "cl@ve!")
        self.assertFalse(valido)

    def test_clave_con_numeral_valida(self):
        valido, msg = validar_login_form("demo@fvncr.org", "clave#1")
        self.assertTrue(valido)
        self.assertEqual(msg, "")


if __name__ == "__main__":
    unittest.main()
