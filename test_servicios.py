
import unittest

from servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from excepciones import DatoInvalidoError


class TestServicios(unittest.TestCase):

    def test_crear_reserva_sala(self):
        sala = ReservaSala("Sala Norte", 50000, 10)

        self.assertEqual(sala.nombre, "Sala Norte")
        self.assertEqual(sala.calcular_costo(2), 100000)

    def test_capacidad_invalida(self):
        with self.assertRaises(DatoInvalidoError):
            ReservaSala("Sala Norte", 50000, 0)

    def test_horas_invalidas_sala(self):
        sala = ReservaSala("Sala Norte", 50000, 10)

        with self.assertRaises(DatoInvalidoError):
            sala.calcular_costo(13)

    def test_crear_alquiler_equipo(self):
        equipo = AlquilerEquipo("Portatil Pro", 8000, 100000)

        self.assertEqual(equipo.nombre, "Portatil Pro")
        self.assertEqual(equipo.calcular_costo(2), 116000)

    def test_deposito_invalido(self):
        with self.assertRaises(DatoInvalidoError):
            AlquilerEquipo("Portatil Pro", 8000, -100)

    def test_horas_invalidas_equipo(self):
        equipo = AlquilerEquipo("Portatil Pro", 8000, 100000)

        with self.assertRaises(DatoInvalidoError):
            equipo.calcular_costo(73)

    def test_crear_asesoria(self):
        asesoria = AsesoriaEspecializada(
            "Asesoria Python", 60000, "senior"
        )

        self.assertEqual(asesoria.nombre, "Asesoria Python")
        self.assertEqual(asesoria.calcular_costo(2), 180000)

    def test_nivel_invalido_asesoria(self):
        with self.assertRaises(DatoInvalidoError):
            AsesoriaEspecializada("Asesoria Python", 60000, "maestro")

    def test_horas_invalidas_asesoria(self):
        asesoria = AsesoriaEspecializada(
            "Asesoria Python", 60000, "senior"
        )

        with self.assertRaises(DatoInvalidoError):
            asesoria.calcular_costo(9)

    def test_polimorfismo(self):
        servicios = [
            ReservaSala("Sala Norte", 50000, 10),
            AlquilerEquipo("Portatil Pro", 8000, 100000),
            AsesoriaEspecializada("Asesoria Python", 60000, "senior")
        ]

        resultados = [servicio.calcular_costo(2) for servicio in servicios]

        self.assertEqual(resultados, [100000, 116000, 180000])


if __name__ == "__main__":
    unittest.main(verbosity=2)
