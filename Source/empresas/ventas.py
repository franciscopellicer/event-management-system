"""
Modulo que define la clase `Venta`, la cual modela una venta realizada por un cliente para un evento específico.

La clase proporciona métodos para acceder a la información de cada venta, como el cliente, el evento, la cantidad de entradas
y el precio final.

"""


from Source.clientes.cliente import Cliente
from Source.eventos.evento import Evento

class Venta:
    """
       Clase que modela una venta realizada por un cliente, asociada a un evento específico.
       La venta incluye la cantidad de entradas compradas y el precio final de la venta.
       """

    def __init__(self, cliente: 'Cliente', evento: 'Evento', cantidad: int, precio_final: float):
        """
                Constructor de la clase Venta. Inicializa los atributos con los valores proporcionados.

                :param cliente: El cliente que realiza la compra.
                :param evento: El evento para el cual se realiza la compra.
                :param cantidad: La cantidad de entradas compradas.
                :param precio_final: El precio total de la venta.
                """
        self._cliente = cliente
        self._evento = evento
        self._cantidad = cantidad
        self._precio_final = precio_final

    def get_cliente(self) -> Cliente:
        return self._cliente

    def get_evento(self)-> Evento:
        return self._evento

    def get_cantidad(self) -> int :
        return self._cantidad

    def get_precio_final(self) -> float:
        return self._precio_final