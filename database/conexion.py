import sqlite3
from contextlib import closing
from pathlib import Path


RUTA_DB = Path(__file__).resolve().parent.parent / "musica.db"


def conectar():
    conexion = sqlite3.connect(RUTA_DB)
    conexion.row_factory = sqlite3.Row
    conexion.execute("PRAGMA foreign_keys = ON")
    return conexion


def crear_tablas():
    with closing(conectar()) as conexion, conexion:
        conexion.executescript(
            """
            CREATE TABLE IF NOT EXISTS artistas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                genero TEXT NOT NULL,
                pais TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS albumes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                anio_lanzamiento INTEGER NOT NULL,
                id_artista INTEGER NOT NULL,
                FOREIGN KEY (id_artista) REFERENCES artistas (id)
                    ON UPDATE CASCADE ON DELETE RESTRICT
            );

            CREATE TABLE IF NOT EXISTS conciertos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre_evento TEXT NOT NULL,
                fecha TEXT NOT NULL,
                ciudad TEXT NOT NULL,
                id_artista INTEGER NOT NULL,
                FOREIGN KEY (id_artista) REFERENCES artistas (id)
                    ON UPDATE CASCADE ON DELETE RESTRICT
            );
            """
        )


def insertar_datos_iniciales():
    with closing(conectar()) as conexion, conexion:
        cantidad = conexion.execute("SELECT COUNT(*) FROM artistas").fetchone()[0]
        if cantidad:
            return
        conexion.executemany(
            "INSERT INTO artistas (nombre, genero, pais) VALUES (?, ?, ?)",
            [
                ("Bizarrap", "Urbano", "Argentina"),
                ("Dua Lipa", "Pop", "Reino Unido"),
                ("Bad Bunny", "Reggaetón", "Puerto Rico"),
            ],
        )


def inicializar_base_de_datos():
    crear_tablas()
    insertar_datos_iniciales()


if __name__ == "__main__":
    inicializar_base_de_datos()
    print("Base de datos creada y lista para usar.")
