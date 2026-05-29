from datetime import datetime

class Album:

    def __init__(self, id, titulo, anio_lanzamiento, id_artista):
        self.id = id
        self.titulo = titulo
        self.anio_lanzamiento = anio_lanzamiento
        self.id_artista = id_artista

    def antiguedad(self):
        return datetime.now().year - self.anio_lanzamiento

    def mostrar_info(self):
        return f"{self.titulo} ({self.anio_lanzamiento})"