""""Módulo que alberga todas las excepciones específicas que pueden ir ocurriendo en el programa"""

class ClienteYaSocio(Exception):
    """Error lanzado cuando el número de socio es igual al ID del cliente."""
    def __init__(self, message):
        super().__init__(message)

class ClienteEmpresarialError(Exception):
    """Error lanzado cuando un cliente particular intenta acceder a un evento empresarial."""
    def __init__(self, message):
        super().__init__(message)

class SaldoInsuficienteError(Exception):
    """Error lanzado cuando no hay suficiente saldo en la tarjeta del cliente."""
    def __init__(self, message):
        super().__init__(message)


class CantidadInvalidaError(Exception):
    """Excepción lanzada cuando se intenta recargar un saldo con una cantidad no permitida."""
    def __str__(self):
        return "La cantidad a recargar debe ser 5, 10, 20 o 50 euros."


class PeriodoRenovacionError(Exception):
     """"Excepción lanzada cuando se intenta renovar o hacerte socio introduciendo un periodo no válido"""
     def __init__(self, message="Periodo inválido. Debe ser 30, 90 o 365 dias."):
        super().__init__(message)


class EventoNoEncontradoError(Exception):
    """Excepción lanzada cuando un evento no se encuentra."""
    def __init__(self, message):
        super().__init__(message)

class FechaInvalidaError(Exception):
    """Excepción lanzada cuando no se proporciona una fecha válida para el evento."""
    def __init__(self, message):
        super().__init__(message)

class AccederFechas(Exception):
    """"Error lanzado cuando ocurre una incongruencia en la gestion de fechas"""
    def __init__(self, message):
        super().__init__(message)

class EstablecerEntradas(Exception):
    """"Excepcion lanzada si se intenta establecer un nº de entradas negativo"""
    def __init__(self, message):
        super().__init__(message)

class DeporteInvalidoError(Exception):
    """Excepción lanzada para deportes no válidos."""
    def __init__(self, mensaje):
        super().__init__(mensaje)

class MaximoEntradasFeriaError(Exception):
    """Excepción lanzada cuando se excede el máximo de entradas para ferias empresariales."""
    def __init__(self, mensaje):
        super().__init__(mensaje)

class FechaMinimaReserva(Exception):
    """"Excepcion lanzada cuando se intenta hacer una reserva fuera de plazo"""
    def __init__(self,mensaje):
        super().__init__(mensaje)

class ReservaYaPagada(Exception):
    """"Excepcion lanzada cuando se intenta pagar una reserva que ya está pagada"""
    def __init__(self, mensaje):
        super().__init__(mensaje)

class RecargaNegativaError(Exception):
    """Excepción lanzada cuando se proporciona un valor incorrecto."""
    def __init__(self, mensaje):
        super().__init__(mensaje)


class NoHaySuficientesEntradasError(Exception):
    """Excepción lanzada cuando no hay suficientes entradas disponibles. En este caso lo gestiono desde la propia clase sin perder especificación"""
    def __init__(self, message):
        super().__init__(message)

class CompraFueraDelPlazoError(Exception):
    """Excepción lanzada cuando se intenta realizar una compra fuera del plazo permitido."""
    def __init__(self,mensaje):
        super().__init__(mensaje)

class TipoEventoNoReconocidoError(Exception):
    """Excepción lanzada cuando se proporciona un tipo de evento no reconocido."""
    def __init__(self,mensaje):
        super().__init__(mensaje)

class EventoNoEncontradoErrorOganizador(Exception):
    """Excepción lanzada cuando no se encuentra un evento específico. Logica gestionada desde la propia clase del error,
    recibe como parametro el id del evento no encontrado y el nombre de la empresa que organiza el evento"""
    def __init__(self, evento_id, nombre_organizador):
        message = f"Evento con ID {evento_id} no encontrado, en los eventos organizados por {nombre_organizador}."
        super().__init__(message)

class ModificacionEventoError(Exception):
    """Excepción lanzada cuando ocurre un error al modificar un evento."""
    def __init__(self,mensaje):
        super().__init__(mensaje)

class ReservaInexistenteError(Exception):
    """"Error creado que ayuda a gestionar la simulación de la interfaz gráfica y evita que se queden variables sin definir"""
    def __init__(self, mensaje):
        super().__init__(mensaje)
