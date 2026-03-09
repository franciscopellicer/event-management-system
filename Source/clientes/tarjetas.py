"""
Este módulo define las clases `TarjetaPersonal` y `TarjetaSocio`, que modelan las operaciones relacionadas con la gestión de saldos y transacciones en un sistema de tarjetas personales y de socios.
El módulo proporciona una infraestructura básica para manejar saldos, incluyendo operaciones de recarga y deducción, así como la generación de identificadores únicos para tarjetas. La clase `TarjetaPersonal` permite a los usuarios gestionar su propio saldo y realizar recargas a tarjetas de socios, mientras que `TarjetaSocio` maneja las transacciones específicas para los socios. Este diseño facilita la administración de un sistema financiero simplificado para membresías o programas de beneficios.
"""

import random
from Source.excepciones_propias.excepciones import SaldoInsuficienteError, CantidadInvalidaError, RecargaNegativaError

class TarjetaPersonal:
    """
        Clase que representa una tarjeta personal. Gestiona el saldo, la generación de números de tarjeta únicos,
        y las operaciones de recarga y deducción de saldo.

        Atributos:
            _numeros_tarjeta_existentes: Conjunto que almacena los números de tarjeta ya generados.
            _rango_tarjetas: Rango de números posibles para generar las tarjetas.
            _MAX_INTENTOS: Límite de intentos para generar un número de tarjeta único antes de ampliar el rango.
            _saldo: El saldo disponible en la tarjeta personal.
            _numero_tarjeta: El número único de la tarjeta personal.
        """
    _numeros_tarjeta_existentes = set()
    _rango_tarjetas = [1, 10000]  # Rango inicial de números de tarjeta (1 a 10000)
    _MAX_INTENTOS = 100  # Límite de intentos antes de ampliar el rango
    
    def __init__(self):
        """
                Constructor de la clase TarjetaPersonal. Inicializa el saldo de la tarjeta en 0 y genera un número único
                para la tarjeta utilizando el metodo de generación de números únicos.
                """
        self._saldo = 0  # Inicializa el saldo en p
        self._numero_tarjeta = self._generar_num_tarjeta_unico()

    def _get_saldo(self):
        return self._saldo

    @classmethod
    def _generar_num_tarjeta_unico(cls) -> int:
        """
                Genera un número único de tarjeta dentro del rango de tarjetas disponible. Si no se puede generar un número
                único dentro del número máximo de intentos, amplía el rango de generación.

                :return: Un número único de tarjeta.
                :raises: Si no se puede generar un número único dentro del rango actual, se amplía el rango y se vuelve a intentar.
                """
        intentos = 0
        # Intentar hasta _MAX_INTENTOS veces
        while intentos < cls._get_max_intentos():
            # Generar un número dentro del rango actual
            numero_tarjeta = random.randint(cls._rango_tarjetas[0], cls._rango_tarjetas[1])
            if numero_tarjeta not in cls._numeros_tarjeta_existentes:
                # Si el número no ha sido utilizado, lo añadimos al conjunto de números usados
                cls._numeros_tarjeta_existentes.add(numero_tarjeta)
                return numero_tarjeta  # Devolvemos el número único

            intentos += 1  # Incrementamos el contador de intentos

        # Si no se ha encontrado un número único en los intentos dados, ampliamos el rango
        cls._rango_tarjetas[1] *= 2  # Duplicar el límite superior del rango
        return cls._generar_num_tarjeta_unico()  # Volver a intentar con el rango ampliado

    @classmethod
    def _get_max_intentos(cls) -> int:
        return cls._MAX_INTENTOS

    def get_saldo(self) -> float:
        return self._saldo

    def sumar_saldo(self, cantidad_a_sumar: float):
        """
                Suma una cantidad de dinero, dada como parámetro al saldo de la tarjeta personal.
                :param cantidad_a_sumar.
                """
        self._saldo += cantidad_a_sumar

    def _restar_saldo(self, cantidad_a_restar: float):
        """
                Resta una cantidad de dinero, dada como parámetro al saldo de la tarjeta personal.
                :param cantidad_a_restar.
                """
        self._saldo -= cantidad_a_restar

    def recargar_saldo_a_socio(self, tarjeta_socio: 'TarjetaSocio', cantidad: float):
        """
                Recarga una cantidad de dinero dada como parámetro al saldo de la tarjeta de socio, dada como parámetro
                desde la tarjeta personal, deduciendo el saldo de la tarjeta personal.
                :param tarjeta_socio.
                :param cantidad.

                :raises RecargaNegativaError: Si la cantidad a recargar es negativa.
                :raises SaldoInsuficienteError: Si el saldo de la tarjeta personal es insuficiente para realizar la recarga.
                :raises CantidadInvalidaError: Si la cantidad de recarga no es una cantidad válida (5, 10, 20 o 50).
                """
        if cantidad <= 0:
            raise RecargaNegativaError(f"La cantidad {cantidad} a recargar debe ser positiva")
        if self.get_saldo() < cantidad:
            raise SaldoInsuficienteError("No tienes suficiente dinero para recargar")
        if cantidad not in [5, 10, 20, 50]:
            raise CantidadInvalidaError()

        # Deduce el saldo de la tarjeta personal y recarga la tarjeta de socio
        self.quitar_saldo(cantidad)
        tarjeta_socio.recargar(cantidad)

    
    def quitar_saldo(self, cantidad: float):
        """
               Resta una cantidad dada como parámetro de saldo de la tarjeta personal.
               :param cantidad.
               :raises SaldoInsuficienteError: Si la cantidad a restar es mayor al saldo disponible.
               """
        if cantidad > self.get_saldo():
            raise SaldoInsuficienteError(f"Saldo insuficiente. Saldo restante= {self.get_saldo()} euros")
        self._restar_saldo(cantidad)


class TarjetaSocio:
    """
        Clase que representa una tarjeta de socio. Gestiona el saldo de la tarjeta y permite realizar operaciones de recarga
        y deducción de saldo.

        Atributos:
            saldo: El saldo disponible en la tarjeta del socio.
        """

    def __init__(self):
        """
              Constructor de la clase TarjetaSocio. Inicializa el saldo de la tarjeta del socio en 0.
              """
        self._saldo = 0

    def recargar(self, cantidad: float ):
        """
                Recarga una cantidad de dinero en la tarjeta del socio.

                :param cantidad: La cantidad de dinero a añadir al saldo de la tarjeta del socio.
                """

        self._saldo += cantidad

    def deducir(self, cantidad: int):
        """
                Deduce una cantidad de dinero del saldo de la tarjeta del socio.

                :param cantidad: La cantidad de dinero a deducir del saldo de la tarjeta del socio.

                :raises SaldoInsuficienteError: Si la cantidad a deducir es mayor al saldo disponible.
                """
        if cantidad > self._saldo:
            raise SaldoInsuficienteError(f"Saldo insuficiente. Saldo restante= {self._get_saldo()} euros")
        self._saldo -= cantidad

    def _get_saldo(self):
        """
                Obtiene el saldo actual de la tarjeta del socio.

                :return: El saldo disponible en la tarjeta del socio.
                """
        return self._saldo