from contextlib import closing

from database.conexion import conectar
from utils.validaciones import limpiar_texto


def obtener_artistas(genero="", pais=""):
    consulta = "SELECT id, nombre, genero, pais FROM artistas WHERE 1 = 1"
    parametros = []
    if genero:
        consulta += " AND genero = ?"
        parametros.append(genero)
    if pais:
        consulta += " AND pais = ?"
        parametros.append(pais)
    consulta += " ORDER BY nombre"
    with closing(conectar()) as conexion:
        return conexion.execute(consulta, parametros).fetchall()


def obtener_artista(id_artista):
    with closing(conectar()) as conexion:
        return conexion.execute(
            "SELECT id, nombre, genero, pais FROM artistas WHERE id = ?",
            (id_artista,),
        ).fetchone()


def agregar_artista(nombre, genero, pais):
    with closing(conectar()) as conexion, conexion:
        cursor = conexion.execute(
            "INSERT INTO artistas (nombre, genero, pais) VALUES (?, ?, ?)",
            (
                limpiar_texto(nombre, "El nombre"),
                limpiar_texto(genero, "El género"),
                limpiar_texto(pais, "El país"),
            ),
        )
        return cursor.lastrowid


def eliminar_artista(id_artista):
    with closing(conectar()) as conexion, conexion:
        cursor = conexion.execute("DELETE FROM artistas WHERE id = ?", (id_artista,))
        return cursor.rowcount == 1


def actualizar_artista(id_artista, nombre, genero, pais):
    with closing(conectar()) as conexion, conexion:
        cursor = conexion.execute(
            """UPDATE artistas
               SET nombre = ?, genero = ?, pais = ?
               WHERE id = ?""",
            (
                limpiar_texto(nombre, "El nombre"),
                limpiar_texto(genero, "El género"),
                limpiar_texto(pais, "El país"),
                id_artista,
            ),
        )
        return cursor.rowcount == 1


def valores_filtro_artistas(campo):
    consultas = {
        "genero": "SELECT DISTINCT genero FROM artistas ORDER BY genero",
        "pais": "SELECT DISTINCT pais FROM artistas ORDER BY pais",
    }
    if campo not in consultas:
        raise ValueError("Filtro no permitido.")
    with closing(conectar()) as conexion:
        return [fila[0] for fila in conexion.execute(consultas[campo]).fetchall()]
