""""Modulo que contiene la clase UmuTicketsGui, que será nuestra interfaz de nuestro proyecto, esta contiene todos los metodos necesarios para
dar de alta a un cliente en formato json sin perder la persistencia entre flujos de ejecución y además de mostrar la simulación requerida junto a otros
métodos auxiliares que facilitan el gestionar toda la informacion requerida."""



import tkinter as tk
from tkinter import messagebox
from Source.empresas.umutickets import UMUTickets
from Source.clientes.cliente import Cliente, ClienteParticular, ClienteEmpresarial
from Source.clientes.tarjetas import TarjetaPersonal
import json
from pathlib import Path
from Source.empresas.empresa import Empresa
from Source.clientes.personas import Persona
from datetime import datetime
from Source.enumerados.tipo_evento import TipoEvento
from Source.enumerados.tipo_deporte import TipoDeporte
from Source.eventos.evento import Evento
from Source.empresas.organizador import Organizador
import Source.excepciones_propias.excepciones as error

class UmuTicketsGui:
    """
        Interfaz gráfica para la gestión de clientes y eventos en UMUTickets.

        Esta clase proporciona una ventana para registrar, cargar y simular clientes y eventos
        en el sistema UMUTickets.
        """
    sistema = UMUTickets()
    def __init__(self, master):
        """
                Inicializa la ventana principal de la aplicación y define los elementos de la interfaz.

                :param master: Ventana principal de Tkinter que contiene la GUI.
                """
        self._master = master
        self._master.title("Umu Tickets")
        self._master.geometry("800x425")
        self._master.config(bg="#f9f9f9")  # Fondo claro y suave
        self._master.columnconfigure(0, weight=1)
        self._master.columnconfigure(1, weight=3)
        self._master.columnconfigure(2, weight=1)

        # Instancia de UMUTickets para manejar clientes y eventos
        self.umu_tickets = UMUTickets()

        # Defino las variables de control para la entrada de texto
        self._identificador = tk.IntVar()
        self._identificador.set(Cliente.generar_id_unico())
        self._nombre = tk.StringVar()
        self._apellido = tk.StringVar()
        self._direccion = tk.StringVar()
        self._dni = tk.StringVar()

        # Definir una fuente moderna (Calibri)
        self.font = ("Calibri", 12)

        # Creo los pares etiquetas-entrada de texto con estilo moderno
        self._etiqueta_informacion = tk.Label(self._master,
                                              text="Introduzca sus datos personales para ser dado de alta.",
                                              font=("Calibri", 16, "bold"), bg="#f9f9f9", fg="#333333")

        self._etiqueta_id = tk.Label(self._master, text="Identificador:", font=self.font, bg="#f9f9f9", fg="#333333")
        self._entry_id = tk.Entry(self._master, textvariable=self._identificador, font=self.font, bd=2, relief="solid", state="readonly")

        self._etiqueta_nombre = tk.Label(self._master, text="Nombre:", font=self.font, bg="#f9f9f9", fg="#333333")
        self._entry_nombre = tk.Entry(self._master, textvariable=self._nombre, font=self.font, bd=2, relief="solid")

        self._etiqueta_apellidos = tk.Label(self._master, text="Apellidos:", font=self.font, bg="#f9f9f9", fg="#333333")
        self._entry_apellidos = tk.Entry(self._master, textvariable=self._apellido, font=self.font, bd=2,
                                         relief="solid")

        self._etiqueta_direccion = tk.Label(self._master, text="Direccion postal:", font=self.font, bg="#f9f9f9",
                                            fg="#333333")
        self._entry_direccion = tk.Entry(self._master, textvariable=self._direccion, font=self.font, bd=2,
                                         relief="solid")

        self._etiqueta_dni = tk.Label(self._master, text="DNI:", font=self.font, bg="#f9f9f9", fg="#333333")
        self._entry_dni = tk.Entry(self._master, textvariable=self._dni, font=self.font, bd=2, relief="solid")

        # Botones con diseÃ±o moderno
        self._button_guardar_cliente = tk.Button(self._master, text="Guardar Cliente", command=self.guardar_cliente,
                                                 font=self.font, relief="solid", height=2, width=20)

        self._button_cargar_cliente = tk.Button(self._master, text="Cargar Clientes", command=self.cargar_clientes,
                                                font=self.font, bg="#E3F2FD", fg="#1565C0", relief="flat",
                                                activebackground="#BBDEFB", height=2, width=20)

        self._button_simulacion = tk.Button(self._master, text="Simulación", command=self.mostrar_simulacion,
                                            font=self.font, bg="#FFEBEE", fg="#C2185B", relief="flat",
                                            activebackground="#FFCDD2", height=2, width=20)

    def muestra_ventana(self):
        """
                Configura y muestra la ventana principal con los widgets de la interfaz gráfica.
                """
        self._etiqueta_informacion.grid(row=0, column=0, columnspan=3, padx=10, pady=20)

        self._etiqueta_id.grid(row=1, column=0, padx=20, pady=10, sticky="e")
        self._entry_id.grid(row=1, column=1, padx=20, pady=10, sticky="ew")

        self._etiqueta_nombre.grid(row=2, column=0, padx=20, pady=10, sticky="e")
        self._entry_nombre.grid(row=2, column=1, padx=20, pady=10, sticky="ew")

        self._etiqueta_apellidos.grid(row=3, column=0, padx=20, pady=10, sticky="e")
        self._entry_apellidos.grid(row=3, column=1, padx=20, pady=10, sticky="ew")

        self._etiqueta_direccion.grid(row=4, column=0, padx=20, pady=10, sticky="e")
        self._entry_direccion.grid(row=4, column=1, padx=20, pady=10, sticky="ew")

        self._etiqueta_dni.grid(row=5, column=0, padx=20, pady=10, sticky="e")
        self._entry_dni.grid(row=5, column=1, padx=20, pady=10, sticky="ew")

        # Colocar los botones en una fila horizontal (centrados)
        self._button_guardar_cliente.grid(row=6, column=0, padx=20, pady=20, sticky="ew")
        self._button_cargar_cliente.grid(row=6, column=1, padx=20, pady=20, sticky="ew")
        self._button_simulacion.grid(row=6, column=2, padx=20, pady=20, sticky="ew")

        # Mantener la ventana abierta
        self._master.mainloop()
    
    def guardar_cliente(self):
        """
                Guarda los datos de un cliente en un archivo JSON y los añade al sistema UMUTickets.

                La información ingresada en los campos de texto se valida y almacena.
                """
        cliente = {
            "ID": self._identificador.get(),
            "Nombre": self._nombre.get(),
            "Apellidos": self._apellido.get(),
            "Direccion": self._direccion.get(),
            "DNI": self._dni.get()
        }
        ruta = Path("DB")/"clientes.json"
        try:
            with open(ruta, "r") as archivo_json:
                listado_clientes = json.load(archivo_json)
        except (FileNotFoundError, json.JSONDecodeError):
            listado_clientes = []

        dic_a_cliente = ClienteParticular(nombre=cliente["Nombre"], apellidos=cliente["Apellidos"],direccion_postal=cliente["Direccion"], dni=cliente["DNI"],tarjeta_credito= TarjetaPersonal())
        listado_clientes.append(cliente)
        UmuTicketsGui.sistema.agregar_cliente(dic_a_cliente)

        with open(ruta, "w") as archivo_json:
            json.dump(listado_clientes, archivo_json, indent=4)

        # Mostrar un mensaje de confirmaciÃ³n
        messagebox.showinfo("Información", "Cliente guardado correctamente")

        # Limpiar los campos de entrada
        self._identificador.set(Cliente.generar_id_unico())
        self._nombre.set('')
        self._apellido.set('')
        self._direccion.set('')
        self._dni.set('')


    def cargar_clientes(self):
        """
                Carga la lista de clientes desde un archivo JSON y la muestra en un cuadro de diálogo.
                """
        ruta = Path("DB")/"clientes.json"

        # Cargar los datos de los clientes
        with open(ruta, "r") as archivo_json:
            lista_clientes = json.load(archivo_json)
        string = ""
        for cliente in lista_clientes:
            string += self._diccionario_a_string(cliente)
        messagebox.showinfo("Clientes Cargados", string)


    @staticmethod
    def _diccionario_a_string(diccionario):
        """
                Convierte un diccionario en un string con formato legible.

                :param diccionario: Diccionario que contiene información de un cliente.
                :return: String con las claves y valores del diccionario formateados.
                """
        mensaje = ""
        for clave, valor in diccionario.items():
            mensaje += f"{clave}: {valor}\n"
        return mensaje

    @classmethod
    def _cargar_clientes_sistema(cls):
        """
                Carga los clientes desde el archivo JSON y los añade al sistema UMUTickets.

                Este metodo asegura que los clientes previos se incluyan en el sistema al inicio.
                """
        ruta = Path("DB")/"clientes.json"
        try:
            with open(ruta, "r") as archivo_json:
                lista_clientes = json.load(archivo_json)
        except (FileNotFoundError, json.JSONDecodeError):
            lista_clientes = []

        for cliente in lista_clientes:
            nuevo_cliente = ClienteParticular(
                nombre=cliente["Nombre"],
                apellidos=cliente["Apellidos"],
                direccion_postal=cliente["Direccion"],
                dni=cliente["DNI"],
                tarjeta_credito=TarjetaPersonal()
            )
            cls.sistema.agregar_cliente(nuevo_cliente)

    @staticmethod
    def _mostrar_reservas(reservas):
        mensaje = ""
        for reserva in reservas:
            mensaje += reserva.get_evento().get_nombre() + "\n"
        return mensaje

    def mostrar_simulacion(self):
        """
                Realiza una simulación en UMUTickets.

                La simulación incluye la creación de nuevos clientes (particulares, empresariales y socios),
                eventos deportivos, espectáculos y ferias, así como una empresa organizadora.
                """
        mensaje_parte_2 = ""
        simulacion_resultado = ""
        try:
            sistema = UMUTickets()
            # 1. Mostrar información sobre los clientes existentes
            #primero cargo todos los datos del clientes.json para que muestre todos los clientes añadidos en anteriores simulaciones
            UmuTicketsGui._cargar_clientes_sistema()
            clientes_info = "\nClientes actuales en UMUTickets:\n"
            for cliente in UmuTicketsGui.sistema.get_clientes():
                if type(cliente) == ClienteParticular:
                    clientes_info += f"{cliente.get_name()}, {cliente.get_apellidos()}, Dni:{cliente.get_dni()}, direccion postal: {cliente.get_direccion_postal()}\n"

                if type(cliente) == ClienteEmpresarial:
                    clientes_info += (f"Empresa {cliente.get_empresa().get_razon_social()}, telefono:{cliente.get_empresa().get_telefono}, direccion postal:{cliente.get_empresa().get_direccion_postal}"
                                      f"cif: {cliente.get_empresa().get_cif()}")

            simulacion_resultado = (
                f"Simulación completada con éxito!\n"
                f"{clientes_info}"
                f"--------------------------------------\n"
            )
            # 2. Alta de un cliente adicional que no es socio
            cliente_no_socio = ClienteParticular("Paco", "Pérez García", "Calle Ficticia 123", "12345678A",
                                                 TarjetaPersonal())


            cliente_no_socio.get_tarjeta_personal().sumar_saldo(200)
            # Se tendria que poner lo de sumar, e incializarla coo vacio la tarjeta primero
            sistema.agregar_cliente(cliente_no_socio)

            simulacion_resultado += (
                f"Nuevo cliente (no socio) creado: {cliente_no_socio.get_name()}  {cliente_no_socio.get_apellidos()} \n"
                f"--------------------------------------\n"
            )

            # Alta del cliente socio
            cliente_socio = ClienteParticular("Ana", "Gómez Ruiz", "Calle Ejemplo 456", "87654321B", TarjetaPersonal())
            cliente_socio.get_tarjeta_personal().sumar_saldo(200)
            # Intentar hacer socio al cliente
            cliente_socio.hacerse_socio(90)  # Convertimos en socio por defecto con un plan trimestral
            sistema.agregar_cliente(cliente_socio)

            simulacion_resultado += (
                f"Nueva clienta (socia) creada: {cliente_socio.get_name()}  {cliente_socio.get_apellidos()} \n"
                f"--------------------------------------\n")

            # Creación de un cliente empresarial
            empresa = Empresa(razon_social="TechCorp", cif="B56478998", telefono="639903138",
                              direccion_postal="30001")
            cliente_empresa = ClienteEmpresarial(empresa,
                                                 Persona("Carlos", "López", "Calle Corporativa 789", "65432112C"),
                                                 TarjetaPersonal())
            cliente_empresa.hacerse_socio(90)
            cliente_empresa.get_tarjeta_personal().sumar_saldo(200)
            sistema.agregar_cliente(cliente_empresa)

            simulacion_resultado += (
                f"Nueva empresa creada: {empresa.get_razon_social()}\n"
                f"--------------------------------------\n"
            )

            # 4. Creación de una empresa organizadora
            empresa_organizadora = Organizador(razon_social="Wevents S.L", cif="C56472232", telefono="655909138",
                                               direccion_postal="30001")
            simulacion_resultado += (
                f"Nueva empresa organizadora creada: {empresa_organizadora.get_razon_social()}\n"
                f"--------------------------------------\n"
            )

            # 5. Alta de un evento deportivo y un espectáculo audiovisual

            fecha_inicio_deportivo = datetime(2025, 6, 1, 10, 0)
            fecha_inicio_espectaculo = datetime(2025, 6, 1, 20, 0)

            evento_deportivo: Evento = sistema.crear_evento(TipoEvento.DEPORTIVO, nombre="Champions League",
                                                            descripcion="Un partido emocionante",
                                                            direccion="Estadio Nacional",
                                                            url="http://evento.com", entradas_disponibles=100,
                                                            precio_original=20, fecha_1=fecha_inicio_deportivo,
                                                            deporte= TipoDeporte.FUTBOL)


            espectaculo_audiovisual = sistema.crear_evento(TipoEvento.ESPECTACULO, nombre="Cruz Cafuné en concierto",
                                                           descripcion="El artista canario vuelve a Murcia",
                                                           direccion="Plaza de toros", url="http://cruzcafone.com",
                                                           entradas_disponibles=5000, precio_original=5.0,
                                                           fecha_1=fecha_inicio_espectaculo)

            simulacion_resultado += (
                f"Evento deportivo creado: {evento_deportivo.get_nombre()}\n"
                f"Espectáculo audiovisual creado: {espectaculo_audiovisual.get_nombre()}\n"
                f"--------------------------------------\n"
            )

            # 6. Alta de un evento de tipo feria, a través de la empresa organizadora
            fecha_inicio_feria = datetime(2025, 5, 15, 9, 0)
            evento_feria = empresa_organizadora.crear_evento(
                tipo=TipoEvento.FERIA,
                nombre="Feria de Innovación",
                descripcion="Feria de nuevas tecnologías",
                direccion="Centro de Convenciones",
                url="http://feriainnovacion.com",
                entradas_disponibles=90,
                precio_original=20,
                umuTickets=sistema,
                fecha_1=fecha_inicio_feria
            )

            simulacion_resultado += (
                f"Evento empresarial creado por la empresa organizadora: {empresa_organizadora.get_razon_social()}\n"
                f"--------------------------------------\n"
            )

            # 7. Realizar la reserva del cliente no socio a los eventos deportivo y audiovisual
            # Lo hago con try except ya que si la reserva no se realiza posteriormente en el apartado 11, las variables no estarian
            # definidas y daria error
            try:

                reserva_no_socio_evento_deportivo = sistema.reservar_entrada(cliente=cliente_no_socio, cantidad=1,
                                                                             evento=evento_deportivo)
            except (error.NoHaySuficientesEntradasError, error.FechaMinimaReserva) as e:
                reserva_no_socio_evento_deportivo_socio_evento_deportivo = None
                messagebox.showinfo(title="Error",
                message=f"No se pudo realizar la reserva a {evento_deportivo.get_nombre()}, debido a: {e} ")

            try:
                reserva_no_socio_espectaculo = sistema.reservar_entrada(cliente=cliente_no_socio, cantidad=1,
                                                                    evento=espectaculo_audiovisual)
            except (error.NoHaySuficientesEntradasError, error.FechaMinimaReserva) as e:
                reserva_no_socio_evento_deportivo = None
                messagebox.showinfo(title="Error",
                                    message=f"No se pudo realizar la reserva a {evento_deportivo.get_nombre()}, debido a: {e} ")

            simulacion_resultado += (
                f"El cliente no socio ha realizado las siguientes reservas: \n"
                f"{self._mostrar_reservas(cliente_no_socio.get_reservas())}"
                f"--------------------------------------\n"
            )

            # 8. Realizar la reserva del cliente socio a los eventos deportivo y audiovisual
            #Lo hago con try except como en el apartado 7

            try:
                reserva_socio_evento_deportivo = sistema.reservar_entrada(cliente=cliente_socio, cantidad=1,
                                                                          evento=evento_deportivo)

            except (error.NoHaySuficientesEntradasError, error.FechaMinimaReserva) as e:
                reserva_socio_evento_deportivo = None
                messagebox.showinfo(title="Error",
                message=f"No se pudo realizar la reserva a {evento_deportivo.get_nombre()}, debido a: {e} ")
            try:
                reserva_socio_espectaculo = sistema.reservar_entrada(cliente=cliente_socio, cantidad=1,
                                                                   evento=espectaculo_audiovisual)
            except (error.NoHaySuficientesEntradasError, error.FechaMinimaReserva) as e:
                    reserva_socio_espectaculo = None
                    messagebox.showinfo(title="Error",
                    message=f"No se pudo realizar la reserva a {evento_deportivo.get_nombre()}, debido a: {e} ")

            mensaje_parte_2 += (
                f"El cliente socio ha realizado las siguientes reservas: \n"
                f"{self._mostrar_reservas(cliente_socio.get_reservas())}"
                f"--------------------------------------\n"
            )

            # 9. Realizar la reserva del cliente empresarial al evento ferial
            reserva_feria = sistema.reservar_entrada(cliente=cliente_empresa, cantidad=1, evento=evento_feria)
            mensaje_parte_2 += (
                f"El cliente empresarial ha realizado la reserva al evento ferial: {evento_feria.get_nombre()}\n"
                f"--------------------------------------\n"
            )

            # 10. Simular la compra de al menos 3 eventos previamente reservados
            sistema.pagar_reserva(reserva_socio_espectaculo)
            sistema.pagar_reserva(reserva_no_socio_evento_deportivo)
            sistema.pagar_reserva(reserva_feria)

            mensaje_parte_2 += (
                f"Se han pagado los siguientes eventos:\n"
                f"- Cliente socio: {reserva_socio_espectaculo.get_evento().get_nombre()}\n"
                f"- Cliente no socio: {reserva_no_socio_evento_deportivo.get_evento().get_nombre()}\n"
                f"- Cliente empresarial: {reserva_feria.get_evento().get_nombre()}\n"
                f"--------------------------------------\n"
            )
        except (error.ClienteYaSocio, error.ClienteEmpresarialError,
                error.SaldoInsuficienteError, error.FechaInvalidaError, error.AccederFechas, error.EstablecerEntradas,
                error.DeporteInvalidoError, error.MaximoEntradasFeriaError, error.ModificacionEventoError,
                error.TipoEventoNoReconocidoError, error.EventoNoEncontradoError, error.NoHaySuficientesEntradasError, error.FechaMinimaReserva,
                error.ReservaYaPagada, error.CompraFueraDelPlazoError,
                error.EventoNoEncontradoErrorOganizador, error.PeriodoRenovacionError, error.CantidadInvalidaError,
                error.RecargaNegativaError, error.ReservaInexistenteError) as e:
            messagebox.showerror("Error", {e})

            # 11. Intentar anular una reserva pagada y una no pagada
        mensaje_parte_2 += (
            f"Intentando anular la reserva del cliente socio al concierto de Cruz Cafuné (ya pagada):\n"
        )
        #Si la reserva no se realiza no se guarda nada en la variable reserva_socio_espectaculo y evento_deportivo
        try:
            sistema.anular_reserva(reserva_socio_espectaculo)
        except (error.ReservaYaPagada, error.ReservaInexistenteError) as e:
            mensaje_parte_2 += f"Error: {e}\n"

        mensaje_parte_2 += (
            f"Intentando anular la reserva del cliente socio al partido de Champions (no pagada):\n"
        )
        #Necesito la condicion de que no sea none ya que sino la fun
        try:
            sistema.anular_reserva(reserva_socio_evento_deportivo)
            mensaje_parte_2 += (
            f"La reserva de {reserva_socio_evento_deportivo.get_evento().get_nombre()} ha sido cancelada con éxito.\n"
                )

        except (error.ReservaYaPagada, error.ReservaInexistenteError) as e:
            mensaje_parte_2 += f"Error: {e}\n"

        # 12. Mostrar información sobre la anulación
        try:
            mensaje_parte_2 += f"--------------------------------------\n"
            sistema.eliminar_evento(evento_deportivo.get_id())
            mensaje_parte_2 += (
                    f" Se ha realizado la anulación del evento: {evento_deportivo.get_nombre()}, por consiguiente, se les abonará el importe a aquellos que lo hayan pagado.\n"
                    f"--------------------------------------\n"
                )
        except AttributeError as e:
            mensaje_parte_2 += f"Error: {e}\n"

        # 13. Mostrar beneficios obtenidos por reservas
        beneficio = sum(sistema.calcular_beneficio(evento) for evento in sistema.get_eventos())
        mensaje_parte_2 += (
            f"Las reservas han generado un beneficio de {beneficio} euros.\n"
            f"--------------------------------------\n"
        )

        # 14. Mostrar información sobre el número de socios y los ingresos por sus cuotas
        num_socios, ingresos_socios = sistema.contar_socios_y_beneficio()
        mensaje_parte_2 += (
            f"El número de socios actuales es {num_socios} y los ingresos generados por cuotas son de {ingresos_socios} euros.\n"
        )

        messagebox.showinfo("Simulación Realizada (Primera Parte)", simulacion_resultado)
        messagebox.showinfo( title = "Simulacion Realizada (Segunda Parte)", message= mensaje_parte_2 )

      
        #messagebox.showerror("Error", f"Ocurrió un error durante la simulación: {e}")
