#Creado por: Daniel Campos y Alejandro Madrigal
#Creación: 10-10-2023 
#Ultima modificación: 15-10-2023 
#Versión: 3.12.0
#Importacion de librerias
import tkinter as tk
import requests
#Definicion de funciones
def estudiantesSede():
    """
    Función: Define la cantidad de estudiantes de primer ingreso que entran por sede.
    Entradas:
    Salidas:
    """
    return

def estudiantesCarrera():
    """
    Función: Crea dinámicamente la base de datos de todos los admitidos en cada carrera por cada sede.
    Entradas:
    Salidas:
    """
    return

def crearMentores():
    """
    Función: Dada la cantidad de estudiantes de primer ingreso generados por sede en cada carrera.
    Entradas:
    Salidas:
    """
    return

def asignarMentores():
    """
    Función: Según la cantidad de mentores, asigna a los estudiantes con misma carrera y sede de forma distribuida a los mentores.
    Entradas:
    Salidas:
    """
    return

def actualizarEstudiante():
    """
    Función: Muestra los datos en una ventana de formulario, donde sea posible modificar: nombre completo, teléfono, correo y guarda los cambios luego de verificar su formato.
    Entradas:
    Salidas:
    """
    return

def generarReportes():
    """
    Función: Genera los reportes en HTML.
    Entradas:
    Salidas:
    """
    return

def crearBaseDatos():
    """
    Función: Crea un archivo string a guardar en disco duro con extensión ".csv".
    Entradas:
    Salidas:
    """
    return

def enviarCorreo():
    """
    Función: Solicita el correo de un encargado y adjunta el ".csv".
    Entradas:
    Salidas:
    """
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