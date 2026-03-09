import tkinter as tk
from Source.interfaces.interfaz_grafica import UmuTicketsGui
"""Modulo main donde se prueba el código"""
if __name__ == "__main__":
    root = tk.Tk()
    app = UmuTicketsGui(root)
    app.muestra_ventana()

