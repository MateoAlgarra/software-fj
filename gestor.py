"""Gestor central: guarda clientes, servicios y reservas en listas internas.

Cada operación pasa por `_intentar`, que atrapa los errores, los escribe
en el log y deja el sistema funcionando (nunca se cae).
"""

from cliente import Cliente
from excepciones import ClienteInvalidoError, SoftwareFJError
from logger_config import obtener_logger
from reserva import Reserva

log = obtener_logger()


class GestorSoftwareFJ:
    def __init__(self):
        self._clientes = []
        self._servicios = []
        self._reservas = []
        self.ultimo_error = None
        self.operaciones = 0

    @property
    def clientes(self):
        return tuple(self._clientes)

    @property
    def servicios(self):
        return tuple(self._servicios)

    @property
    def reservas(self):
        return tuple(self._reservas)

    def _intentar(self, nombre_operacion, funcion, *args, **kwargs):
        """Ejecuta una operación con manejo completo de excepciones.

        Devuelve el resultado, o None si hubo error (el error queda en el log).
        """
        self.ultimo_error = None
        try:
            resultado = funcion(*args, **kwargs)
        except SoftwareFJError as error:
            self.ultimo_error = f"{type(error).__name__}: {error}"
            log.error("%s | %s", nombre_operacion, self.ultimo_error)
            if error.__cause__ is not None:
                log.error("   causa original: %s: %s",
                          type(error.__cause__).__name__, error.__cause__)
            return None
        except Exception as error:  # error inesperado: se registra igual
            self.ultimo_error = f"Error inesperado {type(error).__name__}: {error}"
            log.exception("%s | %s", nombre_operacion, self.ultimo_error)
            return None
        else:
            log.info("%s | OK", nombre_operacion)
            return resultado
        finally:
            self.operaciones += 1

    # ---- registros ----
    def registrar_cliente(self, **datos):
        def accion():
            cliente = Cliente(**datos)
            if any(c.documento == cliente.documento for c in self._clientes):
                raise ClienteInvalidoError(
                    f"Ya existe un cliente con documento {cliente.documento}"
                )
            self._clientes.append(cliente)
            return cliente

        return self._intentar("Registrar cliente", accion)

    def registrar_servicio(self, clase_servicio, **datos):
        def accion():
            servicio = clase_servicio(**datos)
            self._servicios.append(servicio)
            return servicio

        return self._intentar(f"Crear servicio {clase_servicio.__name__}", accion)

    # ---- reservas ----
    def crear_reserva(self, cliente, servicio, horas):
        def accion():
            reserva = Reserva(cliente, servicio, horas)
            self._reservas.append(reserva)
            return reserva

        return self._intentar("Crear reserva", accion)

    def confirmar_reserva(self, reserva):
        return self._intentar(f"Confirmar reserva", lambda: reserva.confirmar() or reserva)

    def cancelar_reserva(self, reserva):
        return self._intentar(f"Cancelar reserva", lambda: reserva.cancelar() or reserva)

    def procesar_reserva(self, reserva, impuesto=0.0, descuento=0.0):
        return self._intentar(
            "Procesar reserva", reserva.procesar, impuesto, descuento
        )
