"""
LOS TRES SERVICIOS ESPECIALIZADOS - Software FJ
Autor: Hector Andres Arango Murcia

Cada uno hereda de Servicio y cambia (sobrescribe) tres cosas:
  - validar_parametros: que reglas debe cumplir la duracion
  - calcular_costo_base: como se calcula su costo
  - describir: como se explica a si mismo
Asi, con el mismo metodo calcular_costo(), cada servicio responde distinto
(polimorfismo).
"""

from excepciones import DatoInvalidoError
from servicio import Servicio


class ReservaSala(Servicio):
    """Sala de reuniones: se cobra por hora y depende de la capacidad."""

    def __init__(self, nombre, tarifa_hora, capacidad):
        super().__init__(nombre, tarifa_hora)
        if not isinstance(capacidad, int) or capacidad <= 0:
            raise DatoInvalidoError("La capacidad debe ser un numero entero mayor que cero")
        self._capacidad = capacidad

    def validar_parametros(self, horas):
        if not 1 <= horas <= 12:
            raise DatoInvalidoError("Una sala se reserva entre 1 y 12 horas")

    def calcular_costo_base(self, horas):
        return self._tarifa_hora * horas

    def describir(self):
        return (f"Sala '{self.nombre}' (id {self.id}) | capacidad: {self._capacidad} personas | "
                f"${self.tarifa_hora:,.0f} por hora")


class AlquilerEquipo(Servicio):
    """Alquiler de equipos: tarifa por hora mas un deposito fijo."""

    def __init__(self, nombre, tarifa_hora, deposito):
        super().__init__(nombre, tarifa_hora)
        if deposito < 0:
            raise DatoInvalidoError("El deposito no puede ser negativo")
        self._deposito = deposito

    def validar_parametros(self, horas):
        if not 1 <= horas <= 72:
            raise DatoInvalidoError("Un equipo se alquila entre 1 y 72 horas")

    def calcular_costo_base(self, horas):
        return self._tarifa_hora * horas + self._deposito

    def describir(self):
        return (f"Equipo '{self.nombre}' (id {self.id}) | deposito: ${self._deposito:,.0f} | "
                f"${self.tarifa_hora:,.0f} por hora")


class AsesoriaEspecializada(Servicio):
    """Asesoria: el precio sube segun el nivel del asesor."""

    RECARGO_NIVEL = {"junior": 1.0, "senior": 1.5, "experto": 2.0}

    def __init__(self, nombre, tarifa_hora, nivel):
        super().__init__(nombre, tarifa_hora)
        nivel = str(nivel).strip().lower()
        if nivel not in self.RECARGO_NIVEL:
            raise DatoInvalidoError("El nivel debe ser junior, senior o experto")
        self._nivel = nivel

    def validar_parametros(self, horas):
        if not 1 <= horas <= 8:
            raise DatoInvalidoError("Una asesoria dura entre 1 y 8 horas")

    def calcular_costo_base(self, horas):
        return self._tarifa_hora * self.RECARGO_NIVEL[self._nivel] * horas

    def describir(self):
        return (f"Asesoria '{self.nombre}' (id {self.id}) | nivel: {self._nivel} | "
                f"${self.tarifa_hora:,.0f} por hora base")