
import unittest

from cliente import Cliente
from excepciones import ClienteInvalidoError


class TestCliente(unittest.TestCase):

    # Prueba 1: registrar un cliente con datos correctos
    def test_cliente_valido(self):
        cliente = Cliente(
            "Carlos Perez",
            "1020304050",
            "carlos@gmail.com",
            "3001234567"
        )

        self.assertEqual(cliente.nombre, "Carlos Perez")
        self.assertEqual(cliente.documento, "1020304050")
        self.assertEqual(cliente.correo, "carlos@gmail.com")
        self.assertEqual(cliente.telefono, "3001234567")

    # Prueba 2: rechazar un nombre incorrecto
    def test_nombre_invalido(self):
        with self.assertRaises(ClienteInvalidoError):
            Cliente("A1", "1020304050", "ana@gmail.com", "3001234567")

    # Prueba 3: rechazar un documento incorrecto
    def test_documento_invalido(self):
        with self.assertRaises(ClienteInvalidoError):
            Cliente("Ana Lopez", "123", "ana@gmail.com", "3001234567")

    # Prueba 4: rechazar un correo incorrecto
    def test_correo_invalido(self):
        with self.assertRaises(ClienteInvalidoError):
            Cliente("Ana Lopez", "1020304050", "anagmail.com", "3001234567")

    # Prueba 5: rechazar un teléfono incorrecto
    def test_telefono_invalido(self):
        with self.assertRaises(ClienteInvalidoError):
            Cliente("Ana Lopez", "1020304050", "ana@gmail.com", "abc")


if __name__ == "__main__":
    unittest.main(verbosity=2)
