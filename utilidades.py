"""
UTILIDADES DE MANEJO DE ERRORES - Software FJ
Autor: Hector Andres Arango Murcia

Aqui estan las funciones que muestran los bloques de manejo de errores que
pide la guia, listas para usarlas en todo el proyecto:
  - try / except              -> atrapar un error
  - try / except / else       -> hacer algo solo si NO hubo error
  - try / except / finally    -> hacer algo siempre, haya error o no
  - encadenamiento (raise ... from ...) -> conservar la causa original
"""

from excepciones import (ErrorSoftwareFJ, DatoInvalidoError,
                         ParametroFaltanteError, CalculoInconsistenteError)
from registro import registrar_evento, registrar_error


def convertir_a_numero(valor, nombre_dato):
    """
    Convierte un texto a numero. Si no se puede, lanza un error propio.
    Usa ENCADENAMIENTO: 'from error' guarda el error original de Python
    como causa del error nuevo, asi no se pierde la informacion.
    """
    if valor is None or str(valor).strip() == "":
        raise ParametroFaltanteError(nombre_dato)
    try:
        return float(valor)
    except ValueError as error:
        raise DatoInvalidoError(
            f"'{valor}' no es un numero valido para {nombre_dato}") from error


def calcular_con_proteccion(operacion, *argumentos):
    """
    Ejecuta una operacion cuidando que el programa nunca se caiga.
    Muestra los tres bloques juntos:
      - except: si algo falla, se anota en el log y se devuelve None
      - else:   si todo salio bien, se anota el exito
      - finally: siempre se anota que la operacion termino
    """
    nombre = getattr(operacion, "__name__", "operacion")
    try:
        resultado = operacion(*argumentos)
    except ErrorSoftwareFJ as error:
        registrar_error(f"Fallo controlado en {nombre}", error)
        return None
    except Exception as error:
        # Cualquier otro error inesperado tambien se atrapa para no detener el programa.
        registrar_error(f"Error inesperado en {nombre}", error)
        return None
    else:
        registrar_evento(f"Operacion {nombre} realizada con exito")
        return resultado
    finally:
        registrar_evento(f"Fin de la operacion {nombre}")


def verificar_costo(costo):
    """Revisa que un costo calculado tenga sentido; si no, lanza un error propio."""
    if costo < 0:
        raise CalculoInconsistenteError(f"El costo calculado no puede ser negativo: {costo}")
    return costo