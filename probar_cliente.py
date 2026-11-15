"""Prueba rapida de Cliente y de la clase abstracta Entidad."""

from entidad import Entidad
from cliente import crear_cliente_seguro


def main():
    # 1) La clase abstracta no se puede crear directamente
    try:
        Entidad()
    except TypeError as error:
        print("Entidad es abstracta, no se puede crear:", error)

    # 2) Clientes validos e invalidos
    datos = [
        ("Maria Lopez",  "1020304050", "maria@correo.com", "3001234567"),   # valido
        ("Juan Perez",   "99887766",   "juan.perez@mail.co", "3109876543"), # valido
        ("A1",           "1020304050", "ana@correo.com",   "3001234567"),   # nombre malo
        ("Luis Gomez",   "12",         "luis@correo.com",  "3001234567"),   # documento malo
        ("Sara Rojas",   "5544332211", "sara-correo.com",  "3001234567"),   # correo malo
        ("Pedro Mora",   "6677889900", "pedro@correo.com", "abc"),          # telefono malo
    ]
    for d in datos:
        cliente = crear_cliente_seguro(*d)
        print(cliente if cliente else f"  -> No se registro: {d[0]}")


if __name__ == "__main__":
    main()