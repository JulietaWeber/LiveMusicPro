from contextlib import closing

from database.conexion import conectar
from utils.validaciones import limpiar_texto, validar_anio


def obtener_albumes(genero="", id_artista=None):
    consulta = """
        SELECT al.id, al.titulo, al.anio_lanzamiento, al.id_artista,
               ar.nombre AS artista_nombre
        FROM albumes al
        INNER JOIN artistas ar ON al.id_artista = ar.id
        WHERE 1 = 1
    """
    parametros = []
    if genero:
        consulta += " AND ar.genero = ?"
        parametros.append(genero)
    if id_artista is not None:
        consulta += " AND al.id_artista = ?"
        parametros.append(id_artista)
    consulta += " ORDER BY al.anio_lanzamiento DESC, al.titulo"
    with closing(conectar()) as conexion:
        return conexion.execute(consulta, parametros).fetchall()


def obtener_album(id_album):
    with closing(conectar()) as conexion:
        return conexion.execute(
            """SELECT id, titulo, anio_lanzamiento, id_artista
               FROM albumes WHERE id = ?""",
            (id_album,),
        ).fetchone()


def agregar_album(titulo, anio, id_artista):
    with closing(conectar()) as conexion, conexion:
        cursor = conexion.execute(
            """INSERT INTO albumes (titulo, anio_lanzamiento, id_artista)
               VALUES (?, ?, ?)""",
            (limpiar_texto(titulo, "El título"), validar_anio(anio), id_artista),
        )
        return cursor.lastrowid


def actualizar_album(id_album, titulo, anio, id_artista):
    with closing(conectar()) as conexion, conexion:
        cursor = conexion.execute(
            """UPDATE albumes
               SET titulo = ?, anio_lanzamiento = ?, id_artista = ?
               WHERE id = ?""",
            (
                limpiar_texto(titulo, "El título"),
                validar_anio(anio),
                id_artista,
                id_album,
            ),
        )
        return cursor.rowcount == 1


def eliminar_album(id_album):
    with closing(conectar()) as conexion, conexion:
        cursor = conexion.execute("DELETE FROM albumes WHERE id = ?", (id_album,))
        return cursor.rowcount == 1
