"""
CLASE ABSTRACTA BASE: Entidad - Software FJ
Autor: Hector Andres Arango Murcia

Esta es la clase "madre" de todo lo que el sistema guarda (por ahora los
clientes, y tambien se puede usar para servicios y reservas). Es abstracta:
no se puede crear un objeto directamente de ella, solo sirve de molde para
que las demas clases la hereden y obliguen a tener ciertos metodos.
"""

from abc import ABC, abstractmethod


class Entidad(ABC):
    """Molde general: toda entidad tiene un numero de identificacion propio."""

    # Contador compartido por todas las entidades: cada una nueva recibe el siguiente numero.
    _contador_id = 0

    def __init__(self):
        Entidad._contador_id += 1
        self._id = Entidad._contador_id

    @property
    def id(self):
        """El numero de identificacion solo se puede leer, no cambiar."""
        return self._id

    @abstractmethod
    def describir(self):
        """Cada clase hija esta obligada a explicar quien es (metodo abstracto)."""
        pass

    def __str__(self):
        return self.describir()