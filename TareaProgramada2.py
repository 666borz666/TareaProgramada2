#Creado por: Daniel Campos y Alejandro Madrigal
#Creación: 10-10-2023 10:00 pm
#Ultima modificación: 12-10-2023 9:00 am
#Versión: 3.12.0
#Importacion de librerias
import tkinter as tk
#Definicion de funciones
def estudiantes_por_sede():
    return

def estudiantes_de_carrera_por_sede():
    return

def crear_mentores():
    return

def asignar_mentores():
    return

def actualizar_estudiante():
    return

def generar_reportes():
    return

def crear_base_de_datos():
    return

def enviar_correo():
    return
#Interfaz gráfica
ventana = tk.Tk()
ventana.title("Atención a la Generación 2024")
ventana.attributes('-fullscreen', True)
boton1 = tk.Button(ventana, text="Estudiantes por sede", command=estudiantes_por_sede)
boton2 = tk.Button(ventana, text="Estudiantes de carrera por sede", command=estudiantes_de_carrera_por_sede, state="disabled")
boton3 = tk.Button(ventana, text="Crear mentores", command=crear_mentores, state="disabled")
boton4 = tk.Button(ventana, text="Asignar mentores", command=asignar_mentores, state="disabled")
boton5 = tk.Button(ventana, text="Actualizar estudiante", command=actualizar_estudiante, state="disabled")
boton6 = tk.Button(ventana, text="Generar reportes", command=generar_reportes)
boton7 = tk.Button(ventana, text="Crear base de datos en Excel", command=crear_base_de_datos)
boton8 = tk.Button(ventana, text="Enviar correo", command=enviar_correo)
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