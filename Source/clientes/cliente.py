"""
En este módulo se definen las clases necesarias para gestionar clientes y sus reservas en UmuTickets.
Incluye clases para modelar tanto a clientes particulares como empresariales, permitiendo manejar sus reservas,
eventos asociados, y la interacción con pagos.

Clases:
    Cliente.
    ClienteParticular
    ClienteEmpresarial.
    Reserva
"""


from Source.excepciones_propias.excepciones import ClienteYaSocio, ClienteEmpresarialError, SaldoInsuficienteError
from datetime import datetime
from Source.clientes.tarjetas import TarjetaPersonal
from Source.clientes.personas import Persona
from Source.eventos.evento import Evento
from Source.eventos.evento import FeriaEmpresarial
from Source.eventos.evento import EventoDeportivo
from Source.eventos.evento import EspectaculoAudiovisual
from Source.clientes.socio import Socio
from Source.empresas.empresa import Empresa
import random



class Cliente:
    """
        Clase base que  modela clientes. Maneja clientes únicos mediante IDs únicos
        y ofrece metodos relacionadas con eventos y reservas.
        """
    _ids_existentes: list[int] = []

    def __init__(self, tarjeta_credito=None):  # Se mantiene el argumento de tarjeta_credito
        """
                Inicializa un cliente con un ID único, una tarjeta de crédito,
                y atributos para reservas y eventos.

                Args:
                    tarjeta_credito (TarjetaPersonal), tarjeta de débito del cliente.
                """
        self._id_cliente = self.generar_id_unico()
        self._tarjeta_credito = tarjeta_credito if tarjeta_credito else TarjetaPersonal()  # Usa el valor pasado o crea uno por defecto
        self._es_socio = False
        self._eventos: list[Evento] = []
        self._reservas: list["Reserva"] = []

    @classmethod
    def _get_lista_ids(cls) -> list[int]:
        return cls._ids_existentes

    def get_reservas(self) -> list["Reserva"]:
        return self._reservas
    
    def get_tarjeta_personal(self) -> "TarjetaPersonal":
        return self._tarjeta_credito

    def get_id(self) -> int:
        return self._id_cliente

    def get_eventos(self) -> list["Evento"]:
        return self._eventos

    def get_socio(self) -> Socio:
        return self._socio
    
    def es_socio(self) ->bool:
        return self._es_socio
    
    def _set_socio(self) -> None:
        """No hay restricciones, metodo auxiliar que marca el atributo _es_socio como True cuando un cliente se convierte en socio """
        self._es_socio = True

    def anyadir_reserva(self, reserva: "Reserva") -> None:
        """
                Añade una reserva a la lista de reservas del cliente.

                Args:
                    reserva (Reserva): Reserva a añadir.
                """
        self.get_reservas().append(reserva)

    def anyadir_evento(self, evento: "Evento") -> None:
        """
                Añade un evento a la lista de eventos del cliente.

                Args:
                    evento (Evento): Evento a añadir.
                """
        self.get_eventos().append(evento)

    def anular_reserva(self, reserva: 'Reserva') -> bool:
        """
                Anula una reserva del cliente. Lanza un error si la reserva no existe.

                Args:
                    reserva (Reserva): Reserva a eliminar.

                Raises:
                    ValueError: Si la reserva no está en la lista del cliente.

                Returns:
                     True si se ha podidio hacer la anulación de la reserva
                """
        if reserva not in self.get_reservas():
            raise ValueError("No existe la reserva")
        self.get_reservas().remove(reserva)
        return True

    def anular_evento_cliente(self, id_evento) -> bool:
        """Metodo que saca de la lista de eventos un evento si este ha sido anulado
           :param id_evento: ID del evento.
           :return True si se ha eliminado, False en caso contrario.
           """
        index = 0
        eventos_cliente = self.get_eventos()
        eventos_cliente_encontrado = False
        while index < len(eventos_cliente) and not eventos_cliente_encontrado:
            if eventos_cliente[index].get_id() == id_evento:
                eventos_cliente.pop(index) #La suma de saldo la tendremos en cuenta en umutickets ya que ahi, tenemos accedso a las ventas
                eventos_cliente_encontrado = True
            else: index += 1
        return eventos_cliente_encontrado

    @classmethod
    def generar_id_unico(cls) -> int :
        """
                Genera un ID único para el cliente.

                Returns:
                    int: ID único generado.
                """
        nuevo_id = random.randint(1, 10000)   #si necesitas añadir mas de 100000 clientes amplias el numero
        while nuevo_id in cls._get_lista_ids():
            nuevo_id = random.randint(1, 10000)
        cls._get_lista_ids().append(nuevo_id)
        return nuevo_id

    def hacerse_socio(self, tiempo) -> bool:
        """
                Convierte al cliente en socio por un período de tiempo.

                Args:
                    tiempo (int): Duración de la membresía.

                Raises:
                    ClienteYaSocio: Si el cliente ya es socio.

                Returns:
                    True si se ha podido hacerse socio
                """
        if not self.es_socio():  # Usar _socio directamente
            self._socio = Socio(tiempo)
            self._set_socio()
            return True
        else:
            raise ClienteYaSocio(f"El cliente con id {self.get_id()} ya es socio")


    def calcular_precio_final(self, evento: Evento, cantidad: int) -> float:
        """
                Calcula el precio final para una reserva.

                Args:
                    evento (Evento): Evento a reservar.
                    cantidad (int): Cantidad de entradas.

                Returns:
                    float: Precio final calculado.

                Raises:
                    ClienteEmpresarialError: Si un cliente no empresarial reserva una feria empresarial.
                """
        precio_base = evento.get_precio_original() * cantidad
        precio_final = precio_base

    # Aplicar descuento si el cliente es socio
        if self.es_socio():  # Ahora accede a _es_socio directamente
            if isinstance(evento, FeriaEmpresarial) and not isinstance(self, ClienteEmpresarial):
                raise ClienteEmpresarialError(f"El cliente {self.get_id()} no es un cliente empresarial y no puede reservar en una feria empresarial")
            if isinstance(evento, FeriaEmpresarial):
                precio_final *= 0.7  # Descuento del 30%
            elif isinstance(evento, (EventoDeportivo, EspectaculoAudiovisual)):
                precio_final *= 0.8  # Descuento del 20%

        # Calcular aumentos de precio segun la disponibilidad de entradas
        entradas_totales = evento.get_entradas_disponibles()
        if isinstance(evento, EventoDeportivo):
            if evento.get_entradas_disponibles() <= 0.25 * entradas_totales:
                precio_final *= 1.1  # Aumento del 10%
        elif isinstance(evento, EspectaculoAudiovisual):
            if evento.get_entradas_disponibles() <= 0.1 * entradas_totales:
                precio_final *= 1.3  # Aumento del 30%

        return precio_final


    def realizar_pago(self, cantidad: float) -> bool:
        """
                Realiza un pago desde la tarjeta de crédito del cliente.

                Args:
                    cantidad (float): Cantidad a pagar.

                Raises:
                    SaldoInsuficienteError: Si el saldo de la tarjeta es insuficiente.

                Returns:
                    True si se ha podido realizar la pago
                """
        if  cantidad <= self._tarjeta_credito.get_saldo():
            self.get_tarjeta_personal().quitar_saldo(cantidad)
            return True
        else:
            raise SaldoInsuficienteError(f"Saldo insuficiente. Saldo restante= {self.get_tarjeta_personal().get_saldo()} euros")

class ClienteParticular(Persona, Cliente):
    """
        Clase modeladora de un cliente particular. Hereda de las clases Persona y Cliente. Un cliente particular tiene los
        atributos y comportamientos de una persona, además de una TarjetaPersonal para realizar transacciones.

        """

    def __init__(self, nombre: str, apellidos: str, direccion_postal: str, dni: str, tarjeta_credito: TarjetaPersonal):
        """
                Constructor de la clase ClienteParticular. Inicializa los atributos de Persona y Cliente, además de asociar una
                tarjeta personal para manejar las transacciones.

                :param nombre: El nombre del cliente particular.
                :param apellidos: Los apellidos del cliente particular.
                :param direccion_postal: La dirección postal del cliente particular.
                :param dni: El DNI del cliente particular.
                :param tarjeta_credito: El objeto de tipo TarjetaPersonal que representa la tarjeta de crédito del cliente.
                """
        Persona.__init__(self, nombre, apellidos, direccion_postal, dni)
        Cliente.__init__(self, tarjeta_credito)  # Se pasa el objeto TarjetaPersonal


class ClienteEmpresarial(Cliente):

    """Clase que representa a un cliente empresarial. Hereda de la clase Cliente y tiene atributos adicionales para
    gestionar la información de la empresa y la persona de contacto asociada."""


    def __init__(self, empresa: Empresa, persona_contacto: Persona, tarjeta_credito: TarjetaPersonal):
        """
                Constructor de la clase ClienteEmpresarial. Inicializa los atributos de Cliente y asocia una empresa y una
                persona de contacto a este cliente empresarial.

                :param empresa: La instancia de la clase Empresa que representa la empresa cliente.
                :param persona_contacto: La instancia de la clase Persona que representa al contacto de la empresa.
                :param tarjeta_credito: El objeto de tipo TarjetaPersonal que representa la tarjeta de crédito del cliente.
                """
        super().__init__(tarjeta_credito)  # Llama al constructor de Cliente, pasando tarjeta_credito
        self._persona_contacto = persona_contacto
        self._empresa = empresa  # Instancia de la clase Empresa


class Reserva:
    """
        Clase que modela una reserva realizada por un cliente para un evento determinado.
        Permite acceder a los atributos propios de la reserva.
        """
    def __init__(self, cliente: Cliente, evento: 'Evento', fecha_reserva: datetime, cantidad: int, precio_final: float):
        """
                Constructor de la clase Reserva. Tiene como atributos los datos recibidos como parámetros además de self._pagado, que indica si la reserva ha sido pagada,
                inicializado en False por defecto.

                :param cliente: Instancia de la clase Cliente que realiza la reserva.
                :param evento: Instancia de la clase Evento que representa el evento reservado.
                :param fecha_reserva: Fecha en que se realiza la reserva.
                :param cantidad: Número de entradas reservadas.
                :param precio_final: Precio total de la reserva.
                """
        self._evento = evento
        self._fecha_reserva = fecha_reserva
        self._cantidad = cantidad
        self._precio_final = precio_final
        self._cliente = cliente
        self._pagado = False  # Indica si la reserva ha sido pagada

    def get_fecha_reserva(self):
        return self._fecha_reserva

    def get_esta_pagada(self) -> bool:
        return self._pagado

    def get_precio_final(self) -> float:
        return self._precio_final

    def get_cliente(self) -> Cliente:
        return self._cliente

    def get_evento(self) -> Evento:
        return self._evento

    def get_cantidad(self) -> int:
        return self._cantidad

    def marcar_como_pagada(self) -> None:
        """
                Marca la reserva como pagada.

                Este metodo cambia el estado de pago de la reserva a True, indicando que la reserva
                ha sido pagada.

                :return: None
                """
        self._pagado = True

    def __eq__(self, other):
        """
        Compara dos objetos Reserva para determinar si son iguales

        Dos reservas se consideran iguales si tienen el mismo cliente, el mismo evento, y la misma fecha de reserva.

        :param other: Otro objeto reserva con el que comparar
        :return: True si las reservas son iguales, False si no.
        """
        if isinstance(other, Reserva):
            return(self.get_cliente() == other.get_cliente() and
                   self.get_evento() == other.get_evento() and
                   self.get_fecha_reserva() == other.get_fecha_reserva())
        return False


