import sqlite3
import tempfile
from pathlib import Path

from database import conexion
from database.albumes_db import (
    actualizar_album,
    agregar_album,
    eliminar_album,
    obtener_albumes,
)
from database.artistas_db import (
    actualizar_artista,
    agregar_artista,
    eliminar_artista,
    obtener_artista,
    obtener_artistas,
)
from database.conciertos_db import (
    actualizar_concierto,
    agregar_concierto,
    eliminar_concierto,
    obtener_conciertos,
)
from models.album import Album
from models.artista import Artista
from models.concierto import Concierto
from utils.analisis_datos import (
    calcular_tendencia_central,
    importar_albumes_desde_csv,
    interpretar_tendencia_central,
    leer_albumes_desde_base,
)


def ejecutar_pruebas():
    with tempfile.TemporaryDirectory() as carpeta:
        conexion.RUTA_DB = Path(carpeta) / "prueba.db"
        conexion.crear_tablas()

        artista_id = agregar_artista("Artista de prueba", "Rock", "Argentina")
        artista = Artista.desde_fila(obtener_artista(artista_id))
        assert artista.es_argentino()
        assert actualizar_artista(artista_id, "Artista editado", "Pop", "Uruguay")

        album_id = agregar_album("Álbum de prueba", 2024, artista_id)
        album = Album.desde_fila(obtener_albumes()[0])
        assert album.id == album_id
        assert actualizar_album(album_id, "Álbum editado", 2025, artista_id)

        concierto_id = agregar_concierto(
            "Evento de prueba", "2027-01-15", "Rosario", artista_id
        )
        concierto = Concierto.desde_fila(obtener_conciertos()[0])
        assert concierto.id == concierto_id
        assert actualizar_concierto(
            concierto_id, "Evento editado", "2027-02-20", "Córdoba", artista_id
        )

        assert len(obtener_artistas(genero="Pop")) == 1
        assert len(obtener_albumes(genero="Pop")) == 1
        assert len(obtener_conciertos(ciudad="Córdoba")) == 1

        try:
            eliminar_artista(artista_id)
            raise AssertionError("No debe eliminarse un artista con datos asociados")
        except sqlite3.IntegrityError:
            pass

        assert eliminar_concierto(concierto_id)
        assert eliminar_album(album_id)

        resultado_importacion = importar_albumes_desde_csv()
        assert resultado_importacion == {"importados": 15, "omitidos": 0, "total": 15}
        assert len(obtener_albumes()) == 15

        segunda_importacion = importar_albumes_desde_csv()
        assert segunda_importacion == {"importados": 0, "omitidos": 15, "total": 15}
        assert len(obtener_albumes()) == 15

        resultados = calcular_tendencia_central(leer_albumes_desde_base())
        assert resultados["cantidad"] == 15
        assert resultados["mediana"] == 2022
        assert resultados["modas"] == [2020]
        assert resultados["frecuencia_moda"] == 3
        assert resultados["hay_moda_clara"]
        assert "La moda es 2020" in interpretar_tendencia_central(resultados)

        for album_importado in obtener_albumes():
            assert eliminar_album(album_importado["id"])
        assert eliminar_artista(artista_id)

        for operacion in (
            lambda: agregar_artista("", "Pop", "Argentina"),
            lambda: agregar_album("Inválido", -1, 999),
            lambda: agregar_concierto("Evento", "2027-99-99", "Rosario", 999),
        ):
            try:
                operacion()
                raise AssertionError("La validación debía rechazar el dato")
            except ValueError:
                pass


if __name__ == "__main__":
    ejecutar_pruebas()
    print("Todas las pruebas finalizaron correctamente.")
