"""
    Módulo que define la clase Empresa, la cual modela una empresa y gestiona su información básica,

    Justificación:
    El módulo es fundamental para manejar los datos básicos de una empresa dentro de UmuTickets,
    permitiendo obtener y trabajar con la información necesaria de manera estructurada y controlada.

"""

class Empresa:
    """
        Clase que modela una empresa, incluyendo sus datos básicos como razón social, CIF,
        teléfono y dirección postal. Proporciona métodos para acceder a estos atributos.

        """
    def __init__(self, razon_social: str, cif: str, telefono: str, direccion_postal: str):
        """
                Constructor de la clase Empresa. Inicializa los atributos con los valores proporcionados.

                :param razon_social, nombre de registro de la empresa.
                :param cif: Código de Identificación Fiscal (CIF).
                :param telefono.
                :param direccion_postal.
                """
        self._razon_social = razon_social  # str: RazÃ³n social de la empresa
        self._cif = cif  # str: CIF de la empresa
        self._telefono = telefono  # str: TelÃ©fono de la empresa
        self._direccion_postal = direccion_postal  # str: DirecciÃ³n postal de la empresa

    def get_razon_social(self) -> str:
        return self._razon_social

    def get_cif(self) -> str:
        return self._cif

    def get_telefono(self) -> str:
        return self._telefono

    def get_direccion_postal(self) -> str:
        return self._direccion_postal