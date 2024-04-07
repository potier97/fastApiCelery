import logging
import colorlog

# Crear el logger con el nombre del módulo actual
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Formateador para el log en consola con colores
console_formatter = colorlog.ColoredFormatter(
    '%(log_color)s%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bold_red',
    }
)

# Manejador para el log en consola
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(console_formatter)

# Eliminar todos los manejadores existentes para evitar duplicados
logger.handlers = []

# Agregar el nuevo manejador con el formateador de colores
logger.addHandler(console_handler)
