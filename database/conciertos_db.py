from contextlib import closing

from database.conexion import conectar
from utils.validaciones import limpiar_texto, validar_fecha


def obtener_conciertos(ciudad="", id_artista=None):
    consulta = """
        SELECT co.id, co.nombre_evento, co.fecha, co.ciudad, co.id_artista,
               ar.nombre AS artista_nombre
        FROM conciertos co
        INNER JOIN artistas ar ON co.id_artista = ar.id
        WHERE 1 = 1
    """
    parametros = []
    if ciudad:
        consulta += " AND co.ciudad = ?"
        parametros.append(ciudad)
    if id_artista is not None:
        consulta += " AND co.id_artista = ?"
        parametros.append(id_artista)
    consulta += " ORDER BY co.fecha ASC"
    with closing(conectar()) as conexion:
        return conexion.execute(consulta, parametros).fetchall()


def obtener_concierto(id_concierto):
    with closing(conectar()) as conexion:
        return conexion.execute(
            """SELECT id, nombre_evento, fecha, ciudad, id_artista
               FROM conciertos WHERE id = ?""",
            (id_concierto,),
        ).fetchone()


def agregar_concierto(nombre, fecha, ciudad, id_artista):
    with closing(conectar()) as conexion, conexion:
        cursor = conexion.execute(
            """INSERT INTO conciertos (nombre_evento, fecha, ciudad, id_artista)
               VALUES (?, ?, ?, ?)""",
            (
                limpiar_texto(nombre, "El nombre del evento"),
                validar_fecha(fecha),
                limpiar_texto(ciudad, "La ciudad"),
                id_artista,
            ),
        )
        return cursor.lastrowid


def actualizar_concierto(id_concierto, nombre, fecha, ciudad, id_artista):
    with closing(conectar()) as conexion, conexion:
        cursor = conexion.execute(
            """UPDATE conciertos
               SET nombre_evento = ?, fecha = ?, ciudad = ?, id_artista = ?
               WHERE id = ?""",
            (
                limpiar_texto(nombre, "El nombre del evento"),
                validar_fecha(fecha),
                limpiar_texto(ciudad, "La ciudad"),
                id_artista,
                id_concierto,
            ),
        )
        return cursor.rowcount == 1


def eliminar_concierto(id_concierto):
    with closing(conectar()) as conexion, conexion:
        cursor = conexion.execute("DELETE FROM conciertos WHERE id = ?", (id_concierto,))
        return cursor.rowcount == 1


def obtener_ciudades():
    with closing(conectar()) as conexion:
        filas = conexion.execute(
            "SELECT DISTINCT ciudad FROM conciertos ORDER BY ciudad"
        ).fetchall()
        return [fila[0] for fila in filas]
