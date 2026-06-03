# LEBL Airport Management

Proyecto de Informatica 1 para gestionar aeropuertos, vuelos de llegada/salida y asignacion de gates en el aeropuerto de Barcelona LEBL.

## Equipo

Autores/equipo: TODO completar con los nombres del grupo.

## Como ejecutar

1. Abrir la carpeta del proyecto en PyCharm o en una terminal.
2. Ejecutar:

```bash
python interface.py
```

Tambien se pueden probar los modulos por separado:

```bash
python airport.py
python aircraft.py
python LEBL.py
```

## Archivos principales

- `airport.py`: clase `Airport`, carga/guardado de aeropuertos, Schengen, graficos y KML.
- `aircraft.py`: clase `Aircraft`, llegadas, salidas, merge de movimientos, night aircraft, plots y rutas.
- `LEBL.py`: estructura de LEBL, terminales, boarding areas, gates y asignacion dinamica.
- `utils.py`: validacion de horas, conversiones, lectura/escritura segura y helpers generales.
- `interface.py`: interfaz grafica final con Tkinter y matplotlib incrustado.
- `Airports.txt`, `Arrivals.txt`, `Departures.txt`, `Terminals.txt`, `T1_Airlines.txt`, `T2_Airlines.txt`: datos del proyecto.

## Funcionalidades por version

### Version 1

- Cargar aeropuertos desde fichero.
- Anadir y eliminar aeropuertos.
- Detectar aeropuertos Schengen.
- Guardar aeropuertos Schengen.
- Graficar y generar mapa KML de aeropuertos.

### Version 2

- Cargar vuelos de llegada.
- Guardar vuelos.
- Graficos de llegadas, aerolineas y vuelos Schengen/no Schengen.
- Generar rutas KML y detectar vuelos de larga distancia.

### Version 3

- Cargar estructura de terminales de LEBL.
- Cargar aerolineas por terminal.
- Crear boarding areas y gates.
- Buscar terminal por aerolinea.
- Asignar gates y consultar ocupacion.

### Version 4

- Cargar salidas con formato `AIRCRAFT DESTINATION DEPARTURE AIRLINE`.
- Fusionar llegadas y salidas por aircraft id.
- Controlar multiples movimientos del mismo avion durante el dia.
- Detectar night aircraft: aviones sin llegada pero con salida.
- Liberar gates cuando un avion sale.
- Asignar gates por franja horaria.
- Simular ocupacion de todo el dia.
- Mostrar vuelos no asignados por hora.

## Extras implementados

- Dashboard visual de ocupacion diaria por terminal con aircraft no asignados.
- Mapa visual de gates con puertas libres/ocupadas e id del aircraft cuando cabe.
- Exportacion de informe resumen a `.txt`.

## Robustez

El programa evita crashear ante:

- Ficheros inexistentes o vacios.
- Lineas con formato incorrecto.
- Horas invalidas.
- Listas vacias.
- Aerolineas no encontradas.
- Terminal o estructura no cargada.
- Falta de gates libres.
- Botones pulsados antes de cargar datos.

## Capturas

TODO insertar capturas de la interfaz, dashboard y mapa de gates.

## Video

TODO insertar link al video de presentacion.

## Uso de IA

Se ha usado asistencia de IA para revisar, refactorizar y robustecer el codigo, manteniendo una estructura y estilo adecuados para Informatica 1: clases simples, listas, ficheros de texto, matplotlib y tkinter.

## Puntos a revisar antes de entregar

- Completar nombres de autores.
- Confirmar que el `Departures.txt` definitivo coincide con el fichero de datos pedido por el profesor.
- Probar manualmente la interfaz en el ordenador de entrega.
- Anadir capturas y link del video.
# Airport-Management-SA
