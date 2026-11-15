"""
CLASE ABSTRACTA SERVICIO - Software FJ
Autor: Hector Andres Arango Murcia

Es el molde de todos los servicios que ofrece la empresa. No se puede crear
directamente: cada servicio concreto (sala, equipo, asesoria) la hereda y
esta obligado a decir como calcula su costo base, como se describe y que
parametros acepta.

El metodo calcular_costo() esta SOBRECARGADO usando parametros opcionales:
    calcular_costo(horas)                          -> costo normal
    calcular_costo(horas, descuento=0.10)          -> con 10% de descuento
    calcular_costo(horas, impuesto=0.19)           -> con 19% de impuesto
    calcular_costo(horas, descuento=0.10, impuesto=0.19) -> con los dos
"""

from abc import abstractmethod

from entidad import Entidad
from excepciones import (DatoInvalidoError, ParametroFaltanteError,
                         ServicioNoDisponibleError)
from utilidades import convertir_a_numero, verificar_costo


class Servicio(Entidad):
    """Servicio general: nombre, tarifa por hora y si esta disponible."""

    def __init__(self, nombre, tarifa_hora):
        super().__init__()
        if not isinstance(nombre, str) or not nombre.strip():
            raise ParametroFaltanteError("nombre del servicio")
        tarifa = convertir_a_numero(tarifa_hora, "tarifa por hora")
        if tarifa <= 0:
            raise DatoInvalidoError("La tarifa por hora debe ser mayor que cero")
        self._nombre = nombre.strip()
        self._tarifa_hora = tarifa
        self._disponible = True

    # ---------------- Datos que se pueden consultar ----------------

    @property
    def nombre(self):
        return self._nombre

    @property
    def tarifa_hora(self):
        return self._tarifa_hora

    @property
    def disponible(self):
        return self._disponible

    def cambiar_disponibilidad(self, estado):
        """Marca el servicio como disponible (True) o no disponible (False)."""
        self._disponible = bool(estado)

    def verificar_disponibilidad(self):
        """Si el servicio no esta disponible, lanza el error propio."""
        if not self._disponible:
            raise ServicioNoDisponibleError(self._nombre)

    # ---------------- Metodos que cada hija debe escribir ----------------

    @abstractmethod
    def validar_parametros(self, horas):
        """Revisa que la duracion (y otros datos) sean validos para este servicio."""
        pass

    @abstractmethod
    def calcular_costo_base(self, horas):
        """Calcula el costo sin impuestos ni descuentos (cada servicio lo hace distinto)."""
        pass

    # ---------------- Metodo sobrecargado (parametros opcionales) ----------------

    def calcular_costo(self, horas, descuento=0.0, impuesto=0.0):
        """
        Costo final: primero el costo base, luego se resta el descuento y
        despues se suma el impuesto. Descuento e impuesto son opcionales.
        """
        self.verificar_disponibilidad()
        horas = convertir_a_numero(horas, "horas")
        self.validar_parametros(horas)

        if not 0 <= descuento <= 0.5:
            raise DatoInvalidoError("El descuento debe estar entre 0% y 50%")
        if not 0 <= impuesto <= 0.3:
            raise DatoInvalidoError("El impuesto debe estar entre 0% y 30%")

        costo = self.calcular_costo_base(horas)
        costo = costo * (1 - descuento)
        costo = costo * (1 + impuesto)
        return round(verificar_costo(costo), 2)