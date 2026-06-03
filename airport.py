lista_aerpuertos_schengen=['LO', 'EB', 'LK', 'LC', 'EK', 'EE', 'EF', 'LF', 'ED', 'LG', 'EH', 'LH',
'BI','LI', 'EV', 'EY', 'EL', 'LM', 'EN', 'EP', 'LP', 'LZ', 'LJ', 'LE', 'ES',
'LS']
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
class Airport:
    def __init__(self, ICAO, latitude, longitude):
        self.ICAO= ICAO
        self.latitude= latitude
        self.longitude= longitude
        self.schengen=False

def GDtoGMS_latitude (latitude):
    grados = float(latitude[1:3])
    minutos = float(latitude[3:5])
    segundos = float(latitude[5:7])
    latitude_decimal = grados + minutos / 60 + segundos / 3600
    return latitude_decimal

def return_GD_latitude (latitude):
    grados = int(latitude)
    minutos_reales = (latitude - grados) * 60
    minutos = int(minutos_reales)
    segundos_reales = (minutos_reales - minutos) * 60
    segundos = int(segundos_reales)
    valores_latitude = str(grados) + str(minutos) + str(segundos)
    return valores_latitude

def GDtoGMS_longitude (longitude):
    grados = float(longitude[1:4])
    minutos = float(longitude[4:6])
    segundos = float(longitude[6:8])
    longitude_decimal = grados + minutos / 60 + segundos / 3600
    return longitude_decimal

def return_GD_longitude (longitude):
    grados = int(longitude)
    minutos_reales = (longitude - grados) * 60
    minutos = int(minutos_reales)
    segundos_reales = (minutos_reales - minutos) * 60
    segundos = int(segundos_reales)
    longitude = str(grados) + str(minutos) + str(segundos)
    return longitude

def IsSchengenAirport (ICAO):
    es_schengen = False
    num = 0
    # Las dos primeras letras del ICAO del aeropuerto son:
    lista_ICAO = list(ICAO)
    if len(lista_ICAO)<2:
        return es_schengen
    dos_primeros_digitos=str(lista_ICAO[0])+str(lista_ICAO[1])
    while es_schengen == False and num<len(lista_aerpuertos_schengen):
        if lista_aerpuertos_schengen[num]==dos_primeros_digitos:
            es_schengen = True
        else:
            num+=1
    return es_schengen

def SetSchengen (airport):
    for i in range (0, len(airport)):
        es_schengen = IsSchengenAirport(airport[i].ICAO)
        airport[i].schengen = es_schengen
    return airport

def PrintAirport (airport):
    print(airport.__dict__)

def LoadAirports (filename):
    f = open(filename,'r')
    lista_aeropuertos=[]
    lineas = f.readlines()
    for i in range (1, len(lineas)):
        aeropuertos_por_lineas = lineas[i]
        elementos_aeropuerto = aeropuertos_por_lineas.split()
        ICAO=elementos_aeropuerto[0]
        aeropuerto=Airport( ICAO, 0.0, 0.0)
        aeropuerto.ICAO=ICAO
        #Conseguimos la latitud, recordamos que tenemos que quitar el primer caracter ya que es una letra, y ese caracter hay que ver cual es.
        latitude=elementos_aeropuerto[1]
        letra_latitude=latitude[0]
        latitude_decimal=GDtoGMS_latitude(latitude)
        if letra_latitude == 'S':
            latitude_decimal= (latitude_decimal) * (-1)
        #añadimos la latitude a la clase de aeropuerto
        aeropuerto.latitude=latitude_decimal

        #Conseguimos la longitude, recordamos que tenemos que quitar el primer caracter ya que es una letra, y ese caracter hay que ver cual es.
        longitude=elementos_aeropuerto[2]
        #Cojemos la letra:
        letra_longitude=longitude[0]
        longitude_decimal = GDtoGMS_longitude(longitude)
        if letra_longitude == 'W':
            longitude_decimal = (longitude_decimal) * (-1)
        aeropuerto.longitude=longitude_decimal

        #Añadimos el aeropuerto a la lista:
        lista_aeropuertos.append(aeropuerto)
    return lista_aeropuertos


def SaveSchengenAirports (airports, filename):
    SetSchengen(airports)
    f = open(filename,'w')
    f.write('CODE LAT LON\n')
    for i in range (0, len(airports)):
        if airports[i].schengen == True:
            letra_lat='N'
            latitude= airports[i].latitude
            if airports[i].latitude<0:
                latitude=-latitude
                letra_lat='S'
            latitude=return_GD_latitude(latitude)#usamos la función.
            latitude=letra_lat+latitude

            letra_lon='E'
            longitude=airports[i].longitude
            if airports[i].longitude<0:
                longitude=-longitude
                letra_lon='W'
            longitude=return_GD_longitude(longitude)
            longitude=letra_lon+longitude

            f.write(airports[i].ICAO + ' ' + latitude + ' ' + longitude +'\n')


def AddAirport(airports, airport):
    i = 0
    encontrado = False

    while i < len(airports) and encontrado == False:
        if airports[i].ICAO == airport.ICAO:
            encontrado = True
        else:
            i += 1

    if encontrado == False:
        airports.append(airport)
        return airports
    else:
        return 'Error|El aeropuerto ya existe'

def RemoveAirport (airports, code):
    i = 0
    encontrado = False

    while i < len(airports) and encontrado == False:
        if airports[i].ICAO == code:
            airports.pop(i)
            encontrado = True
        else:
            i += 1

    if encontrado == True:
        return airports
    else:
        return 'Error|Aeropuerto no encontrado'



def PlotAirports (airports):
    schengen=0
    no_schengen=0
    for i in range (0, len(airports)):
        if airports[i].schengen == True:
            schengen+=1
        elif airports[i].schengen == False:
            no_schengen+=1

    fig, ax = plt.subplots()
    ax.bar(["Airports"], [schengen], label="Schengen")
    ax.bar(["Airports"], [no_schengen], bottom=[schengen], label="No Schengen")

    ax.set_ylabel("Count")
    ax.set_title("Schengen Airports")
    ax.legend()

    return fig



def MapAirports (Airports):
    f = open('mapAirports.kml', 'w')
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    f.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
    f.write('<Document>\n')
    for i in range(len(Airports)): #Creamos un bucle para añadir un punto por cada aeropuerto de la lista.
        airport_name=Airports[i].ICAO
        airport_longitude=Airports[i].longitude
        airport_latitude=Airports[i].latitude
        f.write('<Placemark> ')
        f.write(f' <name> {airport_name} </name>\n')
        f.write('  <Point>\n')
        f.write('    <coordinates>\n')
        f.write(f'    {airport_longitude},{airport_latitude}\n')
        f.write('    </coordinates>\n')
        f.write('   </Point>\n')
        f.write('</Placemark>\n')
    f.write('</Document>\n')
    f.write('</kml>\n')

    f.close()
