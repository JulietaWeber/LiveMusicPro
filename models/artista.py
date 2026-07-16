class Artista:
    def __init__(self, id, nombre, genero, pais):
        self.id = id
        self.nombre = nombre
        self.genero = genero
        self.pais = pais

    def mostrar_ficha(self):
        return f"{self.nombre} - {self.genero} - {self.pais}"

    def es_argentino(self):
        return self.pais.casefold() == "argentina"

    def a_diccionario(self):
        return {
            "ID": self.id,
            "Nombre": self.nombre,
            "Género": self.genero,
            "País": self.pais,
        }

    @classmethod
    def desde_fila(cls, fila):
        return cls(fila["id"], fila["nombre"], fila["genero"], fila["pais"])
