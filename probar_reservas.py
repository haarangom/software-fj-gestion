"""Prueba rapida de Reserva: casos validos y casos con error."""

from cliente import Cliente
from reserva import Reserva
from servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from excepciones import ErrorSoftwareFJ


def intentar(descripcion, accion):
    """Ejecuta una accion y muestra el resultado, sin que el programa se caiga."""
    try:
        resultado = accion()
    except ErrorSoftwareFJ as error:
        causa = f"  (causa: {error.__cause__})" if error.__cause__ else ""
        print(f"  [ERROR] {descripcion}: {error}{causa}")
    else:
        print(f"  [OK]    {descripcion}: {resultado if resultado is not None else ''}")


def main():
    maria = Cliente("Maria Lopez", "1020304050", "maria@correo.com", "3001234567")
    sala = ReservaSala("Sala Norte", 50000, 10)
    equipo = AlquilerEquipo("Portatil Pro", 8000, 100000)
    asesoria = AsesoriaEspecializada("Asesoria en Python", 60000, "senior")

    print("--- Flujo normal ---")
    r1 = Reserva(maria, sala, 3, descuento=0.10, impuesto=0.19)
    intentar("confirmar", r1.confirmar)
    intentar("procesar", r1.procesar)
    print(" ", r1)

    print("--- Cancelacion ---")
    r2 = Reserva(maria, equipo, 10)
    intentar("cancelar", r2.cancelar)
    print(" ", r2)

    print("--- Casos con error ---")
    intentar("cancelar una ya procesada", r1.cancelar)
    intentar("confirmar dos veces", lambda: (r2.confirmar()))
    intentar("procesar sin confirmar", Reserva(maria, asesoria, 2).procesar)
    intentar("horas fuera de rango", lambda: Reserva(maria, sala, 50))
    intentar("horas no numericas", lambda: Reserva(maria, sala, "abc"))
    intentar("sin cliente", lambda: Reserva(None, sala, 2))
    intentar("cliente falso", lambda: Reserva("Pedro", sala, 2))

    asesoria.cambiar_disponibilidad(False)
    intentar("servicio no disponible", lambda: Reserva(maria, asesoria, 2))


if __name__ == "__main__":
    main()