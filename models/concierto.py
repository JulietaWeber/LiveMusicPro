from datetime import date, datetime


class Concierto:
    def __init__(self, id, nombre_evento, fecha, ciudad, id_artista, artista_nombre=""):
        self.id = id
        self.nombre_evento = nombre_evento
        self.fecha = fecha
        self.ciudad = ciudad
        self.id_artista = id_artista
        self.artista_nombre = artista_nombre

    def mostrar_evento(self):
        return f"{self.nombre_evento} - {self.ciudad} - {self.fecha}"

    def es_en_buenos_aires(self):
        return self.ciudad.casefold() == "buenos aires"

    def esta_programado(self):
        return datetime.strptime(self.fecha, "%Y-%m-%d").date() >= date.today()

    def a_diccionario(self):
        return {
            "ID": self.id,
            "Evento": self.nombre_evento,
            "Fecha": self.fecha,
            "Ciudad": self.ciudad,
            "Artista": self.artista_nombre,
            "Estado": "Próximo" if self.esta_programado() else "Finalizado",
        }

    @classmethod
    def desde_fila(cls, fila):
        claves = fila.keys()
        return cls(
            fila["id"],
            fila["nombre_evento"],
            fila["fecha"],
            fila["ciudad"],
            fila["id_artista"],
            fila["artista_nombre"] if "artista_nombre" in claves else "",
        )
