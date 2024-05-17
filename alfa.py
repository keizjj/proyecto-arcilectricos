import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import Calendar
from datetime import datetime
import matplotlib.pyplot as plt
import csv

# Variables globales para el registro de tiempo de actividad
tiempo_inicio = None
tiempo_fin = None
actividad_en_curso = False

# Diccionario para almacenar las actividades registradas
actividades = []

def guardar_actividades():
    with open("actividades.csv", mode="w", newline="") as archivo_csv:
        escritor_csv = csv.writer(archivo_csv)
        escritor_csv.writerow(["Inicio", "Fin", "Descripción"])
        for actividad in actividades:
            escritor_csv.writerow([actividad["inicio"], actividad["fin"], actividad["descripcion"]])

def iniciar_actividad():
    global actividad_en_curso, tiempo_inicio
    if not actividad_en_curso:
        tiempo_inicio = datetime.now()
        actividad_en_curso = True
        messagebox.showinfo("Registro de actividad", "Actividad iniciada.")

def terminar_actividad():
    global actividad_en_curso, tiempo_fin
    if actividad_en_curso:
        tiempo_fin = datetime.now()
        actividad_en_curso = False
        duracion = tiempo_fin - tiempo_inicio
        descripcion = descripcion_entry.get()
        actividades.append({
            "inicio": tiempo_inicio,
            "fin": tiempo_fin,
            "descripcion": descripcion
        })
        guardar_actividades()
        messagebox.showinfo("Registro de actividad", f"Actividad registrada exitosamente.\nDuración: {duracion}")

def consultar_tiempo_trabajado_por_dia():
    tiempo_trabajado_por_dia = {}
    for actividad in actividades:
        inicio = actividad["inicio"]
        fin = actividad["fin"]
        fecha = inicio.date()
        duracion = (fin - inicio).total_seconds() / 3600  # Duración en horas
        if fecha not in tiempo_trabajado_por_dia:
            tiempo_trabajado_por_dia[fecha] = 0
        tiempo_trabajado_por_dia[fecha] += duracion

    fechas = list(tiempo_trabajado_por_dia.keys())
    tiempo_trabajado = list(tiempo_trabajado_por_dia.values())

    plt.figure(figsize=(10, 6))
    plt.plot(fechas, tiempo_trabajado, marker='o', linestyle='-')
    plt.xlabel('Fecha')
    plt.ylabel('Tiempo trabajado (horas)')
    plt.title('Tiempo trabajado por día')
    plt.grid(True)
    plt.xticks(rotation=45)  # Rotación de las etiquetas de fecha
    plt.tight_layout()
    plt.show()

def consultar_tiempo_entre_fechas(fecha_inicio, fecha_fin):
    tiempo_total = 0
    for actividad in actividades:
        inicio = actividad["inicio"]
        fin = actividad["fin"]
        if inicio.date() >= fecha_inicio and fin.date() <= fecha_fin:
            duracion = (fin - inicio).total_seconds() / 3600  # Duración en horas
            tiempo_total += duracion
    return tiempo_total

def seleccionar_fechas():
    def obtener_fechas():
        fecha_inicio = cal_inicio.selection_get()
        fecha_fin = cal_fin.selection_get()
        tiempo_total = consultar_tiempo_entre_fechas(fecha_inicio, fecha_fin)
        messagebox.showinfo("Tiempo Trabajado", f"Tiempo total trabajado entre {fecha_inicio} y {fecha_fin}: {tiempo_total:.2f} horas")
        ventana_emergente2.destroy()

    ventana_emergente2 = tk.Toplevel(root)
    ventana_emergente2.title("Seleccionar Fechas")

    tk.Label(ventana_emergente2, text="Fecha de Inicio").pack(pady=5)
    cal_inicio = Calendar(ventana_emergente2, selectmode='day')
    cal_inicio.pack(pady=5)

    tk.Label(ventana_emergente2, text="Fecha de Fin").pack(pady=5)
    cal_fin = Calendar(ventana_emergente2, selectmode='day')
    cal_fin.pack(pady=5)

    tk.Button(ventana_emergente2, text="Consultar", command=obtener_fechas).pack(pady=20)

def mostrar_ventana_emergente():
    ventana_emergente = tk.Toplevel(root)
    ventana_emergente.title("Ventana Emergente")

    # Botón para consultar grafica tiempo trabajado por día
    consultar_button = tk.Button(ventana_emergente, text="Grafica", command=consultar_tiempo_trabajado_por_dia)
    consultar_button.pack(pady=20)
    
    # Botón para abrir la ventana emergente
    boton = tk.Button(ventana_emergente, text="suma de horas", command=seleccionar_fechas)
    boton.pack(pady=20)
    
        # Botón para consultar el tiempo quetomo realizar cierta actividad
    consultar_button = tk.Button(ventana_emergente, text="actividades", command=mostrar_ventana_emergente3)
    consultar_button.pack(pady=20)

def mostrar_ventana_emergente3():
    def calcular_tiempo_actividad():
        actividad_seleccionada = actividad_combo.get()
        tiempo_total = sum((act['fin'] - act['inicio']).total_seconds() / 3600 for act in actividades if act['descripcion'] == actividad_seleccionada)
        messagebox.showinfo("Tiempo Total", f"Tiempo total invertido en '{actividad_seleccionada}': {tiempo_total:.2f} horas")
        ventana_emergente3.destroy()

    ventana_emergente3 = tk.Toplevel(root)
    ventana_emergente3.title("Consultar Tiempo de Actividad")

    actividad_label = tk.Label(ventana_emergente3, text="Seleccione la actividad:")
    actividad_label.pack(pady=5)

    actividades_descripciones = list(set(act['descripcion'] for act in actividades))
    actividad_combo = ttk.Combobox(ventana_emergente3, values=actividades_descripciones)
    actividad_combo.pack(pady=5)

    calcular_button = tk.Button(ventana_emergente3, text="Calcular Tiempo", command=calcular_tiempo_actividad)
    calcular_button.pack(pady=20)

# Crear la ventana principal
root = tk.Tk()
root.title("Registro de Actividades")

# Etiqueta y entrada para la descripción de la actividad
descripcion_label = tk.Label(root, text="Descripción:")
descripcion_label.grid(row=0, column=0, padx=5, pady=5)
descripcion_entry = tk.Entry(root, width=50)
descripcion_entry.grid(row=0, column=1, padx=5, pady=5)

# Botón para iniciar actividad
iniciar_button = tk.Button(root, text="Iniciar Actividad", command=iniciar_actividad)
iniciar_button.grid(row=1, column=0, padx=5, pady=5, sticky="WE")

# Botón para terminar actividad
terminar_button = tk.Button(root, text="Terminar Actividad", command=terminar_actividad)
terminar_button.grid(row=1, column=1, padx=5, pady=5, sticky="WE")

# Botón para abrir la ventana emergente
boton = tk.Button(root, text="funciones", command=mostrar_ventana_emergente)
boton.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="WE")

# Función para cerrar la ventana
def cerrar_ventana():
    root.destroy()

# Configurar cierre de la ventana
root.protocol("WM_DELETE_WINDOW", cerrar_ventana)

# Cargar actividades al inicio
try:
    with open("actividades.csv", mode="r", newline="") as archivo_csv:
        lector_csv = csv.reader(archivo_csv)
        next(lector_csv)  # Saltar la fila de encabezado
        for fila in lector_csv:
            inicio = datetime.strptime(fila[0], "%Y-%m-%d %H:%M:%S.%f")
            fin = datetime.strptime(fila[1], "%Y-%m-%d %H:%M:%S.%f")
            descripcion = fila[2]
            actividades.append({
                "inicio": inicio,
                "fin": fin,
                "descripcion": descripcion
            })
except FileNotFoundError:
    pass

# Iniciar el bucle de eventos
root.mainloop()

