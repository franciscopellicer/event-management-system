""""Módulo que contiene la interfaz IGestorEventos, una clase utilizazda para modelar el comportamiento que deben de tener las clases UmuTickets y organizador
sin importar como gestione cada una los metodos que deben implementar: crear_evento modificar_evento y eliminar_evento"""

from abc import ABC, abstractmethod
from Source.enumerados.tipo_evento import TipoEvento
import datetime

class IGestorEventos(ABC):
    """
        Interfaz abstracta para gestionar eventos.

        Define los métodos que deben implementarse para crear, modificar y eliminar eventos.
        """
    @abstractmethod
    def crear_evento(self, tipo: TipoEvento, nombre: str, descripcion: str, direccion: str,
                     url: str, entradas_disponibles: int, precio_original: float, umuTickets = None, #No le ponemos el tipo umuticeks para evitar importacion circular, y ponemos none ya que en organizadro se pasa como instancia y en umuticekts no
                     deporte: str = None, artista: str = None, edad_minima: int = None, fecha_1: datetime = None,
                     fecha_2: datetime = None):
        """
             Crea un nuevo evento con los parámetros especificados.

             Args:
                 tipo (TipoEvento): Tipo del evento.
                 nombre (str): Nombre del evento.
                 descripcion (str): Descripción del evento.
                 direccion (str): Dirección donde se llevará a cabo el evento.
                 url (str): URL asociada al evento.
                 entradas_disponibles (int): Cantidad de entradas disponibles para el evento.
                 precio_original (float): Precio original de las entradas.
                 umuTickets: Instancia de UMUTickets para gestionar el evento (opcional).
                 deporte (str, optional): Deporte asociado, si aplica (para eventos deportivos).
                 artista (str, optional): Artista involucrado, si aplica (para espectáculos).
                 edad_minima (int, optional): Edad mínima requerida, si aplica.
                 fecha_1 (datetime, optional): Fecha de inicio del evento o primera fecha asociada.
                 fecha_2 (datetime, optional): Fecha de fin del evento o segunda fecha asociada.
             """
        pass


    @abstractmethod
    def modificar_evento(self, evento_id: int, direccion: str = None, url: str = None,
                         fecha_inicio: datetime = None, fecha_fin: datetime = None,
                         fecha_unica: datetime = None):
        """
                Modifica los detalles de un evento existente.

                Args:
                    evento_id (int): Identificador único del evento a modificar.
                    direccion (str, optional): Nueva dirección del evento.
                    url (str, optional): Nueva URL asociada al evento.
                    fecha_inicio (datetime, optional): Nueva fecha de inicio del evento.
                    fecha_fin (datetime, optional): Nueva fecha de finalización del evento.
                    fecha_unica (datetime, optional): Nueva fecha única del evento, si aplica.

                """
        pass

    @abstractmethod
    def eliminar_evento(self, id_evento, umu_tickets = None):
        """
                Elimina un evento identificado por su ID.

                Args:
                    id_evento (int): Identificador único del evento a eliminar.
                    umu_tickets: Instancia de UMUTickets para gestionar el evento (opcional).

                """
        pass
   

    