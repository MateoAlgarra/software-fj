"""Simulación de Software FJ: 12 operaciones (válidas e inválidas).

Se ejecuta con:  python main.py
Los errores se muestran en pantalla y quedan en logs/software_fj.log
"""

from gestor import GestorSoftwareFJ
from logger_config import RUTA_LOG, obtener_logger
from servicios import AlquilerEquipo, AsesoriaEspecializada, ReservaSala

log = obtener_logger()


def mostrar(numero, titulo, resultado, gestor):
    if resultado is not None:
        print(f"[{numero:02d}] OK     {titulo}\n       -> {resultado}")
    else:
        print(f"[{numero:02d}] ERROR  {titulo}\n       -> {gestor.ultimo_error}")


def main():
    log.info("=== Inicio de la simulación de Software FJ ===")
    g = GestorSoftwareFJ()

    # 1. Cliente válido
    ana = g.registrar_cliente(nombre="Ana Gómez", documento="1012345678",
                              email="ana@correo.com", telefono="3101234567")
    mostrar(1, "Registrar cliente válido (Ana)", ana, g)

    # 2. Cliente con correo inválido
    r = g.registrar_cliente(nombre="Luis Pérez", documento="80123456",
                            email="luis-sin-arroba", telefono="3001112233")
    mostrar(2, "Registrar cliente con correo inválido", r, g)

    # 3. Cliente con datos faltantes
    r = g.registrar_cliente(nombre="Carla Ruiz", documento="52987654")
    mostrar(3, "Registrar cliente con datos faltantes", r, g)

    # 4. Segundo cliente válido
    pedro = g.registrar_cliente(nombre="Pedro Mora", documento="79456123",
                                email="pedro@correo.com", telefono="3207654321")
    mostrar(4, "Registrar cliente válido (Pedro)", pedro, g)

    # 5. Servicios válidos (los tres tipos)
    sala = g.registrar_servicio(ReservaSala, nombre="Sala Innovación",
                                tarifa_hora=80_000, capacidad=25)
    equipo = g.registrar_servicio(AlquilerEquipo, nombre="Portátil Pro",
                                  tarifa_hora=15_000, tipo_equipo="Computador")
    asesoria = g.registrar_servicio(AsesoriaEspecializada, nombre="Arquitectura de software",
                                    tarifa_hora=120_000, nivel="senior")
    mostrar(5, "Crear los tres servicios", "\n         ".join(
        s.describir() for s in (sala, equipo, asesoria)), g)

    # 6. Servicio inválido (tarifa negativa)
    r = g.registrar_servicio(AlquilerEquipo, nombre="Proyector",
                             tarifa_hora=-500, tipo_equipo="Video")
    mostrar(6, "Crear servicio con tarifa negativa", r, g)

    # 7. Reserva exitosa de principio a fin (con impuesto y descuento)
    reserva1 = g.crear_reserva(ana, sala, 3)
    g.confirmar_reserva(reserva1)
    total = g.procesar_reserva(reserva1, impuesto=0.19, descuento=0.10)
    mostrar(7, "Reserva completa: crear, confirmar y procesar (IVA 19%, desc. 10%)",
            reserva1 if total is not None else None, g)

    # 8. Reserva con duración inválida (encadena la excepción)
    r = g.crear_reserva(pedro, asesoria, 10)
    mostrar(8, "Reserva de asesoría con 10 horas (máximo 6)", r, g)

    # 9. Reserva de un servicio no disponible
    equipo.disponible = False
    r = g.crear_reserva(pedro, equipo, 5)
    mostrar(9, "Reserva de equipo no disponible", r, g)
    equipo.disponible = True

    # 10. Procesar una reserva sin confirmar (operación no permitida)
    reserva2 = g.crear_reserva(pedro, equipo, 5)
    r = g.procesar_reserva(reserva2)
    mostrar(10, "Procesar reserva PENDIENTE sin confirmarla", r, g)

    # 11. Cancelar una reserva ya procesada
    r = g.cancelar_reserva(reserva1)
    mostrar(11, "Cancelar una reserva ya PROCESADA", r, g)

    # 12. Cálculo inconsistente (descuento del 150%) y recuperación posterior
    g.confirmar_reserva(reserva2)
    r = g.procesar_reserva(reserva2, impuesto=0.19, descuento=1.5)
    mostrar(12, "Procesar con descuento imposible (150%)", r, g)
    total = g.procesar_reserva(reserva2, impuesto=0.19)
    mostrar(13, "El sistema sigue activo: reintento correcto sin descuento",
            reserva2 if total is not None else None, g)

    print("\n--- Resumen ---")
    print(f"Operaciones ejecutadas: {g.operaciones}")
    print(f"Clientes: {len(g.clientes)} | Servicios: {len(g.servicios)} "
          f"| Reservas: {len(g.reservas)}")
    for reserva in g.reservas:
        print(" ", reserva)
    print(f"Log de errores y eventos: {RUTA_LOG}")
    log.info("=== Fin de la simulación ===")


if __name__ == "__main__":
    main()
