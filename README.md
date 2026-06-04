# Managing Airports SA™

## Airport Manager — Sistema Inteligente de Gestión Aeroportuaria

**Managing Airports SA™** presenta **Airport Manager**, una solución digital diseñada para facilitar la gestión operativa de aeropuertos mediante una interfaz visual, intuitiva y robusta.

En un entorno aeroportuario, cada decisión cuenta. Una puerta mal asignada, una salida no prevista o una mala interpretación del tráfico puede afectar a toda la operación. Por eso, **Airport Manager** nace con un objetivo claro: **convertir datos complejos en decisiones rápidas, fiables y visuales**.

Airport Manager permite centralizar en una única plataforma la gestión de aeropuertos, vuelos, rutas, terminales, aerolíneas y puertas de embarque. La herramienta trabaja con información estructurada en ficheros de texto y la transforma en gráficos, mapas y simulaciones operativas fáciles de interpretar.

Disfruta: https://drive.google.com/file/d/1XULBw7zhhhIZY4gg5bdfsGJ0t8e1pAsK/view?usp=sharing
---

## ¿Qué es Airport Manager?

**Airport Manager** es una interfaz de escritorio orientada a la gestión y simulación operativa del aeropuerto de **Barcelona-El Prat (LEBL)**.

El sistema permite:

- Cargar y gestionar bases de datos de aeropuertos.
- Clasificar aeropuertos y vuelos como Schengen o no Schengen.
- Analizar llegadas por aerolínea y por tipo de vuelo.
- Generar rutas de vuelo visuales mediante archivos KML.
- Cargar la estructura interna del aeropuerto LEBL.
- Gestionar terminales, áreas de embarque y puertas.
- Asignar puertas según aerolínea, terminal y tipo de vuelo.
- Simular la ocupación de puertas durante todo el día.
- Gestionar salidas y liberar puertas cuando un avión despega.
- Visualizar el estado de las puertas hora a hora mediante un slider interactivo.

Airport Manager no es solo un visor de datos.  
Es una **herramienta de apoyo a la toma de decisiones operativas**.

---

## ¿Por qué Airport Manager?

La gestión aeroportuaria moderna necesita claridad, rapidez y fiabilidad.

Airport Manager se ha diseñado alrededor de tres pilares principales:

### Robustez

El sistema está preparado para soportar errores habituales sin bloquearse. Detecta ficheros inexistentes, listas vacías, entradas incorrectas, puertas no disponibles y operaciones no válidas, informando al usuario mediante mensajes claros dentro de la interfaz.

### Inteligencia operativa

La aplicación no trata los vuelos como datos aislados. Relaciona llegadas y salidas, detecta aviones que pernoctan en el aeropuerto, asigna puertas según restricciones reales y simula la evolución de la ocupación durante el día.

### Claridad visual

Airport Manager convierte datos en información visual. Mediante gráficos, mapas y planos interactivos de puertas, el usuario puede entender rápidamente la situación del aeropuerto y tomar mejores decisiones.

---

## Áreas principales del sistema

### Gestión de aeropuertos

El módulo de gestión de aeropuertos permite cargar, añadir y eliminar aeropuertos del sistema. Cada aeropuerto queda identificado por su código ICAO y sus coordenadas geográficas.

El sistema también puede clasificar aeropuertos en función de si pertenecen o no al espacio Schengen, permitiendo diferenciar distintos tipos de operación aeroportuaria.

---

### Análisis de llegadas

El módulo de llegadas carga los vuelos programados para aterrizar en LEBL.

Cada llegada incluye:

- Identificador del avión.
- Aeropuerto de origen.
- Hora de llegada.
- Código de aerolínea.

Una vez cargados los datos, el sistema puede generar análisis visuales como:

- Número de vuelos por aerolínea.
- Comparativa entre llegadas Schengen y no Schengen.
- Rutas de llegada hacia Barcelona-El Prat.

Esto permite al operador comprender el flujo de tráfico entrante y detectar qué aerolíneas o regiones generan mayor carga operativa.

---

### Visualización de rutas de vuelo

Airport Manager puede generar archivos KML para visualizar aeropuertos y rutas de vuelo en Google Earth.

El sistema muestra:

- Puntos de aeropuertos.
- Rutas de llegada hacia LEBL.
- Rutas Schengen y no Schengen diferenciadas por colores.

Esto ofrece una visión geográfica de la red aeroportuaria y permite entender mejor la conectividad de Barcelona-El Prat.

---

### Gestión de puertas

El módulo de gestión de puertas es el núcleo del sistema.

Airport Manager carga la estructura de LEBL, incluyendo:

- Terminales.
- Áreas de embarque.
- Puertas.
- Zonas Schengen y no Schengen.
- Aerolíneas asignadas a cada terminal.

Gracias a esta estructura, el sistema puede asignar puertas de forma inteligente teniendo en cuenta:

- La aerolínea del avión.
- La terminal donde opera esa aerolínea.
- El carácter Schengen o no Schengen del vuelo.
- La disponibilidad real de puertas.

El resultado es una simulación realista de asignación de puertas en un aeropuerto.

---

### Salidas y liberación de puertas

Airport Manager también gestiona las salidas.

Cuando un avión despega, su puerta queda liberada y vuelve a estar disponible para futuras llegadas. Esto hace que la simulación sea mucho más realista, ya que el aeropuerto no se trata como un sistema estático.

La aplicación puede unir llegadas y salidas mediante el identificador del avión, entendiendo así el ciclo completo de movimiento de cada aeronave durante el día.

---

### Simulación diaria de ocupación

El sistema simula el aeropuerto hora a hora.

En cada franja horaria puede:

- Asignar puertas a los aviones que llegan.
- Liberar puertas de los aviones que salen.
- Contar cuántas puertas están ocupadas.
- Mostrar la evolución del uso de puertas durante el día.

Esto ayuda a identificar horas críticas, posibles puntos de saturación y momentos de mayor presión sobre la infraestructura aeroportuaria.

---

### Panel interactivo V4

La versión final incorpora un panel visual interactivo.

Mediante un slider temporal, el usuario puede desplazarse por las 24 horas del día y ver el estado de las puertas del aeropuerto en cada momento.

Las puertas libres se muestran en verde.  
Las puertas ocupadas se muestran en rojo.

Esto transforma la interfaz en un panel dinámico de control operativo.

---

## Experiencia de usuario

Airport Manager ha sido diseñado con una interfaz profesional, clara y cómoda de utilizar.

La aplicación incluye:

- Diseño moderno con CustomTkinter.
- Modo claro y modo oscuro.
- Barra de notificaciones de estado.
- Gráficos integrados con Matplotlib.
- Plano visual interactivo del aeropuerto.
- Música ambiental opcional.
- Colores claros para acciones principales, acciones correctas y errores.

El objetivo es que el sistema sea potente, pero también agradable y sencillo de usar.

---

## Visión

Airport Manager se construye alrededor de una idea sencilla:

> **Los datos aeroportuarios no solo deben almacenarse. Deben entenderse.**

Managing Airports SA™ busca ofrecer una herramienta que ayude a pasar de datos sin procesar a control operativo.

Combinando procesamiento de datos, análisis visual, mapas de rutas y simulación de puertas, Airport Manager ofrece una visión completa de la actividad aeroportuaria desde una sola interfaz.

---

## Managing Airports SA™

**Managing Airports SA™** representa una forma moderna de entender la gestión aeroportuaria: eficiente, visual, fiable y preparada para retos operativos reales.

Airport Manager es un paso hacia aeropuertos más inteligentes, donde cada vuelo, cada puerta y cada decisión pueden supervisarse con claridad.

**Managing Airports SA™ — Control, visión y fiabilidad para aeropuertos preparados para despegar.**
