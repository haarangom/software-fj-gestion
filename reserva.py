"""
CLASE RESERVA - Software FJ
Autor: Hector Andres Arango Murcia

Une a un cliente con un servicio por cierta cantidad de horas.
Una reserva pasa por estados, y no se puede saltar los pasos:

    PENDIENTE --confirmar()--> CONFIRMADA --procesar()--> PROCESADA
         |                          |
         +-------cancelar()---------+--> CANCELADA

Si alguien intenta algo que no esta permitido (por ejemplo cancelar una
reserva ya procesada), se lanza OperacionNoPermitidaError.
"""

from cliente import Cliente
from entidad import Entidad
from excepciones import (ErrorSoftwareFJ, ReservaInvalidaError,
                         OperacionNoPermitidaError, ParametroFaltanteError)
from registro import registrar_evento, registrar_error
from servicio import Servicio
from utilidades import convertir_a_numero


class Reserva(Entidad):
    """Reserva de un servicio hecha por un cliente."""

    PENDIENTE = "PENDIENTE"
    CONFIRMADA = "CONFIRMADA"
    CANCELADA = "CANCELADA"
    PROCESADA = "PROCESADA"

    def __init__(self, cliente, servicio, horas, descuento=0.0, impuesto=0.0):
        super().__init__()

        # 1) Se revisa que lleguen los objetos correctos
        if cliente is None:
            raise ParametroFaltanteError("cliente")
        if servicio is None:
            raise ParametroFaltanteError("servicio")
        if not isinstance(cliente, Cliente):
            raise ReservaInvalidaError("El cliente de la reserva no es valido")
        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("El servicio de la reserva no es valido")

        # 2) El servicio debe estar disponible y la duracion debe ser valida.
        #    Si la duracion falla, se ENCADENA el error original con 'from'.
        servicio.verificar_disponibilidad()
        try:
            horas = convertir_a_numero(horas, "horas")
            servicio.validar_parametros(horas)
        except ErrorSoftwareFJ as error:
            raise ReservaInvalidaError(
                f"No se pudo crear la reserva: {error.mensaje}") from error

        self._cliente = cliente
        self._servicio = servicio
        self._horas = horas
        self._descuento = descuento
        self._impuesto = impuesto
        self._estado = Reserva.PENDIENTE
        self._costo_total = None

    # ---------------- Datos que se pueden consultar ----------------

    @property
    def cliente(self):
        return self._cliente

    @property
    def servicio(self):
        return self._servicio

    @property
    def horas(self):
        return self._horas

    @property
    def estado(self):
        return self._estado

    @property
    def costo_total(self):
        return self._costo_total

    # ---------------- Acciones de la reserva ----------------

    def confirmar(self):
        """Pasa de PENDIENTE a CONFIRMADA (solo si el servicio sigue disponible)."""
        if self._estado != Reserva.PENDIENTE:
            raise OperacionNoPermitidaError(
                f"Solo se puede confirmar una reserva PENDIENTE (esta {self._estado})")
        self._servicio.verificar_disponibilidad()
        self._estado = Reserva.CONFIRMADA
        registrar_evento(f"Reserva #{self.id} confirmada")

    def cancelar(self):
        """Cancela la reserva, salvo que ya este cancelada o procesada."""
        if self._estado in (Reserva.CANCELADA, Reserva.PROCESADA):
            raise OperacionNoPermitidaError(
                f"No se puede cancelar una reserva {self._estado}")
        self._estado = Reserva.CANCELADA
        registrar_evento(f"Reserva #{self.id} cancelada")

    def procesar(self):
        """
        Calcula el costo final y deja la reserva PROCESADA.
        Usa try/except/else/finally:
          - except: si el calculo falla, se anota y se lanza ReservaInvalidaError
                    (encadenado con el error original)
          - else:   si salio bien, se guarda el costo y se cambia el estado
          - finally: siempre se anota que el proceso termino
        """
        if self._estado != Reserva.CONFIRMADA:
            raise OperacionNoPermitidaError(
                f"Solo se puede procesar una reserva CONFIRMADA (esta {self._estado})")
        try:
            costo = self._servicio.calcular_costo(
                self._horas, descuento=self._descuento, impuesto=self._impuesto)
        except ErrorSoftwareFJ as error:
            registrar_error(f"No se pudo procesar la reserva #{self.id}", error)
            raise ReservaInvalidaError(
                f"No se pudo calcular el costo de la reserva #{self.id}") from error
        else:
            self._costo_total = costo
            self._estado = Reserva.PROCESADA
            registrar_evento(f"Reserva #{self.id} procesada, total ${costo:,.2f}")
            return costo
        finally:
            registrar_evento(f"Fin del procesamiento de la reserva #{self.id}")

    def describir(self):
        total = f"${self._costo_total:,.2f}" if self._costo_total is not None else "sin calcular"
        return (f"Reserva #{self.id} [{self._estado}] | {self._cliente.nombre} -> "
                f"{self._servicio.nombre} | {self._horas:g} h | total: {total}")