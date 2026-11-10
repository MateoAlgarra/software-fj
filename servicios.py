"""Servicio (clase abstracta) y tres servicios especializados.

Polimorfismo: los tres servicios responden igual a calcular_costo(),
describir() y validar_parametros(), pero cada uno lo hace a su manera.
"""

from abc import ABC, abstractmethod

from entidades import EntidadBase
from excepciones import CalculoInconsistenteError, ServicioInvalidoError

IVA_POR_DEFECTO = 0.19


class Servicio(EntidadBase, ABC):
    """Clase abstracta de todos los servicios de Software FJ."""

    def __init__(self, nombre, tarifa_hora, disponible=True):
        super().__init__()
        if not isinstance(nombre, str) or len(nombre.strip()) < 3:
            raise ServicioInvalidoError(f"Nombre de servicio inválido: {nombre!r}")
        if not isinstance(tarifa_hora, (int, float)) or isinstance(tarifa_hora, bool):
            raise ServicioInvalidoError(f"La tarifa debe ser un número: {tarifa_hora!r}")
        if tarifa_hora <= 0:
            raise ServicioInvalidoError(f"La tarifa debe ser mayor a 0: {tarifa_hora}")
        self._nombre = nombre.strip()
        self._tarifa_hora = float(tarifa_hora)
        self._disponible = bool(disponible)

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def tarifa_hora(self) -> float:
        return self._tarifa_hora

    @property
    def disponible(self) -> bool:
        return self._disponible

    @disponible.setter
    def disponible(self, valor: bool):
        self._disponible = bool(valor)

    # ---- métodos que cada servicio debe sobrescribir ----
    @abstractmethod
    def calcular_costo_base(self, horas: float) -> float:
        """Costo sin impuestos ni descuentos."""

    @abstractmethod
    def validar_parametros(self, horas: float) -> bool:
        """Lanza ServicioInvalidoError si la duración no sirve para este servicio."""

    # ---- método sobrecargado (parámetros opcionales) ----
    def calcular_costo(self, horas, impuesto=0.0, descuento=0.0) -> float:
        """Calcula el costo en sus distintas variantes.

        Python no tiene sobrecarga como Java, así que se simula con
        parámetros opcionales:
            calcular_costo(2)                      -> costo base
            calcular_costo(2, impuesto=0.19)       -> con impuesto
            calcular_costo(2, descuento=0.10)      -> con descuento
            calcular_costo(2, 0.19, 0.10)          -> con ambos
        """
        for nombre, valor in (("impuesto", impuesto), ("descuento", descuento)):
            if not isinstance(valor, (int, float)) or not 0 <= valor < 1:
                raise CalculoInconsistenteError(
                    f"{nombre} debe estar entre 0 y 1 (sin incluir 1): {valor!r}"
                )
        self.validar_parametros(horas)
        base = self.calcular_costo_base(horas)
        total = base * (1 - descuento) * (1 + impuesto)
        if total <= 0:
            raise CalculoInconsistenteError(f"El costo calculado no es válido: {total}")
        return round(total, 2)

    @abstractmethod
    def describir(self) -> str:
        """Descripción del servicio."""


class ReservaSala(Servicio):
    """Reserva de salas. Las salas grandes tienen recargo."""

    def __init__(self, nombre, tarifa_hora, capacidad, disponible=True):
        super().__init__(nombre, tarifa_hora, disponible)
        if not isinstance(capacidad, int) or isinstance(capacidad, bool) or capacidad <= 0:
            raise ServicioInvalidoError(f"Capacidad inválida: {capacidad!r}")
        self._capacidad = capacidad

    @property
    def capacidad(self) -> int:
        return self._capacidad

    def validar_parametros(self, horas) -> bool:
        if not isinstance(horas, (int, float)) or not 1 <= horas <= 8:
            raise ServicioInvalidoError(
                f"Una sala se reserva entre 1 y 8 horas, no {horas!r}"
            )
        return True

    def calcular_costo_base(self, horas) -> float:
        recargo = 1.15 if self._capacidad > 20 else 1.0
        return self._tarifa_hora * horas * recargo

    def describir(self) -> str:
        return (
            f"Sala '{self.nombre}' para {self._capacidad} personas, "
            f"${self.tarifa_hora:,.0f} por hora"
        )


class AlquilerEquipo(Servicio):
    """Alquiler de equipos. Cobra un depósito fijo además de las horas."""

    DEPOSITO = 50_000

    def __init__(self, nombre, tarifa_hora, tipo_equipo, disponible=True):
        super().__init__(nombre, tarifa_hora, disponible)
        if not isinstance(tipo_equipo, str) or not tipo_equipo.strip():
            raise ServicioInvalidoError("Debe indicar el tipo de equipo")
        self._tipo_equipo = tipo_equipo.strip()

    @property
    def tipo_equipo(self) -> str:
        return self._tipo_equipo

    def validar_parametros(self, horas) -> bool:
        if not isinstance(horas, (int, float)) or not 1 <= horas <= 72:
            raise ServicioInvalidoError(
                f"Un equipo se alquila entre 1 y 72 horas, no {horas!r}"
            )
        return True

    def calcular_costo_base(self, horas) -> float:
        return self._tarifa_hora * horas + self.DEPOSITO

    def describir(self) -> str:
        return (
            f"Equipo '{self.nombre}' ({self._tipo_equipo}), "
            f"${self.tarifa_hora:,.0f} por hora + depósito de ${self.DEPOSITO:,}"
        )


class AsesoriaEspecializada(Servicio):
    """Asesoría con un experto. El nivel senior cuesta 50% más."""

    NIVELES = {"junior": 1.0, "senior": 1.5}

    def __init__(self, nombre, tarifa_hora, nivel="junior", disponible=True):
        super().__init__(nombre, tarifa_hora, disponible)
        if not isinstance(nivel, str) or nivel.lower() not in self.NIVELES:
            raise ServicioInvalidoError(
                f"Nivel inválido: {nivel!r} (use 'junior' o 'senior')"
            )
        self._nivel = nivel.lower()

    @property
    def nivel(self) -> str:
        return self._nivel

    def validar_parametros(self, horas) -> bool:
        if not isinstance(horas, (int, float)) or not 0.5 <= horas <= 6:
            raise ServicioInvalidoError(
                f"Una asesoría dura entre 0.5 y 6 horas, no {horas!r}"
            )
        return True

    def calcular_costo_base(self, horas) -> float:
        return self._tarifa_hora * horas * self.NIVELES[self._nivel]

    def describir(self) -> str:
        return (
            f"Asesoría '{self.nombre}' nivel {self._nivel}, "
            f"${self.tarifa_hora:,.0f} por hora"
        )
