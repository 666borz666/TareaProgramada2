#Creado por: Daniel Campos y Alejandro Madrigal
#Creación: 10-10-2023 
#Ultima modificación: 15-10-2023 
#Versión: 3.12.0

#Importacion de librerias
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import random
from faker import Faker
import pandas as pd

#Variables globales
fake = Faker()
cantidadEstudiantes = None
excel = r'D:\Estudios de Ale\Compu\GitHub\Tareas Programadas\TareaProgramada2\TareaProgramada2\Main (no listo)\sedes.xlsx'
carreras = pd.read_excel(excel)
asignacionesEstudiantes = []
cantidadEstudiantes = None 

#Funciones
def estudiantesSede():
    global asignacionesEstudiantes
    ventanaEstudiantes = tk.Toplevel(ventana)
    ventanaEstudiantes.title("Estudiantes por Sede")
    etiquetaSede = tk.Label(ventanaEstudiantes, text="Selecciona una sede:")
    etiquetaSede.pack()
    opcionesSedes = ["CAMPUS TECNOLÓGICO LOCAL SAN CARLOS", "CAMPUS TECNOLÓGICO LOCAL SAN JOSÉ","CENTRO ACADÉMICO DE LIMÓN", "CAMPUS TECNOLÓGICO CENTRAL CARTAGO","CENTRO ACADÉMICO DE ALAJUELA"]
    sedeSeleccionada = tk.StringVar()
    sedeSeleccionada.set(opcionesSedes[0])
    listaSede = ttk.Combobox(ventanaEstudiantes, textvariable=sedeSeleccionada, values=opcionesSedes)
    listaSede.config(width=42)
    listaSede.pack()
    etiquetaCantidad = tk.Label(ventanaEstudiantes, text="Cantidad total de estudiantes:")
    etiquetaCantidad.pack()
    cantidadEstudiantes_entry = tk.Entry(ventanaEstudiantes)
    cantidadEstudiantes_entry.pack()
    def asignarEstudiantes():
        sede = sedeSeleccionada.get()
        cantidad_estudiantes = int(cantidadEstudiantes_entry.get())
        sedeCarreras = carreras[sede].dropna().index.tolist()
        estudiantesAsignados = {carrera: 0 for carrera in sedeCarreras}
        estudiantesRestantes = cantidad_estudiantes
        while estudiantesRestantes > 0:
            carreraAleatoria = random.choice(sedeCarreras)
            estudiantesAsignados[carreraAleatoria] += 1
            estudiantesRestantes -= 1
        asignacion_sede = {'sede': sede, 'asignaciones': estudiantesAsignados}
        asignacionesEstudiantes.append(asignacion_sede)
        ventanaResultados = tk.Toplevel(ventana)
        ventanaResultados.title("Resultados de Asignación de Estudiantes")
        for carrera, cantidad_estudiantes in estudiantesAsignados.items():
            nombreCarrera = carreras.loc[carrera, sede]
            labelResultado = tk.Label(ventanaResultados, text=f"{nombreCarrera}: {cantidad_estudiantes} estudiantes asignados")
            labelResultado.pack()
    botonAsignarEstudiantes = tk.Button(ventanaEstudiantes, text="Asignar Estudiantes", command=asignarEstudiantes)
    botonAsignarEstudiantes.pack()
    botonCerrar = tk.Button(ventanaEstudiantes, text="Cerrar", command=ventanaEstudiantes.destroy)
    botonCerrar.pack()

def estudiantesCarrera():
    def mostrar_estudiantes_de_sede():
        sedeElegida = sedeSeleccionada.get()
        if sedeElegida in carreras:
            sedeCarreras = carreras[sedeElegida].dropna().index.tolist()
            ventanaResultados = tk.Toplevel(ventana)
            ventanaResultados.title("Estudiantes de la Sede")
            tabla = ttk.Treeview(ventanaResultados, columns=["Carnet", "Nombre Completo", "Carrera", "Teléfono", "Correo Electrónico", "Carnet de Mentor"])
            tabla.heading("#0", text="Carnet")
            tabla.heading("#1", text="Nombre Completo")
            tabla.heading("#2", text="Carrera")
            tabla.heading("#3", text="Teléfono")
            tabla.heading("#4", text="Correo Electrónico")
            tabla.heading("#5", text="Carnet de Mentor")
            tabla.pack()
            admitidosCarreras = {carrera: cantidadAdmitidos(sedeElegida, carrera) for carrera in sedeCarreras}
            estudiantesGenerados = []
            telefonosGenerados = set()
            for carrera in sedeCarreras:
                nombreCarrera = carreras.loc[carrera, sedeElegida]
                for _ in range(admitidosCarreras[carrera]):
                    carnet = f"2024{opcionesSedes.index(sedeElegida) + 1:02d}{random.randint(1000, 9999)}"
                    nombreCompleto = (fake.last_name(), fake.last_name(), fake.first_name())
                    telefono = generarTelefono(telefonosGenerados)
                    correo = generar_correo(nombreCompleto[2], nombreCompleto[0])
                    estudiantesGenerados.append({'Carnet': carnet, 'Nombre Completo': f"{nombreCompleto[0]} {nombreCompleto[1]} {nombreCompleto[2]}", 'Carrera': nombreCarrera, 'Teléfono': telefono, 'Correo Electrónico': correo, 'Carnet de Mentor': "0"})
            for estudiante in estudiantesGenerados:
                tabla.insert("", "end", values=(estudiante['Carnet'], estudiante['Nombre Completo'], estudiante['Carrera'], estudiante['Teléfono'], estudiante['Correo Electrónico'], estudiante['Carnet de Mentor']))
        else:
            messagebox.showerror("Error", f"La sede '{sedeElegida}' no se encuentra en el archivo Excel.")        
    ventanaSede = tk.Toplevel(ventana)
    ventanaSede.title("Seleccionar Sede")
    etiquetaSeleccionSede = tk.Label(ventanaSede, text="Selecciona una sede:")
    etiquetaSeleccionSede.pack()
    opcionesSedes = ["CAMPUS TECNOLÓGICO LOCAL SAN CARLOS","CAMPUS TECNOLÓGICO LOCAL SAN JOSÉ","CENTRO ACADÉMICO DE LIMÓN","CAMPUS TECNOLÓGICO CENTRAL CARTAGO","CENTRO ACADÉMICO DE ALAJUELA"]
    sedeSeleccionada = tk.StringVar()
    sedeSeleccionada.set(opcionesSedes[0])
    listaSede = ttk.Combobox(ventanaSede, textvariable=sedeSeleccionada, values=opcionesSedes)
    listaSede.config(width=42)
    listaSede.pack()
    botonConfirmarSede = tk.Button(ventanaSede, text="Mostrar Estudiantes", command=mostrar_estudiantes_de_sede)
    botonConfirmarSede.pack()
    
def cantidadAdmitidos(sede, carrera):
    infoSede = [info for info in asignacionesEstudiantes if info['sede'] == sede]
    if infoSede:
        asignaciones = infoSede[0]['asignaciones']
        if carrera in asignaciones:
            return asignaciones[carrera]
    return 0

def generarTelefono(telefonosGenerados):
    while True:
        primerDigito = random.choice("6789")
        otrosDigitos = random.sample("0123456789", 7)
        telefono = primerDigito + ''.join(otrosDigitos)
        if telefono not in telefonosGenerados:
            telefonosGenerados.add(telefono)
            return telefono

def generar_correo(nombre, apellido):
    correo = nombre[:2] + apellido.split()[0] + "@estudiantec.cr"
    return correo.lower()

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
boton2 = tk.Button(ventana, text="Estudiantes de carrera por sede", command=estudiantesCarrera)
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