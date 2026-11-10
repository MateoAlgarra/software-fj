"""Configuración del archivo de logs (única persistencia del sistema)."""

import logging
from pathlib import Path

RUTA_LOG = Path(__file__).resolve().parent / "logs" / "software_fj.log"


def obtener_logger() -> logging.Logger:
    """Devuelve el logger del sistema, listo para escribir en el archivo."""
    logger = logging.getLogger("software_fj")
    if logger.handlers:  # evita duplicar mensajes si se llama varias veces
        return logger

    RUTA_LOG.parent.mkdir(parents=True, exist_ok=True)
    logger.setLevel(logging.INFO)
    manejador = logging.FileHandler(RUTA_LOG, mode="w", encoding="utf-8")
    manejador.setFormatter(
        logging.Formatter("%(asctime)s | %(levelname)-8s | %(message)s")
    )
    logger.addHandler(manejador)
    return logger
