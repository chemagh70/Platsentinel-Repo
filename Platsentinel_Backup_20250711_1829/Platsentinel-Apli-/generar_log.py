# codigo_fuente/api/app/logging_config.py
import logging
import os
from pathlib import Path
from datetime import datetime


def configurar_logging():
    # Crear directorio de logs si no existe
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # Nombre del archivo de log con marca temporal
    log_file = log_dir / f"platsentinel_{datetime.now().strftime('%Y%m%d')}.log"

    # Configuración del logger raíz
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
        handlers=[
            logging.FileHandler(log_file),  # Guardar logs en archivo
            logging.StreamHandler()  # Mostrar logs en consola
        ]
    )

    # Logger personalizado para PlatSentinel
    logger = logging.getLogger("PlatSentinel")

    # Configurar nivel de logging desde variables de entorno
    entorno = os.getenv("ENTORNO", "desarrollo")
    if entorno == "produccion":
        logger.setLevel(logging.WARNING)

    return logger


# Logger global para importar en otros módulos
logger = configurar_logging()