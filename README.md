# 🎵 Live Music Pro

## Descripción del Proyecto

Live Music Pro es una aplicación desarrollada para la productora musical **ORT Sounds** con el objetivo de centralizar la gestión de artistas, álbumes y conciertos.

Actualmente muchas productoras utilizan archivos dispersos para organizar su información, lo que puede provocar errores, duplicados o pérdida de datos. Este sistema busca resolver ese problema mediante una aplicación con base de datos SQLite y una interfaz gráfica desarrollada con Streamlit.

---

# Objetivos

* Gestionar artistas musicales.
* Gestionar álbumes asociados a cada artista.
* Gestionar conciertos y eventos.
* Mantener la información almacenada de forma persistente mediante SQLite.
* Aplicar Programación Orientada a Objetos (POO).
* Implementar operaciones CRUD completas.
* Utilizar una interfaz gráfica intuitiva.

---

# Estructura del Proyecto

```plaintext
live_music_pro/
│
├── app.py
│
├── database/
│   ├── conexion.py
│   ├── artistas_db.py
│   ├── albumes_db.py
│   └── conciertos_db.py
│
├── models/
│   ├── artista.py
│   ├── album.py
│   └── concierto.py
│
├── utils/
│   └── validaciones.py
│
├── musica.db
│
├── requirements.txt
│
└── README.md
```

---

# Explicación de cada carpeta

## app.py

Es el archivo principal de la aplicación.

Contiene:

* Interfaz Streamlit.
* Menú de navegación.
* Dashboard.
* Formularios.
* Visualización de datos.

Para ejecutar la aplicación se debe correr este archivo.

---

## database/

Contiene toda la lógica relacionada con la base de datos.

### conexion.py

Responsable de:

* Crear la conexión SQLite.
* Crear tablas.
* Insertar datos iniciales.

### artistas_db.py

CRUD de artistas:

* Crear artista.
* Obtener artistas.
* Modificar artista.
* Eliminar artista.

### albumes_db.py

CRUD de álbumes.

### conciertos_db.py

CRUD de conciertos.

---

## models/

Contiene las clases del proyecto (POO).

### artista.py

Representa un artista.

Métodos sugeridos:

* mostrar_ficha()
* es_argentino()

### album.py

Representa un álbum.

Métodos sugeridos:

* mostrar_info()
* antiguedad()

### concierto.py

Representa un concierto.

Métodos sugeridos:

* mostrar_evento()
* es_en_buenos_aires()

---

## utils/

Contiene funciones auxiliares.

### validaciones.py

Funciones para validar:

* Campos vacíos.
* Fechas.
* Años de lanzamiento.
* Datos incorrectos.

---

# Base de Datos

El sistema utiliza SQLite.

Tablas principales:

## artistas

| Campo  | Tipo    |
| ------ | ------- |
| id     | INTEGER |
| nombre | TEXT    |
| genero | TEXT    |
| pais   | TEXT    |

---

## albumes

| Campo            | Tipo    |
| ---------------- | ------- |
| id               | INTEGER |
| titulo           | TEXT    |
| anio_lanzamiento | INTEGER |
| id_artista       | INTEGER |

---

## conciertos

| Campo         | Tipo    |
| ------------- | ------- |
| id            | INTEGER |
| nombre_evento | TEXT    |
| fecha         | TEXT    |
| ciudad        | TEXT    |
| id_artista    | INTEGER |

---

# Funcionalidades Actuales

## Artistas

* Listar artistas.
* Agregar artistas.
* Modificar artistas.
* Eliminar artistas.

## Álbumes

* Listar álbumes.
* Agregar álbumes.
* Modificar álbumes.
* Eliminar álbumes.

## Conciertos

* Listar conciertos.
* Agregar conciertos.
* Modificar conciertos.
* Eliminar conciertos.

---

# Funcionalidades Pendientes

## Prioridad Alta

* CRUD completo para todas las tablas.
* Filtros de búsqueda.
* Validaciones avanzadas.
* Dashboard con estadísticas.

## Prioridad Media

* Gráficos.
* Exportar CSV.
* Reportes.

## Extra (si hay tiempo)

* Sistema de tickets.
* Login de usuarios.
* Calendario de eventos.
* Ranking de artistas.

---

# Cómo ejecutar el proyecto

## 1. Instalar dependencias

```bash
pip install streamlit pandas
```

o

```bash
pip install -r requirements.txt
```

---

## 2. Crear la base de datos

```bash
python database/conexion.py
```

---

## 3. Ejecutar la aplicación

```bash
streamlit run app.py
```

---

# Distribución sugerida del trabajo

## Integrante 1

Base de datos

* Tablas.
* Relaciones.
* CRUD.

---

## Integrante 2

Programación Orientada a Objetos

* Clases.
* Métodos.
* Conversión de registros a objetos.

---

## Integrante 3

Interfaz Streamlit

* Formularios.
* Dashboard.
* Navegación.

---

## Integrante 4

Validaciones y pruebas

* Manejo de errores.
* Filtros.
* Testing.

---

# Tecnologías utilizadas

* Python
* SQLite
* Streamlit
* Pandas

---

# Estado del Proyecto

🟡 En desarrollo

Próximos pasos:

* Completar CRUD.
* Agregar filtros.
* Implementar estadísticas.
* Mejorar interfaz visual.
