class Artista:

    def __init__(self, id, nombre, genero, pais):
        self.id = id
        self.nombre = nombre
        self.genero = genero
        self.pais = pais

    def mostrar_ficha(self):
        return f"{self.nombre} - {self.genero} - {self.pais}"

    def es_argentino(self):
        return self.pais.lower() == "argentina"