"""
PROGRAMA PRINCIPAL - Software FJ (Sistema de gestion de clientes, servicios y reservas)
Autor: Hector Andres Arango Murcia

Este archivo ejecuta 16 operaciones de prueba (validas e invalidas) para
mostrar que el sistema funciona y que NUNCA se detiene ante un error.
Todo lo que pasa queda guardado en logs/sistema.log.

Para ejecutarlo:   python main.py
"""

from cliente import crear_cliente_seguro
from excepciones import ErrorSoftwareFJ
from registro import registrar_evento, registrar_error, ARCHIVO_LOG
from reserva import Reserva
from servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada

# Resultados de las simulaciones (para el resumen del final)
resultados = {"exitosas": 0, "con_error": 0}

# "Base de datos" en memoria: solo listas, como pide la guia
clientes = []
servicios = []
reservas = []


def simular(numero, descripcion, operacion):
    """
    Ejecuta UNA operacion de prueba sin que el programa se caiga.
      - except ErrorSoftwareFJ: error propio, se anota y se sigue
      - except Exception:       error inesperado, tambien se anota y se sigue
      - else:                   si salio bien, se cuenta como exitosa
      - finally:                siempre se anota que la operacion termino
    """
    print(f"\n[{numero:02d}] {descripcion}")
    registrar_evento(f"Simulacion {numero:02d}: {descripcion}")
    try:
        resultado = operacion()
    except ErrorSoftwareFJ as error:
        resultados["con_error"] += 1
        registrar_error(f"Simulacion {numero:02d} fallo de forma controlada", error)
        print(f"     ERROR CONTROLADO -> {error}")
    except Exception as error:
        resultados["con_error"] += 1
        registrar_error(f"Simulacion {numero:02d} tuvo un error inesperado", error)
        print(f"     ERROR INESPERADO CONTROLADO -> {type(error).__name__}: {error}")
    else:
        resultados["exitosas"] += 1
        registrar_evento(f"Simulacion {numero:02d} exitosa")
        print(f"     OK -> {resultado}")
    finally:
        registrar_evento(f"Fin de la simulacion {numero:02d}")


# ---------------- Operaciones de prueba ----------------

def registrar_cliente(nombre, documento, correo, telefono):
    cliente = crear_cliente_seguro(nombre, documento, correo, telefono)
    if cliente is None:
        # crear_cliente_seguro ya anoto el error; aqui lo volvemos a lanzar
        # para que la simulacion lo cuente como fallida.
        from excepciones import ClienteInvalidoError
        raise ClienteInvalidoError(f"No se pudo registrar a '{nombre}'")
    clientes.append(cliente)
    return cliente


def agregar_servicio(servicio):
    servicios.append(servicio)
    return servicio


def reservar_y_procesar(cliente, servicio, horas, descuento=0.0, impuesto=0.0):
    reserva = Reserva(cliente, servicio, horas, descuento, impuesto)
    reservas.append(reserva)
    reserva.confirmar()
    reserva.procesar()
    return reserva


def main():
    registrar_evento("========== INICIO DE LA SIMULACION ==========")

    # --- Clientes (validos e invalidos) ---
    simular(1, "Registrar cliente valido (Maria Lopez)",
            lambda: registrar_cliente("Maria Lopez", "1020304050", "maria@correo.com", "3001234567"))
    simular(2, "Registrar cliente valido (Juan Perez)",
            lambda: registrar_cliente("Juan Perez", "99887766", "juan.perez@mail.co", "3109876543"))
    simular(3, "Registrar cliente con correo invalido",
            lambda: registrar_cliente("Sara Rojas", "5544332211", "sara-correo.com", "3001234567"))
    simular(4, "Registrar cliente con documento demasiado corto",
            lambda: registrar_cliente("Luis Gomez", "12", "luis@correo.com", "3001234567"))

    # --- Servicios (validos e invalidos) ---
    simular(5, "Crear sala de reuniones valida",
            lambda: agregar_servicio(ReservaSala("Sala Norte", 50000, 10)))
    simular(6, "Crear servicio con tarifa negativa",
            lambda: agregar_servicio(ReservaSala("Sala Sur", -5000, 8)))
    simular(7, "Crear alquiler de equipo valido",
            lambda: agregar_servicio(AlquilerEquipo("Portatil Pro", 8000, 100000)))
    simular(8, "Crear asesoria valida",
            lambda: agregar_servicio(AsesoriaEspecializada("Asesoria en Python", 60000, "senior")))
    simular(9, "Crear asesoria con nivel inexistente",
            lambda: agregar_servicio(AsesoriaEspecializada("Asesoria X", 40000, "maestro")))

    # Si los registros anteriores salieron bien, se usan en las reservas
    maria, juan = clientes[0], clientes[1]
    sala, equipo, asesoria = servicios[0], servicios[1], servicios[2]

    # --- Reservas (exitosas y fallidas) ---
    simular(10, "Reserva exitosa de sala con descuento e impuesto",
            lambda: reservar_y_procesar(maria, sala, 3, descuento=0.10, impuesto=0.19).describir())
    simular(11, "Reserva exitosa de equipo",
            lambda: reservar_y_procesar(juan, equipo, 24).describir())
    simular(12, "Reserva con horas fuera de rango (sala por 50 horas)",
            lambda: reservar_y_procesar(maria, sala, 50))
    simular(13, "Reserva sin cliente",
            lambda: reservar_y_procesar(None, sala, 2))

    def cancelar_y_confirmar():
        reserva = Reserva(juan, asesoria, 2)
        reservas.append(reserva)
        reserva.cancelar()
        reserva.confirmar()          # no esta permitido: ya estaba cancelada
    simular(14, "Confirmar una reserva que ya fue cancelada", cancelar_y_confirmar)

    simular(15, "Procesar una reserva sin haberla confirmado",
            lambda: Reserva(maria, asesoria, 2).procesar())

    asesoria.cambiar_disponibilidad(False)
    simular(16, "Reservar un servicio que no esta disponible",
            lambda: reservar_y_procesar(juan, asesoria, 2))

    # Una prueba mas: un error que NO es del sistema (division entre cero),
    # para demostrar que tambien se controla y el programa sigue.
    simular(17, "Error inesperado de Python (division entre cero)",
            lambda: 10 / 0)

    # ---------------- Resumen final ----------------
    total = resultados["exitosas"] + resultados["con_error"]
    print("\n" + "=" * 60)
    print(f"RESUMEN: {total} simulaciones | {resultados['exitosas']} exitosas | "
          f"{resultados['con_error']} con error controlado")
    print(f"Clientes registrados: {len(clientes)} | Servicios: {len(servicios)} | "
          f"Reservas creadas: {len(reservas)}")
    print(f"El programa termino sin detenerse. Revisa el log: {ARCHIVO_LOG}")
    print("=" * 60)
    registrar_evento(f"========== FIN: {total} simulaciones, el sistema siguio estable ==========")


if __name__ == "__main__":
    main()
