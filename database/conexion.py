import sqlite3

def conectar():
    conexion = sqlite3.connect("musica.db")
    return conexion

def crear_tablas():
    conexion = conectar()
    cursor = conexion.cursor()

    # TABLA ARTISTAS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS artistas(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        genero TEXT NOT NULL,
        pais TEXT NOT NULL
    )
    """)

    # TABLA ALBUMES
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS albumes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        anio_lanzamiento INTEGER,
        id_artista INTEGER,
        FOREIGN KEY(id_artista) REFERENCES artistas(id)
    )
    """)

    # TABLA CONCIERTOS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS conciertos(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_evento TEXT NOT NULL,
        fecha TEXT,
        ciudad TEXT,
        id_artista INTEGER,
        FOREIGN KEY(id_artista) REFERENCES artistas(id)
    )
    """)

    conexion.commit()
    conexion.close()

def insertar_datos_iniciales():
    conexion = conectar()
    cursor = conexion.cursor()

    artistas = [
        ("Bizarrap", "Urbano", "Argentina"),
        ("Dua Lipa", "Pop", "Reino Unido"),
        ("Bad Bunny", "Reggaeton", "Puerto Rico")
    ]

    cursor.executemany("""
    INSERT INTO artistas(nombre, genero, pais)
    VALUES(?,?,?)
    """, artistas)

    conexion.commit()
    conexion.close()

if __name__ == "__main__":
    crear_tablas()
    insertar_datos_iniciales()
    print("Base de datos creada")