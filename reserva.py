"""Clase Reserva: une cliente, servicio, duración y estado."""

from cliente import Cliente
from entidades import EntidadBase
from excepciones import (
    CalculoInconsistenteError,
    OperacionNoPermitidaError,
    ReservaInvalidaError,
    ServicioNoDisponibleError,
    SoftwareFJError,
)
from logger_config import obtener_logger
from servicios import Servicio

PENDIENTE = "PENDIENTE"
CONFIRMADA = "CONFIRMADA"
CANCELADA = "CANCELADA"
PROCESADA = "PROCESADA"

log = obtener_logger()


class Reserva(EntidadBase):
    """Reserva de un servicio por parte de un cliente."""

    def __init__(self, cliente, servicio, horas):
        if not isinstance(cliente, Cliente):
            raise ReservaInvalidaError("La reserva necesita un cliente válido")
        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("La reserva necesita un servicio válido")
        if not servicio.disponible:
            raise ServicioNoDisponibleError(
                f"El servicio '{servicio.nombre}' no está disponible"
            )
        # Si la duración no sirve para ese servicio, se encadena la excepción
        # para conservar la causa original (raise ... from ...).
        try:
            servicio.validar_parametros(horas)
        except SoftwareFJError as causa:
            raise ReservaInvalidaError(
                f"No se pudo crear la reserva: {causa}"
            ) from causa

        super().__init__()  # el id se asigna solo si la reserva es válida
        self._cliente = cliente
        self._servicio = servicio
        self._horas = horas
        self._estado = PENDIENTE
        self._total = None

    @property
    def cliente(self) -> Cliente:
        return self._cliente

    @property
    def servicio(self) -> Servicio:
        return self._servicio

    @property
    def horas(self) -> float:
        return self._horas

    @property
    def estado(self) -> str:
        return self._estado

    @property
    def total(self):
        return self._total

    def confirmar(self) -> None:
        if self._estado != PENDIENTE:
            raise OperacionNoPermitidaError(
                f"Reserva #{self.id}: solo se confirma una reserva PENDIENTE "
                f"(estado actual: {self._estado})"
            )
        self._estado = CONFIRMADA

    def cancelar(self) -> None:
        if self._estado in (CANCELADA, PROCESADA):
            raise OperacionNoPermitidaError(
                f"Reserva #{self.id}: no se puede cancelar una reserva {self._estado}"
            )
        self._estado = CANCELADA

    def procesar(self, impuesto=0.0, descuento=0.0) -> float:
        """Calcula el total y deja la reserva PROCESADA."""
        if self._estado != CONFIRMADA:
            raise OperacionNoPermitidaError(
                f"Reserva #{self.id}: debe estar CONFIRMADA para procesarse "
                f"(estado actual: {self._estado})"
            )
        try:
            total = self._servicio.calcular_costo(self._horas, impuesto, descuento)
        except (ValueError, TypeError, ArithmeticError) as causa:
            raise CalculoInconsistenteError(
                f"Reserva #{self.id}: falló el cálculo del costo"
            ) from causa
        else:
            self._total = total
            self._estado = PROCESADA
            return total
        finally:
            log.info("Intento de procesar reserva #%s (estado: %s)", self.id, self._estado)

    def describir(self) -> str:
        total = f", total ${self._total:,.2f}" if self._total is not None else ""
        return (
            f"Reserva #{self.id} [{self._estado}] {self._cliente.nombre} -> "
            f"{self._servicio.nombre} por {self._horas} h{total}"
        )
