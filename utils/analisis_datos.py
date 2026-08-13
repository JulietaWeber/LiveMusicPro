from contextlib import closing
from pathlib import Path

import pandas as pd

from database.albumes_db import agregar_album, obtener_albumes
from database.conexion import conectar


RUTA_DATASET_ALBUMES = (
    Path(__file__).resolve().parent.parent / "data" / "albumes.csv"
)
COLUMNAS_DATASET_ALBUMES = {"titulo", "anio_lanzamiento", "id_artista"}


def leer_dataset_albumes(ruta_csv=RUTA_DATASET_ALBUMES):
    """Lee y valida el CSV propio de álbumes con Pandas."""
    datos = pd.read_csv(ruta_csv)
    columnas_faltantes = COLUMNAS_DATASET_ALBUMES - set(datos.columns)
    if columnas_faltantes:
        faltantes = ", ".join(sorted(columnas_faltantes))
        raise ValueError(f"Faltan columnas obligatorias en el CSV: {faltantes}.")
    if datos.empty:
        raise ValueError("El CSV no contiene álbumes para importar.")
    return datos


def importar_albumes_desde_csv(ruta_csv=RUTA_DATASET_ALBUMES):
    """Importa cada fila mediante el alta existente y evita duplicados exactos."""
    datos = leer_dataset_albumes(ruta_csv)
    existentes = {
        (
            fila["titulo"].strip().casefold(),
            int(fila["anio_lanzamiento"]),
            int(fila["id_artista"]),
        )
        for fila in obtener_albumes()
    }
    importados = 0
    omitidos = 0

    for _, fila in datos.iterrows():
        clave = (
            str(fila["titulo"]).strip().casefold(),
            int(fila["anio_lanzamiento"]),
            int(fila["id_artista"]),
        )
        if clave in existentes:
            omitidos += 1
            continue

        agregar_album(
            fila["titulo"],
            fila["anio_lanzamiento"],
            fila["id_artista"],
        )
        existentes.add(clave)
        importados += 1

    return {"importados": importados, "omitidos": omitidos, "total": len(datos)}


def leer_albumes_desde_base():
    """Obtiene con Pandas los álbumes ya cargados en SQLite."""
    consulta = """
        SELECT al.id, al.titulo, al.anio_lanzamiento,
               ar.nombre AS artista
        FROM albumes al
        INNER JOIN artistas ar ON ar.id = al.id_artista
        ORDER BY al.anio_lanzamiento, al.titulo
    """
    with closing(conectar()) as conexion:
        return pd.read_sql_query(consulta, conexion)


def calcular_tendencia_central(datos, columna="anio_lanzamiento"):
    """Calcula media, mediana y moda de una columna numérica con Pandas."""
    if columna not in datos.columns:
        raise ValueError(f"La columna '{columna}' no existe en los datos.")

    valores = pd.to_numeric(datos[columna], errors="coerce").dropna()
    if valores.empty:
        raise ValueError("No hay valores numéricos para analizar.")

    frecuencias = valores.value_counts()
    modas = [int(valor) for valor in valores.mode().tolist()]
    hay_moda_clara = int(frecuencias.iloc[0]) > 1 and len(modas) == 1

    return {
        "media": float(valores.mean()),
        "mediana": float(valores.median()),
        "modas": modas,
        "frecuencia_moda": int(frecuencias.iloc[0]),
        "hay_moda_clara": hay_moda_clara,
        "cantidad": int(valores.count()),
    }


def interpretar_tendencia_central(resultados):
    diferencia = abs(resultados["media"] - resultados["mediana"])
    if diferencia <= 1:
        comparacion = (
            "La media y la mediana son parecidas, por lo que los años de "
            "lanzamiento están bastante equilibrados y no hay valores extremos "
            "que desplacen mucho el promedio."
        )
    else:
        comparacion = (
            "La media y la mediana son diferentes. Esto indica que algunos años "
            "alejados del centro están desplazando el promedio."
        )

    if resultados["hay_moda_clara"]:
        moda = resultados["modas"][0]
        explicacion_moda = (
            f"La moda es {moda}: aparece {resultados['frecuencia_moda']} veces, "
            "así que es el año de lanzamiento más frecuente."
        )
    else:
        explicacion_moda = (
            "No hay una única moda clara; los años más frecuentes están "
            "repartidos o aparecen una sola vez."
        )

    return f"{comparacion} {explicacion_moda}"
