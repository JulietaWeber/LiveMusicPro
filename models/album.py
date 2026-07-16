from datetime import date


class Album:
    def __init__(self, id, titulo, anio_lanzamiento, id_artista, artista_nombre=""):
        self.id = id
        self.titulo = titulo
        self.anio_lanzamiento = anio_lanzamiento
        self.id_artista = id_artista
        self.artista_nombre = artista_nombre

    def antiguedad(self):
        return max(0, date.today().year - self.anio_lanzamiento)

    def mostrar_info(self):
        artista = f" - {self.artista_nombre}" if self.artista_nombre else ""
        return f"{self.titulo} ({self.anio_lanzamiento}){artista}"

    def a_diccionario(self):
        return {
            "ID": self.id,
            "Título": self.titulo,
            "Año": self.anio_lanzamiento,
            "Artista": self.artista_nombre,
            "Antigüedad": self.antiguedad(),
        }

    @classmethod
    def desde_fila(cls, fila):
        claves = fila.keys()
        return cls(
            fila["id"],
            fila["titulo"],
            fila["anio_lanzamiento"],
            fila["id_artista"],
            fila["artista_nombre"] if "artista_nombre" in claves else "",
        )
