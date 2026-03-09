"""
Modulo que alberga las clases UmuTickets y Estadisticas. Umu tickets es fundamental para la gestion de compras, reservas, eventos...
Es el módulo más importante del programa, es donde se gestiona toda la lógica del proyecto. Además la clase Estadísticas sirve de apoyo
a UmuTickets para calcular beneficios, anulaciones y lo relacionado con los ingresos y flujo de clientes y dinero
"""



from Source.excepciones_propias.excepciones import TipoEventoNoReconocidoError,EventoNoEncontradoError, NoHaySuficientesEntradasError, FechaMinimaReserva, ReservaYaPagada, CompraFueraDelPlazoError
from Source.eventos.evento import   EspectaculoAudiovisual
from Source.eventos.evento import EventoDeportivo
from Source.eventos.evento import FeriaEmpresarial
from Source.enumerados.tipo_evento import TipoEvento
from Source.eventos.evento import Evento
from Source.enumerados.tipo_deporte import TipoDeporte
from datetime import datetime, timedelta
from Source.clientes.cliente import Cliente, Reserva
from Source.empresas.ventas import Venta
from Source.interfaces.gestor_eventos import IGestorEventos
from Source.excepciones_propias.excepciones import ReservaInexistenteError


# Clase UMUTickets para gestionar eventos
class UMUTickets(IGestorEventos):
    """
        Clase que gestiona los eventos, clientes, reservas y ventas en UMUTickets.
        Permite agregar, modificar y eliminar eventos y clientes, así como realizar reservas, pagos y ventas de entradas.
        """
    def __init__(self):
        """
                Inicializa las listas vacias de clientes, eventos, reservas y ventas para su posterior gestión. No recibe parametros.
                """
        self._clientes: list[Cliente] = []
        self._eventos: list[Evento] = []
        self._reservas: list[Reserva] = []
        self._ventas: list[Venta] = []  # Lista de ventas para despues calcular su beneficio

    def get_clientes(self):
        return self._clientes

    def get_reservas(self):
        return self._reservas

    def get_ventas(self):
        return self._ventas

    def get_eventos(self):
        return self._eventos

    def agregar_cliente(self, cliente):
        """
                Agrega un cliente a la lista de clientes.

                :param cliente: Cliente que se desea agregar.
                """
        self.get_clientes().append(cliente)

    def eliminar_cliente(self, id_cliente: int):
        """
                Elimina un cliente de la lista dado su ID.

                :param id_cliente: ID del cliente a eliminar.
                """
        self._clientes = [cliente for cliente in self._clientes if
                          cliente.get_id() != id_cliente]  # Asi el que coincida con su id, sera omitido y no se pndra en la lsita de clientes

    def anyadir_reserva(self, reserva : Reserva):
        """
              Agrega una reserva a la lista de reservas.

              :param reserva: Reserva que se desea agregar.
              """
        self.get_reservas().append(reserva)

    @staticmethod
    def calcular_numero_entradas(evento: 'Evento'):
        """
                Calcula el siguiente número de entrada disponible para un evento.

                :param evento: El evento para el cual calcular el número de entrada.
                :return: El próximo número de entrada.
                """
        numero_entrada = len(evento.get_lista_numero_entradas()) + 1  # Comenzar desde 1 y asegurar que no se repita
        evento.get_lista_numero_entradas().append(numero_entrada)  # Agregar el nuevo ID a los existentes
        return numero_entrada


    def crear_evento(self, tipo: TipoEvento, nombre: str, descripcion: str, direccion: str,
                     url: str, entradas_disponibles: int, precio_original: float, fecha_1: datetime,
                     deporte: TipoDeporte = None, artista: str = None, edad_minima: int = None, fecha_2: datetime = None):
        """
                Crea un evento de tipo deportivo, espectáculo o feria, y lo agrega a la lista de eventos.
                :param tipo: Tipo de evento (deportivo, espectáculo o feria).
                :param nombre: Nombre del evento.
                :param descripcion: Descripción del evento.
                :param direccion: Dirección del evento.
                :param url: URL relacionada con el evento.
                :param entradas_disponibles: Número de entradas disponibles.
                :param precio_original: Precio original de la entrada.
                :param fecha_1: Fecha de inicio del evento.
                :param deporte: Tipo de deporte para eventos deportivos.
                :param artista: Artista para eventos de espectáculo.
                :param edad_minima: Edad mínima para eventos de espectáculo.
                :param fecha_2: Fecha de fin del evento si es un evento deportivo con duración múltiple.
                :raise TipoEventoNoReconocidoError si el evento no es de tipo deportivo, espectaculo audiovisual o feria empresarial.
                :return: El evento creado.
                """
        evento = None
        if tipo == TipoEvento.DEPORTIVO:
            evento = EventoDeportivo(nombre = nombre, descripcion= descripcion, direccion= direccion, url = url, entradas_disponibles = entradas_disponibles,
                                     precio_original = precio_original, fecha_1 = fecha_1, fecha_2 = fecha_2, organizador = self, deporte = deporte)
            self.get_eventos().append(evento)

        elif tipo == TipoEvento.ESPECTACULO:
            evento = EspectaculoAudiovisual(nombre = nombre,descripcion= descripcion, direccion= direccion, url = url, entradas_disponibles = entradas_disponibles,
                                             precio_original = precio_original, fecha_1 = fecha_1, fecha_2 = fecha_2, organizador = self, artista = artista, edad_minima = edad_minima)
            self.get_eventos().append(evento)

        elif tipo == TipoEvento.FERIA:
            evento = FeriaEmpresarial(nombre = nombre,descripcion= descripcion, direccion= direccion, url = url, entradas_disponibles = entradas_disponibles,
                                            precio_original = precio_original, fecha_1 = fecha_1, fecha_2 = fecha_2, organizador = self)
            self.get_eventos().append(evento)

        else:
            raise TipoEventoNoReconocidoError(f"El evento no puede ser de tipo {tipo}. Debe ser de tipo feria, deportivo o espectaculo audiovisual")
    

        self.agregar_evento(evento)
        return evento


    def agregar_evento(self, evento: Evento):
        """
                Agrega un evento a la lista de eventos.

                :param evento: Evento que se desea agregar.
                """
        #Asumimos que evento es de tipo evento
        self.get_eventos().append(evento)
      


    def modificar_evento(self, evento_id: int, direccion: str =None, url :str = None ,fecha_inicio: datetime =None,
                         fecha_fin: datetime =None, fecha_unica: datetime=None):
        """
              Modifica un evento dado su ID.

              :param evento_id: ID del evento a modificar.
              :param direccion: Nueva dirección del evento.
              :param url: URL del evento.
              :param fecha_inicio: Nueva fecha de inicio del evento.
              :param fecha_fin: Nueva fecha de fin del evento (solo para eventos con duración múltiple).
              :param fecha_unica: Nueva fecha para eventos de una sola fecha.
              :raise: EventoNoEncontradoError si no se encuentra el evento.
              :return: True si se modifica el evento.
              """
        evento: 'Evento' = self.obtener_evento_por_id(evento_id)
        if evento:
            evento.modificar_evento(direccion,url,fecha_inicio, fecha_fin, fecha_unica)
            return True
        else:
            raise EventoNoEncontradoError(f"El evento con id:{evento_id} no existe")


    def eliminar_evento(self, id_evento: int) -> bool:
        """
                Elimina un evento dado su ID.

                :param id_evento: ID del evento a eliminar.
                :return: True si el evento fue eliminado, False si no se encontró.
                """
        eventos = self.get_eventos()
        evento_encontrado = False
        index = 0

        while index < len(eventos) and not evento_encontrado:
            evento = eventos[index]
            if evento.get_id() == id_evento:
                eventos.pop(index)
                evento_encontrado = True
            else:
                index += 1

        if not evento_encontrado:
            raise EventoNoEncontradoError(f"El evento conn id:{id_evento} no existe")
        for cliente in self.get_clientes():
                for reserva in cliente.get_reservas():
                    if reserva.get_evento().get_id() == id_evento:
                        cliente.anular_reserva(reserva)
                    if reserva.get_esta_pagada():
                        reserva.get_cliente().get_tarjeta_personal().sumar_saldo(reserva.get_precio_final())
                for evento in cliente.get_eventos():
                    if evento.get_id() == id_evento:
                        for venta in self.get_ventas():
                            if venta.get_cliente().get_id() == cliente.get_eventos():
                                cliente.get_tarjeta_personal().sumar_saldo(venta.get_precio_final())
        #Pongo esto asi por lo siguiente: Puede ocurrir que hayas reservado la entrada coon 10 dias de antelacion,
        # y a falta de 6 dias puedes querer comprar mas(pero ya no puedes reservar) y si el evento es anulado el dia de antes
        #se tiene que tener en cuenta la reserva del evento ya que puede pasar que la hayas pagado o no, y la que si has pagado.
        #Asi cubrimos todas las posibilidades.
        #Nota: con los while, no se podría porque puedes tener muchas instancias tanto de reservas como eventos pagados




    def obtener_evento_por_id(self, evento_id):
        """
                Obtiene un evento dado su ID.

                :param evento_id: ID del evento a obtener.
                :return: Evento si se encuentra, None si no se encuentra.
                """
        index = 0
        while index < len(self.get_eventos()):
            evento = self._eventos[index]
            if evento.get_id() == evento_id:
                return evento
            index += 1
        return None


    def obtener_eventos_por_tipo(self, tipo_evento):
        """
                Obtiene eventos filtrados por tipo.

                :param tipo_evento: Tipo de evento a filtrar.
                :return: Lista de eventos filtrados por tipo.
                """
        return [evento for evento in self._eventos if isinstance(evento, tipo_evento)]




    #esta habria que quitarla?
    def reservar_entrada(self, cliente: Cliente, evento: Evento, cantidad: int):
        """
                Realiza una reserva de entradas para un cliente en un evento.

                :param cliente: Cliente que realiza la reserva.
                :param evento: Evento para el cual se realiza la reserva.
                :param cantidad: Cantidad de entradas a reservar.
                :return: Reserva creada si la operación fue exitosa.
                """
        if cantidad > evento.get_entradas_disponibles():
            raise NoHaySuficientesEntradasError(f"No hay suficientes entradas para el evento {evento.get_nombre()}."
                                                f" Se solicitaron {cantidad} entradas, quedan {evento.get_entradas_disponibles()} entradas.")

        fecha_actual = datetime.now()

        if evento.es_evento_doble():
            fecha_evento = evento.get_fecha_inicio()

        else:
            fecha_evento = evento.get_fecha_unica()


        if fecha_actual + timedelta(days=7) > fecha_evento and not evento.es_evento_doble():
            raise FechaMinimaReserva(f"La reserva al evento {evento.get_nombre()}, con fecha de inicio {evento.get_fecha_unica()}"
                                     f"\n debe realizarse con 7 dias de antelacion")

        if fecha_actual + timedelta(days=7) > fecha_evento and evento.es_evento_doble():
            raise FechaMinimaReserva(f"La reserva al evento {evento.get_nombre()}, con fecha de inicio {evento.get_fecha_inicio()}"
                                     f"\n debe realizarse con 7 dias de antelacion")


        # Calcular el precio base utilizando el método de cliente
        precio_base = cliente.calcular_precio_final(evento, cantidad)

        # Aplicar descuento del 10% para reservas
        precio_final = precio_base * 0.9  # Descuento del 10%

        # Crear reserva
        reserva = Reserva(evento = evento, fecha_reserva= fecha_actual,  cantidad=cantidad ,precio_final= precio_final, cliente= cliente )
        self.get_reservas().append(reserva)
        cliente.anyadir_reserva(reserva)
        evento.set_entradas_disponibles(evento.get_entradas_disponibles() - cantidad)  # Reducir entradas disponibles

        return reserva

    # METODO para que puede pagar despues de la reserva
    def pagar_reserva(self, reserva: Reserva):
        """
                Realiza el pago de una reserva de entradas para un cliente..
                :param reserva: Reserva que se está pagando.
                :return: True si se realizó el pago de la reserva.
                """
        if reserva is None:
            raise ReservaInexistenteError("La reserva no existe")
        if reserva.get_esta_pagada():
            raise ReservaYaPagada(f"Su reserva al evento {reserva.get_evento().get_nombre()} ya ha sido pagada")

        reserva.get_cliente().realizar_pago(reserva.get_precio_final())
        reserva.get_cliente().anyadir_evento(reserva.get_evento())  # Asi cuando paguemos el evento se nos añadira el evento al conjnto de eventos que un cleinte tiene, lo usaremos para las estdisticas
        reserva.marcar_como_pagada()
        venta = Venta(reserva.get_cliente(), reserva.get_evento(), reserva.get_cantidad(), reserva.get_evento().get_precio_original() * reserva.get_cantidad())
        self.get_ventas().append(venta)
        return True

      

    @staticmethod
    def pagar_sin_reserva( cliente: Cliente, evento: Evento, cantidad: int):
        """
            Permite realizar una compra de entradas sin necesidad de realizar una reserva previa.

            Verifica si hay suficientes entradas disponibles para la compra, si la compra se realiza antes del inicio del evento,
            y realiza el pago. También reduce las entradas disponibles en el evento y añade la reserva al cliente.

            :param cliente: Cliente que realiza la compra.
            :param evento: Evento para el cual se realiza la compra.
            :param cantidad: Cantidad de entradas a comprar.
            :raises NoHaySuficientesEntradasError: Si no hay suficientes entradas disponibles.
            :raises CompraFueraDelPlazoError: Si la compra se realiza después del inicio del evento.
            :return: True si la compra se realiza con éxito.
            """
        if cantidad > evento.get_entradas_disponibles():
            raise NoHaySuficientesEntradasError(f"No hay suficientes entradas disponible para el evento {evento.get_nombre()} "
                                                f"Se solicitaron {cantidad} entradas, quedan {evento.get_entradas_disponibles()} entradas. ")
        
        fecha_actual = datetime.now()

        if evento.es_evento_doble():
            fecha_evento = evento.get_fecha_inicio()
        else:
            fecha_evento = evento.get_fecha_unica()

        # Comprobar si la compra se realiza antes del inicio del evento
        if fecha_actual >= fecha_evento:
            raise CompraFueraDelPlazoError(f"EL evento {evento.get_nombre()} ya ha comenzado y no puede comprar entradas")
        # Calcular el precio total utilizando el metodo del cliente (sin descuento por reserva)
        precio_final = cliente.calcular_precio_final(evento, cantidad)

        # Realizar el pago
        cliente.realizar_pago(precio_final)
        cliente.anyadir_evento(evento)
        venta = Venta(cliente, evento, cantidad, precio_final= cantidad*evento.get_precio_original())

        # Reducir entradas disponibles en el evento
        evento.set_entradas_disponibles(evento.get_entradas_disponibles() - cantidad)

        return True  # Retorna True si la compra se realiza con éxito

    @staticmethod
    def anular_reserva(reserva: Reserva):
        """
            Anula una reserva existente, devolviendo las entradas al evento y eliminando la reserva del cliente.

            Si la reserva ya está pagada, no se puede anular. Además, si el evento es una feria empresarial,
            se registra el número de anulaciones.

            :param reserva: La reserva a anular.
            :raises ReservaInexistenteError: Si la reserva no existe.
            :raises ReservaYaPagada: Si la reserva ya ha sido pagada y no puede ser anulada.
            :return: True si la reserva se anuló correctamente.
            """
        if reserva is None:
            raise ReservaInexistenteError("La reserva no existe")
        if reserva.get_esta_pagada():
            raise ReservaYaPagada(f"Su reserva al evento {reserva.get_evento().get_nombre()} ya ha sido pagada y no se puede anular")

        evento = reserva.get_evento()
        entradas_actuales = evento.get_entradas_disponibles()
        nuevo_total = entradas_actuales + reserva.get_cantidad()
        evento.set_entradas_disponibles(nuevo_total)  # Usar el método set para actualizar las entradas
        reserva.get_cliente().anular_reserva(reserva)

        # Registrar anulaciones de ferias empresariales
        if isinstance(reserva.get_evento(), FeriaEmpresarial):
            FeriaEmpresarial.sumar_anulaciones()

        return True

    @staticmethod
    def mostrar_venta(fecha_venta: datetime, numeros_entrada: list[int], cliente: 'Cliente'):
        """
            Muestra los detalles de una venta realizada.

            Imprime la fecha de la venta, el ID del cliente y los números de las entradas vendidas.

            :param fecha_venta: Fecha en que se realizó la venta.
            :param numeros_entrada: Lista de números de entradas vendidas.
            :param cliente: Cliente que realizó la compra.
            """
        print(f"Venta realizada correctamente para el cliente ID {cliente.get_id()}")
        print(f"Fecha de venta: {fecha_venta}")
        for numero in numeros_entrada:
            print(f"Numero de entrada: {numero}")


    def vender_entrada(self, cliente: Cliente, evento: Evento, cantidad: int):
        """
                Realiza la venta de entradas, validando la disponibilidad y estado de las reservas.

                :param cliente: Cliente que realiza la compra.
                :param evento: Evento de las entradas.
                :param cantidad: Cantidad de entradas a vender.
                """
        entradas_registradas = []  # Necesario ya que cuando mostremos los datos si un cliente ha comprado varias entradas debemos aber cuantas para mostrarlas

        # Verificar si el cliente tiene una reserva para el evento
        for reserva in cliente.get_reservas():
            if reserva.get_evento() == evento:
                # Si hay una reserva, se procede a pagarla y registrar las entradas
                self.pagar_reserva(reserva)
                for _ in range(reserva.get_cantidad()):
                    numero_entrada = self.calcular_numero_entradas(evento)
                    entradas_registradas.append(numero_entrada)
                    evento.get_lista_numero_entradas().append(numero_entrada)



        # Si no hay reserva, se paga sin reserva y se registran las entradas
        if len(entradas_registradas) < cantidad:  # Lo hacemos asi ya que si un cliente quiere comprar 6 entradas y ha reservado 4, se pagen de una esas 4 con reserva y las otras si se puede sin reserva

            cantidad_sin_reserva = cantidad - len(entradas_registradas)
            self.pagar_sin_reserva(cliente, evento,
                                   cantidad_sin_reserva)  # Esta funcion ya comprueba si se pueden comprar dichas entradas

            for _ in range(cantidad_sin_reserva):
                numero_entrada = self.calcular_numero_entradas(evento)
                entradas_registradas.append(numero_entrada)
                evento.get_lista_numero_entradas().append(
                    numero_entrada)  # Calcular el precio de las entradas vendidas sin reserva


        # Mostrar la venta con todas las entradas registradas
        self.mostrar_venta(datetime.now(), entradas_registradas, cliente)


    def calcular_beneficio(self, evento: 'Evento'):
        """
            Calcula el beneficio de un evento determinado.

            :param evento: El evento para calcular su beneficio.
            :return: El beneficio calculado del evento.
            """
        return Estadisticas.calcular_beneficio(self, evento)


    def contar_socios_y_beneficio(self):
        """
            Cuenta los socios registrados y calcula el beneficio total.

            :return: El número de socios y el beneficio total.
            """
        return Estadisticas.contar_socios_y_beneficio(self)


    def porcentaje_anulaciones_ferias_empreariales(self):
        """
            Calcula el porcentaje de anulaciones en eventos de tipo FeriaEmpresarial.

            :return: El porcentaje de anulaciones de las ferias empresariales.
            """
        return Estadisticas.porcentaje_anulaciones_ferias_empreariales(self)


class Estadisticas:
    """
        Clase que contiene métodos estáticos para calcular estadísticas relacionadas
        con los eventos y las ventas en el sistema UMUTickets.
        """
    @staticmethod
    def calcular_beneficio(umu_tickets: 'UMUTickets', evento: 'Evento'):
        """
                Calcula el beneficio total de un evento en UMUTickets basado en las ventas y reservas.

                Dependiendo del tipo de evento (deportivo, audiovisual o feria empresarial),
                se aplica un porcentaje diferente sobre el precio final de cada venta o reserva.

                :param umu_tickets: Instancia de UMUTickets que contiene las ventas y reservas.
                :param evento: Evento para el cual se calcula el beneficio.
                :return: El beneficio total generado por las ventas y reservas del evento.
                """
        beneficio = 0
        for venta in umu_tickets.get_ventas() and umu_tickets.get_reservas():
            if isinstance(evento, EventoDeportivo):
                beneficio += venta.get_precio_final() * (0.1 if not venta.get_cliente().es_socio() else 0.05)
            elif isinstance(evento, EspectaculoAudiovisual):
                beneficio += venta.get_precio_final() * (0.15 if not venta.get_cliente().es_socio() else 0.1)
            elif isinstance(evento, FeriaEmpresarial):
                beneficio += venta.get_precio_final() * (0.1 if not venta.get_cliente().es_socio() else 0.05)
        return beneficio


    @staticmethod
    def contar_socios_y_beneficio(umu_tickets: 'UMUTickets'):
        """
                Cuenta el número de socios registrados en UMUTickets y calcula el beneficio generado por ellos.

                :param umu_tickets: Instancia de UMUTickets que contiene los clientes.
                :return: Una tupla con el número de socios y el beneficio total generado por ellos.
                """
        numero_socios = 0
        beneficio_socios = 0
        for cliente in umu_tickets.get_clientes():
            if cliente.es_socio():
                numero_socios += 1
                beneficio_socios += cliente.get_socio().get_ganancias()

        return numero_socios, beneficio_socios

    @staticmethod
    def porcentaje_anulaciones_ferias_empreariales(umu_tickets: 'UMUTickets'):
        """
                Calcula el porcentaje de anulaciones en eventos de tipo FeriaEmpresarial.

                Se divide el número total de anulaciones por el número total de eventos de tipo FeriaEmpresarial.

                :param umu_tickets: Instancia de UMUTickets que contiene los eventos.
                :return: El porcentaje de anulaciones en los eventos de tipo FeriaEmpresarial.
                """

        numero_eventos_ferias = 0
        for evento in umu_tickets.get_eventos():
            if isinstance(evento, FeriaEmpresarial):
                numero_eventos_ferias += 1
        return (FeriaEmpresarial.get_total_anulaciones() / numero_eventos_ferias) * 100