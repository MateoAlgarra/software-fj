# Software FJ – Sistema de gestión de clientes, servicios y reservas

Proyecto de Programación Orientada a Objetos en Python (curso 213023, UNAD – Fase 4).
No usa base de datos: todo vive en objetos y listas; solo se escribe un archivo de logs.

## Cómo ejecutarlo

```bash
python main.py
```

Necesita Python 3.8 o superior y no instala nada extra. Los errores y eventos quedan en `logs/software_fj.log`.

## Archivos

| Archivo | Qué hace |
|---|---|
| `excepciones.py` | Excepciones personalizadas (todas heredan de `SoftwareFJError`) |
| `entidades.py` | Clase abstracta `EntidadBase` (id y `describir()`) |
| `cliente.py` | `Cliente` con datos privados y validaciones |
| `servicios.py` | `Servicio` (abstracta) + `ReservaSala`, `AlquilerEquipo`, `AsesoriaEspecializada` |
| `reserva.py` | `Reserva` con confirmar, cancelar y procesar |
| `gestor.py` | Listas internas y manejo central de errores |
| `logger_config.py` | Configuración del archivo de logs |
| `main.py` | Simulación de 13 operaciones válidas e inválidas |

## Conceptos aplicados

- **Abstracción:** `EntidadBase` y `Servicio` son clases abstractas (`ABC`).
- **Herencia:** `Cliente`, `Servicio` y `Reserva` heredan de `EntidadBase`; los tres servicios heredan de `Servicio`.
- **Polimorfismo:** cada servicio sobrescribe `calcular_costo_base`, `validar_parametros` y `describir`.
- **Encapsulación:** atributos privados con propiedades que validan.
- **Sobrecarga:** `calcular_costo(horas, impuesto=0, descuento=0)` tiene varias variantes con parámetros opcionales.
- **Excepciones:** personalizadas, `try/except`, `try/except/else`, `try/except/else/finally` y encadenamiento con `raise ... from ...`.
