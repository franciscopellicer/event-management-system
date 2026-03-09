from abc import ABC, abstractmethod
from datetime import datetime



from Source.excepciones_propias.excepciones import FechaInvalidaError, AccederFechas, EstablecerEntradas, ModificacionEventoError, DeporteInvalidoError,MaximoEntradasFeriaError
from Source.enumerados.tipo_deporte import TipoDeporte
# Hecho
"""
Módulo eventos 

Este módulo define una jerarquía de clases para representar eventos de diferentes tipos, como espectáculos audiovisuales,
eventos deportivos y ferias empresariales. Cada clase proporciona funcionalidades específicas en funcion del tipo de evento para manejar
información relacionada con su tipo de evento y asegurar un acceso controlado a sus datos. Este módulo es parte fundamental de UmuTickets

Clases disponibles:
- Evento (clase abstracta): Base para todos los eventos.
- EspectaculoAudiovisual: Representa un espectáculo audiovisual.
- EventoDeportivo: Representa un evento deportivo.
- FeriaEmpresarial: Representa una feria empresarial.
"""
class Evento(ABC):
    """
        Clase base para representar un evento genérico.
        Proporciona atributos comunes y funcionalidad general para los eventos. Es abstracta y no puede ser instanciada
        directamente.
        Atributos de clase:
        - _ids_existentes: Lista que almacena los IDs únicos generados para cada evento.

        Métodos abstractos:
        - `calcular_precio_final`: Debe ser implementado en cada clase hija para calcular el precio final del evento.
        """
    _ids_existentes: list[int] = []
    def __init__(self, nombre: str, descripcion: str, direccion: str,
                 url: str, entradas_disponibles: int, precio_original: float, organizador,   #No declaro explicitamente la variable
                 fecha_1: datetime, fecha_2: datetime = None):                               #organizador porque puede ser de tipo UmuTickets
                                                                                            # o de tipo Organizador.
        """
                Inicializa los atributos de un evento.

                :param nombre: Nombre del evento.
                :param descripcion: Descripción del evento.
                :param direccion: Dirección donde se realizará el evento.
                :param url: URL asociada al evento.
                :param entradas_disponibles: Número de entradas disponibles.
                :param precio_original: Precio base de las entradas.
                :param organizador: Organizador del evento.
                :param fecha_1: Primera fecha del evento (o fecha única).
                :param fecha_2: Segunda fecha del evento (opcional).

                :raises FechaInvalidaError: Si no se proporcionan fechas válidas.
                """
        self._id = self.generar_id_unico()
        self._nombre = nombre
        self._descripcion = descripcion
        self._direccion = direccion
        self._url = url
        self._entradas_disponibles = entradas_disponibles
        self._lista_numeros_cogidos = []  # Lista de números de entradas ya cogidas
        self._precio_original = precio_original
        self._organizador = organizador

        # Lógica para manejar los tipos de fechas
        if fecha_1 is not None and fecha_2 is None:  # Solo fecha única
            self._fecha_unica = fecha_1
            self._es_evento_doble = False
        elif fecha_1 is None and fecha_2 is not None:  # Solo fecha de fin proporcionada
            self._fecha_unica = fecha_2
            self._es_evento_doble = False
        elif fecha_1 is not None and fecha_2 is not None:  # Ambas fechas proporcionadas
            self._fecha_inicio = min(fecha_1, fecha_2)
            self._fecha_fin = max(fecha_1, fecha_2)
            self._es_evento_doble = True
        else:  # Ninguna fecha proporcionada
            raise  FechaInvalidaError(f"Para crear el evento: {self.get_nombre()}, debe tener al menos una fecha en formato YYYY-MM-DD-HH-MM")

    @classmethod
    def generar_id_unico(cls):
        """
                Genera un ID único para un evento.

                :return: Un ID único como un número entero.
                """
        # Generar un nuevo ID único
        nuevo_id = len(cls._ids_existentes) + 1  # Comenzar desde 1 y asegurar que no se repita
        cls._ids_existentes.append(nuevo_id)  # Agregar el nuevo ID a los existentes
        return nuevo_id


    def es_evento_doble(self):
        """
                Verifica si el evento tiene dos fechas.

                :return: `True` si el evento es doble, `False` en caso contrario.
                """
        return self._es_evento_doble

    # Getters
    def get_direccion(self) -> str:
        return self._direccion

    def get_fecha_unica(self) -> datetime:
        if not self.es_evento_doble():
            return self._fecha_unica
        raise AccederFechas(f"El evento {self.get_nombre()} no tiene una fecha única.")

    def get_fecha_inicio(self) -> datetime:
        if self.es_evento_doble():
            return self._fecha_inicio
        raise AccederFechas(f"El evento {self.get_nombre()} al ser doble debe tener una fecha única.")  # Mensaje específico aquí

    def get_fecha_fin(self) -> datetime:
        if self.es_evento_doble():
            return self._fecha_fin
        raise AccederFechas(f"El evento {self.get_nombre()} al ser doble debe tener una fecha de fin.")  # Mensaje específico aquí, si accedes a la fecha fin es porque te refieres a un ento doble, si no seria a un evento unico

    def get_url(self) -> str:
        return self._url

    def get_id(self) -> int:
        return self._id

    def get_nombre(self) -> str:
        return self._nombre

    def get_precio_original(self) -> float:
        return self._precio_original

    def get_entradas_disponibles(self) -> int:
        return self._entradas_disponibles

    def get_lista_numero_entradas(self):
        return self._lista_numeros_cogidos

    def _set_direccion(self, direccion: str) -> None:
        """Debe recibir una string con una dirección"""
        self._direccion = direccion

    def _set_fecha_unica(self, fecha_unica: datetime) -> None:
        """Debe recibir una fecha datetime"""
        self._fecha_unica = fecha_unica

    def _set_fecha_inicio(self, fecha_inicio: datetime) -> None:
        """Debe recibir una fecha datetime"""
        self._fecha_inicio = fecha_inicio

    def _set_fecha_fin(self, fecha_fin: datetime) -> None:
        """Debe recibir una fecha datetime"""
        self._fecha_fin = fecha_fin

    def _set_url(self, url: str) -> None:
        """Debe recibir un string con la url"""
        self._url = url


    def __eq__(self, other):
        """"Metodo que comprara la igualdad entre dos eventos
            recibe otro evento como parametro
            retornará True si todos los atributos de los eventos coinciden y false en caso contrario"""
        if isinstance(other, Evento): # Necesario para comparar dos eventos
            # Comparar todos los atributos relevantes de manera directa
            return (self.get_nombre() == other.get_nombre() and
                    self.get_precio_original() == other.get_precio_original() and
                    self.get_direccion() == other.get_direccion() and
                    self.get_url() == other.get_url() and
                    self.get_entradas_disponibles() == other.get_entradas_disponibles() and
                    self.get_lista_numero_entradas() == other.get_lista_numero_entradas() and
                    # Comparar las fechas según el tipo de evento
                    (self.get_fecha_inicio() == other.get_fecha_inicio() and
                     self.get_fecha_fin() == other.get_fecha_fin()) if self.es_evento_doble() else
                    self.get_fecha_unica() == other.get_fecha_unica()
            )
        return False

    def __str__(self):
        return f"{self._nombre} - {self._descripcion} ({self._precio_original})"


    def set_entradas_disponibles(self, cantidad):
        """
                Establece el número de entradas disponibles para el evento.

                :param cantidad: Nuevo número de entradas disponibles.
                :raises EstablecerEntradas: Si el valor de `cantidad` es negativo.
                """
        if cantidad < 0:
            raise EstablecerEntradas(f"El numero de entradas para el evento {self.get_nombre} no puede ser negativo")
        self._entradas_disponibles = cantidad

    @abstractmethod
    def calcular_precio_final(self):
        """
                Calcula el precio final de las entradas para el evento.

                Debe ser implementado en las clases derivadas.
                """
        pass

    def modificar_evento(self, direccion: str = None, url: str = None,
                         fecha_inicio: datetime = None, fecha_fin: datetime = None,
                         fecha_unica: datetime = None):
        """
                Modifica los atributos del evento según los parámetros proporcionados.

                :param direccion: Nueva dirección del evento (opcional).
                :param url: Nueva url (opcional, para eventos dobles)
                :param fecha_inicio: Nueva fecha de inicio (opcional, para eventos dobles).
                :param fecha_fin: Nueva fecha de fin (opcional, para eventos dobles).
                :param fecha_unica: Nueva fecha única (opcional, para eventos simples).

                :return: `True` si el evento fue modificado, `False` en caso contrario.
                :raises ModificacionEventoError: Si no se proporciona ningún parámetro modificable.
                """

        modificado = False

        # Modificación de la dirección
        if direccion is not None:
            self._set_direccion(direccion)
            if url is None:
                self._set_url(direccion.replace(" ",'_')) #Si la variable url es None, entonces se establece una URL a partir de direccion, donde se reemplazan los espacios " " por guiones bajos "_"
            modificado = True                                          #Asi, si se nos cambia la ubicacion del evento y no se cambia la url asociada a esta direccion, forzamos a que cambie en funcion del nombre de este

        if url is not None:
            self._set_url(url)
            modificado = True


        # Modificación de las fechas
        if self.es_evento_doble():
            if fecha_inicio is not None and fecha_fin is not None:
                self._set_fecha_inicio(min(fecha_inicio, fecha_fin))
                self._set_fecha_fin(max(fecha_inicio, fecha_fin))
                modificado = True
        else:
            # Si no es un evento doble, se modifica la fecha única si se proporciona
            if fecha_unica is not None:
                self._set_fecha_unica(fecha_unica)
                modificado = True

        # Comprobación para asegurarse de que se han proporcionado parámetros para modificar
        if direccion is None and fecha_unica is None and fecha_inicio is None and fecha_fin is None:
            raise ModificacionEventoError("Para modificar el evento, debe establecer los datos necesarios para un evento, que son:"
                                          "\ndirección y la fecha o fechas dependiendo del evento")

        return modificado


# Evento Espectáculo Audiovisual
class EspectaculoAudiovisual(Evento):
    """
       Representa un Espectáculo Audiovisual.

       Un Espectáculo Audiovisual es un tipo de evento que incluye información sobre el artista o grupo
       que lo realiza y la edad mínima recomendada para asistir. Hereda de la clase base `Evento`.
       """
    def __init__(self, nombre: str, descripcion: str, direccion: str,
                 url: str, entradas_disponibles: int, precio_original: float, organizador, artista: str,
                 edad_minima: int, fecha_1: datetime, fecha_2: datetime = None):
        """
                Inicializa una instancia de la clase EspectaculoAudiovisual.

                Args:
                    nombre (str): Nombre del evento.
                    descripcion (str): Descripción del evento.
                    direccion (str): Dirección donde se realizará el evento.
                    url (str): URL relacionada con el evento.
                    entradas_disponibles (int): Cantidad de entradas disponibles.
                    precio_original (float): Precio original de las entradas.
                    organizador (Organizador): Organizador del evento.
                    artista (str): Artista o grupo que realiza el espectáculo.
                    edad_minima (int): Edad mínima recomendada para asistir al evento.
                    fecha_1 (datetime): Fecha inicial del evento.
                    fecha_2 (datetime, opcional): Fecha final del evento, si es un evento doble.
                """
        super().__init__(nombre, descripcion, direccion, url, entradas_disponibles, precio_original, organizador,
                         fecha_1, fecha_2)
        self._artista = artista  # Artista o grupo que realiza el espectáculo
        self._edad_minima = edad_minima  # Edad mínima recomendada

    def calcular_precio_final(self):
        """
                Calcula el precio final de las entradas para el espectáculo audiovisual.

                Returns:
                    float: El precio original, ya que no se aplican descuentos o ajustes en esta implementación.
                """
        return self._precio_original  # Aquí puedes aplicar lógica específica para calcular el precio

class EventoDeportivo(Evento):
    """
        Representa un Evento Deportivo.

        Un Evento Deportivo es un tipo de evento que está asociado a un deporte específico,
        como fútbol, tenis o baloncesto. Hereda de la clase base `Evento`.
        """
    def __init__(self, nombre: str, descripcion: str, direccion: str,
                 url: str, entradas_disponibles: int, precio_original: float, organizador, deporte: TipoDeporte,
                 fecha_1: datetime, fecha_2: datetime = None):
        """
                Inicializa una instancia de la clase EventoDeportivo.

                Args:
                    nombre (str): Nombre del evento.
                    descripcion (str): Descripción del evento.
                    direccion (str): Dirección donde se realizará el evento.
                    url (str): URL relacionada con el evento.
                    entradas_disponibles (int): Cantidad de entradas disponibles.
                    precio_original (float): Precio original de las entradas.
                    organizador (Organizador): Organizador del evento.
                    deporte (TipoDeporte): Tipo de deporte asociado al evento (fútbol, tenis o baloncesto).
                    fecha_1 (datetime): Fecha inicial del evento.
                    fecha_2 (datetime, opcional): Fecha final del evento, si es un evento doble.

                Raises:
                    DeporteInvalidoError: Si el deporte especificado no es válido.
                """
        if not isinstance(deporte, TipoDeporte):
            raise DeporteInvalidoError(f"El evento no puede ser de  {deporte}, tiene que ser de fútbol tenis o baloncesto")

        super().__init__(nombre, descripcion, direccion, url, entradas_disponibles, precio_original, organizador,
                         fecha_1, fecha_2)
        self._deporte = deporte  # Deporte del evento

    def calcular_precio_final(self):
        """
                Calcula el precio final de las entradas para el evento deportivo.

                Returns:
                    float: El precio original, ya que no se aplican descuentos o ajustes en esta implementación.
                """
        return self._precio_original  # Aquí puedes aplicar lógica específica para calcular el precio

class FeriaEmpresarial(Evento):
    """
        Representa una Feria Empresarial.

        Una Feria Empresarial es un tipo de evento que permite un número limitado de entradas (máximo 100).
        Hereda de la clase base `Evento` e incluye restricciones específicas para este tipo de eventos.

        Atributos:
            total_anulaciones (int): Contador global de anulaciones de entradas para todas las ferias empresariales.
        """
    _total_anulaciones = 0

    def __init__(self, nombre: str, descripcion: str, direccion: str,
                 url: str, entradas_disponibles: int, precio_original: float, organizador , fecha_1: datetime,
                 fecha_2: datetime = None):
        """
                Inicializa una instancia de la clase FeriaEmpresarial.

                Args:
                    nombre (str): Nombre del evento.
                    descripcion (str): Descripción del evento.
                    direccion (str): Dirección donde se realizará el evento.
                    url (str): URL relacionada con el evento.
                    entradas_disponibles (int): Cantidad de entradas disponibles (máximo 100).
                    precio_original (float): Precio original de las entradas.
                    organizador (Organizador): Organizador del evento.
                    fecha_1 (datetime): Fecha inicial del evento.
                    fecha_2 (datetime, opcional): Fecha final del evento, si es un evento doble.

                Raises:
                    MaximoEntradasFeriaError: Si el número de entradas disponibles supera el límite permitido de 100.
                """
        super().__init__(nombre, descripcion, direccion, url, entradas_disponibles, precio_original, organizador,
                         fecha_1, fecha_2)
        if entradas_disponibles > 100:
            raise MaximoEntradasFeriaError(f"No puedes crear una feria empresarial con {entradas_disponibles} entradas.\n"
                                           f"El numero máximo de entradas es de 100")

    @classmethod
    def get_total_anulaciones(cls):
        return cls._total_anulaciones

    @classmethod
    def sumar_anulaciones(cls):
        cls._total_anulaciones+=1

    def calcular_precio_final(self):
        """
                Calcula el precio final de las entradas para la feria empresarial.

                Returns:
                    float: El precio original, ya que no se aplican descuentos o ajustes en esta implementación.
                """
        return self._precio_original  # Aquí puedes aplicar lógica específica para calcular el precio
