from database.conexion import conectar

def obtener_albumes():

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
    SELECT albumes.id,
           albumes.titulo,
           albumes.anio_lanzamiento,
           artistas.nombre
    FROM albumes
    JOIN artistas
    ON albumes.id_artista = artistas.id
    """)

    datos = cursor.fetchall()

    conexion.close()

    return datos

def agregar_album(titulo, anio, id_artista):

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
    INSERT INTO albumes(titulo, anio_lanzamiento, id_artista)
    VALUES(?,?,?)
    """, (titulo, anio, id_artista))

    conexion.commit()
    conexion.close()