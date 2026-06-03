# LIBRERÍAS DE PYTHON

import folium
from tkinterweb import HtmlFrame  # Permite ver páginas web o mapas dentro de nuestra ventana.
import tkinter as tk
from tkinter import messagebox
import os
from PIL import ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import winsound  # Sirve para reproducir sonido y música en ordenadores con Windows.
import customtkinter as ctk  # Librería para hacer la interfaz más atractiva

from airport import *
from aircraft import *
from LEBL_NEW import *

# Configuración de customtkinter
ctk.set_appearance_mode("Light")  # Hace que el programa empiece con el Modo Claro por defecto
ctk.set_default_color_theme("blue")  # Hace que los botones y barras por defecto sean de color azul.


# COLORES DE LA APLICACIÓN

# En Modo Claro:
CL_BG = "#F8FAFC"  # Color para el fondo de la ventana.
CL_FRAME = "#E2E8F0"  # Color para los LabelFrames.
CL_TEXT = "#0F172A"  # Color para las letras.
CL_ACCENT = "#3B82F6"  # Color azul para botones normales de cargar datos o buscar.
CL_SUCCESS = "#10B981"  # Color verde para botones positivos (como "Añadir" o "Asignar").
CL_DANGER = "#EF4444"  # Color rojo para botones de peligro o borrar (como "Eliminar").
CL_ENTRY = "#FFFFFF"  # Color blanco para el fondo donde el usuario escribe texto.

# En Modo Oscuro:
DK_BG = "#0F172A"
DK_FRAME = "#1E293B"
DK_TEXT = "#F8FAFC"
DK_ACCENT = "#2563EB"
DK_SUCCESS = "#059669"
DK_DANGER = "#DC2626"
DK_ENTRY = "#1E293B"

# Aquí creamos parejas de colores (Color Claro, Color Oscuro).
# El programa sabe automáticamente cuál usar según si elegimos modo claro o modo oscuro
CTK_BG = (CL_BG, DK_BG)
CTK_FRAME = (CL_FRAME, DK_FRAME)
CTK_TEXT = (CL_TEXT, DK_TEXT)
CTK_ACCENT = (CL_ACCENT, DK_ACCENT)
CTK_SUCCESS = (CL_SUCCESS, DK_SUCCESS)
CTK_DANGER = (CL_DANGER, DK_DANGER)
CTK_ENTRY = (CL_ENTRY, DK_ENTRY)

# Diccionarios de colores para las partes del programa que no entienden el sistema automático de arriba.
PALETA_CLARA = {"bg": CL_BG, "fg": CL_TEXT, "card": CL_ENTRY, "frame_bg": CL_FRAME}
PALETA_OSCURA = {"bg": DK_BG, "fg": DK_TEXT, "card": DK_ENTRY, "frame_bg": DK_FRAME}

# Tipos de letra y tamaños
FONT_LABEL = ("Segoe UI", 9)  # Letra normal de los textos.
FONT_BTN = ("Segoe UI", 9, "bold")  # Letra en negrita para los botones.
FONT_TITLE = ("Segoe UI", 14)  # Letra más grande para los títulos de cada sección.
FONT_STATUS = ("Segoe UI", 9, "bold")  # Letra para el aviso de texto de la parte inferior.

# Función para aplicar el diseño de los títulos de forma fácil
def estilo_frame(bg=CL_FRAME, fg=CL_TEXT):
    return dict(bg=bg, fg=fg, font=FONT_TITLE)


# DATOS GLOBALES

Airports_list = []
Arrivals_list = []
pady_number = 3  # Separación de 3 píxeles entre botones para que no estén pegados.

visualizacion_activa = "ninguna"  # Nos dice qué se está viendo a la derecha: "grafico", "mapa" o "ninguna".
canvas_puertas_global = None  # Guardará el dibujo interactivo de las terminales del aeropuerto.

bcn = BarcelonaAP("LEBL")

# VENTANA PRINCIPAL

ventana = ctk.CTk()
ventana.geometry('1200x800')
ventana.minsize(1050, 700)  # No deja que el usuario la haga más pequeña de este tamaño para que no se rompa el diseño.
ventana.title('Airport Manager | By: Managing Airports SA™')
ventana.configure(fg_color=CTK_BG)

# REPARTO DEL ESPACIO
ventana.columnconfigure(0, weight=0, minsize=300)  # La columna izquierda (menú) mide 300 píxeles de ancho fijo.
ventana.columnconfigure(1, weight=1)  # La columna derecha (dibujos/gráficos) se estira.
ventana.rowconfigure(0, weight=1)  # La parte de arriba se estira verticalmente.
ventana.rowconfigure(1, weight=0)  # La parte de abajo ocupa lo justo.


# BARRA LATERAL IZQUIERDA

# Creamos una barra a la izquierda que si tiene muchas opciones, te deja bajar usando un scrollbar.
sidebar = ctk.CTkScrollableFrame(ventana, width=300, fg_color=CTK_BG)
sidebar.grid(row=0, column=0, rowspan=6, sticky=tk.NSEW, padx=5, pady=5)
sidebar.columnconfigure(0, weight=1)


# TEXTO DE AVISOS ABAJO
# Reemplaza los messagebox.showinfo por una barra informativa en la base de la app
status_label = ctk.CTkLabel(ventana, text="System Ready",font=FONT_STATUS,fg_color=("#DBEAFE", "#1E3A8A"), text_color=("#1D4ED8", "#93C5FD"),
        height=35, corner_radius=6)
status_label.grid(row=6, column=0, columnspan=2, sticky=tk.NSEW, padx=5, pady=5)

#Función para poner un mensaje abajo.
def mostrar_aviso(texto, es_error=False):
    if es_error:
        bg = ("#FEE2E2", "#7F1D1D")
        fg = ("#B91C1C", "#FCA5A5")
    else:
        bg = ("#DBEAFE", "#1E3A8A")
        fg = ("#1D4ED8", "#93C5FD")

    status_label.configure(text=texto, text_color=fg, fg_color=bg)

    #Borra el texto de la barra para dejarla limpia
    def limpiar():
        if status_label.cget("text") == texto:
            status_label.configure(text="", fg_color=("#DBEAFE", "#1E3A8A"), text_color=("#1D4ED8", "#93C5FD"))

    # Hace que el programa espere 4 segundos (4000 milisegundos) antes de borrar el mensaje de la pantalla de forma automática.
    ventana.after(4000, limpiar)


# BLOQUE 1: AIRPORT MANAGEMENT:

#Marco principal de la sección Airport Management
airport_management_frame = tk.LabelFrame(sidebar, text='  Airport Management  ',**estilo_frame())
airport_management_frame.grid(row=0, column=0, padx=5, pady=5,sticky=tk.N + tk.S + tk.E + tk.W)
airport_management_frame.rowconfigure(0, weight=1)
airport_management_frame.rowconfigure(1, weight=3)
airport_management_frame.rowconfigure(2, weight=1)
airport_management_frame.columnconfigure(0, weight=1)

#Busca y lee el archivo 'Airports.txt' con la lista de aeropuertos y los guarda en la memoria.
def Load_Airports_INT():
    global Airports_list
    Airports_list = LoadAirports('Airports.txt')  # Lógica del cerebro del programa.
    if len(Airports_list) > 0:
        mostrar_aviso('Airports Loaded Successfully')
    else:
        mostrar_aviso('No Airports Found', es_error=True)

#Creamos el botón para cargar esos aeropuertos
load_airports_button = ctk.CTkButton(airport_management_frame, text="Load Airports",
    command=Load_Airports_INT, fg_color=CTK_ACCENT, text_color="#FFFFFF", font=FONT_BTN)
load_airports_button.grid(column=0, row=0, padx=8, pady=pady_number,sticky=tk.W + tk.E + tk.N + tk.S)

# Añadir un aeropuerto nuevo a mano
add_airport_frame = tk.LabelFrame(airport_management_frame, text='  Add Airport  ',**estilo_frame())
add_airport_frame.grid(column=0, row=1, padx=5, pady=pady_number,sticky=tk.W + tk.E + tk.N + tk.S)
add_airport_frame.rowconfigure(0, weight=1)
add_airport_frame.rowconfigure(1, weight=1)
add_airport_frame.rowconfigure(2, weight=1)
add_airport_frame.columnconfigure(0, weight=1)

# Cuadro para escribir el código ICAO del aeropuerto
ICAO = tk.LabelFrame(add_airport_frame, text='ICAO', **estilo_frame())
ICAO.grid(column=0, row=0, padx=5, pady=pady_number,sticky=tk.W + tk.E + tk.N + tk.S)
ICAO.rowconfigure(0, weight=1)
ICAO.columnconfigure(0, weight=1)
ICAO_entry = ctk.CTkEntry(ICAO, fg_color=CTK_ENTRY, text_color=CTK_TEXT, font=FONT_LABEL)
ICAO_entry.grid(column=0, row=0, padx=5, pady=pady_number,sticky=tk.W + tk.E + tk.N + tk.S)

# Cuadro para escribir la Latitud
Lat = tk.LabelFrame(add_airport_frame, text='Latitude', **estilo_frame())
Lat.grid(column=0, row=1, padx=5, pady=pady_number, sticky=tk.NSEW)
Lat.columnconfigure(0, weight=1)
Lat_entry = ctk.CTkEntry(Lat, fg_color=CTK_ENTRY, text_color=CTK_TEXT, font=FONT_LABEL)
Lat_entry.grid(column=0, row=0, padx=5, pady=pady_number, sticky=tk.NSEW)

# Cuadro para escribir la Longitud
Lon = tk.LabelFrame(add_airport_frame, text='Longitude', **estilo_frame())
Lon.grid(column=0, row=2, padx=5, pady=pady_number, sticky=tk.NSEW)
Lon.columnconfigure(0, weight=1)
Lon_entry = ctk.CTkEntry(Lon, fg_color=CTK_ENTRY, text_color=CTK_TEXT, font=FONT_LABEL)
Lon_entry.grid(column=0, row=0, padx=5, pady=pady_number, sticky=tk.NSEW)

#Lee lo que el usuario ha escrito en las casillas, comprueba que esté bien y añade el aeropuerto.
def Add_Airport_INT():
    global Airports_list
    if len(Airports_list) <= 0:
        mostrar_aviso('Load the Airports first', es_error=True)
        return
    # Recoge los textos, les quita los espacios sobrantes y los pone en mayúsculas
    v_icao = ICAO_entry.get().strip().upper()
    latitude = Lat_entry.get().strip()
    longitude = Lon_entry.get().strip()
    # Crea el objeto y comprueba si ya existía antes de guardarlo
    added_airport = Airport(v_icao, latitude, longitude)
    resultado = AddAirport(Airports_list, added_airport)

    if resultado == 'Error|El aeropuerto ya existe':
        mostrar_aviso('Error | Airport already exists', es_error=True)
    else:
        mostrar_aviso('Airport Added Successfully')


# Botón verde para confirmar y guardar el aeropuerto nuevo
add_airport_button = ctk.CTkButton(add_airport_frame, command=Add_Airport_INT,text='＋  Add Airport',
    fg_color=CTK_SUCCESS, text_color="#FFFFFF", font=FONT_BTN)
add_airport_button.grid(row=3, column=0, padx=8, pady=pady_number,sticky=tk.W + tk.E + tk.N + tk.S)

# Borrar un Aeropuerto
remove_frame = tk.LabelFrame(airport_management_frame, text='  Removal of Airports  ',**estilo_frame())
remove_frame.grid(column=0, row=2, padx=5, pady=pady_number,sticky=tk.W + tk.E + tk.N + tk.S)
remove_frame.rowconfigure(0, weight=1)
remove_frame.rowconfigure(1, weight=1)
remove_frame.columnconfigure(0, weight=1)

# Cuadro para escribir cuál queremos borrar
remove_ICAO = tk.LabelFrame(remove_frame, text='ICAO', **estilo_frame())
remove_ICAO.grid(row=0, column=0, padx=5, pady=pady_number,sticky=tk.W + tk.E + tk.N + tk.S)
remove_ICAO.rowconfigure(0, weight=1)
remove_ICAO.columnconfigure(0, weight=1)
remove_ICAO_entry = ctk.CTkEntry(remove_ICAO, fg_color=CTK_ENTRY, text_color=CTK_TEXT, font=FONT_LABEL)
remove_ICAO_entry.grid(row=0, column=0, padx=5, pady=pady_number,sticky=tk.W + tk.E + tk.N + tk.S)

#Busca el código que escribió el usuario y si existe en la lista, lo elimina.
def Remove_Airport_INT():
    global Airports_list
    if len(Airports_list) <= 0:
        mostrar_aviso('Load the Airports first', es_error=True)
        return

    ICAO_removal = remove_ICAO_entry.get().strip().upper()
    resultado = RemoveAirport(Airports_list, ICAO_removal)

    if resultado == 'Error|Aeropuerto no encontrado':
        mostrar_aviso('Error | Airport not found', es_error=True)
    else:
        mostrar_aviso('Airport Removed Successfully')


# Botón para eliminar el aeropuerto escrito
remove_ICAO_button = ctk.CTkButton(remove_ICAO, text="✕  Remove",command=Remove_Airport_INT, fg_color=CTK_DANGER, text_color="#FFFFFF", font=FONT_BTN)
remove_ICAO_button.grid(row=1, column=0, padx=8, pady=pady_number,sticky=tk.W + tk.E + tk.N + tk.S)


# PANEL DE VISUALIZACIÓN  (columna derecha)

# Es el cuadro gigante en blanco de la derecha donde aparecerán todos los gráficos y planos del aeropuerto.
canvas_frame = tk.LabelFrame(ventana, text='  Advanced Visualization System®  ',
    bg=CL_BG, fg=CL_TEXT, font=FONT_TITLE)
canvas_frame.grid(row=0, column=1, rowspan=4, padx=5, pady=pady_number,sticky=tk.W + tk.E + tk.N + tk.S)
canvas_frame.rowconfigure(0, weight=1)
canvas_frame.columnconfigure(0, weight=1)
canva = tk.Canvas(canvas_frame, width=200, height=400, bg=CL_BG,highlightthickness=0)
canva.grid(row=0, column=0, rowspan=5, padx=5, pady=pady_number,sticky=tk.W + tk.E + tk.N + tk.S)

# Se encarga de borrar cualquier dibujo o gráfico que haya a la derecha para dejar el espacio totalmente vacío.
def Clear_Canvas():
    for widget in canvas_frame.winfo_children():
        widget.destroy()


# MAPAS Y GRÁFICOS

#Comprueba cuáles de los aeropuertos cargados están dentro del espacio Schengen y los dibuja.
def Schengen_Plot_INT():
    global Airports_list
    if len(Airports_list) <= 0:
        mostrar_aviso('Load the Airports first', es_error=True)
        return

    Clear_Canvas()  # Limpia la pantalla derecha.
    SetSchengen(Airports_list)  # Analiza cuáles son europeos.
    fig = PlotAirports(Airports_list)  # Genera el gráfico

    # Dibuja ese gráfico dentro de la ventana de nuestro programa
    canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=0, sticky=tk.NSEW)

    if 'canva' in globals():
        canva.grid_forget()  # Esconde el lienzo vacío de bienvenida.


# Botón para dibujar el gráfico:
schengen_plot_button = ctk.CTkButton(sidebar, text='◑  Plot Schengen Airports',
    command=Schengen_Plot_INT, fg_color=CTK_ACCENT, text_color="#FFFFFF", font=FONT_BTN)
schengen_plot_button.grid(column=0, row=1, padx=8, pady=pady_number,sticky=tk.W + tk.E + tk.N + tk.S)

#Crea un archivo de mapa KML de los aeropuertos y pide al ordenador que lo abra con Google Earth
def open_maps():
    global Arrivals_list

    # Validamos que se hayan cargado las llegadas previamente
    if len(Arrivals_list) <= 0:
        mostrar_aviso('Load arrivals first to draw the routes.', es_error=True)
        return

    # Invocamos la función lógica unificada que acabamos de programar
    archivo_combinado = MapCombined(Arrivals_list)

    # Abrimos directamente el archivo resultante en Google Earth
    if os.path.exists(archivo_combinado):
        os.startfile(archivo_combinado)
        mostrar_aviso('Opening combined Schengen Airports and Arrival Routes in Google Earth.')
    else:
        mostrar_aviso('Error: KML file could not be generated.', es_error=True)

# Botón para ver el mapa
open_maps_button = ctk.CTkButton(sidebar, text='🗺  Show Map',
    command=open_maps, fg_color=CTK_SUCCESS, text_color="#FFFFFF", font=FONT_BTN)
open_maps_button.grid(row=2, column=0, padx=8, pady=pady_number,sticky=tk.W + tk.E + tk.N)


# BLOQUE 2: ARRIVALS

# Cajita en el menú para agrupar los datos de vuelos que aterrizan
arrivals = tk.LabelFrame(sidebar, text='  Arrivals  ',**estilo_frame())
arrivals.grid(row=3, column=0, padx=5, pady=pady_number,sticky=tk.W + tk.E + tk.N)
arrivals.columnconfigure(0, weight=1)
arrivals.columnconfigure(1, weight=1)
arrivals.rowconfigure(0, weight=1)
arrivals.rowconfigure(1, weight=1)

#Lee el archivo 'Arrivals.txt' que contiene los vuelos programados para hoy.
def Load_Arrivals_INT():
    global Arrivals_list
    Arrivals_list = LoadArrivals('Arrivals.txt')

    # Comprueba si hubo algún fallo leyendo el archivo de texto
    if isinstance(Arrivals_list, str) and "Error" in Arrivals_list:
        mostrar_aviso(Arrivals_list, es_error=True)
        Arrivals_list = []
    elif len(Arrivals_list) <= 0:
        mostrar_aviso('No arrivals found.', es_error=True)
    else:
        mostrar_aviso('Arrivals loaded successfully.')


# Botón para cargar los vuelos
load_arrivals_button = ctk.CTkButton(arrivals, text='Load Arrivals',
    command=Load_Arrivals_INT, fg_color=CTK_ACCENT, text_color="#FFFFFF", font=FONT_BTN)
load_arrivals_button.grid(row=0, column=0, padx=5, pady=pady_number,rowspan=2, sticky=tk.W + tk.E + tk.N + tk.S)

#Crea un gráfico que muestra el porcentaje de vuelos de cada aerolínea.
def Plot_Arrivals_INT():
    global Arrivals_list
    if len(Arrivals_list) <= 0:
        mostrar_aviso('Load arrivals first', es_error=True)
        return
    Clear_Canvas()
    fig = PlotAirlines(Arrivals_list)
    canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=0, padx=5, pady=pady_number, sticky=tk.NSEW)
    if 'canvas' in globals():
        canva.grid_forget()


# Botón para ver el gráfico de aerolíneas
plot_arrivals_button = ctk.CTkButton(arrivals, text='◑  By Airline',
    command=Plot_Arrivals_INT, fg_color=CTK_ACCENT, text_color="#FFFFFF", font=FONT_BTN)
plot_arrivals_button.grid(row=0, column=1, padx=5, pady=pady_number,sticky=tk.W + tk.E + tk.N + tk.S)


def PlotFlightsType_INT():
    global Arrivals_list
    if len(Arrivals_list) <= 0:
        mostrar_aviso('Load arrivals first', es_error=True)
        return
    fig = PlotFlightsType(Arrivals_list)  # Pide el gráfico por tipo de avión.
    Clear_Canvas()
    canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=0, padx=5, pady=pady_number, sticky=tk.NSEW)
    if 'canvas' in globals():
        canvas.grid_forget()


# Botón para ver el gráfico por tipo de avión
plot_type_button = ctk.CTkButton(arrivals, command=PlotFlightsType_INT,
    text='◑  By Type', fg_color=CTK_ACCENT, text_color="#FFFFFF", font=FONT_BTN)
plot_type_button.grid(column=1, row=1, padx=5, pady=pady_number,sticky=tk.W + tk.E + tk.N + tk.S)


# BLOQUE 3: GATE MANAGEMENT EN LEBL

# Cajita para las herramientas del simulador de Barcelona-El Prat
gates_frame = tk.LabelFrame(sidebar, text='  Airport Gate Management  ',**estilo_frame())
gates_frame.grid(row=4, column=0, padx=5, pady=pady_number,sticky=tk.W + tk.E + tk.N + tk.S)
gates_frame.columnconfigure(0, weight=1)
gates_frame.columnconfigure(1, weight=1)
gates_frame.columnconfigure(2, weight=1)
gates_frame.rowconfigure(0, weight=1)
gates_frame.rowconfigure(1, weight=1)
gates_frame.rowconfigure(2, weight=1)

# Casilla pequeña para escribir "T1" o "T2"
terminal_input_frame = tk.LabelFrame(gates_frame, text="Terminal (T1/T2)", **estilo_frame())
terminal_input_frame.grid(row=0, column=2, padx=5, pady=pady_number, sticky=tk.NSEW)
terminal_entry = ctk.CTkEntry(terminal_input_frame, width=60, fg_color=CTK_ENTRY, text_color=CTK_TEXT, font=FONT_LABEL)
terminal_entry.grid(row=0, column=0, padx=5, pady=5)

#Carga cómo está construido el aeropuerto físicamente.
def LoadAirport_Structure_INT():
    global bcn
    nombre_archivo = "Terminals.txt"
    resultado = LoadAirportStructure(nombre_archivo)

    if resultado == "Error | File not found":
        mostrar_aviso(f"Error: {nombre_archivo} no encontrado", es_error=True)
    elif resultado == -1:
        mostrar_aviso("Error al procesar la estructura del aeropuerto", es_error=True)
    else:
        bcn = resultado  # Rellena el aeropuerto con las puertas de verdad.
        mostrar_aviso('Barcelona Airport Structure (LEBL) loaded successfully.')


# Botón para cargar la estructura del aeropuerto
load_airport_structure = ctk.CTkButton(gates_frame, text='Load Airport Structure',
    command=LoadAirport_Structure_INT, fg_color=CTK_ACCENT, text_color="#FFFFFF", font=FONT_BTN)
load_airport_structure.grid(row=0, column=0, columnspan=2, padx=5,pady=pady_number, sticky=tk.W + tk.E + tk.N + tk.S)

#Configura qué compañías vuelan en la terminal que hemos escrito en la casilla
def LoadAirlines_INT():
    t_name = terminal_entry.get().strip().upper()
    if t_name not in ["T1", "T2"]:
        mostrar_aviso('Please input T1 or T2 in the text field.', es_error=True)
        return

    # Comprobamos que el aeropuerto esté cargado buscando si la terminal existe en la memoria
    terminal_encontrada = None
    for term in bcn.terminals:
        if term.name == t_name:
            terminal_encontrada = term
            break

    if not terminal_encontrada:
        mostrar_aviso('Load Airport Structure first.', es_error=True)
        return

    resultado = LoadAirlines(terminal_encontrada, t_name)
    if resultado == "Error | File not found":
        mostrar_aviso(f'File {t_name}_Airlines.txt not found.', es_error=True)
    else:
        mostrar_aviso(f'Airlines for {t_name} loaded successfully.')


# Botón para cargar las aerolíneas de la terminal elegida
load_airlines_button = ctk.CTkButton(
    gates_frame, text='Load Airlines',
    command=LoadAirlines_INT, fg_color=CTK_ACCENT, text_color="#FFFFFF", font=FONT_BTN)
load_airlines_button.grid(row=1, column=0, padx=5, pady=pady_number,
                          sticky=tk.W + tk.E + tk.N + tk.S)

#Dibuja un gráfico que muestra qué puertas están ocupadas a lo largo de las 24 horas
def PlotGateOccupancy_INT():
    global bcn, visualizacion_activa
    if len(bcn.terminals) == 0:
        mostrar_aviso('Load Airport Structure first.', es_error=True)
        return

    departures_list = LoadDepartures('Departures.txt')  # Carga los vuelos que salen.
    vuelos_del_dia = MergeMovements(Arrivals_list, departures_list)  # Los junta ordenados por hora.

    if vuelos_del_dia == -1 or len(vuelos_del_dia) == 0:
        mostrar_aviso('Load Arrivals/Departures first for simulation.', es_error=True)
        return

    visualizacion_activa = "grafico"
    Clear_Canvas()
    PlotDayOccupancy(bcn, vuelos_del_dia)
    plt.tight_layout()

    fig = plt.gcf()
    fig.set_size_inches(9.5, 4.5)  # Le da el tamaño adecuado.

    canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=0, sticky=tk.NSEW)


# Botón para ver la ocupación diaria de todas las puertas
plot_Gate_Occupancy_button = ctk.CTkButton(gates_frame, text='◑  Gate Occupancy',
    command=PlotGateOccupancy_INT, fg_color=CTK_ACCENT, text_color="#FFFFFF", font=FONT_BTN)
plot_Gate_Occupancy_button.grid(row=1, column=2, padx=5, pady=pady_number,sticky=tk.W + tk.E + tk.N + tk.S)

# Buscador: En qué terminal opera cada aerolínea
search_terminal_frame = tk.LabelFrame(gates_frame, text='  Search Terminal  ', **estilo_frame())
search_terminal_frame.grid(row=2, column=0, columnspan=3, padx=5,pady=pady_number, sticky=tk.W + tk.E + tk.N + tk.S)
search_terminal_frame.columnconfigure(0, weight=1)
search_terminal_frame.rowconfigure(0, weight=1)

airline_entry_frame = tk.LabelFrame(search_terminal_frame, text='Airline', **estilo_frame())
airline_entry_frame.grid(row=0, column=0, padx=5, pady=pady_number,sticky=tk.W + tk.E + tk.N + tk.S)
airline_entry_frame.columnconfigure(0, weight=1)
airline_entry_frame.rowconfigure(0, weight=1)
airline_entry = ctk.CTkEntry(airline_entry_frame, fg_color=CTK_ENTRY, text_color=CTK_TEXT, font=FONT_LABEL)
airline_entry.grid(row=0, column=0, padx=5, pady=pady_number,sticky=tk.W + tk.E + tk.N + tk.S)

#Dice si una aerolínea vuela desde la Terminal 1 o la Terminal 2.
def SearchTerminal_INT():
    global bcn
    target_airline = airline_entry.get().strip().upper()
    if target_airline == "":
        mostrar_aviso('Enter airline name.', es_error=True)
        return

    term_name = SearchTerminal(bcn, target_airline)
    if term_name != "":
        mostrar_aviso('Airline ' + target_airline + ' belongs to Terminal ' + term_name)
    else:
        mostrar_aviso('Airline ' + target_airline + ' not registered. Use format, e.g.: VLG', es_error=True)


# Botón para buscar la terminal de la aerolínea escrita
search_terminal_button = ctk.CTkButton(search_terminal_frame, text='⌕  Search Terminal',
    command=SearchTerminal_INT, fg_color=CTK_ACCENT, text_color="#FFFFFF", font=FONT_BTN)
search_terminal_button.grid(row=1, column=0, padx=5, pady=pady_number,sticky=tk.W + tk.E + tk.N + tk.S)

#Asignar una puerta libre a un avión
assign_gate_frame = tk.LabelFrame(gates_frame, text='  Gate Assignation  ', **estilo_frame())
assign_gate_frame.grid(row=3, column=0, columnspan=3, padx=5, pady=pady_number,sticky=tk.W + tk.E + tk.N + tk.S)
assign_gate_frame.columnconfigure(0, weight=1)
assign_gate_frame.rowconfigure(0, weight=1)

aircraft_entry_frame = tk.LabelFrame(assign_gate_frame, text='Aircraft', **estilo_frame())
aircraft_entry_frame.grid(row=0, column=0, padx=5, pady=pady_number,sticky=tk.W + tk.E + tk.N + tk.S)
aircraft_entry_frame.columnconfigure(0, weight=1)
aircraft_entry_frame.rowconfigure(0, weight=1)
aircraft_entry = ctk.CTkEntry(aircraft_entry_frame, fg_color=CTK_ENTRY, text_color=CTK_TEXT, font=FONT_LABEL)
aircraft_entry.grid(row=0, column=0, padx=5, pady=5,sticky=tk.W + tk.E + tk.N + tk.S)

#El programa busca un sitio libre para el código de avión teniendo en cuenta la aerolìnea.
def AssignGate_INT():
    global bcn
    ac_id = aircraft_entry.get().strip().upper()
    if ac_id == "":
        mostrar_aviso('Enter Aircraft ID.', es_error=True)
        return

    departures_list = LoadDepartures('Departures.txt')
    vuelos_totales = MergeMovements(Arrivals_list, departures_list)
    if vuelos_totales == -1 or len(vuelos_totales) == 0:
        mostrar_aviso('No flights lists loaded.', es_error=True)
        return

    # Busca en la lista si existe ese avión exacto
    seleccionado = None
    for ac in vuelos_totales:
        if ac.id == ac_id:
            seleccionado = ac
            break

    if seleccionado == None:
        mostrar_aviso('Aircraft ID not found in flights database.', es_error=True)
        return

    resultado = AssignGate(bcn, seleccionado)  # Intenta darle una puerta libre.
    if type(resultado) == str:
        mostrar_aviso(resultado, es_error=True)  # Si no cabe o no hay sitio, da un error.
    else:
        mostrar_aviso('Gate assigned successfully to flight ' + ac_id + '.')


# Botón para la asignación de puerta
assign_gate_button = ctk.CTkButton(assign_gate_frame, text='✔  Assign Gate',
    command=AssignGate_INT, fg_color=CTK_SUCCESS, text_color="#FFFFFF", font=FONT_BTN)
assign_gate_button.grid(row=1, column=0, padx=5, pady=pady_number,sticky=tk.W + tk.E + tk.N + tk.S)


# FUNCIONALIDADES EXTRA DE LA VERSIÓN 4

#Esta clase añade funciones extra como la música de fondo, el control de cambiar a modo oscuro y el mapa interactivo con el slider.
class AppExtensionV4:
    def __init__(self, master_window):
        self.ventana = master_window  # Guarda la ventana del programa para poder usarla aquí.
        self.modo_oscuro = False  # Empezamos con el modo claro activado.
        self.colores = PALETA_CLARA  # Elegimos los colores claros para empezar.
        self.musica_sonando = False  # La música empieza apagada.

        # Busca el archivo de música "musica.wav" en la misma carpeta del programa
        self.ruta_cancion = os.path.join(os.path.dirname(os.path.abspath(__file__)), "musica.wav")
        if os.path.exists(self.ruta_cancion):
            try:
                # SND_ASYNC hace que la música suene sin congelar los botones; SND_LOOP hace que cuando acabe vuelva a empezar.
                winsound.PlaySound(self.ruta_cancion, winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_LOOP)
                self.musica_sonando = True
            except Exception as e:
                print("Aviso de música:", e)

        self.crear_panel_v4()  # Llama a la función que crea los botones en la pantalla.

    #Dibuja las opciones de la Versión 4 en la zona inferior derecha.
    def crear_panel_v4(self):
        self.v4_frame = tk.LabelFrame(
            self.ventana, text='  Funcionalidades Extra V4  ',
            bg=CL_FRAME, fg=CL_TEXT, font=FONT_TITLE)
        self.v4_frame.grid(row=4, column=1, rowspan=2, padx=5, pady=5, sticky="nsew")
        self.v4_frame.columnconfigure(0, weight=1)

        # Barra horizontal para agrupar los dos botones superiores
        self.toolbar = tk.Frame(self.v4_frame, bg=CL_FRAME)
        self.toolbar.pack(fill="x", padx=5, pady=4)

        # Botón para cambiar entre Modo Claro y Modo Oscuro
        self.btn_tema = ctk.CTkButton(
            self.toolbar, text="🌓  Cambiar Modo (Claro/Oscuro)",
            font=FONT_BTN, fg_color=CTK_BG, text_color=CTK_TEXT,
            command=self.cambiar_modo_color)
        self.btn_tema.pack(side="left", padx=5)

        # Botón para encender o apagar la música
        txt_musica = "🎵  Pausar Música" if self.musica_sonando else "🎵  Reproducir Música"
        self.btn_musica = ctk.CTkButton(
            self.toolbar, text=txt_musica,
            font=FONT_BTN, fg_color=CTK_BG, text_color=CTK_TEXT,
            command=self.controlar_musica)
        self.btn_musica.pack(side="left", padx=5)

        # Pequeña barra secundaria de avisos exclusiva de la versión 4
        self.lbl_notif = ctk.CTkLabel(
            self.v4_frame, text="Sistema Aeroportuario Unificado Iniciado con Éxito",
            font=FONT_BTN, fg_color=("#DBEAFE", "#1E3A8A"), text_color=("#1D4ED8", "#93C5FD"),
            corner_radius=4)
        self.lbl_notif.pack(fill="x", padx=5, pady=3)

        # Zona del Slider de tiempo
        self.slider_frame = tk.LabelFrame(
            self.v4_frame, text="  Mapa de Ocupación de Compuertas por Franja Horaria  ",
            bg=CL_FRAME, fg=CL_TEXT, font=FONT_TITLE)
        self.slider_frame.pack(fill="both", expand=True, padx=5, pady=5)

        self.slider_label = ctk.CTkLabel(
            self.slider_frame, text="Arrastra para cambiar la hora de consulta del Aeropuerto:",
            font=FONT_LABEL, text_color=CTK_TEXT)
        self.slider_label.pack(anchor="w", padx=15, pady=(4, 0))

        # Barra que puedes arrastrar del 0 al 23 (las 24 horas del día).
        # Al moverla, avisa automáticamente a la función 'dibujar_puertas_tiempo_real' para cambiar el plano del aeropuerto según la hora elegida.
        self.slider = ctk.CTkSlider(
            self.slider_frame, from_=0, to=23, number_of_steps=23,
            fg_color=CTK_BG, progress_color=CTK_ACCENT,
            command=lambda val: self.dibujar_puertas_tiempo_real(val))
        self.slider.set(0)  # Empieza marcando las 00:00 de la noche.
        self.slider.pack(fill="x", padx=15, pady=(0, 4))

    #Cambia el texto de la pequeña barra de avisos inferior de la V4 y lo borra automáticamente a los 4 segundos.
    def lanzar_notificacion(self, texto, tipo="info"):

        self.lbl_notif.configure(text=texto)
        if tipo == "success":
            bg, fg = ("#DBEAFE", "#1E3A8A"), ("#1D4ED8", "#93C5FD")
        elif tipo == "error":
            bg, fg = ("#FEE2E2", "#7F1D1D"), ("#B91C1C", "#FCA5A5")
        else:
            bg, fg = ("#DBEAFE", "#1E3A8A"), ("#1D4ED8", "#93C5FD")

        self.lbl_notif.configure(fg_color=bg, text_color=fg)
        self.ventana.after(4000, lambda: self.lbl_notif.configure(
            text="", fg_color=("#DBEAFE", "#1E3A8A"), text_color=("#1D4ED8", "#93C5FD")))

    #Apaga o enciende la música de fondo cambiando el texto del botón de la interfaz.
    def controlar_musica(self):
        if self.musica_sonando:
            winsound.PlaySound(None, winsound.SND_PURGE)  # Apaga cualquier sonido de golpe.
            self.musica_sonando = False
            self.btn_musica.configure(text="🎵  Reproducir Música")
            self.lanzar_notificacion("Música ambiental en segundo plano detenida", "info")
        else:
            if os.path.exists(self.ruta_cancion):
                winsound.PlaySound(self.ruta_cancion, winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_LOOP)
                self.musica_sonando = True
                self.btn_musica.configure(text="🎵  Pausar Música")
                self.lanzar_notificacion("Música reanudada con éxito", "success")
            else:
                self.lanzar_notificacion("Falta el archivo 'musica.wav' en el directorio", "error")

    #Cambia el programa entre Modo Claro y Modo Oscuro, obligando a cada elemento visual a pintarse con los nuevos colores.
    def cambiar_modo_color(self):
        self.modo_oscuro = not self.modo_oscuro
        self.colores = PALETA_OSCURA if self.modo_oscuro else PALETA_CLARA

        # Le dice a la librería CustomTkinter que cambie su diseño
        ctk.set_appearance_mode("Dark" if self.modo_oscuro else "Light")

        #Función interna para las partes viejas que va mirando uno a uno todos los botones y cajitas de la pantalla y les cambia el color de fondo a mano.
        def aplicar_estilos_recursivos(widget):
            tipo_widget = widget.winfo_class()
            if tipo_widget in ('LabelFrame', 'Frame', 'Label'):
                if not tipo_widget.startswith("CTk"):  # Se salta los modernos de CTK porque esos ya se pintan solos.
                    widget.configure(bg=self.colores["frame_bg"] if tipo_widget == 'LabelFrame' else self.colores["bg"],
                                     fg=self.colores["fg"])
            elif tipo_widget == 'Canvas':
                widget.configure(bg=self.colores["bg"])

            for child in widget.winfo_children():
                aplicar_estilos_recursivos(child)

        aplicar_estilos_recursivos(self.ventana)

        # Vuelve a dibujar el plano interactivo de las puertas para que cambie de color según el modo día/noche elegido
        self.dibujar_puertas_tiempo_real(self.slider.get())
        self.lanzar_notificacion(f"Cambiado a Modo {'Oscuro' if self.modo_oscuro else 'Claro'} Global", "info")

    #La siguiente función calcula cómo está el aeropuerto a la hora exacta marcada por el slider.
    #Borra lo que había antes a la derecha y dibuja un plano visual interactivo de rectángulos y líneas:
    #Si una puerta está libre se dibuja de color verde, y si hay un avión metido a esa hora, se pinta de color rojo.
    def dibujar_puertas_tiempo_real(self, value):

        global bcn, Arrivals_list, visualizacion_activa, canvas_puertas_global

        hora_seleccionada = int(value)  # Convierte la posición de la barra en un número de hora redondo (0-23).

        # Selecciona qué colores usar para pintar según si estamos en modo claro o modo oscuro
        c_bg = self.colores["bg"]
        c_card = self.colores["card"]
        c_text = self.colores["fg"]
        color_pasillo = "#334155" if not self.modo_oscuro else "#64748b"
        color_divisor = "#94A3B8" if not self.modo_oscuro else "#475569"

        #Si falta algún archivo por cargar en los botones del menú izquierdo, interrumpe el dibujo y pone un texto rojo para avisar.
        def _mostrar_error(msg):
            Clear_Canvas()
            c = tk.Canvas(canvas_frame, bg=c_bg, borderwidth=0, highlightthickness=0)
            c.grid(row=0, column=0, sticky=tk.NSEW)
            c.create_text(450, 150, text=msg, fill=CL_DANGER, font=("Segoe UI", 16, "bold"))

        if len(bcn.terminals) == 0:
            visualizacion_activa = "ninguna"
            _mostrar_error("[!] Por favor, pulsa primero el botón 'Load Airport Structure'")
            return

        departures_list = LoadDepartures('Departures.txt')
        vuelos_totales = MergeMovements(Arrivals_list, departures_list)

        if vuelos_totales == -1 or type(vuelos_totales) == str or len(vuelos_totales) == 0:
            visualizacion_activa = "ninguna"
            _mostrar_error("[!] Por favor, pulsa primero el botón 'Load Arrivals' antes de mover el barra temporal")
            return

        # Actualiza qué aviones están y cuáles se han ido a la hora elegida
        ActualizarSimulacionHastaHora(bcn, vuelos_totales, hora_seleccionada)

        # MEDIDAS EN PÍXELES PARA HACER EL PLANO DE LA TERMINAL
        PASO_X = 130  # Separación horizontal entre los pasillos de las puertas.
        PASO_Y = 34  # Separación vertical entre una puerta y la de abajo.
        MUELLE_W = 24  # Grosor de las paredes de los pasillos de la terminal.
        Y_PASILLO = 55  # Altura inicial en la pantalla para empezar a dibujar.
        MARGEN_X = 60  # Margen izquierdo para separar el dibujo del borde.
        GATE_W = 16  # Ancho del cuadradito de parking del avión.
        GATE_H = 13  # Alto del cuadradito de parking del avión.
        BRAZO_LEN = 20  # Largo de la pasarela que conecta la terminal con el avión

        def _max_gates(terminal):
            #Calcula cuál es la zona con más puertas para saber cómo de alto va a ser el dibujo.
            return max((len(a.gates) for a in terminal.boardingareas), default=0)

        def _ancho_terminal(terminal):
            #Calcula el ancho total en píxeles que necesita la terminal.
            return MARGEN_X + (len(terminal.boardingareas) * PASO_X) + 80

        # Calcula las dimensiones máximas necesarias para el papel de dibujo
        max_g_t1 = _max_gates(bcn.terminals[0])
        alto_t1 = Y_PASILLO + MUELLE_W + max_g_t1 * PASO_Y + 50
        ancho_t1 = _ancho_terminal(bcn.terminals[0])
        ancho_t2 = _ancho_terminal(bcn.terminals[1]) if len(bcn.terminals) > 1 else 0

        SEPARADOR_X = ancho_t1 + 20  # Punto central donde se dividen los planos de la T1 y la T2.
        ancho_total = SEPARADOR_X + ancho_t2 + 20
        alto_total = max(alto_t1, Y_PASILLO + MUELLE_W + _max_gates(bcn.terminals[1]) * PASO_Y + 50) if len(
            bcn.terminals) > 1 else alto_t1
        alto_total += 40

        # CREACIÓN DE LAS BARRAS DE SCROLL
        # Si la ventana es pequeña y el dibujo del aeropuerto no cabe entero, este código añade scrollbars para podernos desplazar hacia la derecha o hacia abajo usando el ratón.
        if canvas_puertas_global is not None and not canvas_puertas_global.winfo_exists():
            visualizacion_activa = "ninguna"

        if visualizacion_activa != "mapa":
            Clear_Canvas()  # Deja el cuadro de la derecha totalmente en blanco.
            vsb = tk.Scrollbar(canvas_frame, orient="vertical")
            vsb.grid(row=0, column=1, sticky="ns")
            hsb = tk.Scrollbar(canvas_frame, orient="horizontal")
            hsb.grid(row=1, column=0, sticky="ew")
            canvas_frame.rowconfigure(1, weight=0)
            canvas_frame.columnconfigure(1, weight=0)

            # Crea el espacio de dibujo conectándolo a las barras de movimiento creadas arriba
            canvas_puertas_global = tk.Canvas(
                canvas_frame, bg=c_card, borderwidth=0, highlightthickness=0,
                yscrollcommand=vsb.set, xscrollcommand=hsb.set)
            canvas_puertas_global.grid(row=0, column=0, sticky=tk.NSEW)
            vsb.config(command=canvas_puertas_global.yview)
            hsb.config(command=canvas_puertas_global.xview)

            # Permite usar la rueda del ratón para desplazarse arriba y abajo por el plano del aeropuerto
            canvas_puertas_global.bind("<MouseWheel>",
                                       lambda e: canvas_puertas_global.yview_scroll(-1 * (e.delta // 120), "units"))
            visualizacion_activa = "mapa"

        # Borra el dibujo anterior antes de empezar a pintar los nuevos colores de la hora actual
        canvas_puertas_global.delete("all")
        canvas_puertas_global.configure(bg=c_card, scrollregion=(0, 0, ancho_total, alto_total))

        # Pone el título informativo arriba del dibujo con la hora actual
        canvas_puertas_global.create_text(
            ancho_total // 2, 18,
            text=f"Ocupación a las {hora_seleccionada}:00h  (Verde = Libre | Rojo = Ocupado)",
            font=("Segoe UI", 13, "bold"), fill=c_text)

        if len(bcn.terminals) > 1:
            # Dibuja una línea de puntos gris en medio para separar de forma clara la Terminal 1 de la Terminal 2
            canvas_puertas_global.create_line(SEPARADOR_X, 35, SEPARADOR_X, alto_total - 10, fill=color_divisor,
                                              width=2, dash=(6, 4))

        # CÓMO SE DIBUJA CADA TERMINAL EN LA PANTALLA
        def _dibujar_terminal(terminal, x_origen, etiqueta, color_etiqueta):
            x_pasillo_ini = x_origen + MARGEN_X
            x_pasillo_fin = x_pasillo_ini + len(terminal.boardingareas) * PASO_X

            # Dibuja el pasillo largo principal de la terminal
            canvas_puertas_global.create_rectangle(x_pasillo_ini, Y_PASILLO, x_pasillo_fin, Y_PASILLO + MUELLE_W,
                                                   fill=color_pasillo, outline="")
            canvas_puertas_global.create_text(x_origen + MARGEN_X - 8, Y_PASILLO + MUELLE_W // 2, text=etiqueta,
                                              font=("Segoe UI", 14, "bold"), fill=color_etiqueta, anchor="e")

            # Va recorriendo cada zona de embarque de la terminal
            for i, area in enumerate(terminal.boardingareas):
                x_muelle = x_pasillo_ini + 30 + i * PASO_X
                y_bottom = Y_PASILLO + MUELLE_W + len(area.gates) * PASO_Y
                if y_bottom < Y_PASILLO + MUELLE_W + 80:
                    y_bottom = Y_PASILLO + MUELLE_W + 80

                # Dibuja el pasillo vertical de esa zona de embarque
                canvas_puertas_global.create_rectangle(x_muelle, Y_PASILLO + MUELLE_W, x_muelle + MUELLE_W, y_bottom,
                                                       fill=color_pasillo, outline="")
                canvas_puertas_global.create_text(x_muelle + MUELLE_W // 2, y_bottom + 14, text="Área " + area.name,
                                                  font=("Segoe UI", 9, "bold"), fill=c_text)

                # Recorre todas las puertas individuales de esa zona
                for g, gate in enumerate(area.gates):
                    y_gate = Y_PASILLO + MUELLE_W + g * PASO_Y + 4
                    color_puerta = CL_SUCCESS if not gate.occupancy else CL_DANGER  # Verde si está vacía, rojo si está ocupada por un avión.

                    # Para que queden bonitas, intercala las puertas
                    if g % 2 == 0:
                        # DIBUJAR COMPUERTA HACIA LA IZQUIERDA
                        bx2 = x_muelle
                        bx1 = bx2 - BRAZO_LEN
                        canvas_puertas_global.create_rectangle(bx1, y_gate + 3, bx2, y_gate + 7, fill=color_pasillo,
                                                               outline="")  # Pasarela de pasajeros
                        gx2 = bx1
                        gx1 = gx2 - GATE_W
                        canvas_puertas_global.create_rectangle(gx1, y_gate, gx2, y_gate + GATE_H, fill=color_puerta,
                                                               outline="")  # Cuadrado del avión
                        canvas_puertas_global.create_text(gx1 - 4, y_gate + GATE_H // 2, text=gate.name,
                                                          font=("Segoe UI", 8), fill=c_text,
                                                          anchor="e")  # Nombre de la puerta
                    else:
                        # DIBUJAR COMPUERTA HACIA LA DERECHA
                        bx1 = x_muelle + MUELLE_W
                        bx2 = bx1 + BRAZO_LEN
                        canvas_puertas_global.create_rectangle(bx1, y_gate + 3, bx2, y_gate + 7, fill=color_pasillo,
                                                               outline="")  # Pasarela de pasajeros
                        gx1 = bx2
                        gx2 = gx1 + GATE_W
                        canvas_puertas_global.create_rectangle(gx1, y_gate, gx2, y_gate + GATE_H, fill=color_puerta,
                                                               outline="")  # Cuadrado del avión
                        canvas_puertas_global.create_text(gx2 + 4, y_gate + GATE_H // 2, text=gate.name,
                                                          font=("Segoe UI", 8), fill=c_text,
                                                          anchor="w")  # Nombre de la puerta

        # Llama a pintar la T1 y, si los datos tienen una segunda terminal, también pinta la T2 al lado derecho
        _dibujar_terminal(bcn.terminals[0], x_origen=0, etiqueta="T1", color_etiqueta=CL_ACCENT)
        if len(bcn.terminals) > 1:
            _dibujar_terminal(bcn.terminals[1], x_origen=SEPARADOR_X + 10, etiqueta="T2", color_etiqueta=CL_SUCCESS)

    def mostrar_analiticas_v4(self):
        self.lanzar_notificacion("Consultando cálculos en el script matemático...", "info")
        messagebox.showinfo("Analíticas V4",
                            "Conectando con las funciones gráficas de simulación temporal de ocupación diaria de la pista.")



# ARRANQUE DEL PROGRAMA

if __name__ == "__main__":
    # Arranca los añadidos de sonido y cambio de color  dentro de la ventana principal.
    componente_v4 = AppExtensionV4(ventana)
    # Abre y arranca la ventana en la pantalla.
    ventana.mainloop()