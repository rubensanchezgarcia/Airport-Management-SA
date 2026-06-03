from airport import *
import matplotlib.pyplot as plt
import math
import os
lista_aerpuertos_schengen=['LO', 'EB', 'LK', 'LC', 'EK', 'EE', 'EF', 'LF', 'ED', 'LG', 'EH', 'LH',
'BI','LI', 'EV', 'EY', 'EL', 'LM', 'EN', 'EP', 'LP', 'LZ', 'LJ', 'LE', 'ES',
'LS']
class aircraft:
    # Añadimos destination y departuretime con valores vacíos por defecto
    def __init__(self, id, airline, ICAO, arrivaltime, destination='', departuretime=''):
        self.id=id
        self.airline=airline
        self.ICAO=ICAO
        self.arrivaltime=arrivaltime
        self.destination=destination
        self.departuretime=departuretime


def LoadArrivals (filename):
    f = open(filename, 'r')
    lista_arrivals = []
    lineas = f.readlines()
    for i in range(1, len(lineas)):
        arrivals_por_lineas = lineas[i]
        elementos_arrivals = arrivals_por_lineas.split()
        id = elementos_arrivals[0]
        ICAO = elementos_arrivals[1]
        time = elementos_arrivals[2]
        airline= elementos_arrivals[3]

        arrival = aircraft(id, airline, ICAO, time)

        lista_arrivals.append(arrival)
    if len(lista_arrivals)==0:
        return "Error | No airports found"
    else:
        return lista_arrivals

def PlotArrivals (aircrafts):
    x_lista_airlines=[]
    y_contador_vuelos=[]
    encontrado = False
    b=0
    contador = 0
    for a in range(len(aircrafts)):
        airline_base=aircrafts[a].airline
        while not encontrado and b<len(x_lista_airlines):
            if x_lista_airlines[b]==airline_base:
                encontrado = True
            b+=1
        if not encontrado:
            x_lista_airlines.append(airline_base)
            for c in range(len(aircrafts)):
                airline=aircrafts[c].airline
                if airline==airline_base:
                    contador+=1
            y_contador_vuelos.append(contador)
        encontrado = False
        b=0
        contador = 0

    fig, ax = plt.bar(figsize=(18, 6))
    ax.set_title('Flights by airline')
    ax.set_xlabel('Airline')
    ax.set_ylabel('Number of flights')
    ax.tick_params(axis='x', rotation=90, labelsize=8)
    ax.bar(x_lista_airlines, y_contador_vuelos)

    return fig

def SaveFlights(aircrafts, filename):
    if len (aircrafts)==0:
        print("Error | No airports found")
        return
    f = open(filename, 'w')
    f.write('AIRCRAFT ORIGIN ARRIVAL AIRLINE\n')
    for i in range(0, len(aircrafts)):
        elemento_lista = aircrafts[i]
        f.write(elemento_lista.id + ' ' + elemento_lista.ICAO + ' ' + elemento_lista.arrivaltime + ' ' + elemento_lista.airline + '\n')
        #Falta hacer que si queda algún hueco vacío lo rellene con un 0 o un -(guión)
def PlotAirlines (aircrafts):
    x_lista_airlines=[]
    y_contador_vuelos=[]
    encontrado = False
    b=0
    contador = 0
    for a in range(len(aircrafts)):
        airline_base=aircrafts[a].airline
        while not encontrado and b<len(x_lista_airlines):  #Revisamos a ver si esta aerolinea está ya en la lista de aerolineas.
            if x_lista_airlines[b]==airline_base:
                encontrado = True
            b+=1
        if not encontrado:
            x_lista_airlines.append(airline_base)
            for c in range(len(aircrafts)):
                airline=aircrafts[c].airline
                if airline==airline_base:
                    contador+=1
            y_contador_vuelos.append(contador)
        encontrado = False
        b=0
        contador = 0

    fig, ax = plt.subplots(figsize=(18, 6)) #figura i eixos amb el tamany que volem
    ax.bar(x_lista_airlines, y_contador_vuelos)
    ax.set_title('Flights by airline')
    ax.set_xlabel('Airline')
    ax.set_ylabel('Number of flights')
    ax.tick_params(axis='x', rotation=90, labelsize=8)
    fig.tight_layout()

    return fig


def PlotFlightsType (aircrafts):
    if len (aircrafts)==0:
        return "Error | No airports found"
    #Definimos que vuelos tienen un origen schenghen:
    contadorSchengen=0
    contadorNoSchengen=len(aircrafts)
    x=[]
    y=[]
    for i in range (0, len(aircrafts)):
        es_schengen = False
        num = 0
        # Las dos primeras letras del ICAO del aeropuerto son:
        lista_ICAO = aircrafts[i].ICAO
        if len(lista_ICAO) < 2:
            return 'Error | Index '
        dos_primeros_digitos = lista_ICAO[0] + lista_ICAO[1]
        while es_schengen == False and num < len(lista_aerpuertos_schengen):
            if lista_aerpuertos_schengen[num] == dos_primeros_digitos:
                es_schengen = True
            else:
                num += 1
        if es_schengen:
            contadorSchengen+=1

    contadorNoSchengen= contadorNoSchengen-contadorSchengen
    y.append(contadorSchengen)
    y.append(contadorNoSchengen)
    x.append('Schengen')
    x.append('Non Schengen')

    fig, ax = plt.subplots(figsize=(18, 6))
    ax.clear()
    ax.bar(x,y)
    ax.set_title('Flights from Schengen Airports')
    ax.set_ylabel('Number of Airports')

    return fig


def MapFlights(aircrafts):
    Airports = LoadAirports('Airports.txt')
    kml = open('routes.kml', 'w')
    kml.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    kml.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
    kml.write('<Document>\n')

    for i in range(len(aircrafts)):
        ICAO = aircrafts[i].ICAO
        kml.write(' <Placemark>\n')
        kml.write(f' <name>Route {ICAO} - LEBL</name>\n')
        kml.write('   <LineString>\n')
        kml.write('    <altitudeMode>clampToGround</altitudeMode>\n')
        kml.write('    <extrude>1</extrude>\n')
        kml.write('    <tessellate>1</tessellate>\n')
        kml.write('    <coordinates>\n')

        encontrado = False
        n = 0
        while not encontrado and n < len(Airports):
            airport_name = Airports[n].ICAO
            airport_longitude = Airports[n].longitude
            airport_latitude = Airports[n].latitude
            if airport_name == ICAO:
                encontrado = True
            else:
                n += 1

        kml.write(f'    {airport_longitude},{airport_latitude}\n')
        kml.write('    2.0783333333,41.2969444444\n')
        kml.write('    </coordinates>\n')
        kml.write('   </LineString>\n')
        kml.write(' </Placemark>\n')

    kml.write('</Document>\n')
    kml.write('</kml>\n')
    kml.close()
    #Falta hacer que cambien de colores los que vienen de aeropuerto schengen y los que vienen de aeropuerto no schengen.


def MapCombined(aircrafts, filename='combined_map.kml'):
    # 1. Cargamos y evaluamos qué aeropuertos pertenecen a Schengen
    Airports = LoadAirports('Airports.txt')
    SetSchengen(Airports)

    kml = open(filename, 'w', encoding='utf-8')
    kml.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    kml.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
    kml.write('<Document>\n')
    kml.write('  <name>Schengen Airports and Arrival Routes</name>\n')

    # --- DEFINICIÓN DE ESTILOS DE COLOR (Formato KML: AABBGGRR -> Opacidad, Azul, Verde, Rojo) ---
    # Ruta Schengen: Verde Puro (ff00ff00)
    kml.write('  <Style id="ruta_schengen">\n')
    kml.write('    <LineStyle>\n')
    kml.write('      <color>ff00ff00</color>\n')
    kml.write('      <width>3</width>\n')
    kml.write('    </LineStyle>\n')
    kml.write('  </Style>\n')

    # Ruta NO Schengen: Rojo Puro (ff0000ff)
    kml.write('  <Style id="ruta_no_schengen">\n')
    kml.write('    <LineStyle>\n')
    kml.write('      <color>ff0000ff</color>\n')
    kml.write('      <width>3</width>\n')
    kml.write('    </LineStyle>\n')
    kml.write('  </Style>\n')

    # --- CAPA 1: CARPETA DE AEROPUERTOS ---
    kml.write('  <Folder>\n')
    kml.write('    <name>Aeropuertos</name>\n')
    for i in range(len(Airports)):
        airport_name = Airports[i].ICAO
        airport_longitude = Airports[i].longitude
        airport_latitude = Airports[i].latitude
        is_sch = Airports[i].schengen

        status = "(Schengen)" if is_sch else "(No Schengen)"
        kml.write('    <Placemark>\n')
        kml.write(f'      <name>{airport_name} {status}</name>\n')
        kml.write('      <Point>\n')
        kml.write('        <coordinates>\n')
        kml.write(f'          {airport_longitude},{airport_latitude}\n')
        kml.write('        </coordinates>\n')
        kml.write('      </Point>\n')
        kml.write('    </Placemark>\n')
    kml.write('  </Folder>\n')

    # --- CAPA 2: CARPETA DE RUTAS DE VUELO (ARRIVALS) ---
    kml.write('  <Folder>\n')
    kml.write('    <name>Rutas de Arribo (Arrivals)</name>\n')
    for i in range(len(aircrafts)):
        ICAO = aircrafts[i].ICAO

        encontrado = False
        n = 0
        is_schengen_route = False
        airport_longitude = 0.0
        airport_latitude = 0.0

        # Buscamos las coordenadas y estado Schengen del aeropuerto de origen
        while not encontrado and n < len(Airports):
            if Airports[n].ICAO == ICAO:
                encontrado = True
                airport_longitude = Airports[n].longitude
                airport_latitude = Airports[n].latitude
                is_schengen_route = Airports[n].schengen
            else:
                n += 1

        if encontrado:
            kml.write('    <Placemark>\n')
            kml.write(f'      <name>Route {ICAO} - LEBL ({aircrafts[i].airline})</name>\n')

            # Asignamos el estilo visual dependiendo de si es Schengen o no
            if is_schengen_route:
                kml.write('      <styleUrl>#ruta_schengen</styleUrl>\n')
            else:
                kml.write('      <styleUrl>#ruta_no_schengen</styleUrl>\n')

            kml.write('      <LineString>\n')
            kml.write('        <altitudeMode>clampToGround</altitudeMode>\n')
            kml.write('        <extrude>1</extrude>\n')
            kml.write('        <tessellate>1</tessellate>\n')
            kml.write('        <coordinates>\n')
            kml.write(f'          {airport_longitude},{airport_latitude}\n')
            kml.write('          2.0783333333,41.2969444444\n')  # Destino final: LEBL
            kml.write('        </coordinates>\n')
            kml.write('      </LineString>\n')
            kml.write('    </Placemark>\n')

    kml.write('  </Folder>\n')
    kml.write('</Document>\n')
    kml.write('</kml>\n')
    kml.close()
    return filename

def HaversineDistance(lat1, lon1, lat2, lon2):
    radio_tierra = 6371

    # Pasamos de grados a radianes
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    lambda1 = math.radians(lon1)
    lambda2 = math.radians(lon2)

    # Diferencias
    delta_phi = abs(phi1 - phi2)
    delta_lambda = abs(lambda1 - lambda2)

    # Fórmula de Haversine
    a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = radio_tierra * c

    return d

def LongDistanceArrivals(aircrafts):
    Airports = LoadAirports('Airports.txt')
    Long_flights = []
#Calculamos la distancia con la longitud y la latitud.
    for i in range(len(aircrafts)):
        aircraft= aircrafts[i]
        encontrado = False
        ICAO = aircrafts[i].ICAO
        n = 0
        while not encontrado and n < len(Airports):
            airport_name = Airports[n].ICAO
            airport_longitude = Airports[n].longitude
            airport_latitude = Airports[n].latitude
            if airport_name == ICAO:
                encontrado = True
            else:
                n += 1
        if encontrado == False:
            return 'Error | Missmatch'
        distance = HaversineDistance(airport_latitude, airport_longitude, 41.2969444444, 2.0783333333)
        if distance > 2000:
            Long_flights.append(aircraft)

    return Long_flights


def LoadDepartures(filename):
    if not os.path.exists(filename):
        print("Error | El archivo de salidas no existe.")
        return []

    lista_departures = []

    f = open(filename, 'r')
    lineas = f.readlines()
    f.close()

    #empezamos el bucle desde el índice 1 para ignorar la primera línea
    for i in range(1, len(lineas)):
        linea_limpia = lineas[i].strip()

        # Saltamos la línea si está vacía
        if not linea_limpia:
            continue

        elementos = linea_limpia.split()

        #Separamos la línea donde encuentre espacios en blanco y asigna nombres a cada elemento
        if len(elementos) == 4:
            id_avion = elementos[0]
            destination = elementos[1]
            time = elementos[2]
            airline = elementos[3]

            # Creamos el objeto aircraft asignando destino y hora de salida.
            dep = aircraft(id=id_avion, airline=airline, ICAO='', arrivaltime='',destination=destination, departuretime=time)

            # Lo añadimos a nuestra lista de salidas
            lista_departures.append(dep)

    return lista_departures


def MergeMovements(arrivals, departures):

    if not arrivals or not departures:
        return -1
    merged = []

    #Recorremos los aviones que llegan
    for arr in arrivals:
        #Creamos una copia nueva para trabajar de forma segura sin romper la lista original
        new_ac = aircraft(arr.id, arr.airline, arr.ICAO, arr.arrivaltime)

        # Buscamos en la lista de salidas si este mismo avión tiene un despegue posterior
        for dep in departures:
            if dep.id == arr.id:
                # Comprobamos que el tiempo de llegada sea anterior al de salida
                if arr.arrivaltime < dep.departuretime:
                    # Añadimos los datos de salida a nuestra copia fusionada
                    new_ac.destination = dep.destination
                    new_ac.departuretime = dep.departuretime
                    break

        # Añadimos el avión (ya sea fusionado o solo con llegada) a la lista definitiva
        merged.append(new_ac)

    #Añadimos los aviones que pernoctaron: solo aparecen en salidas, no en llegadas
    for dep in departures:
        found = False
        # Comprobamos si este avión ya fue metido en la lista unificada
        for m in merged:
            if m.id == dep.id:
                found = True
                break

        # Si no se encontró en 'merged', significa que no tuvo llegada hoy, así que lo añadimos directamente
        if not found:
            merged.append(dep)

    return merged


def NightAircraft(aircrafts):

    if not aircrafts:
        return -1

    lista_night = []

    # Recorremos cada avión de la lista
    for ac in aircrafts:
        # Si la hora de llegada está vacía y la de salida contiene datos, es un avión que pernocta
        if ac.arrivaltime == '' and ac.departuretime != '':
            lista_night.append(ac)

    return lista_night
