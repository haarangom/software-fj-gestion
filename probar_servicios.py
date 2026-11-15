"""Prueba rapida de Servicio (abstracto) y de los 3 servicios."""

from servicio import Servicio
from servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from excepciones import ErrorSoftwareFJ
from utilidades import calcular_con_proteccion


def main():
    # 1) La clase abstracta no se puede crear
    try:
        Servicio("X", 1000)
    except TypeError as error:
        print("Servicio es abstracta:", error)

    # 2) Creacion de servicios (validos e invalidos)
    sala = ReservaSala("Sala Norte", 50000, 10)
    equipo = AlquilerEquipo("Portatil Pro", 8000, 100000)
    asesoria = AsesoriaEspecializada("Asesoria en Python", 60000, "senior")
    servicios = [sala, equipo, asesoria]

    for datos in [("ReservaSala", lambda: ReservaSala("Sala X", -5, 10)),
                  ("AlquilerEquipo", lambda: AlquilerEquipo("", 5000, 0)),
                  ("Asesoria", lambda: AsesoriaEspecializada("Asesoria", 40000, "maestro"))]:
        try:
            datos[1]()
        except ErrorSoftwareFJ as error:
            print(f"Creacion invalida de {datos[0]} ->", error)

    # 3) Polimorfismo: el mismo metodo, resultados distintos
    print()
    for s in servicios:
        print(s)
        print("   normal:               ", s.calcular_costo(2))
        print("   con 10% descuento:    ", s.calcular_costo(2, descuento=0.10))
        print("   con 19% impuesto:     ", s.calcular_costo(2, impuesto=0.19))
        print("   descuento + impuesto: ", s.calcular_costo(2, descuento=0.10, impuesto=0.19))

    # 4) Casos con error (el programa sigue funcionando)
    print()
    print("Horas fuera de rango:", calcular_con_proteccion(sala.calcular_costo, 20))
    print("Horas no numericas:  ", calcular_con_proteccion(equipo.calcular_costo, "abc"))
    print("Descuento muy alto:  ", calcular_con_proteccion(asesoria.calcular_costo, 2, 0.9))
    asesoria.cambiar_disponibilidad(False)
    print("Servicio no disponible:", calcular_con_proteccion(asesoria.calcular_costo, 2))


if __name__ == "__main__":
    main()