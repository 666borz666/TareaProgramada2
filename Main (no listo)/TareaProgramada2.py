#Creado por: Daniel Campos y Alejandro Madrigal
#Creación: 10-10-2023 
#Ultima modificación: 15-10-2023 
#Versión: 3.12.0
#Importacion de librerias
import tkinter as tk
from tkinter import ttk
from faker import Faker
fake = Faker()
import pandas as pd
import os
cantidad_estudiantes = None
print(os.getcwd())
df = pd.read_excel("sedes.xlsx", sheet_name=0)
def estudiantesSede():
    # Crear una ventana secundaria para seleccionar la sede
    ventana_estudiantes = tk.Toplevel(ventana)
    ventana_estudiantes.title("Estudiantes por Sede")

    # Etiqueta y lista desplegable para seleccionar la sede
    etiqueta_sede = tk.Label(ventana_estudiantes, text="Selecciona una sede:")
    etiqueta_sede.pack()

    # Obtener opciones de sedes desde los datos cargados con Pandas
    opciones_sedes = df["Sede"].tolist()

    sede_seleccionada = tk.StringVar()
    sede_seleccionada.set(opciones_sedes[0])  # Establece la primera sede como predeterminada

    lista_desplegable_sede = ttk.Combobox(ventana_estudiantes, textvariable=sede_seleccionada, values=opciones_sedes)
    lista_desplegable_sede.pack()

    # Diccionario para almacenar los números por carrera
    numeros_por_carrera = {}

    # Función para mostrar el cuadro de entrada para el número y el botón "Aceptar"
    def mostrar_cuadro_numero():
        # Ocultar la lista desplegable
        lista_desplegable_sede.pack_forget()

        # Ocultar el botón "Aceptar"
        boton_aceptar.pack_forget()

        # Etiqueta para ingresar el número
        etiqueta_numero = tk.Label(ventana_estudiantes, text="Ingresa un número:")
        etiqueta_numero.pack()

        numero_entrada = tk.Entry(ventana_estudiantes)
        numero_entrada.pack()

        # Botón "Generar Número"
        boton_generar_numero = tk.Button(ventana_estudiantes, text="Generar Número", command=lambda: generar_numero(numero_entrada, sede_seleccionada, numeros_por_carrera))
        boton_generar_numero.pack()

    # Función para generar y mostrar un número aleatorio
    def generar_numero(numero_entrada, sede_seleccionada, numeros_por_carrera):
        sede = sede_seleccionada.get()
        numero = numero_entrada.get()

        # Aquí puedes agregar lógica para asociar el número a una carrera específica utilizando los datos de Pandas
        # Ejemplo:
        carrera = df[df["Sede"] == sede]["Carrera"].values[0]
        if carrera not in numeros_por_carrera:
            numeros_por_carrera[carrera] = []

        numeros_por_carrera[carrera].append(numero)
        print(f"{sede}: Número ingresado para {carrera}: {numero}")

    # Botón "Aceptar" para continuar
    boton_aceptar = tk.Button(ventana_estudiantes, text="Aceptar", command=mostrar_cuadro_numero)
    boton_aceptar.pack()


def estudiantesCarrera():
    return

def crearMentores():
    return

def asignarMentores():
    return

def actualizarEstudiante():
    return

def generarReportes():
    return

def crearBaseDatos():
    return

def enviarCorreo():
    return
#Interfaz gráfica
ventana = tk.Tk()
ventana.title("Atención a la Generación 2024")
ventana.attributes('-fullscreen', True)
boton1 = tk.Button(ventana, text="Estudiantes por sede", command=estudiantesSede)
boton2 = tk.Button(ventana, text="Estudiantes de carrera por sede", command=estudiantesCarrera, state="disabled")
boton3 = tk.Button(ventana, text="Crear mentores", command=crearMentores, state="disabled")
boton4 = tk.Button(ventana, text="Asignar mentores", command=asignarMentores, state="disabled")
boton5 = tk.Button(ventana, text="Actualizar estudiante", command=actualizarEstudiante, state="disabled")
boton6 = tk.Button(ventana, text="Generar reportes", command=generarReportes)
boton7 = tk.Button(ventana, text="Crear base de datos en Excel", command=crearBaseDatos)
boton8 = tk.Button(ventana, text="Enviar correo", command=enviarCorreo)
boton9 = tk.Button(ventana, text="Salir", command=ventana.quit)

boton1.pack()
boton2.pack()
boton3.pack()
boton4.pack()
boton5.pack()
boton6.pack()
boton7.pack()
boton8.pack()
boton9.pack()

ventana.mainloop()

