"""
EXCEPCIONES PERSONALIZADAS - Software FJ
Autor: Hector Andres Arango Murcia

Aqui estan todos los errores propios del sistema. En vez de usar errores
genericos de Python, creo errores con nombres claros, para saber de
inmediato que fallo (un cliente mal registrado, un servicio no disponible,
una reserva invalida, etc.).

Todos salen de una misma clase base (ErrorSoftwareFJ). Asi, en cualquier
parte del programa se puede atrapar un error especifico, o atrapar todos
los del sistema de una sola vez con ErrorSoftwareFJ.
"""


class ErrorSoftwareFJ(Exception):
    """Error base: todos los errores del sistema salen de esta clase."""

    def __init__(self, mensaje, codigo="SFJ-000"):
        # Se guarda el mensaje y un codigo corto para encontrarlo facil en el log.
        super().__init__(mensaje)
        self.mensaje = mensaje
        self.codigo = codigo

    def __str__(self):
        return f"[{self.codigo}] {self.mensaje}"


class DatoInvalidoError(ErrorSoftwareFJ):
    """Se usa cuando un dato no cumple lo que se necesita (vacio, formato malo, etc.)."""

    def __init__(self, mensaje):
        super().__init__(mensaje, codigo="SFJ-100")


class ClienteInvalidoError(DatoInvalidoError):
    """Se usa cuando los datos de un cliente no son validos (nombre, correo, telefono)."""

    def __init__(self, mensaje):
        super().__init__(mensaje)
        self.codigo = "SFJ-110"


class ParametroFaltanteError(ErrorSoftwareFJ):
    """Se usa cuando falta un dato obligatorio para hacer una operacion."""

    def __init__(self, parametro):
        super().__init__(f"Falta el parametro obligatorio: {parametro}", codigo="SFJ-120")
        self.parametro = parametro


class ServicioNoDisponibleError(ErrorSoftwareFJ):
    """Se usa cuando se intenta usar un servicio que no esta disponible."""

    def __init__(self, nombre_servicio):
        super().__init__(f"El servicio '{nombre_servicio}' no esta disponible", codigo="SFJ-200")
        self.nombre_servicio = nombre_servicio


class OperacionNoPermitidaError(ErrorSoftwareFJ):
    """Se usa cuando se intenta algo que las reglas no permiten (por ejemplo, cancelar dos veces)."""

    def __init__(self, mensaje):
        super().__init__(mensaje, codigo="SFJ-300")


class ReservaInvalidaError(ErrorSoftwareFJ):
    """Se usa cuando una reserva no se puede crear o procesar."""

    def __init__(self, mensaje):
        super().__init__(mensaje, codigo="SFJ-400")


class CalculoInconsistenteError(ErrorSoftwareFJ):
    """Se usa cuando un calculo da un resultado que no tiene sentido (costo negativo, etc.)."""

    def __init__(self, mensaje):
        super().__init__(mensaje, codigo="SFJ-500")