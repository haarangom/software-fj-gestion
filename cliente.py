"""
CLASE CLIENTE - Software FJ
Autor: Hector Andres Arango Murcia

Representa a una persona que usa los servicios de la empresa.
Sus datos son privados (guion bajo) y solo se cambian con propiedades que
revisan que todo sea valido. Si algo esta mal, se lanza ClienteInvalidoError
y el programa lo atrapa sin caerse.
"""

import re

from entidad import Entidad
from excepciones import ClienteInvalidoError, ErrorSoftwareFJ
from registro import registrar_evento, registrar_error

# Reglas simples para revisar los datos
PATRON_NOMBRE = re.compile(r"^[A-Za-zÁÉÍÓÚáéíóúÑñÜü ]{3,60}$")
PATRON_CORREO = re.compile(r"^[\w.+-]+@[\w-]+\.[\w.-]+$")
PATRON_TELEFONO = re.compile(r"^\d{7,10}$")
PATRON_DOCUMENTO = re.compile(r"^\d{6,12}$")


class Cliente(Entidad):
    """Cliente con datos personales protegidos y validados."""

    def __init__(self, nombre, documento, correo, telefono):
        super().__init__()          # le asigna su numero de identificacion
        # Se usan las propiedades (con validacion), no se asigna directo.
        self.nombre = nombre
        self.documento = documento
        self.correo = correo
        self.telefono = telefono

    # ---------------- Propiedades con validacion ----------------

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        if not isinstance(valor, str) or not PATRON_NOMBRE.match(valor.strip()):
            raise ClienteInvalidoError(
                "El nombre debe tener entre 3 y 60 letras (sin numeros ni simbolos)")
        self._nombre = valor.strip().title()

    @property
    def documento(self):
        return self._documento

    @documento.setter
    def documento(self, valor):
        if not PATRON_DOCUMENTO.match(str(valor).strip()):
            raise ClienteInvalidoError("El documento debe tener entre 6 y 12 numeros")
        self._documento = str(valor).strip()

    @property
    def correo(self):
        return self._correo

    @correo.setter
    def correo(self, valor):
        if not isinstance(valor, str) or not PATRON_CORREO.match(valor.strip()):
            raise ClienteInvalidoError("El correo no tiene un formato valido")
        self._correo = valor.strip().lower()

    @property
    def telefono(self):
        return self._telefono

    @telefono.setter
    def telefono(self, valor):
        if not PATRON_TELEFONO.match(str(valor).strip()):
            raise ClienteInvalidoError("El telefono debe tener entre 7 y 10 numeros")
        self._telefono = str(valor).strip()

    # ---------------- Metodo abstracto implementado ----------------

    def describir(self):
        return (f"Cliente #{self.id}: {self.nombre} | Doc: {self.documento} | "
                f"{self.correo} | Tel: {self.telefono}")


def crear_cliente_seguro(nombre, documento, correo, telefono):
    """
    Intenta crear un cliente sin que el programa se caiga.
      - except: si los datos son malos, se anota el error y se devuelve None
      - else:   si todo sale bien, se anota que se registro el cliente
      - finally: siempre se anota que el intento termino
    """
    try:
        cliente = Cliente(nombre, documento, correo, telefono)
    except ErrorSoftwareFJ as error:
        registrar_error("No se pudo registrar el cliente", error)
        return None
    else:
        registrar_evento(f"Cliente registrado: {cliente.nombre} (id {cliente.id})")
        return cliente
    finally:
        registrar_evento("Fin del intento de registro de cliente")