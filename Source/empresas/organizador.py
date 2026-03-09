"""
Módulo que define la clase Organizador, que hereda de la clase Empresa y la interfaz IGestorEventos.
Esta clase gestiona los eventos organizados por la empresa, permitiendo crear, modificar, eliminar y acceder a ellos.
Además, asegura que los IDs de los organizadores sean únicos y mantiene un registro de los eventos organizados.
"""

from Source.empresas.empresa import Empresa
from Source.enumerados.tipo_deporte import TipoDeporte
from Source.eventos.evento import EventoDeportivo
from Source.eventos.evento import  FeriaEmpresarial
from Source.enumerados.tipo_evento import TipoEvento
from Source.eventos.evento import EspectaculoAudiovisual
from datetime import datetime
from Source.empresas.umutickets import UMUTickets
from Source.interfaces.gestor_eventos import IGestorEventos
from Source.excepciones_propias.excepciones import TipoEventoNoReconocidoError,EventoNoEncontradoErrorOganizador

# Clase Organizador hereda de Empresa
class Organizador(Empresa, IGestorEventos):
    """
        Clase que representa a un organizador de eventos, hereda de la clase Empresa y de la interfaz IGestorEventos.
        Esta clase gestiona los eventos organizados por la empresa, permitiendo crear, modificar y eliminar eventos.

        Atributos:
            _ids_existentes: Lista que mantiene los IDs existentes para asegurar que los IDs de los organizadores sean únicos.
            _eventos_organizados: Lista de eventos organizados por la empresa.
        """
    _ids_existentes = []

    def __init__(self, razon_social: str, cif: str, telefono: str, direccion_postal: str):
        """
                Constructor de la clase Organizador. Inicializa los atributos de la clase Empresa y asigna un ID único
                para el organizador. También inicializa la lista de eventos organizados.

                :param razon_social.
                :param cif.
                :param telefono.
                :param direccion_postal.
                """
        super().__init__(razon_social, cif, telefono, direccion_postal)
        self._id = self.generar_id()
        self._eventos_organizados: list = []

    @classmethod
    def generar_id(cls):
        """
                Metodo de clase que genera un ID único para cada nuevo organizador.

                :return: El nuevo ID generado para el organizador.
                """
        nuevo_id = len(cls._ids_existentes) + 1  # Comenzar desde 1 y asegurar que no se repita
        cls._ids_existentes.append(nuevo_id)  # Agregar el nuevo ID a los existentes
        return nuevo_id

    def get_id(self):
        return self._id

    def get_eventos(self):
        return self._eventos_organizados
    
    def obtener_evento_por_id(self, evento_id):
        """
                Devuelve un evento dado su ID. Si no se encuentra el evento, devuelve None.

                :param evento_id: El ID del evento que se desea buscar.
                :return: El evento correspondiente al ID dado, o None si no se encuentra.
                """
        index = 0
        while index < len(self.get_eventos()):
            evento = self.get_eventos()[index]
            if evento.get_id() == evento_id:
                return evento
            index += 1
        return None

    def modificar_evento(self, evento_id: int, direccion: str = None, url : str = None,
                         fecha_inicio: datetime = None, fecha_fin: datetime = None,
                         fecha_unica: datetime = None):
        """
                Modifica los detalles de un evento ya existente dado su ID.
                :param url: El url que se quiere modificar.
                :param evento_id: El ID del evento que se desea modificar.
                :param direccion: Nueva dirección del evento (opcional).
                :param fecha_inicio: Nueva fecha de inicio del evento (opcional).
                :param fecha_fin: Nueva fecha de finalización del evento (opcional).
                :param fecha_unica: Nueva fecha única del evento (opcional).
                :return: El nuevo evento con las modificaciones realizadas.
                :raises EventoNoEncontradoErrorOganizador: Si el evento con el ID dado no se encuentra.
                """
        
        evento  = self.obtener_evento_por_id(evento_id)
        if evento in self.get_eventos():
            return evento.modificar_evento(direccion,url ,fecha_inicio, fecha_fin,
                                           fecha_unica)  # Se modifica tambien en umutickets al apuntar a la misma referencia de objeto
        raise EventoNoEncontradoErrorOganizador(evento_id= evento_id, nombre_organizador= self.get_razon_social())

    def crear_evento(self, tipo: TipoEvento, nombre: str, descripcion: str, direccion: str,
                     url: str, entradas_disponibles: int, precio_original: float, umuTickets: 'UMUTickets',
                     deporte: "TipoDeporte" = None, artista: str = None, edad_minima: int = None, fecha_1: datetime = None,
                     fecha_2: datetime = None):
        """
                Crea un nuevo evento dependiendo del tipo especificado (deportivo, espectáculo, feria).

                :param tipo: Tipo de evento (deportivo, espectáculo o feria).
                :param nombre: Nombre del evento.
                :param descripcion: Descripción del evento.
                :param direccion: Dirección donde se llevará a cabo el evento.
                :param url: URL del evento.
                :param entradas_disponibles: Número de entradas disponibles para el evento.
                :param precio_original: Precio original de las entradas.
                :param umuTickets: Instancia de UMUTickets donde se almacenan los eventos.
                :param deporte: El deporte si el evento es de tipo deportivo (opcional).
                :param artista: El nombre del artista si el evento es de tipo espectáculo (opcional).
                :param edad_minima: Edad mínima para acceder al evento de tipo espectáculo (opcional).
                :param fecha_1: Fecha de inicio del evento (opcional).
                :param fecha_2: Fecha de finalización del evento (opcional).
                :return: El evento creado.
                :raises TipoEventoNoReconocidoError: Si el tipo de evento no es reconocido.
                """
        evento = None
        if tipo == TipoEvento.DEPORTIVO and deporte is not None:
            evento = EventoDeportivo(nombre, descripcion, direccion, url, entradas_disponibles, precio_original, self,
                                     deporte, fecha_1, fecha_2)
        elif tipo == TipoEvento.ESPECTACULO:
            evento = EspectaculoAudiovisual(nombre, descripcion, direccion, url, entradas_disponibles,
                                            precio_original, self, artista, edad_minima, fecha_1, fecha_2)
        elif tipo == TipoEvento.FERIA:
            evento = FeriaEmpresarial(nombre, descripcion, direccion, url, entradas_disponibles, precio_original,
                                      self, fecha_1, fecha_2)
        else:
            raise TipoEventoNoReconocidoError(f"El evento no puede ser de tipo {tipo}. Debe ser de tipo feria, deportivo o espectaculo audiovisual")

        self.get_eventos().append(evento)
        umuTickets.agregar_evento(
            evento)  # Si lo crea el evento la empresa tambien se debe instanciar en los eventos de UmuTickets ya que en esta estan todos los eventos

        return evento

    def eliminar_evento(self, id_evento: int, umu_ticekts: 'UMUTickets') -> bool:
        """
                Elimina un evento existente dado su ID.
                :param id_evento: El ID del evento que se desea eliminar.
                :param umu_ticekts: Instancia de UMUTickets donde se elimina el evento.
                :return: True si el evento se eliminó correctamente.
                :raises EventoNoEncontradoErrorOganizador: Si el evento con el ID dado no se encuentra.
                """
        eventos = self.get_eventos()  # Obtener la lista de eventos
        evento_encontrado = False  # Variable de control para verificar si el evento fue eliminado
        index = 0


        while index < len(eventos) and not evento_encontrado:
            evento = eventos[index]

            # Si encontramos el evento con el ID proporcionado, lo eliminamos
            if evento.get_id() == id_evento:
                eventos.pop(index)  # Elimina el evento de la lista
                umu_ticekts.eliminar_evento(evento.get_id())
                evento_encontrado = True  # Marcar que el evento ha sido encontrado
            else:
                index += 1  # Solo incrementar si no se elimina el evento

        if evento_encontrado == False:
            raise EventoNoEncontradoErrorOganizador(evento_id=id_evento, nombre_organizador= self.get_razon_social())
        return evento_encontrado
        