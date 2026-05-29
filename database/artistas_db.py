from database.conexion import conectar

def obtener_artistas():

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM artistas")

    artistas = cursor.fetchall()

    conexion.close()

    return artistas

def agregar_artista(nombre, genero, pais):

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
    INSERT INTO artistas(nombre, genero, pais)
    VALUES(?,?,?)
    """, (nombre, genero, pais))

    conexion.commit()
    conexion.close()

def eliminar_artista(id_artista):

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
    DELETE FROM artistas
    WHERE id = ?
    """, (id_artista,))

    conexion.commit()
    conexion.close()

def actualizar_artista(id_artista, nombre, genero, pais):

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
    UPDATE artistas
    SET nombre = ?, genero = ?, pais = ?
    WHERE id = ?
    """, (nombre, genero, pais, id_artista))

    conexion.commit()
    conexion.close()