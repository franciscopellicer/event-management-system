"""
Este módulo define la clase `Socio`, que gestiona la información y operaciones relacionadas con los socios de una organización.

Justificación:
La clase `Socio` es fundamental para modelar el sistema de membresías, permitiendo llevar un control sobre las renovaciones, cuotas pagadas y beneficios asociados a cada socio. Esto es especialmente útil en sistemas de administración de membresías donde se requiere un seguimiento detallado de cada socio y su interacción con la organización.
"""

#los metodos set los comento aunque sean protegidos y no sean de libre acceso
from datetime import timedelta, datetime
from Source.excepciones_propias.excepciones import PeriodoRenovacionError
from Source.clientes.tarjetas import TarjetaSocio
class Socio:
    """
        Clase que representa a un socio. Gestiona la renovación de la membresía, la cuota de renovación y los beneficios obtenidos.

        Atributos:
            _numero_socios: Número total de socios, utilizado para generar un identificador único para cada socio.
            _numero_socio: Identificador único del socio.
            _tarjeta_socio: Instancia de la tarjeta de socio asociada al socio.
            _fecha_inicio_renovacion: Fecha de inicio de la renovación de la membresía.
            _fecha_expiracion_renovacion: Fecha de expiración de la renovación de la membresía.
            _ganancias_por_cuotas: Ganancias acumuladas por el pago de cuotas del socio.
        """
    _numero_socios : int = 0
    def __init__(self, tiempo):
        """
                Constructor de la clase Socio. Inicializa los atributos de un socio, incluyendo su número de socio, la tarjeta,
                las fechas de inicio y expiración de renovación, y las ganancias de cuotas según el tiempo de renovación.

                :param tiempo: Periodo de renovación en días (debe ser 30, 90 o 365).
                :raises PeriodoRenovacionError: Si el tiempo de renovación no es 30, 90 o 365 días.
                """
        if tiempo not in (30, 90, 365):
            raise PeriodoRenovacionError()
        self._numero_socio = Socio._numero_socios + 100000  #Le sumas 10.000 para que no se de la remota casualidad de que coincida con el nº de cliente
        self._tarjeta_socio = TarjetaSocio()
        self._fecha_inicio_renovacion = datetime.now()
        self._fecha_expiracion_renovacion = datetime.now() + timedelta(days=tiempo)
        # lista para manejar las cuotas
        if tiempo == 30:
            self._ganancias_por_cuotas = 5
        if tiempo == 90:
            self._ganancias_por_cuotas = 20
        if tiempo == 365:
            self._ganancias_por_cuotas = 50
        Socio._numero_socios += 1


    def _get_numero_socio(self):
        return self._numero_socio

    def _set_numero_socio(self, numero_socio):
        """"Debe recibir un entero como parámetro"""
        self._numero_socio = numero_socio

    def _get_tarjeta_socio(self):
        return self._tarjeta_socio

    def _set_tarjeta_socio(self, tarjeta_socio):
        """Debe recibir un objeto TarjetaPersonal como parámetro"""
        self._tarjeta_socio = tarjeta_socio

    def _get_fecha_inicio_renovacion(self):
        return self._fecha_inicio_renovacion

    def _set_fecha_inicio_renovacion(self, fecha):
        """Debe recibir una fecha datetime"""
        self._fecha_inicio_renovacion = fecha

    def _get_fecha_expiracion_renovacion(self):
        return self._fecha_expiracion_renovacion

    def _set_fecha_expiracion_renovacion(self, fecha):
        """Debe recibir una fecha datetime"""
        self._fecha_expiracion_renovacion = fecha

    def _get_veces_renovado(self):
        return self._veces_renovado

    def _set_veces_renovado(self, veces_renovado):
        """Debe recibir un entero positivo"""
        self._veces_renovado = veces_renovado

    def _get_ganancias_por_cuotas(self):
        return self._ganancias_por_cuotas

    def _set_ganancias_por_cuotas(self, ganancias_por_cuotas):
        """Debe recibir un valor real positivo"""
        self._ganancias_por_cuotas = ganancias_por_cuotas

    def get_ganancias(self):
        return self._ganancias_por_cuotas

    def renovar(self, periodicidad: int ):
        """
                Renueva la membresía del socio, actualizando las fechas de inicio y expiración de renovación,
                y deduciendo el costo de la renovación de la tarjeta de socio.

                :param periodicidad: La periodicidad de la renovación (30, 90 o 365 días).

                :raises PeriodoRenovacionError: Si la periodicidad de la renovación no es válida.
                """
        if periodicidad == 30:
            coste = 5
            duracion = timedelta(days=30)
        elif periodicidad == 90:
            coste = 20
            duracion = timedelta(days=90)
        elif periodicidad == 365:
            coste = 50
            duracion = timedelta(days=365)
        else:
            raise PeriodoRenovacionError()

        self._get_tarjeta_socio().deducir(coste)
        self._set_fecha_inicio_renovacion(datetime.now())
        self._set_fecha_expiracion_renovacion(datetime.now() + duracion)
        self._set_ganancias_por_cuotas(self._get_ganancias_por_cuotas() + coste)
