"""Prueba rapida de mi parte: excepciones, logs y utilidades."""

from excepciones import (ErrorSoftwareFJ, ClienteInvalidoError, ServicioNoDisponibleError,
                         OperacionNoPermitidaError, ReservaInvalidaError)
from utilidades import convertir_a_numero, calcular_con_proteccion, verificar_costo
from registro import registrar_evento, ARCHIVO_LOG


def main():
    registrar_evento("=== Inicio de la prueba de excepciones ===")

    print(calcular_con_proteccion(convertir_a_numero, "150.5", "horas"))     # valido
    print(calcular_con_proteccion(convertir_a_numero, "abc", "horas"))       # texto no numerico
    print(calcular_con_proteccion(convertir_a_numero, "", "duracion"))       # dato faltante
    print(calcular_con_proteccion(verificar_costo, -20))                     # costo negativo
    print(calcular_con_proteccion(verificar_costo, 300))                     # costo bien

    for error in (ClienteInvalidoError("Correo sin @"),
                  ServicioNoDisponibleError("Sala VIP"),
                  OperacionNoPermitidaError("La reserva ya estaba cancelada"),
                  ReservaInvalidaError("Duracion igual a cero")):
        try:
            raise error
        except ErrorSoftwareFJ as capturado:
            print("Atrapado:", capturado)

    registrar_evento("=== Fin de la prueba ===")
    print("Revisa el archivo:", ARCHIVO_LOG)


if __name__ == "__main__":
    main()