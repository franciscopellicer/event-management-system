""""Modulo con el enumerado TipoDeporte"""

from enum import Enum

# Evento Deportivo
class TipoDeporte(Enum):
    """
        Enumerado que representa los tipos de deportes disponibles.

        Los valores posibles son:
            - FUTBOL.
            - TENIS.
            - BALONCESTO.
        """
    FUTBOL = "Fútbol"
    TENIS = "Tenis"
    BALONCESTO = "Baloncesto"