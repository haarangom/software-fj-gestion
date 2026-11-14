"""
REGISTRO DE EVENTOS Y ERRORES (LOGS) - Software FJ
Autor: Hector Andres Arango Murcia

Este archivo se encarga de guardar en un archivo de texto (logs/sistema.log)
todo lo importante que pasa en el programa: lo que sale bien y los errores.
Sirve para revisar despues que paso, aunque el programa ya se haya cerrado.

Uso desde cualquier otro archivo:
    from registro import registrar_evento, registrar_error
"""

import logging
import os

CARPETA_LOGS = "logs"
ARCHIVO_LOG = os.path.join(CARPETA_LOGS, "sistema.log")


def _crear_logger():
    """Prepara el logger una sola vez: carpeta, archivo y formato del texto."""
    os.makedirs(CARPETA_LOGS, exist_ok=True)

    logger = logging.getLogger("software_fj")
    logger.setLevel(logging.INFO)

    # Si ya tiene un manejador no se agrega otro (evita lineas repetidas en el log).
    if not logger.handlers:
        manejador = logging.FileHandler(ARCHIVO_LOG, encoding="utf-8")
        formato = logging.Formatter("%(asctime)s | %(levelname)-8s | %(message)s",
                                    datefmt="%Y-%m-%d %H:%M:%S")
        manejador.setFormatter(formato)
        logger.addHandler(manejador)
    return logger


_logger = _crear_logger()


def registrar_evento(mensaje):
    """Guarda en el log algo normal que paso (INFO)."""
    _logger.info(mensaje)


def registrar_advertencia(mensaje):
    """Guarda en el log algo raro pero que no rompe el programa (WARNING)."""
    _logger.warning(mensaje)


def registrar_error(mensaje, excepcion=None):
    """
    Guarda en el log un error (ERROR). Si se pasa la excepcion, tambien
    se anota de que tipo era y, si venia encadenada, cual fue la causa original.
    """
    if excepcion is not None:
        mensaje = f"{mensaje} | {type(excepcion).__name__}: {excepcion}"
        if excepcion.__cause__ is not None:
            causa = excepcion.__cause__
            mensaje += f" | Causa original: {type(causa).__name__}: {causa}"
    _logger.error(mensaje)