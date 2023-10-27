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

#Variables globales
fake = Faker()
cantidadEstudiantes = None
excel = r'C:\Users\k1r1e\Documents\GitHub\TareaProgramada2\Main (no listo)\sedes.xlsx' #Cambiar el directorio en donde está el archivo sedes.xlsx
carreras = pd.read_excel(excel)
asignacionesEstudiantes = []
cantidadEstudiantes = None 
cantidad_estudiantes = 0
estudiantesPorSede = {}
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
        if sede in estudiantesPorSede:
            estudiantesPorSede[sede].append(estudiantesAsignados)
        else:
            estudiantesPorSede[sede] = [estudiantesAsignados]
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
mentoresGenerados = {}

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
                    cantidad_estudiantes = admitidosCarreras[carrera]
                    cantidad_mentores_a_generar = int(cantidad_estudiantes * 0.05)
                    for _ in range(cantidad_mentores_a_generar):
                        carnet = f"2023{opcionesSedes.index(sedeElegida) + 1:02d}{random.randint(1000, 9999)}"
                        nombreCompleto = (fake.last_name(), fake.last_name(), fake.first_name())
                        correo = generarCorreo(nombreCompleto[2], nombreCompleto[0])
                        mentoresGenerados[sedeElegida].append({'Carnet': carnet, 'Nombre Completo': f"{nombreCompleto[0]} {nombreCompleto[1]} {nombreCompleto[2]}", 'Carrera': nombreCarrera, 'Correo Electrónico': correo})
            ventanaResultados = tk.Toplevel(ventana)
            ventanaResultados.title("Mentores de la Sede")
            tabla = ttk.Treeview(ventanaResultados, columns=["Carnet", "Nombre Completo", "Carrera", "Correo Electrónico"])
            tabla.heading("#0", text="Carnet")
            tabla.heading("#1", text="Nombre Completo")
            tabla.heading("#2", text="Carrera")
            tabla.heading("#3", text="Correo Electrónico")
            tabla.pack()
            for mentor in mentoresGenerados[sedeElegida]:
                tabla.insert("", "end", values=(mentor['Carnet'], mentor['Nombre Completo'], mentor['Carrera'], mentor['Correo Electrónico']))
            with open('mentores.pkl', 'wb') as archivo_pkl:
                pickle.dump(mentoresGenerados, archivo_pkl)
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
                    estudiantes_sede = estudiantesGenerados[sedeElegida]
                    estudiantes_para_asignar = [estudiante for estudiante in estudiantes_sede if estudiante['Carnet de Mentor'] == "0"]
                    for estudiante in estudiantes_para_asignar:
                        mentor_asignado = random.choice([mentor for mentor in mentoresGenerados[sedeElegida] if mentor['Carrera'] == estudiante['Carrera']])
                        estudiante['Carnet de Mentor'] = mentor_asignado['Carnet']
                    tabla.delete(*tabla.get_children()) 
                    for estudiante in estudiantes_sede:
                        nombre_mentor = ""
                        if estudiante['Carnet de Mentor'] != "0":
                            mentor = next((mentor for mentor in mentoresGenerados[sedeElegida] if mentor['Carnet'] == estudiante['Carnet de Mentor']), None)
                            if mentor:
                                nombre_mentor = mentor['Nombre Completo']
                        tabla.insert("", "end", values=(estudiante['Carnet'], estudiante['Nombre Completo'], estudiante['Carrera'], estudiante['Teléfono'], estudiante['Correo Electrónico'], estudiante['Carnet de Mentor'], nombre_mentor))
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
        ventana_actualizar = tk.Toplevel(ventana)
        ventana_actualizar.title("Actualizar Estudiante para la Sede " + sedeElegida)
        def actualizarVentana(estudiante_encontrado):
            for widget in ventana_actualizar.winfo_children():
                widget.destroy()
            tk.Label(ventana_actualizar, text="Carné del Estudiante:").pack()
            carné_var = tk.StringVar(value=estudiante_encontrado['Carnet'])
            carné_entry = tk.Entry(ventana_actualizar, textvariable=carné_var)
            carné_entry.pack()
            tk.Label(ventana_actualizar, text="Tipo de Estudiante: Mentor" if 'Carnet de Mentor' in estudiante_encontrado else "Tipo de Estudiante: Estudiante de Primer Ingreso").pack()
            tk.Label(ventana_actualizar, text="Nombre Completo:").pack()
            nombre_var = tk.StringVar(value=estudiante_encontrado['Nombre Completo'])
            nombre_entry = tk.Entry(ventana_actualizar, textvariable=nombre_var)
            nombre_entry.pack()
            if 'Teléfono' in estudiante_encontrado:
                tk.Label(ventana_actualizar, text="Teléfono:").pack()
                telefono_var = tk.StringVar(value=estudiante_encontrado.get('Teléfono', ''))
                telefono_entry = tk.Entry(ventana_actualizar, textvariable=telefono_var)
                telefono_entry.pack()
            tk.Label(ventana_actualizar, text="Correo Electrónico:").pack()
            correo_var = tk.StringVar(value=estudiante_encontrado['Correo Electrónico'])
            correo_entry = tk.Entry(ventana_actualizar, textvariable=correo_var)
            correo_entry.pack()
            def guardar_cambios():
                nombre = nombre_var.get()
                estudiante_encontrado['Nombre Completo'] = nombre
                if 'Teléfono' in estudiante_encontrado:
                    telefono = telefono_var.get()
                    estudiante_encontrado['Teléfono'] = telefono
                correo = correo_var.get()
                estudiante_encontrado['Correo Electrónico'] = correo
                messagebox.showinfo("Éxito", "Los cambios se han guardado exitosamente.")
                ventana_actualizar.destroy()
            guardar_button = tk.Button(ventana_actualizar, text="Guardar Cambios", command=guardar_cambios)
            guardar_button.pack()
        tk.Label(ventana_actualizar, text="Carné del Estudiante:").pack()
        carné_var = tk.StringVar()
        carné_entry = tk.Entry(ventana_actualizar, textvariable=carné_var)
        carné_entry.pack()
        def buscar_y_modificar_estudiante():
            carné = carné_var.get()
            estudiante_encontrado = None
            for estudiante in estudiantesGenerados[sedeElegida]:
                if estudiante['Carnet'] == carné:
                    estudiante_encontrado = estudiante
                    break
            for mentor in mentoresGenerados[sedeElegida]:
                if mentor['Carnet'] == carné:
                    estudiante_encontrado = mentor
                    break
            if estudiante_encontrado is not None:
                actualizarVentana(estudiante_encontrado)
            else:
                messagebox.showerror("Error", "El carné ingresado no se encuentra en la lista de estudiantes ni mentores.")
        buscar_button = tk.Button(ventana_actualizar, text="Buscar Estudiante", command=buscar_y_modificar_estudiante)
        buscar_button.pack()
    ventanaSeleccionSede = tk.Toplevel(ventana)
    ventanaSeleccionSede.title("Seleccionar Sede")
    tk.Label(ventanaSeleccionSede, text="Selecciona una sede:").pack()
    opcionesSedes = [
        "CAMPUS TECNOLÓGICO LOCAL SAN CARLOS",
        "CAMPUS TECNOLÓGICO LOCAL SAN JOSÉ",
        "CENTRO ACADÉMICO DE LIMÓN",
        "CAMPUS TECNOLÓGICO CENTRAL CARTAGO",
        "CENTRO ACADÉMICO DE ALAJUELA"
    ]
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
    
def generarReportes():
    def reporteSede():
        sede = sede_combobox.get()
        if sede:
            estudiantes_sede = estudiantesPorSede.get(sede, [])
            if estudiantes_sede:
                generar_reporte_estudiantes(sede, estudiantes_sede)
            else:
                messagebox.showwarning("Advertencia", f"No hay estudiantes para la sede {sede}.")

    def reporteCarrera():
        sede = sede_combobox.get()
        if sede:
            estudiantes_sede = estudiantesPorSede.get(sede, [])
            carreras = set(estudiante['Carrera'] for estudiante in estudiantes_sede)
            seleccionar_carrera(sede, carreras)

    def seleccionar_carrera(sede, carreras):
        ventana_carrera = tk.Toplevel(ventana)
        ventana_carrera.title(f"Seleccionar Carrera en {sede}")
        carrera_combobox = ttk.Combobox(ventana_carrera, values=list(carreras))
        carrera_combobox.pack()
        generar_carrera_button = tk.Button(ventana_carrera, text="Generar Reporte por Carrera", command=lambda: reporteCarreraCarrera(sede, carrera_combobox.get()))
        generar_carrera_button.pack()

    def reporteCarreraCarrera(sede, carrera):
        estudiantes_sede = estudiantesPorSede.get(sede, [])
        estudiantes_carrera = [estudiante for estudiante in estudiantes_sede if estudiante['Carrera'] == carrera]
        if estudiantes_carrera:
            generar_reporte_estudiantes(sede, estudiantes_carrera)
        else:
            messagebox.showwarning("Advertencia", f"No hay estudiantes en la carrera {carrera} para la sede {sede}.")

    def generar_reporte_estudiantes(sede, estudiantes):
        reporte = f"<html><head><title>Reporte de Estudiantes en {sede}</title></head><body>"
        reporte += f"<h1>Reporte de Estudiantes en {sede}</h1>"

        reporte += "<table border='1'><tr><th>Carnet</th><th>Nombre Completo</th><th>Carrera</th><th>Teléfono</th><th>Correo Electrónico</th><th>Carnet de Mentor</th></tr>"
        for estudiante in estudiantes:
            reporte += f"<tr><td>{estudiante.get('Carnet', '')}</td><td>{estudiante.get('Nombre Completo', '')}</td><td>{estudiante.get('Carrera', '')}</td><td>{estudiante.get('Teléfono', '')}</td><td>{estudiante.get('Correo Electrónico', '')}</td><td>{estudiante.get('Carnet de Mentor', '')}</td></tr>"
        reporte += "</table>"

        reporte += "</body></html>"

        with open(f"reporte_{sede.replace(' ', '_')}.html", "w") as archivo:
            archivo.write(reporte)

        messagebox.showinfo("Éxito", f"Reporte de Estudiantes en {sede} generado con éxito. Puedes encontrarlo en el archivo reporte_{sede.replace(' ', '_')}.html")

    def generar_reporte_mentores():
        mentores = cargar_mentores()
        if mentores:
            reporte = "<html><head><title>Reporte de Mentores</title></head><body>"
            reporte += "<h1>Reporte de Mentores</h1>"

            for sede, mentores_sede in mentores.items():
                reporte += f"<h2>Sede: {sede}</h2>"
                for mentor in mentores_sede:
                    reporte += f"<h3>Mentor: {mentor.get('Nombre Completo', '')}</h3>"
                    reporte += "<ul>"
                    estudiantes_asignados = mentor.get('Estudiantes Asignados', [])
                    for estudiante in estudiantes_asignados:
                        reporte += f"<li>{estudiante.get('Carnet', '')} - {estudiante.get('Nombre Completo', '')}</li>"
                    reporte += "</ul>"

            reporte += "</body></html>"

            with open("reporte_mentores.html", "w") as archivo:
                archivo.write(reporte)

            messagebox.showinfo("Éxito", "Reporte de Mentores generado con éxito. Puedes encontrarlo en el archivo reporte_mentores.html")
        else:
            messagebox.showwarning("Advertencia", "No hay datos de mentores disponibles.")

    def cargar_mentores():
        try:
            with open("mentores.pkl", "rb") as archivo:
                return pickle.load(archivo)
        except (FileNotFoundError, EOFError):
            return None

    ventanaReportes = tk.Toplevel(ventana)
    ventanaReportes.title("Generar Reportes")

    botonSede = tk.Button(ventanaReportes, text="Reporte por Sede", command=reporteSede)
    botonCarrera = tk.Button(ventanaReportes, text="Reporte por Carrera", command=reporteCarrera)
    botonMentor = tk.Button(ventanaReportes, text="Reporte por Mentor", command=generar_reporte_mentores)

    botonSede.pack()
    botonCarrera.pack()
    botonMentor.pack()

    sede_combobox = ttk.Combobox(ventanaReportes, values=list(estudiantesPorSede.keys()))
    sede_combobox.set("Selecciona una sede")

    def mostrar_sede_combobox():
        sede_combobox.pack()

    botonSede.config(command=mostrar_sede_combobox)

def crearBaseDatos():
    try:
        with open('estudiantesGenerados.pkl', 'rb') as estudiantes_file:
            estudiantesPorSede = pickle.load(estudiantes_file)
    except FileNotFoundError:
        messagebox.showerror("Error", "No se encontraron datos. Asegúrate de que lo hayas creado antes.")
        return
    try:
        with open('mentores.pkl', 'rb') as mentores_file:
            mentoresGenerados = pickle.load(mentores_file)
    except FileNotFoundError:
        messagebox.showerror("Error", "No se encontraron datos. Asegúrate de que lo hayas creado antes.")
        return
    datos = []
    for sede, estudiantes in estudiantesPorSede.items():
        for estudiante in estudiantes:
            carrera = estudiante.get('Carrera', 'Sin Carrera')
            carnet = estudiante.get('Carnet', 'Sin Carnet')
            nombre_completo = estudiante.get('Nombre Completo', 'Sin Nombre')
            correo = estudiante.get('Correo Electrónico', 'Sin Correo')
            telefono = estudiante.get('Teléfono', 'Sin Teléfono')
            datos.append([sede, carrera, carnet, nombre_completo, correo, telefono, True])
    for sede, mentores in mentoresGenerados.items():
        for mentor in mentores:
            carrera = mentor.get('Carrera', 'Sin Carrera')
            carnet = mentor.get('Carnet', 'Sin Carnet')
            nombre_completo = mentor.get('Nombre Completo', 'Sin Nombre')
            correo = mentor.get('Correo Electrónico', 'Sin Correo')
            telefono = 'Sin Teléfono'
            datos.append([sede, carrera, carnet, nombre_completo, correo, telefono, False])
    fecha_hora = datetime.datetime.now().strftime("%d-%m-%Y_%H-%M")
    nombre_archivo = f"BDIntegraTEC_{fecha_hora}.csv"
    with open(nombre_archivo, 'w', newline='') as archivo_csv:
        writer = csv.writer(archivo_csv)
        writer.writerow(["Sede", "Carrera", "Carnet", "Nombre", "Correo", "Teléfono", "Es Estudiante"])
        writer.writerows(datos)
    messagebox.showinfo("Éxito", f"La base de datos se ha guardado en '{nombre_archivo}'.")
    return nombre_archivo

def buscarCSV():
    nombreArchivo = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("csv files","*.csv"),("all files","*.*")))
    return nombreArchivo

def enviarCorreo():
    nombreArchivo = buscarCSV()
    remitente = "integratec2024@gmail.com"
    asunto = "Base de datos de IntegraTEC"
    destinatario_var = tk.StringVar()
    destinatario_entry = tk.Entry(ventanaCorreo, textvariable=destinatario_var)
    destinatario_entry.pack()
    destinatario = destinatario_var.get()
    mensaje = mensaje_var.get()
    email = EmailMessage()
    email['from'] = remitente
    email['subject'] = asunto
    email['to'] = destinatario
    email.set_content(mensaje)
    archivo_adjunto = f'C:\\Users\\k1r1e\\Documents\\GitHub\\TareaProgramada2\\{nombreArchivo}.csv'
    with open(archivo_adjunto, 'rb') as archivo:
        contenido = archivo.read()
        nombreArchivo = archivo_adjunto.split("\\")[-1]
        email.add_attachment(contenido, maintype='application', subtype='octet-stream', filename=nombreArchivo)
    try:
        smtp = smtplib.SMTP_SSL('smtp.gmail.com')
        smtp.login(remitente, "teix qjdp sgcy cvf")
        smtp.send_message(email)
        smtp.quit()
        messagebox.showinfo("Éxito", "El correo se ha enviado exitosamente.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo enviar el correo. Error: {str(e)}")
    ventanaCorreo = tk.Toplevel(ventana)
    ventanaCorreo.title("Enviar Correo")
    tk.Label(ventanaCorreo, text=asunto).pack()
    tk.Label(ventanaCorreo, text="Para:").pack()
    tk.Label(ventanaCorreo, text="Mensaje:").pack()
    mensaje_var = tk.StringVar()
    mensaje_entry = tk.Entry(ventanaCorreo, textvariable=mensaje_var)
    mensaje_entry.pack()
    botonEnviarCorreo = tk.Button(ventanaCorreo, text="Enviar Correo", command=lambda: enviarCorreo(nombreArchivo))
    botonEnviarCorreo.pack()

#Interfaz gráfica
ventana = tk.Tk()
ventana.title("Atención a la Generación 2024")
ventana.geometry("1200x600")  

imagen_fondo = Image.open("tec.png")
imagen_fondo = imagen_fondo.resize((ventana.winfo_screenwidth(), ventana.winfo_screenheight()))
imagen_fondo = ImageTk.PhotoImage(imagen_fondo)

etiqueta_fondo = tk.Label(ventana, image=imagen_fondo)
etiqueta_fondo.place(x=0, y=0, relwidth=1, relheight=1)

fondo_gris = tk.Frame(ventana, bg="#D0ECE7")
fondo_gris.place(relx=0.25, rely=0, relwidth=0.5, relheight=1)

frame_botones = tk.Frame(fondo_gris, bg="#D0ECE7")
frame_botones.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)

logo_image = Image.open("integratec.png")
logo_image = logo_image.resize((int(ventana.winfo_screenwidth() * 0.3), int(ventana.winfo_screenheight() * 0.2)))
logo_image = ImageTk.PhotoImage(logo_image)

etiqueta_logo = tk.Label(fondo_gris, image=logo_image, bg="#D0ECE7")
etiqueta_logo.pack(pady=(30, 10)) 

def create_button(text, command):
    return tk.Button(frame_botones, text=text, command=command, bg="#A6CFCF", fg="black", relief="raised", font=("Arial", 12))

boton1 = ttk.Button(fondo_gris, text="Estudiantes por sede", command=estudiantesSede)
boton2 = ttk.Button(fondo_gris, text="Estudiantes de carrera por sede", command=estudiantesCarrera)
boton3 = ttk.Button(fondo_gris, text="Crear mentores", command=crearMentores)
boton4 = ttk.Button(fondo_gris, text="Asignar mentores", command=asignarMentores)
boton5 = ttk.Button(fondo_gris, text="Actualizar estudiante", command=actualizarEstudiante)
boton6 = ttk.Button(fondo_gris, text="Generar reportes", command=generarReportes)
boton7 = ttk.Button(fondo_gris, text="Crear base de datos en Excel", command=crearBaseDatos)
boton8 = ttk.Button(fondo_gris, text="Enviar correo", command=enviarCorreo)

boton1.pack(fill="both", expand=True)
boton2.pack(fill="both", expand=True)
boton3.pack(fill="both", expand=True)
boton4.pack(fill="both", expand=True)
boton5.pack(fill="both", expand=True)
boton6.pack(fill="both", expand=True)
boton7.pack(fill="both", expand=True)
boton8.pack(fill="both", expand=True)

ventana.mainloop()