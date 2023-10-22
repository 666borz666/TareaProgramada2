#Creado por: Daniel Campos y Alejandro Madrigal
#Creación: 10-10-2023 
#Ultima modificación: 15-10-2023 
#Versión: 3.12.0
#Importacion de librerias
import tkinter as tk
import random
from tkinter import ttk
from faker import Faker
fake = Faker()
import pandas as pd
import os
from tkinter import messagebox
cantidad_estudiantes = None
print(os.getcwd())
import os

archivo_excel = r'D:\Estudios de Ale\Compu\GitHub\Tareas Programadas\TareaProgramada2\TareaProgramada2\Main (no listo)\sedes.xlsx'
df_carreras = pd.read_excel(archivo_excel)
asignaciones_estudiantes = []
cantidad_estudiantes_entry = None 
def estudiantesSede():
    def asignar_estudiantes():
        global asignaciones_estudiantes  # Accede a la variable global

        cantidad_total_estudiantes = int(cantidad_estudiantes_entry.get())
        sede = sede_seleccionada.get()
        carreras_sede = df_carreras[sede].dropna().index.tolist()
        
        # Distribuir equitativamente entre carreras
        estudiantes_asignados = {carrera: 0 for carrera in carreras_sede}
        estudiantes_restantes = cantidad_total_estudiantes

        while estudiantes_restantes > 0:
            # Seleccionar una carrera aleatoria
            carrera_aleatoria = random.choice(carreras_sede)
            
            # Asignar un estudiante a la carrera aleatoria
            estudiantes_asignados[carrera_aleatoria] += 1
            
            # Reducir el número de estudiantes restantes
            estudiantes_restantes -= 1

        # Almacenar información de asignación de estudiantes en la variable global
        asignaciones_estudiantes = asignaciones_estudiantes + [{
            'carrera': carrera,
            'cantidad_estudiantes': cantidad_estudiantes
        } for carrera, cantidad_estudiantes in estudiantes_asignados.items()]

        # Crear una ventana emergente para mostrar los resultados
        ventana_resultados = tk.Toplevel(ventana)
        ventana_resultados.title("Resultados de Asignación de Estudiantes")

        for carrera, estudiantes_asignados in estudiantes_asignados.items():
            # Obtener el nombre de la carrera desde el archivo Excel
            nombre_carrera = df_carreras.loc[carrera, sede]
            label_resultado = tk.Label(ventana_resultados, text=f"{nombre_carrera}: {estudiantes_asignados} estudiantes asignados")
            label_resultado.pack()

    # Crear una ventana secundaria para seleccionar la sede
    ventana_estudiantes = tk.Toplevel(ventana)
    ventana_estudiantes.title("Estudiantes por Sede")

    # Etiqueta y lista desplegable para seleccionar la sede
    etiqueta_sede = tk.Label(ventana_estudiantes, text="Selecciona una sede:")
    etiqueta_sede.pack()

    # Opciones de sedes
    opciones_sedes = [
        "CAMPUS TECNOLÓGICO LOCAL SAN CARLOS",
        "CAMPUS TECNOLÓGICO LOCAL SAN JOSÉ",
        "CENTRO ACADÉMICO DE LIMÓN",
        "CAMPUS TECNOLÓGICO CENTRAL CARTAGO",
        "CENTRO ACADÉMICO DE ALAJUELA"
    ]

    sede_seleccionada = tk.StringVar()
    sede_seleccionada.set(opciones_sedes[0])  # Establece la primera sede como predeterminada

    lista_desplegable_sede = ttk.Combobox(ventana_estudiantes, textvariable=sede_seleccionada, values=opciones_sedes)
    lista_desplegable_sede.pack()

    # Etiqueta y campo de entrada para especificar la cantidad de estudiantes
    etiqueta_cantidad = tk.Label(ventana_estudiantes, text="Cantidad total de estudiantes:")
    etiqueta_cantidad.pack()

    cantidad_estudiantes_entry = tk.Entry(ventana_estudiantes)
    cantidad_estudiantes_entry.pack()

    # Botón para asignar estudiantes
    boton_asignar_estudiantes = tk.Button(ventana_estudiantes, text="Asignar Estudiantes", command=asignar_estudiantes)
    boton_asignar_estudiantes.pack()

archivo_excel = r'D:\Estudios de Ale\Compu\GitHub\Tareas Programadas\TareaProgramada2\TareaProgramada2\Main (no listo)\sedes.xlsx'
df_carreras = pd.read_excel(archivo_excel)

def estudiantesCarrera():
    def mostrar_estudiantes_de_sede():
        # Obtener la sede seleccionada
        sede_elegida = sede_seleccionada.get()

        # Verificar si la sede seleccionada se encuentra en el archivo Excel
        if sede_elegida in df_carreras:
            # Obtener las carreras asociadas a la sede
            carreras_sede = df_carreras[sede_elegida].dropna().index.tolist()

            # Seleccionar una carrera aleatoria
            nombre_carrera = random.choice(carreras_sede)

            # Crear una ventana emergente para mostrar los datos de los estudiantes de la sede en una tabla
            ventana_resultados = tk.Toplevel(ventana)
            ventana_resultados.title("Estudiantes de la Sede")

            # Crear una tabla
            tabla = ttk.Treeview(ventana_resultados, columns=["Carné", "Nombre Completo", "Carrera", "Teléfono", "Correo Electrónico", "Carné de Mentor"])
            tabla.heading("#1", text="Carné")
            tabla.heading("#2", text="Nombre Completo")
            tabla.heading("#3", text="Carrera")
            tabla.heading("#4", text="Teléfono")
            tabla.heading("#5", text="Correo Electrónico")
            tabla.heading("#6", text="Carné de Mentor")
            tabla.pack()

            # Obtener la cantidad de admitidos en la carrera seleccionada en la opción 1 (estudiantesSede)
            admitidos_carrera_seleccionada = obtener_cantidad_admitidos_carrera(sede_elegida, nombre_carrera)

            estudiantes_generados = []
            telefonos_generados = set()  # Utilizado para evitar duplicados de teléfonos

            for _ in range(admitidos_carrera_seleccionada):
                # Generar un número de carné que refleje el año y el número de sede, junto con un número de 4 dígitos aleatorio
                carnet = f"2024{opciones_sedes.index(sede_elegida) + 1:02d}{random.randint(1000, 9999)}"

                # Generar nombres completos aleatorios
                nombre_completo = (fake.last_name(), fake.last_name(), fake.first_name())

                # Generar teléfono y correo electrónico
                telefono = generar_telefono(telefonos_generados)
                correo = generar_correo(nombre_completo[2], nombre_completo[0])

                # Utilizar el nombre de la carrera seleccionada
                # como el valor de la columna 'Carrera' en los datos generados
                estudiantes_generados.append({
                    'Carné': carnet,
                    'Nombre Completo': f"{nombre_completo[0]} {nombre_completo[1]} {nombre_completo[2]}",
                    'Carrera': nombre_carrera,
                    'Teléfono': telefono,
                    'Correo Electrónico': correo,
                    'Carné de Mentor': "0",
                })

            for estudiante in estudiantes_generados:
                # Insertar los datos del estudiante en la tabla
                tabla.insert("", "end", values=(estudiante['Carné'], estudiante['Nombre Completo'], estudiante['Carrera'], estudiante['Teléfono'], estudiante['Correo Electrónico'], estudiante['Carné de Mentor']))
        else:
            # Manejar el caso en el que la sede no se encuentra en el archivo Excel
            messagebox.showerror("Error", f"La sede '{sede_elegida}' no se encuentra en el archivo Excel.")

    # Crear una ventana emergente para seleccionar la sede
    ventana_seleccion_sede = tk.Toplevel(ventana)
    ventana_seleccion_sede.title("Seleccionar Sede")

    # Etiqueta para la selección de sede
    etiqueta_seleccion_sede = tk.Label(ventana_seleccion_sede, text="Selecciona una sede:")
    etiqueta_seleccion_sede.pack()

    opciones_sedes = [
        "CAMPUS TECNOLÓGICO LOCAL SAN CARLOS",
        "CAMPUS TECNOLÓGICO LOCAL SAN JOSÉ",
        "CENTRO ACADÉMICO DE LIMÓN",
        "CAMPUS TECNOLÓGICO CENTRAL CARTAGO",
        "CENTRO ACADÉMICO DE ALAJUELA"
    ]

    sede_seleccionada = tk.StringVar()
    sede_seleccionada.set(opciones_sedes[0])

    lista_desplegable_sede = ttk.Combobox(ventana_seleccion_sede, textvariable=sede_seleccionada, values=opciones_sedes)
    lista_desplegable_sede.pack()

    # Botón para confirmar la selección de sede y generar estudiantes
    boton_confirmar_sede = tk.Button(ventana_seleccion_sede, text="Mostrar Estudiantes", command=mostrar_estudiantes_de_sede)
    boton_confirmar_sede.pack()


# Función para obtener la cantidad de estudiantes por carrera desde la opción 1
def obtener_cantidad_admitidos_carrera(sede, carrera):
    # Obtén la información de la cantidad de estudiantes admitidos para la sede y carrera dadas
    sede_info = [info for info in asignaciones_estudiantes if info['sede'] == sede]
    if sede_info:
        asignaciones = sede_info[0]['asignaciones']
        if carrera in asignaciones:
            return asignaciones[carrera]
    return 0  # Devuelve 0 si no se encuentra información
def generar_telefono(telefonos_generados):
    # Generar un teléfono que comience con 6, 7, 8 o 9 y tenga 7 dígitos distintos
    while True:
        primer_digito = random.choice("6789")
        otros_digitos = random.sample("0123456789", 7)
        telefono = primer_digito + ''.join(otros_digitos)
        if telefono not in telefonos_generados:
            telefonos_generados.add(telefono)
            return telefono

def generar_correo(nombre, apellido):
    # Generar un correo con las 2 primeras letras del nombre, primer apellido y dominio
    correo = nombre[:2] + apellido.split()[0] + "@estudiantec.cr"
    return correo
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

