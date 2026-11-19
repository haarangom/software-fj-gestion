# Software FJ – Sistema de gestión de clientes, servicios y reservas

Proyecto de la **Fase 4 (Prácticas simuladas)** del curso **Programación (213023)**, UNAD – Ingeniería de Sistemas.

Es un programa en Python, sin base de datos, que maneja clientes, servicios y reservas de una empresa llamada *Software FJ*. Lo más importante es que **nunca se detiene cuando hay un error**: cada problema se atrapa, se anota en un archivo de registro (log) y el programa sigue funcionando.

## ¿Qué hace?
- Registra **clientes** y revisa que sus datos sean correctos (nombre, documento, correo y teléfono).
- Maneja tres **servicios**: reserva de salas, alquiler de equipos y asesorías especializadas.
- Crea **reservas** que pasan por estados: pendiente → confirmada → procesada (o cancelada).
- Calcula el costo de cada servicio, con **descuento e impuesto opcionales**.
- Guarda todo lo importante y todos los errores en `logs/sistema.log`.

## Archivos del proyecto
| Archivo | Para qué sirve |
|---|---|
| `excepciones.py` | Errores propios del sistema (cliente inválido, servicio no disponible, reserva inválida, etc.) |
| `registro.py` | Guarda los eventos y errores en el archivo de log |
| `utilidades.py` | Ejemplos de `try/except`, `try/except/else`, `try/except/finally` y encadenamiento de excepciones |
| `entidad.py` | Clase abstracta base de la que salen las demás |
| `cliente.py` | Clase `Cliente` con datos protegidos y validaciones |
| `servicio.py` | Clase abstracta `Servicio` con el cálculo de costo sobrecargado |
| `servicios.py` | Los tres servicios: `ReservaSala`, `AlquilerEquipo` y `AsesoriaEspecializada` |
| `reserva.py` | Clase `Reserva` con confirmar, cancelar y procesar |
| `main.py` | Programa principal con 17 simulaciones (válidas e inválidas) |
| `probar_*.py` | Pruebas rápidas de cada parte |

## Conceptos de programación orientada a objetos que se usan
- **Abstracción:** `Entidad` y `Servicio` son clases abstractas, no se pueden crear directamente.
- **Herencia:** `Cliente` y `Servicio` salen de `Entidad`; los tres servicios salen de `Servicio`.
- **Polimorfismo:** cada servicio calcula su costo y se describe a su manera.
- **Encapsulación:** los datos van con guion bajo (`_`) y se cambian con propiedades que validan.
- **Sobrecarga:** `calcular_costo()` se puede usar solo con las horas, con descuento, con impuesto o con ambos.

## Manejo de excepciones
- Excepciones personalizadas que salen de una clase base (`ErrorSoftwareFJ`).
- Bloques `try/except`, `try/except/else` y `try/except/finally`.
- **Encadenamiento** con `raise ... from error`, para no perder la causa original.
- Todos los errores quedan en `logs/sistema.log`.

## ¿Cómo se ejecuta?
Se necesita Python 3 instalado. Desde la carpeta del proyecto:

```
python main.py
```

Al final se muestra un resumen: cuántas simulaciones fueron exitosas, cuántas tuvieron error controlado y dónde quedó el log.

## Trabajo en equipo
Cada integrante trabaja en su propia rama y envía sus cambios con un *pull request*. Las tareas están en los **Issues** del repositorio.

| Parte | Responsable |
|---|---|
| Excepciones, logs y utilidades | Héctor Andrés Arango Murcia |
| Entidad y Cliente | Héctor Andrés Arango Murcia |
| Servicio y servicios especializados | Héctor Andrés Arango Murcia |
| Reserva | Héctor Andrés Arango Murcia |
| Simulaciones, README y PDF | Héctor Andrés Arango Murcia |

> Si algún compañero se une, se actualiza esta tabla.
