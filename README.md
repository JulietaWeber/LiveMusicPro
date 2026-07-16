# 🎵 Live Music Pro

Aplicación para centralizar la gestión de artistas, álbumes y conciertos de **ORT Sounds**. Utiliza Python, SQLite y una interfaz gráfica desarrollada con Streamlit.

## Funcionalidades terminadas

- Clases `Artista`, `Album` y `Concierto`, cada una con métodos de instancia.
- Conversión de registros SQLite en listas de objetos antes de mostrarlos.
- CRUD completo de artistas, álbumes y conciertos.
- Altas y modificaciones validadas.
- Bajas seguras por ID y protección de artistas con registros asociados.
- Filtros de artistas por género y país, álbumes por género y conciertos por ciudad.
- Dashboard con cantidades y próximos conciertos.
- Capa de base de datos separada de la interfaz.
- Datos iniciales idempotentes, sin duplicados al reiniciar.
- Pruebas automatizadas de las operaciones principales.

## Estructura

```text
app.py                 Interfaz Streamlit
database/
  conexion.py          Conexión, tablas y datos iniciales
  artistas_db.py       CRUD y filtros de artistas
  albumes_db.py        CRUD y filtros de álbumes
  conciertos_db.py     CRUD y filtros de conciertos
models/
  artista.py           Clase Artista
  album.py             Clase Album
  concierto.py         Clase Concierto
utils/
  validaciones.py      Validaciones reutilizables
pruebas.py             Pruebas funcionales
requirements.txt       Dependencias
musica.db              Base de datos SQLite
```

## Ejecución

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

La aplicación crea las tablas y carga los artistas iniciales automáticamente cuando la base está vacía.

## Pruebas

```bash
python pruebas.py
```

Las pruebas utilizan una base temporal y no modifican `musica.db`.
