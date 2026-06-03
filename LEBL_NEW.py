#Importamos todo lo que tenemos que importar.
from airport import *
from aircraft import *
import matplotlib.pyplot as plt

lista_aerpuertos_schengen=['LO', 'EB', 'LK', 'LC', 'EK', 'EE', 'EF', 'LF', 'ED', 'LG', 'EH', 'LH',
'BI','LI', 'EV', 'EY', 'EL', 'LM', 'EN', 'EP', 'LP', 'LZ', 'LJ', 'LE', 'ES',
'LS']

#Creamos las clases que necesitamos para esta nueva versión.

class BarcelonaAP:
    def __init__(self, code):
        self.code = code
        self.terminals=[]#Lista de objetos del tipo terminal
class Terminal:
    def __init__(self, name):
        self.name = name
        self.boardingareas=[]#Lista del tipo boarding Area.
        self.airlines=[]
class BoardingArea:
    def __init__(self, name):
        self.name = name
        self.schengen=False
        self.gates=[]#Lista de objetos del tipo gate.
class Gate:
    def __init__(self, name):
        self.name = name
        self.occupancy=False#False = puerta no ocupada, True = puerta ocupada
        self.aircraft_id=""#En el caso que ocupied es igual a True, se deberá guardar el ID del avión que esté ocupando esta gate

#Definimos la función set gate.
def SetGates (area, init_gate, end_gate, prefix): #area es un objeto del tipo BoardingArea, init and end gate son número,, el init mayor que el end y prefix es una string. El prefijo que llevará cada puerta de la Boarding Area.
    gates=[] #Creamos una lista vacía.
    #Nos cercioramos que el valor de init_gate es mayor a de end_gate.
    if init_gate >= end_gate:
        return -1
    #Hacemos un bucle en el cual va a ir asignando un nombre a cada gate.
    i=init_gate
    while i <= end_gate:
        gate_name = prefix + str(i)
        gate = Gate(gate_name)
        gate.occupancy = False
        gates.append(gate)
        i+=1
    #Añadimos la lista de puertas a la BoardingArea(variable area de la función)
    area.gates=gates

#Definimos la función LoadAirlines.
def LoadAirlines(terminal, t_name):

    file_name = t_name + "_Airlines.txt"
    f = open(file_name, "r")
    lines = f.readlines()

    airlines_list = []

    # Recorremos cada línea del archivo
    for i in range(len(lines)):
        linea_actual = lines[i].strip()

        #Si la linea no está vacía:
        if linea_actual != "":
            partes = linea_actual.split()

            # Cogemos la última palabra de la línea (el código de 3 letras)
            posicion_final = len(partes) - 1
            airline_code = partes[posicion_final]

            # Guardamos el código en nuestra lista
            airlines_list.append(airline_code)

    # Guardamos la lista definitiva dentro de la terminal correspondiente
    terminal.airlines = airlines_list
    f.close()

def LoadAirportStructure (filename):
    try:
        f = open(filename, "r")
    except: return "Error | File not found"

    lines = f.readlines()
    #De la primera línea obtenemos el nombre del aeropuerto y la cantidad de terminales que tiene.
    partes = lines[0].split()
    airport_code = partes[0]
    number_of_terminals = partes[1]
    airport = BarcelonaAP(airport_code)
    lista_terminals = []#Creamos una lista para las terminales que crearemos.
    i=1
    while i < len(lines):
        partes = lines[i].split()
        if partes[0]== "Terminal":
            terminal_name = partes[1]
            number_of_areas = partes[2]
            terminal = Terminal(terminal_name)#Creamos la terminal y le añadimos las aerolineas que le corresponden.
            LoadAirlines(terminal, terminal_name)
            n=i
            lista_boarding_area = []  # Creamos una lista de áreas de embarque.
            #Creamos un nuevo bucle que determinara la construcción interna de cada terminal
            while i < int(number_of_areas)+n:

                i+=1
                #Creamos un objeto del tipo terminal con su correspondiente nombre y le asignamos a esa terminal una lista de aerolineas.

                partes = lines[i].split()
                area_name = partes[1]
                init_gate = partes[4]
                end_gate = partes[6]
                schengen_admision = partes[2]
                #Creamos una área con el nombre area_name
                area = BoardingArea(area_name)
                #Creamos el prefijo para poder ejecutar la función Setgates que precisa de uno.
                prefix= terminal_name + "BA" +area_name + "G"
                resultado = SetGates(area, int(init_gate), int(end_gate), prefix)
                if resultado == -1:
                    return -1
                #Definimos si el área de embarque admite o no vuelos del espacio schengen.
                if schengen_admision == "Schengen":
                    area.schengen = True
                else:
                    area.schengen = False
                lista_boarding_area.append(area)
            #Con todas las boarding áreas definidas completamente y añadidas a la lista, las introducimos en la Terminal correspondiente.
            lista_terminals.append(terminal)
            terminal.boardingareas = lista_boarding_area
        else:
            i+=1



    airport.terminals= lista_terminals

    return airport

def GateOccupancy (bcn):
    airport_gates=[]#creamos una lista global de puertas de embarque de todo el aeropuerto bcn.
    terminals = bcn.terminals #Recordamos que esto es una lista. Así que hacemos un recorrido por todas las puertas de cada terminal.
    for i in range(len(terminals)):
        boarding_areas = terminals[i].boardingareas #Esto es otra lista, que habrá que recorrer en toda su longitud
        for n in range(len(boarding_areas)):
            gates = boarding_areas[n].gates
            for k in range(len(gates)):
                gate = gates[k]
                airport_gates.append(gate)

    return airport_gates


def IsAirlineInTerminal (terminal, name):
    if name == "":
        return False
    terminal_airlines = terminal.airlines  #Recorremos toda la lista y observamos a ver si la aerolinea indicada esta en esta lista.
    encontrado = False
    i = 0
    while not encontrado and i<len(terminal_airlines):
        if terminal_airlines[i] == name:
            encontrado = True
            return True
        else:
            i+=1
    return False

def SearchTerminal (bcn, name):
    bcn_terminals = bcn.terminals
    #Buscamos en cada terminal con la función anterior.
    i=0
    resultado = False
    while resultado == False and i < len(bcn_terminals):
        resultado = IsAirlineInTerminal(bcn_terminals[i], name)
        if resultado == True:
            return bcn_terminals[i].name
        else:
            i+=1
    return ""
def AssignGate (bcn, aircraft):
    #Hacemos una busqueda de en que terminal tiene que ir este vuelo por su aerolinea. Lo hacemos con un bucle.
    aircraft_airline = aircraft.airline
    assigned_terminal = SearchTerminal(bcn, aircraft_airline)
    if assigned_terminal == "":
        return "Airline with not assigned terminal."
    #Ahora que ya tenemos la terminal buscamos una puerta libre que tenga las características correctas.
    #Buscamos la terminal correcta en el aeropuerto.
    encontrado = False
    i=0
    terminals = bcn.terminals
    while not encontrado and i<len(terminals):
        selected_terminal = terminals[i]
        if selected_terminal.name == assigned_terminal:
            encontrado = True
        else:
            i+=1
    if not encontrado:
        return "Terminal not found."
    i=0
    #Buscamos dentro de las Boarding Areas que corresponden a categoria Schengen o no Schengen dependiendo de donde venga el vuelo.
    aircraft_schengen=IsSchengenAirport (aircraft.ICAO)
    encontrado = False
    while not encontrado and i<len(selected_terminal.boardingareas):
        boarding_area = selected_terminal.boardingareas[i]
        area_schengen = boarding_area.schengen
        if area_schengen == aircraft_schengen:
            n=0
            while n<len(boarding_area.gates) and not encontrado:
                if boarding_area.gates[n].occupancy == False:#En este caso, la puerta idonea ha sido encontrada por lo que le asignamos el Aircraft id.
                    encontrado = True
                    boarding_area.gates[n].occupancy=True
                    boarding_area.gates[n].aircraft_id = aircraft.id
                else:
                    n+=1

        i+=1

    if not encontrado:
        return "Error | No gates found with selected parameters"

def AssignNightGates(bcn, aircrafts):
    contador_nocturnos = 0

    # Recorremos la lista completa de aviones del día
    for ac in aircrafts:
        # Un avión es nocturno si su hora de llegada está vacía y su hora de salida está ocupada
        if ac.arrivaltime == '' and ac.departuretime != '':

            #Copiamos su 'destination' en su 'ICAO' para que AssignGate no falle al clasificarlo.
            original_icao = ac.ICAO
            if ac.ICAO == '' and ac.destination != '':
                ac.ICAO = ac.destination

            # Intentamos asignarle una puerta llamando a la función AssignGate
            resultado = AssignGate(bcn, ac)

            # Devolvemos el ICAO a su estado original para no alterar los datos reales del objeto
            ac.ICAO = original_icao

            # Si se asignó con éxito, sumamos al contador
            if resultado is None:
                contador_nocturnos += 1

    return contador_nocturnos

def FreeGate(bcn, aircraft):

    #Recorremos cada terminal del aeropuerto bcn
    for terminal in bcn.terminals:
        #Recorremos cada área de embarque de la terminal
        for area in terminal.boardingareas:
            #Recorremos cada una de las gates del área
            for gate in area.gates:

                if gate.occupancy == True and gate.aircraft_id == aircraft.id: #Si la puerta está ocupada y contiene el ID del avión que buscamos
                    #Liberamos la puerta reseteando sus variables
                    gate.occupancy = False
                    gate.aircraft_id = ""
                    return True

    # Si termina todos los bucles y el avión no estaba en ninguna puerta, da error:
    return "Error | Aircraft not found in any gate"

def AssignGatesAtTime(bcn, aircrafts, time):

    # Extraemos el número de la hora como entero para evitar fallos de formato
    partes_tiempo = time.split(":")
    hora_actual = int(partes_tiempo[0])

    #Liberamos puertas de aviones que despegan:
    #Recorremos todas las terminales, áreas y gates del aeropuerto para buscar aviones estacionados
    for terminal in bcn.terminals:
        for area in terminal.boardingareas:
            for gate in area.gates:
                if gate.occupancy == True:
                    # Buscamos los datos completos de ese avión en nuestra lista de vuelos
                    for ac in aircrafts:
                        if ac.id == gate.aircraft_id:
                            # Si el avión tiene una hora de salida registrada
                            if ac.departuretime != "":
                                partes_dep = ac.departuretime.split(":")
                                hora_dep = int(partes_dep[0])
                                #Si su despegue cae dentro de la hora actual, lo liberamos de la puerta
                                if hora_dep == hora_actual:
                                    FreeGate(bcn, ac)
                            break

    #Asignamos puertas a los aviones que llegan
    contador_asignados = 0

    # Buscamos en la lista de vuelos qué aviones van a aterrizar ahora
    for ac in aircrafts:
        if ac.arrivaltime != "":
            parts_arr = ac.arrivaltime.split(":")
            hora_arr = int(parts_arr[0])

            #Si el avión aterriza en la hora que estamos evaluando
            if hora_arr == hora_actual:
                # Intentamos asignarle gate llamando a la función AssignGate
                resultado = AssignGate(bcn, ac)

                if resultado is None:
                    contador_asignados += 1

    return contador_asignados


def PlotDayOccupancy(bcn, aircrafts):

    #Posicionamos en las gates a los aviones que se quedaron a dormir
    AssignNightGates(bcn, aircrafts)

    # Preparamos dos listas vacías donde guardaremos los datos para la gráfica
    lista_horas = []
    lista_ocupacion = []

    # Bucle que recorre las 24 horas del día
    for hora in range(24):
        # Convertimos el número de la hora en el formato de texto que espera nuestra simulación
        string_hora = str(hora) + ":00"

        # Ejecutamos la gestión de esa hora: libera despegues y asigna aterrizajes de la hora actual
        AssignGatesAtTime(bcn, aircrafts, string_hora)

        #Contamos cuántas puertas están ocupadas justo en este momento de la simulación
        puertas_ocupadas = 0

        # Entramos a mirar cada terminal, area y gate del aeropuerto
        for terminal in bcn.terminals:
            for area in terminal.boardingareas:
                for gate in area.gates:
                    # Si la puerta tiene el estado de ocupación en True, la sumamos
                    if gate.occupancy == True:
                        puertas_ocupadas += 1

        # Guardamos la hora actual y el número de puertas ocupadas en nuestras listas de datos
        lista_horas.append(hora)
        lista_ocupacion.append(puertas_ocupadas)

    # Generaramos y configuramos la gráfica
    fig, ax = plt.subplots(figsize=(10, 5))

    # 'marker="o"' añade un puntito en cada hora, 'color="blue"' pinta la línea de azul
    ax.plot(lista_horas, lista_ocupacion, marker='o', color='blue', linestyle='-')

    # Ponemos los textos informativos de la gráfica
    ax.set_title("Ocupación de Puertas de Embarque a lo Largo del Día (Versión 4)")
    ax.set_xlabel("Hora del día")
    ax.set_ylabel("Cantidad de puertas ocupadas")
    ax.set_xticks(range(24))

#Creamos una nueva funcion para que "limpie"  aeropuerto y simule bien los vuelos en el slider
def ActualizarSimulacionHastaHora(bcn, lista_vuelos, hora_objetivo):
    #Ponemos todas las puertas a False (las libres) para empezar de cero
    for t in bcn.terminals:
        for area in t.boardingareas:
            for gate in area.gates:
                gate.occupancy = False
                gate.aircraft_id = ""

    #Metemos a los aviones que pernoctaron
    AssignNightGates(bcn, lista_vuelos)

    #Simulamos hora por hora hasta llegar a la hora del slider
    for h in range(hora_objetivo + 1):
        # Creamos el texto de la hora (ej: "10:00")
        string_hora = str(h) + ":00"
        AssignGatesAtTime(bcn, lista_vuelos, string_hora)