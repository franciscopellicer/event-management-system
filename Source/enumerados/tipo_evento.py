
""""Modulo con el enumerado TipoEvento"""
from enum import Enum

# Enum para los tipos de evento
class TipoEvento(Enum):
    """
        Enumerado que representa los tipos de eventos disponibles.

        Los valores posibles son:
            - DEPORTIVO.
            - ESPECTACULO.
            - FERIA.
        """
    DEPORTIVO = 'deportivo'
    ESPECTACULO = 'espectaculo'
    FERIA = 'feria'