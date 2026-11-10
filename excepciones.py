"""Excepciones personalizadas del sistema Software FJ.

Todas heredan de SoftwareFJError, así el programa puede atrapar cualquier
error propio con un solo `except SoftwareFJError`.
"""


class SoftwareFJError(Exception):
    """Error base de todo el sistema."""


class ParametroFaltanteError(SoftwareFJError):
    """Falta un dato obligatorio."""


class ClienteInvalidoError(SoftwareFJError):
    """Los datos del cliente no cumplen las validaciones."""


class ServicioInvalidoError(SoftwareFJError):
    """Los datos o parámetros del servicio no son válidos."""


class ServicioNoDisponibleError(SoftwareFJError):
    """El servicio existe pero no se puede reservar ahora."""


class ReservaInvalidaError(SoftwareFJError):
    """La reserva no se pudo crear por datos incorrectos."""


class OperacionNoPermitidaError(SoftwareFJError):
    """La acción no está permitida en el estado actual de la reserva."""


class CalculoInconsistenteError(SoftwareFJError):
    """El cálculo de costos dio un resultado imposible o falló."""
