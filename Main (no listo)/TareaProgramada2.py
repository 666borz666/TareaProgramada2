#Creado por: Daniel Campos y Alejandro Madrigal
#Creación: 10-10-2023 
#Ultima modificación: 15-10-2023 
#Versión: 3.12.0

#Importacion de librerias
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import random
from faker import Faker
import pandas as pd
import pickle
from PIL import Image, ImageTk
import csv
import datetime
from email.message import EmailMessage
import smtplib
import os
import sys

#Variables globales
fake = Faker()
cantidadEstudiantes = None
excel = excel = r'D:\Estudios de Ale\Compu\GitHub\Tareas Programadas\TareaProgramada2\TareaProgramada2\Main (no listo)\sedes.xlsx'
carreras = pd.read_excel(excel)
asignacionesEstudiantes = []
cantidadEstudiantes = None 
cantidadestudiantes = 0
estudiantesPorSede = {}
mentoresGenerados = {}

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
    cantidadEstudianteEntry = tk.Entry(ventanaEstudiantes)
    cantidadEstudianteEntry.pack()
    def asignarEstudiantes():
        sede = sedeSeleccionada.get()
        cantidadestudiantes = int(cantidadEstudianteEntry.get())
        sedeCarreras = carreras[sede].dropna().index.tolist()
        estudiantesAsignados = {carrera: 0 for carrera in sedeCarreras}
        estudiantesRestantes = cantidadestudiantes
        while estudiantesRestantes > 0:
            carreraAleatoria = random.choice(sedeCarreras)
            estudiantesAsignados[carreraAleatoria] += 1
            estudiantesRestantes -= 1
        asignacionSede = {'sede': sede, 'asignaciones': estudiantesAsignados}
        asignacionesEstudiantes.append(asignacionSede)
        if sede in estudiantesPorSede:
            estudiantesPorSede[sede].append(estudiantesAsignados)
        else:
            estudiantesPorSede[sede] = [estudiantesAsignados]
        ventanaResultados = tk.Toplevel(ventana)
        ventanaResultados.title("Resultados de Asignación de Estudiantes")
        for carrera, cantidadestudiantes in estudiantesAsignados.items():
            nombreCarrera = carreras.loc[carrera, sede]
            labelResultado = tk.Label(ventanaResultados, text=f"{nombreCarrera}: {cantidadestudiantes} estudiantes asignados")
            labelResultado.pack()
    botonAsignarEstudiantes = tk.Button(ventanaEstudiantes, text="Asignar Estudiantes", command=asignarEstudiantes)
    botonAsignarEstudiantes.pack()
    botonCerrar = tk.Button(ventanaEstudiantes, text="Cerrar", command=ventanaEstudiantes.destroy)
    botonCerrar.pack()
if 'estudiantesGenerados' not in globals():
    estudiantesGenerados = {}
    
def estudiantesCarrera():
    def mostrarSede():
        sedeElegida = sedeSeleccionada.get()
        if sedeElegida in carreras:
            if sedeElegida not in estudiantesGenerados:
                estudiantesGenerados[sedeElegida] = []
            if not estudiantesGenerados[sedeElegida]:
                sedeCarreras = carreras[sedeElegida].dropna().index.tolist()
                admitidosCarreras = {carrera: cantidadAdmitidos(sedeElegida, carrera) for carrera in sedeCarreras}
                telefonosGenerados = set()
                for carrera in sedeCarreras:
                    nombreCarrera = carreras.loc[carrera, sedeElegida]
                    for _ in range(admitidosCarreras[carrera]):
                        carnet = f"2024{opcionesSedes.index(sedeElegida) + 1:02d}{random.randint(1000, 9999)}"
                        nombreCompleto = (fake.last_name(), fake.last_name(), fake.first_name())
                        telefono = generarTelefono(telefonosGenerados)
                        correo = generarCorreo(nombreCompleto[2], nombreCompleto[0])
                        estudiantesGenerados[sedeElegida].append({'Carnet': carnet, 'Nombre Completo': f"{nombreCompleto[0]} {nombreCompleto[1]} {nombreCompleto[2]}", 'Carrera': nombreCarrera, 'Teléfono': telefono, 'Correo Electrónico': correo, 'Carnet de Mentor': "0"})
            ventanaResultados = tk.Toplevel(ventana)
            ventanaResultados.title("Estudiantes de la Sede")
            tabla = ttk.Treeview(ventanaResultados, columns=["Carnet", "Nombre Completo", "Carrera", "Teléfono", "Correo Electrónico", "Carnet de Mentor"])
            tabla.heading("#1", text="Carnet")
            tabla.heading("#2", text="Nombre Completo")
            tabla.heading("#3", text="Carrera")
            tabla.heading("#4", text="Teléfono")
            tabla.heading("#5", text="Correo Electrónico")
            tabla.heading("#6", text="Carnet de Mentor")
            tabla.pack()
            pickle.dump(estudiantesGenerados, open("estudiantesGenerados.pkl", "wb"))
            for estudiante in estudiantesGenerados[sedeElegida]:
                tabla.insert("", "end", values=(estudiante['Carnet'], estudiante['Nombre Completo'], estudiante['Carrera'], estudiante['Teléfono'], estudiante['Correo Electrónico'], estudiante['Carnet de Mentor']))
        else:
            messagebox.showerror("Error", f"La sede '{sedeElegida}' no se encuentra en el archivo Excel.")
    ventanaSede = tk.Toplevel(ventana)
    ventanaSede.title("Seleccionar Sede")
    etiquetaSeleccionSede = tk.Label(ventanaSede, text="Selecciona una sede:")
    etiquetaSeleccionSede.pack()
    opcionesSedes = ["CAMPUS TECNOLÓGICO LOCAL SAN CARLOS", "CAMPUS TECNOLÓGICO LOCAL SAN JOSÉ", "CENTRO ACADÉMICO DE LIMÓN", "CAMPUS TECNOLÓGICO CENTRAL CARTAGO", "CENTRO ACADÉMICO DE ALAJUELA"]
    sedeSeleccionada = tk.StringVar()
    sedeSeleccionada.set(opcionesSedes[0])
    listaSede = ttk.Combobox(ventanaSede, textvariable=sedeSeleccionada, values=opcionesSedes)
    listaSede.config(width=42)
    listaSede.pack()
    botonConfirmarSede = tk.Button(ventanaSede, text="Mostrar Estudiantes", command=mostrarSede)
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

def generarCorreo(nombre, apellido):
    correo = nombre[:2] + apellido.split()[0] + "@estudiantec.cr"
    return correo.lower()

if 'estudiantesGenerados' not in globals():
    estudiantesGenerados = []

def crearMentores():
    def mostrarSede():
        sedeElegida = sedeSeleccionada.get()
        if sedeElegida in carreras:
            global estudiantesGenerados, mentoresGenerados
            if sedeElegida not in mentoresGenerados:
                mentoresGenerados[sedeElegida] = [] 
            if not mentoresGenerados[sedeElegida]:
                sedeCarreras = carreras[sedeElegida].dropna().index.tolist()
                admitidosCarreras = {carrera: cantidadAdmitidos(sedeElegida, carrera) for carrera in sedeCarreras}
                for carrera in sedeCarreras:
                    nombreCarrera = carreras.loc[carrera, sedeElegida]
                    cantidadestudiantes = admitidosCarreras[carrera]
                    cantidadMentoresGenerar = int(cantidadestudiantes * 0.05)
                    for _ in range(cantidadMentoresGenerar):
                        carnet = f"2023{opcionesSedes.index(sedeElegida) + 1:02d}{random.randint(1000, 9999)}"
                        nombreCompleto = (fake.last_name(), fake.last_name(), fake.first_name())
                        correo = generarCorreo(nombreCompleto[2], nombreCompleto[0])
                        mentoresGenerados[sedeElegida].append({'Carnet': carnet, 'Nombre Completo': f"{nombreCompleto[0]} {nombreCompleto[1]} {nombreCompleto[2]}", 'Carrera': nombreCarrera, 'Correo Electrónico': correo})
            ventanaResultados = tk.Toplevel(ventana)
            ventanaResultados.title("Mentores de la Sede")
            tabla = ttk.Treeview(ventanaResultados, columns=["Carnet", "Nombre Completo", "Carrera", "Correo Electrónico"])
            tabla.heading("#1", text="Carnet")
            tabla.heading("#2", text="Nombre Completo")
            tabla.heading("#3", text="Carrera")
            tabla.heading("#4", text="Correo Electrónico")
            tabla.pack()
            for mentor in mentoresGenerados[sedeElegida]:
                tabla.insert("", "end", values=(mentor['Carnet'], mentor['Nombre Completo'], mentor['Carrera'], mentor['Correo Electrónico']))
            with open('mentores.pkl', 'wb') as archivopkl:
                pickle.dump(mentoresGenerados, archivopkl)
        else:
            messagebox.showerror("Error", f"La sede '{sedeElegida}' no se encuentra en el archivo Excel.")
    ventanaSede = tk.Toplevel(ventana)
    ventanaSede.title("Seleccionar Sede")
    etiquetaSeleccionSede = tk.Label(ventanaSede, text="Selecciona una sede:")
    etiquetaSeleccionSede.pack()
    opcionesSedes = ["CAMPUS TECNOLÓGICO LOCAL SAN CARLOS", "CAMPUS TECNOLÓGICO LOCAL SAN JOSÉ", "CENTRO ACADÉMICO DE LIMÓN", "CAMPUS TECNOLÓGICO CENTRAL CARTAGO", "CENTRO ACADÉMICO DE ALAJUELA"]
    sedeSeleccionada = tk.StringVar()
    sedeSeleccionada.set(opcionesSedes[0])
    listaSede = ttk.Combobox(ventanaSede, textvariable=sedeSeleccionada, values=opcionesSedes)
    listaSede.config(width=42)
    listaSede.pack()
    botonConfirmarSede = tk.Button(ventanaSede, text="Mostrar Mentores", command=mostrarSede)
    botonConfirmarSede.pack()

def asignarMentores():
    def mostrarSede():
        sedeElegida = sedeSeleccionada.get()
        if sedeElegida in carreras:
            global estudiantesGenerados, mentoresGenerados
            if not mentoresGenerados:
                messagebox.showerror("Error", "Primero debes generar mentores usando la función 'crearMentores'.")
            else:
                if sedeElegida not in estudiantesGenerados:
                    messagebox.showerror("Error", "Primero debes generar estudiantes para esta sede.")
                else:
                    estudiantesSede = estudiantesGenerados[sedeElegida]
                    estudiantesAsignar = [estudiante for estudiante in estudiantesSede if estudiante['Carnet de Mentor'] == "0"]
                    for estudiante in estudiantesAsignar:
                        mentorAsignado = random.choice([mentor for mentor in mentoresGenerados[sedeElegida] if mentor['Carrera'] == estudiante['Carrera']])
                        estudiante['Carnet de Mentor'] = mentorAsignado['Carnet']
                    tabla.delete(*tabla.get_children()) 
                    for estudiante in estudiantesSede:
                        nombreMentor = ""
                        if estudiante['Carnet de Mentor'] != "0":
                            mentor = next((mentor for mentor in mentoresGenerados[sedeElegida] if mentor['Carnet'] == estudiante['Carnet de Mentor']), None)
                            if mentor:
                                nombreMentor = mentor['Nombre Completo']
                        tabla.insert("", "end", values=(estudiante['Carnet'], estudiante['Nombre Completo'], estudiante['Carrera'], estudiante['Teléfono'], estudiante['Correo Electrónico'], estudiante['Carnet de Mentor'], nombreMentor))
        else:
            messagebox.showerror("Error", f"La sede '{sedeElegida}' no se encuentra en el archivo Excel.")
    ventanaSede = tk.Toplevel(ventana)
    ventanaSede.title("Seleccionar Sede")
    etiquetaSeleccionSede = tk.Label(ventanaSede, text="Selecciona una sede:")
    etiquetaSeleccionSede.pack()
    opcionesSedes = ["CAMPUS TECNOLÓGICO LOCAL SAN CARLOS", "CAMPUS TECNOLÓGICO LOCAL SAN JOSÉ", "CENTRO ACADÉMICO DE LIMÓN", "CAMPUS TECNOLÓGICO CENTRAL CARTAGO", "CENTRO ACADÉMICO DE ALAJUELA"]
    sedeSeleccionada = tk.StringVar()
    sedeSeleccionada.set(opcionesSedes[0])
    listaSede = ttk.Combobox(ventanaSede, textvariable=sedeSeleccionada, values=opcionesSedes)
    listaSede.config(width=42)
    listaSede.pack()
    botonConfirmarSede = tk.Button(ventanaSede, text="Seleccionar Sede", command=mostrarSede)
    botonConfirmarSede.pack()
    ventanaResultados = tk.Toplevel(ventana)
    ventanaResultados.title("Estudiantes con Mentores")
    tabla = ttk.Treeview(ventanaResultados, columns=["Carnet", "Nombre Completo", "Carrera", "Teléfono", "Correo Electrónico", "Carnet de Mentor", "Nombre del Mentor"])
    tabla.heading("#1", text="Carnet")
    tabla.heading("#2", text="Nombre Completo")
    tabla.heading("#3", text="Carrera")
    tabla.heading("#4", text="Teléfono")
    tabla.heading("#5", text="Correo Electrónico")
    tabla.heading("#6", text="Carnet de Mentor")
    tabla.heading("#7", text="Nombre del Mentor")
    tabla.pack()

def actualizarEstudiante():
    def abrirVentanaActualizar(sedeElegida):
        ventanaActualizar = tk.Toplevel(ventana)
        ventanaActualizar.title("Actualizar Estudiante para la Sede " + sedeElegida)
        ventanaActualizar.geometry("200x200")
        def actualizarVentana(estudianteEncontrado):
            for widget in ventanaActualizar.winfo_children():
                widget.destroy()
            tk.Label(ventanaActualizar, text="Carné del Estudiante:").pack()
            carnetVar = tk.StringVar(value=estudianteEncontrado['Carnet'])
            carnetEntry = tk.Entry(ventanaActualizar, textvariable=carnetVar)
            carnetEntry.pack()
            tk.Label(ventanaActualizar, text="Tipo de Estudiante: Mentor" if 'Carnet de Mentor' in estudianteEncontrado else "Tipo de Estudiante: Estudiante de Primer Ingreso").pack()
            tk.Label(ventanaActualizar, text="Nombre Completo:").pack()
            nombreVar = tk.StringVar(value=estudianteEncontrado['Nombre Completo'])
            nombreEntry = tk.Entry(ventanaActualizar, textvariable=nombreVar)
            nombreEntry.pack()
            if 'Teléfono' in estudianteEncontrado:
                tk.Label(ventanaActualizar, text="Teléfono:").pack()
                telefonoVar = tk.StringVar(value=estudianteEncontrado.get('Teléfono', ''))
                telefonoEntry = tk.Entry(ventanaActualizar, textvariable=telefonoVar)
                telefonoEntry.pack()
            tk.Label(ventanaActualizar, text="Correo Electrónico:").pack()
            correoVar = tk.StringVar(value=estudianteEncontrado['Correo Electrónico'])
            correoEntry = tk.Entry(ventanaActualizar, textvariable=correoVar)
            correoEntry.pack()
            def guardarCambios():
                nombre = nombreVar.get()
                estudianteEncontrado['Nombre Completo'] = nombre
                if 'Teléfono' in estudianteEncontrado:
                    telefono = telefonoVar.get()
                    estudianteEncontrado['Teléfono'] = telefono
                correo = correoVar.get()
                estudianteEncontrado['Correo Electrónico'] = correo
                messagebox.showinfo("Éxito", "Los cambios se han guardado exitosamente.")
                ventanaActualizar.destroy()
            guardarBoton = tk.Button(ventanaActualizar, text="Guardar Cambios", command=guardarCambios)
            guardarBoton.pack()
        tk.Label(ventanaActualizar, text="Carné del Estudiante:").pack()
        carnetVar = tk.StringVar()
        carnetEntry = tk.Entry(ventanaActualizar, textvariable=carnetVar)
        carnetEntry.pack()
        def buscarModificarEstudiante():
            carné = carnetVar.get()
            estudianteEncontrado = None
            for estudiante in estudiantesGenerados[sedeElegida]:
                if estudiante['Carnet'] == carné:
                    estudianteEncontrado = estudiante
                    break
            for mentor in mentoresGenerados[sedeElegida]:
                if mentor['Carnet'] == carné:
                    estudianteEncontrado = mentor
                    break
            if estudianteEncontrado is not None:
                actualizarVentana(estudianteEncontrado)
            else:
                messagebox.showerror("Error", "El carné ingresado no se encuentra en la lista de estudiantes ni mentores.")
        botonBuscar = tk.Button(ventanaActualizar, text="Buscar Estudiante", command=buscarModificarEstudiante)
        botonBuscar.pack()
    ventanaSeleccionSede = tk.Toplevel(ventana)
    ventanaSeleccionSede.title("Seleccionar Sede")
    tk.Label(ventanaSeleccionSede, text="Selecciona una sede:").pack()
    opcionesSedes = ["CAMPUS TECNOLÓGICO LOCAL SAN CARLOS","CAMPUS TECNOLÓGICO LOCAL SAN JOSÉ","CENTRO ACADÉMICO DE LIMÓN","CAMPUS TECNOLÓGICO CENTRAL CARTAGO","CENTRO ACADÉMICO DE ALAJUELA"]
    sedeSeleccionada = tk.StringVar()
    sedeSeleccionada.set(opcionesSedes[0])
    listaSede = ttk.Combobox(ventanaSeleccionSede, textvariable=sedeSeleccionada, values=opcionesSedes)
    listaSede.config(width=42)
    listaSede.pack()
    def abrirVentanaActualizarDesdeSede():
        sedeElegida = sedeSeleccionada.get()
        ventanaSeleccionSede.destroy()
        abrirVentanaActualizar(sedeElegida)
    botonSeleccionarSede = tk.Button(ventanaSeleccionSede, text="Seleccionar Sede", command=abrirVentanaActualizarDesdeSede)
    botonSeleccionarSede.pack()
    
def cargarDatosDesdeExcel():
    archivoExcel = excel
    df = pd.read_excel(archivoExcel, usecols="A:E")
    sedes = df.iloc[:, 0].unique().tolist()
    carreras = df.iloc[:, 1:6].values.tolist()
    return sedes, carreras
carreras = pd.read_excel(excel)
carrerasPorSede = {}
for sede in carreras.columns:
    carrerasSede = carreras[sede].dropna().tolist()
    carrerasPorSede[sede] = carrerasSede
    
def crearReporte():
    def reporteSede():
        sede = sedeCombobox.get()
        estudiantesSede = estudiantesGenerados.get(sede, [])
        if not estudiantesSede:
            return
        with open(f"reporte_sede_{sede}.html", "w") as file:
            file.write("<html><body>")
            file.write(f"<h1>Reporte de la Sede: {sede}</h1>")
            file.write("<table border='1'>")
            file.write("<tr>")
            file.write("<th>Carrera</th>")
            file.write("<th>Carnet</th>")
            file.write("<th>Nombre Completo</th>")
            file.write("<th>Teléfono</th>")
            file.write("<th>Correo Electrónico</th>")
            file.write("</tr>")
            for estudiante in estudiantesSede:
                file.write("<tr>")
                file.write(f"<td>{estudiante['Carrera']}</td>")
                file.write(f"<td>{estudiante['Carnet']}</td>")
                file.write(f"<td>{estudiante['Nombre Completo']}</td>")
                file.write(f"<td>{estudiante['Teléfono']}</td>")
                file.write(f"<td>{estudiante['Correo Electrónico']}</td>")
                file.write("</tr>")
            file.write("</table>")
            file.write("</body></html>")

    def reporteCarrera():
        sedeSeleccionada = sedeCombobox.get()
        carreraSeleccionada = carreraCombobox.get()
        if sedeSeleccionada and carreraSeleccionada:
            estudiantesSede = estudiantesGenerados.get(sedeSeleccionada, [])
            estudiantesCarrera = [estudiante for estudiante in estudiantesSede if estudiante['Carrera'] == carreraSeleccionada]
            if not estudiantesCarrera:
                return
            with open(f"reporte_{carreraSeleccionada}_en_{sedeSeleccionada}.html", "w") as file:
                file.write("<html><body>")
                file.write(f"<h1>Reporte de la Carrera: {carreraSeleccionada} en {sedeSeleccionada}</h1>")
                file.write("<ol>")
                for estudiante in estudiantesCarrera:
                    file.write(f"<li>{estudiante['Nombre Completo']} - {estudiante['Carnet']} - {estudiante['Correo Electrónico']}</li>")
                file.write("</ol>")
                file.write("</body></html>")
                
    def reporteMentor():
        for sede, mentores in mentoresGenerados.items():
            with open(f"reporte_mentores_en_{sede}.html", "w") as file:
                file.write("<html><body>")
                file.write(f"<h1>Reporte de Mentores en la Sede: {sede}</h1>")
                file.write("<table>")
                file.write("<tr><th>Nombre del Mentor</th><th>Carrera</th><th>Correo Electrónico</th></tr>")
                for mentor in mentores:
                    file.write(f"<tr><td>{mentor['Nombre Completo']}</td><td>{mentor['Carrera']}</td><td>{mentor['Correo Electrónico']}</td></tr>")
                file.write("</table>")
                file.write("</body></html>")
    def carrerasSegunSede(event):
        sedeSeleccionada = sedeCombobox.get()
        if sedeSeleccionada:
            carrerasSede = carreras[sedeSeleccionada].dropna().tolist()
            carreraCombobox['values'] = carrerasSede
            if carrerasSede:
                carreraCombobox.set(carrerasSede[0])
            else:
                carreraCombobox.set('')
                
    ventana = tk.Tk()
    ventana.title("Generar Informes")
    sedeLabel = tk.Label(ventana, text="Selecciona una sede:")
    sedeLabel.pack()
    sedes = list(estudiantesGenerados.keys())
    sedeCombobox = ttk.Combobox(ventana, values=sedes)
    sedeCombobox.config(width=42)
    sedeCombobox.pack()
    sedeCombobox.bind("<<ComboboxSelected>>", carrerasSegunSede)
    botonSede = tk.Button(ventana, text="Generar Informe de Sede", command=reporteSede)
    botonSede.pack()
    botonCarrera = tk.Button(ventana, text="Generar Informe de Carrera", command=reporteCarrera)
    botonCarrera.pack()
    botonMentor = tk.Button(ventana, text="Generar Informe de Mentor", command=reporteMentor)
    botonMentor.pack()
    carreraLabel = tk.Label(ventana, text="Selecciona una carrera:")
    carreraLabel.pack()
    carreraCombobox = ttk.Combobox(ventana, values=[])
    carreraCombobox.config(width=42)
    carreraCombobox.pack()
    ventana.mainloop()
archivoGlobal = ""

def crearBaseDatos():
    global archivoGlobal
    try:
        with open('estudiantesGenerados.pkl', 'rb') as estudiantesArchivo:
            estudiantesPorSede = pickle.load(estudiantesArchivo)
    except FileNotFoundError:
        messagebox.showerror("Error", "No se encontraron datos. Asegúrate de que lo hayas creado antes.")
        return
    datos = []
    for sede, estudiantes in estudiantesPorSede.items():
        for estudiante in estudiantes:
            carrera = estudiante.get('Carrera')
            carnet = estudiante.get('Carnet')
            nombreCompleto = estudiante.get('Nombre Completo')
            correo = estudiante.get('Correo Electrónico',)
            telefono = estudiante.get('Teléfono')
            datos.append([sede, carrera, carnet, nombreCompleto, correo, telefono, True])
    for sede, mentores in mentoresGenerados.items():
        for mentor in mentores:
            carrera = mentor.get('Carrera')
            carnet = mentor.get('Carnet')
            nombreCompleto = mentor.get('Nombre Completo', 'Sin Nombre')
            correo = mentor.get('Correo Electrónico')
            telefono = 'Sin Teléfono'
            datos.append([sede, carrera, carnet, nombreCompleto, correo, telefono, False])
    fechaHora = datetime.datetime.now().strftime("%d-%m-%Y_%H-%M")
    nombreArchivo = f"BDIntegraTEC_{fechaHora}.csv"
    with open(nombreArchivo, 'w', newline='') as archivocsv:
        writer = csv.writer(archivocsv)
        writer.writerow(["Sede", "Carrera", "Carnet", "Nombre", "Correo", "Teléfono", "Es Estudiante"])
        writer.writerows(datos)
    messagebox.showinfo("Éxito", f"La base de datos se ha guardado en '{nombreArchivo}'.")
    archivoGlobal = nombreArchivo
    return nombreArchivo

def buscarCSV():
    nombreArchivo = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("csv files","*.csv"),("all files","*.*")))
    return nombreArchivo

def enviarCorreo():
    remitente = "alemarra99@hotmail.com"
    asunto = "Base de datos de IntegraTEC"

    def enviarCorreoReal():
        destinatario = destinatarioVar.get()
        mensaje = mensajeVar.get()
        contraseña = "08dic1999"
        if not destinatario or not mensaje:
            messagebox.showerror("Error", "Por favor, ingresa el destinatario y el mensaje.")
            return
        email = EmailMessage()
        email['from'] = remitente
        email['subject'] = asunto
        email['to'] = destinatario
        email.set_content(mensaje)
        archivoAdjunto = archivoGlobal
        with open(archivoAdjunto, 'rb') as archivo:
            contenido = archivo.read()
            nombreArchivo = archivoAdjunto.split("\\")[-1]
            email.add_attachment(contenido, maintype='application', subtype='octet-stream', filename=nombreArchivo)
        try:
            smtp = smtplib.SMTP('smtp.office365.com', 587) 
            smtp.starttls()
            smtp.login(remitente, contraseña)
            smtp.send_message(email)
            smtp.quit()
            messagebox.showinfo("Éxito", "El correo se ha enviado exitosamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo enviar el correo. Error: {str(e)}")
    ventanaCorreo = tk.Toplevel(ventana)
    ventanaCorreo.title("Enviar Correo")
    ventanaCorreo.geometry("200x200")
    tk.Label(ventanaCorreo, text=asunto).pack()
    tk.Label(ventanaCorreo, text="Para:").pack()
    destinatarioVar = tk.StringVar()
    destinatarioEntry = tk.Entry(ventanaCorreo, textvariable=destinatarioVar)
    destinatarioEntry.pack()
    tk.Label(ventanaCorreo, text="Mensaje:").pack()
    mensajeVar = tk.StringVar()
    mensajeEntry = tk.Entry(ventanaCorreo, textvariable=mensajeVar)
    mensajeEntry.pack()
    botonEnviarCorreo = tk.Button(ventanaCorreo, text="Enviar Correo", command=enviarCorreoReal)
    botonEnviarCorreo.pack()

#Interfaz gráfica
ventana = tk.Tk()
ventana.title("Atención a la Generación 2024")
ventana.geometry("1200x600")  
imagen= r'D:\Estudios de Ale\Compu\GitHub\Tareas Programadas\TareaProgramada2\TareaProgramada2\Main (no listo)\tec.png'
imagenFondo = Image.open(imagen)

imagenFondo = imagenFondo.resize((ventana.winfo_screenwidth(), ventana.winfo_screenheight()))
imagenFondo = ImageTk.PhotoImage(imagenFondo)

etiquetaFondo = tk.Label(ventana, image=imagenFondo)
etiquetaFondo.place(x=0, y=0, relwidth=1, relheight=1)

fondoGris = tk.Frame(ventana, bg="#D0ECE7")
fondoGris.place(relx=0.25, rely=0, relwidth=0.5, relheight=1)

frameBotones = tk.Frame(fondoGris, bg="#D0ECE7")
frameBotones.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)
logo= r'D:\Estudios de Ale\Compu\GitHub\Tareas Programadas\TareaProgramada2\TareaProgramada2\Main (no listo)\integratec.png'
logoImagen = Image.open(logo)
logoImagen = logoImagen.resize((int(ventana.winfo_screenwidth() * 0.3), int(ventana.winfo_screenheight() * 0.2)))
logoImagen = ImageTk.PhotoImage(logoImagen)

etiquetaLogo = tk.Label(fondoGris, image=logoImagen, bg="#D0ECE7")
etiquetaLogo.pack(pady=(30, 10)) 

def crearBoton(text, command):
    return tk.Button(frameBotones, text=text, command=command, bg="#A6CFCF", fg="black", relief="raised", font=("Arial", 12))

boton1 = ttk.Button(fondoGris, text="Estudiantes por sede", command=estudiantesSede)
boton2 = ttk.Button(fondoGris, text="Estudiantes de carrera por sede", command=estudiantesCarrera)
boton3 = ttk.Button(fondoGris, text="Crear mentores", command=crearMentores)
boton4 = ttk.Button(fondoGris, text="Asignar mentores", command=asignarMentores)
boton5 = ttk.Button(fondoGris, text="Actualizar estudiante", command=actualizarEstudiante)
boton6 = ttk.Button(fondoGris, text="Generar reportes", command=crearReporte)
boton7 = ttk.Button(fondoGris, text="Crear base de datos en Excel", command=crearBaseDatos)
boton8 = ttk.Button(fondoGris, text="Enviar correo", command=enviarCorreo)

boton1.pack(fill="both", expand=True)
boton2.pack(fill="both", expand=True)
boton3.pack(fill="both", expand=True)
boton4.pack(fill="both", expand=True)
boton5.pack(fill="both", expand=True)
boton6.pack(fill="both", expand=True)
boton7.pack(fill="both", expand=True)
boton8.pack(fill="both", expand=True)

ventana.mainloop()