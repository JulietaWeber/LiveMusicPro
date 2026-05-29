class Concierto:

    def __init__(self, id, nombre_evento, fecha, ciudad, id_artista):
        self.id = id
        self.nombre_evento = nombre_evento
        self.fecha = fecha
        self.ciudad = ciudad
        self.id_artista = id_artista

    def mostrar_evento(self):
        return f"{self.nombre_evento} - {self.ciudad}"

    def es_en_buenos_aires(self):
        return self.ciudad.lower() == "buenos aires"