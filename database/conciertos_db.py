from database.conexion import conectar

def obtener_conciertos():

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
    SELECT conciertos.id,
           conciertos.nombre_evento,
           conciertos.fecha,
           conciertos.ciudad,
           artistas.nombre
    FROM conciertos
    JOIN artistas
    ON conciertos.id_artista = artistas.id
    """)

    datos = cursor.fetchall()

    conexion.close()

    return datos

def agregar_concierto(nombre, fecha, ciudad, id_artista):

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
    INSERT INTO conciertos(nombre_evento, fecha, ciudad, id_artista)
    VALUES(?,?,?,?)
    """, (nombre, fecha, ciudad, id_artista))

    conexion.commit()
    conexion.close()