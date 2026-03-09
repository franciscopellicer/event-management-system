"""
Este módulo define la clase Persona, que representa a una persona con sus atributos propios.
Este módulo es útil ya que se requiere gestionar datos personales de manera estructurada, como en UmuTickets..
"""

class Persona:
    """
        Clase que representa a una persona, con atributos básicos como nombre, apellidos, dirección postal y DNI.

        Atributos:
            _nombre: Nombre de la persona.
            _apellidos: Apellidos de la persona.
            _direccion_postal: Dirección postal de la persona.
            _dni: Documento Nacional de Identidad de la persona.
        """

    def __init__(self, nombre: str, apellidos: str, direccion_postal: str, dni: str):
        """
                Constructor de la clase Persona. Inicializa los atributos de la persona con los valores proporcionados.

                :param nombre.
                :param apellidos.
                :param direccion_postal.
                :param dni.
                """
        self._nombre = nombre
        self._apellidos = apellidos
        self._direccion_postal = direccion_postal
        self._dni = dni

    def get_name(self):
        return self._nombre

    def get_apellidos(self):
        return self._apellidos

    def get_direccion_postal(self):
        return self._direccion_postal

    def get_dni(self):
        return self._dni
