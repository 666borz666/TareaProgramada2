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
import pickle
import os
from PIL import Image, ImageTk
#Variables globales
fake = Faker()
cantidadEstudiantes = None
excel = r'D:\Estudios de Ale\Compu\GitHub\Tareas Programadas\TareaProgramada2\TareaProgramada2\Main (no listo)\sedes.xlsx'
carreras = pd.read_excel(excel)
asignacionesEstudiantes = []
cantidadEstudiantes = None 
cantidad_estudiantes = 0
#Funciones
estudiantesPorSede = {}

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

        # Verificar si ya existe una lista de estudiantes para esta sede
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
                estudiantesGenerados[sedeElegida] = []  # Inicializa una lista vacía para la sede si no existe

            if not estudiantesGenerados[sedeElegida]:
                # Generar estudiantes solo si la lista para esta sede está vacía
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

            # Mostrar los estudiantes en la tabla
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
#Auxiliares para estudiantesCarrera   
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
            global estudiantesGenerados, mentoresGenerados  # Asegura que estamos trabajando con las variables globales

            # Resto del código sin cambios
            # Esta parte genera mentores si no están generados
            if sedeElegida not in mentoresGenerados:
                mentoresGenerados[sedeElegida] = []  # Inicializa una lista vacía para la sede si no existe

            if not mentoresGenerados[sedeElegida]:
                sedeCarreras = carreras[sedeElegida].dropna().index.tolist()
                admitidosCarreras = {carrera: cantidadAdmitidos(sedeElegida, carrera) for carrera in sedeCarreras}
                for carrera in sedeCarreras:
                    nombreCarrera = carreras.loc[carrera, sedeElegida]
                    cantidad_estudiantes = admitidosCarreras[carrera]

                    # Calcular la cantidad de mentores (5% de estudiantes)
                    cantidad_mentores_a_generar = int(cantidad_estudiantes * 0.05)

                    for _ in range(cantidad_mentores_a_generar):
                        carnet = f"2023{opcionesSedes.index(sedeElegida) + 1:02d}{random.randint(1000, 9999)}"
                        nombreCompleto = (fake.last_name(), fake.last_name(), fake.first_name())
                        correo = generarCorreo(nombreCompleto[2], nombreCompleto[0])
                        mentoresGenerados[sedeElegida].append({'Carnet': carnet, 'Nombre Completo': f"{nombreCompleto[0]} {nombreCompleto[1]} {nombreCompleto[2]}", 'Carrera': nombreCarrera, 'Correo Electrónico': correo})

            # Esta parte muestra estudiantes y mentores en la tabla
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

            # Guardar los datos en un archivo .pkl
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
            global estudiantesGenerados, mentoresGenerados  # Asegura que estamos trabajando con las variables globales
            if not mentoresGenerados:
                messagebox.showerror("Error", "Primero debes generar mentores usando la función 'crearMentores'.")
            else:
                if sedeElegida not in estudiantesGenerados:
                    messagebox.showerror("Error", "Primero debes generar estudiantes para esta sede.")
                else:
                    # Obtener los estudiantes de la sede seleccionada
                    estudiantes_sede = estudiantesGenerados[sedeElegida]

                    # Obtener los estudiantes que tienen "0" en el campo "Carnet de Mentor"
                    estudiantes_para_asignar = [estudiante for estudiante in estudiantes_sede if estudiante['Carnet de Mentor'] == "0"]

                    # Asignar mentores a estos estudiantes, asegurándonos de que sean de la misma carrera
                    for estudiante in estudiantes_para_asignar:
                        mentor_asignado = random.choice([mentor for mentor in mentoresGenerados[sedeElegida] if mentor['Carrera'] == estudiante['Carrera']])
                        estudiante['Carnet de Mentor'] = mentor_asignado['Carnet']

                    # Actualizar la tabla con los estudiantes y sus mentores
                    tabla.delete(*tabla.get_children())  # Limpiar la tabla
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

    # Crear la tabla
    ventanaResultados = tk.Toplevel(ventana)
    ventanaResultados.title("Estudiantes con Mentores")
    tabla = ttk.Treeview(ventanaResultados, columns=["Carnet", "Nombre Completo", "Carrera", "Teléfono", "Correo Electrónico", "Carnet de Mentor", "Nombre del Mentor"])
    tabla.heading("#0", text="Carnet")
    tabla.heading("#1", text="Nombre Completo")
    tabla.heading("#2", text="Carrera")
    tabla.heading("#3", text="Teléfono")
    tabla.heading("#4", text="Correo Electrónico")
    tabla.heading("#5", text="Carnet de Mentor")
    tabla.heading("#6", text="Nombre del Mentor")
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

            # Función para guardar los cambios
            def guardar_cambios():
                nombre = nombre_var.get()
                estudiante_encontrado['Nombre Completo'] = nombre

                if 'Teléfono' in estudiante_encontrado:
                    # Si es un estudiante de primer ingreso, permitir la edición del teléfono
                    telefono = telefono_var.get()
                    estudiante_encontrado['Teléfono'] = telefono

                correo = correo_var.get()
                estudiante_encontrado['Correo Electrónico'] = correo

                messagebox.showinfo("Éxito", "Los cambios se han guardado exitosamente.")
                ventana_actualizar.destroy()

            # Botón para guardar los cambios
            guardar_button = tk.Button(ventana_actualizar, text="Guardar Cambios", command=guardar_cambios)
            guardar_button.pack()

        tk.Label(ventana_actualizar, text="Carné del Estudiante:").pack()
        carné_var = tk.StringVar()
        carné_entry = tk.Entry(ventana_actualizar, textvariable=carné_var)
        carné_entry.pack()

        def buscar_y_modificar_estudiante():
            carné = carné_var.get()
            estudiante_encontrado = None

            # Buscar al estudiante por carné en la lista de estudiantesGenerados de la sede seleccionada
            for estudiante in estudiantesGenerados[sedeElegida]:
                if estudiante['Carnet'] == carné:
                    estudiante_encontrado = estudiante
                    break

            # Buscar al mentor por carné en la lista de mentoresGenerados de la sede seleccionada
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
    return

def crearBaseDatos():
    return

def enviarCorreo():
    return  

ventana = tk.Tk()
ventana.title("Atención a la Generación 2024")
ventana.geometry("1200x600")  # Tamaño razonable

# Cargar la imagen de fondo
imagen_fondo = Image.open("tec.png")
imagen_fondo = imagen_fondo.resize((ventana.winfo_screenwidth(), ventana.winfo_screenheight()))
imagen_fondo = ImageTk.PhotoImage(imagen_fondo)

# Crear una etiqueta para mostrar la imagen de fondo
etiqueta_fondo = tk.Label(ventana, image=imagen_fondo)
etiqueta_fondo.place(x=0, y=0, relwidth=1, relheight=1)

# Crear un Frame para el fondo gris en el centro
fondo_gris = tk.Frame(ventana, bg="#D0ECE7")
fondo_gris.place(relx=0.25, rely=0, relwidth=0.5, relheight=1)

# Crear un Frame para los botones en la columna del centro
frame_botones = tk.Frame(fondo_gris, bg="#D0ECE7")
frame_botones.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)
logo_image = Image.open("integratec.png")
logo_image = logo_image.resize((int(ventana.winfo_screenwidth() * 0.3), int(ventana.winfo_screenheight() * 0.2)))
logo_image = ImageTk.PhotoImage(logo_image)

etiqueta_logo = tk.Label(fondo_gris, image=logo_image, bg="#D0ECE7")
etiqueta_logo.pack(pady=(30, 10))  # Espaciado en la parte superior

# Función para crear botones con un estilo diferente
def create_button(text, command):
    return tk.Button(frame_botones, text=text, command=command, bg="#A6CFCF", fg="black", relief="raised", font=("Arial", 12))

# Crear botones con estilo
# Crear botones con estilo y asignar funciones al clic
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




