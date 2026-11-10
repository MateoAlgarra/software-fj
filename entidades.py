"""Clase abstracta que representa cualquier entidad general del sistema."""

from abc import ABC, abstractmethod


class EntidadBase(ABC):
    """Base de Cliente, Servicio y Reserva.

    Da un identificador único a cada objeto y obliga a las clases hijas
    a implementar `describir()` (abstracción + polimorfismo).
    """

    _contadores = {}  # un contador por tipo: Cliente, Servicio y Reserva

    def __init__(self):
        # Busca la clase que hereda directo de EntidadBase (Cliente, Servicio...)
        tipo = next(c for c in type(self).__mro__ if EntidadBase in c.__bases__)
        EntidadBase._contadores[tipo] = EntidadBase._contadores.get(tipo, 0) + 1
        self._id = EntidadBase._contadores[tipo]

    @property
    def id(self) -> int:
        return self._id

    @abstractmethod
    def describir(self) -> str:
        """Texto corto que describe la entidad."""

    def __str__(self) -> str:
        return self.describir()
