import sqlite3
from datetime import date, datetime

import streamlit as st

from database.albumes_db import (
    actualizar_album,
    agregar_album,
    eliminar_album,
    obtener_album,
    obtener_albumes,
)
from database.artistas_db import (
    actualizar_artista,
    agregar_artista,
    eliminar_artista,
    obtener_artistas,
    valores_filtro_artistas,
)
from database.conciertos_db import (
    actualizar_concierto,
    agregar_concierto,
    eliminar_concierto,
    obtener_ciudades,
    obtener_concierto,
    obtener_conciertos,
)
from database.conexion import inicializar_base_de_datos
from models.album import Album
from models.artista import Artista
from models.concierto import Concierto


st.set_page_config(page_title="Live Music Pro", page_icon="🎵", layout="wide")
inicializar_base_de_datos()


def artistas_objeto(genero="", pais=""):
    objetos = []
    for fila in obtener_artistas(genero, pais):
        objetos.append(Artista.desde_fila(fila))
    return objetos


def albumes_objeto(genero=""):
    objetos = []
    for fila in obtener_albumes(genero=genero):
        objetos.append(Album.desde_fila(fila))
    return objetos


def conciertos_objeto(ciudad=""):
    objetos = []
    for fila in obtener_conciertos(ciudad=ciudad):
        objetos.append(Concierto.desde_fila(fila))
    return objetos


def mostrar_tabla(objetos, mensaje_vacio):
    datos = [objeto.a_diccionario() for objeto in objetos]
    if datos:
        st.dataframe(datos, width="stretch", hide_index=True)
    else:
        st.info(mensaje_vacio)


def seleccionar_artista(etiqueta, clave, seleccionado=None):
    artistas = artistas_objeto()
    ids = [artista.id for artista in artistas]
    indice = ids.index(seleccionado) if seleccionado in ids else 0
    return st.selectbox(
        etiqueta,
        ids,
        index=indice,
        format_func=lambda valor: next(
            f"#{artista.id} - {artista.nombre}"
            for artista in artistas
            if artista.id == valor
        ),
        key=clave,
    )


def pagina_inicio():
    st.title("🎵 Live Music Pro")
    st.subheader("Sistema centralizado de gestión para ORT Sounds")

    artistas = artistas_objeto()
    albumes = albumes_objeto()
    conciertos = conciertos_objeto()
    columnas = st.columns(3)
    columnas[0].metric("Artistas", len(artistas))
    columnas[1].metric("Álbumes", len(albumes))
    columnas[2].metric("Conciertos", len(conciertos))

    st.write(
        "Usá el menú lateral para consultar, filtrar, agregar, modificar o "
        "eliminar artistas, álbumes y conciertos."
    )
    st.subheader("Próximos conciertos")
    proximos = [concierto for concierto in conciertos if concierto.esta_programado()]
    mostrar_tabla(proximos, "No hay conciertos próximos cargados.")


def pagina_artistas():
    st.title("Gestión de artistas")
    listar, agregar, modificar, borrar = st.tabs(
        ["Listar y filtrar", "Agregar", "Modificar", "Eliminar"]
    )

    with listar:
        columna_genero, columna_pais = st.columns(2)
        generos = [""] + valores_filtro_artistas("genero")
        paises = [""] + valores_filtro_artistas("pais")
        genero = columna_genero.selectbox(
            "Filtrar por género", generos, format_func=lambda valor: valor or "Todos"
        )
        pais = columna_pais.selectbox(
            "Filtrar por país", paises, format_func=lambda valor: valor or "Todos"
        )
        mostrar_tabla(
            artistas_objeto(genero, pais), "No hay artistas para esos filtros."
        )

    with agregar:
        with st.form("alta_artista", clear_on_submit=True):
            nombre = st.text_input("Nombre")
            genero = st.text_input("Género")
            pais = st.text_input("País")
            if st.form_submit_button("Guardar artista", type="primary"):
                try:
                    identificador = agregar_artista(nombre, genero, pais)
                    st.success(f"Artista creado con ID {identificador}.")
                except ValueError as error:
                    st.error(str(error))

    with modificar:
        artistas = artistas_objeto()
        if artistas:
            id_artista = st.selectbox(
                "Artista a modificar",
                [artista.id for artista in artistas],
                format_func=lambda valor: next(
                    artista.mostrar_ficha()
                    for artista in artistas
                    if artista.id == valor
                ),
            )
            actual = next(a for a in artistas if a.id == id_artista)
            with st.form("modificar_artista"):
                nombre = st.text_input("Nombre", actual.nombre)
                genero = st.text_input("Género", actual.genero)
                pais = st.text_input("País", actual.pais)
                if st.form_submit_button("Guardar cambios", type="primary"):
                    try:
                        actualizar_artista(id_artista, nombre, genero, pais)
                        st.success("Artista actualizado correctamente.")
                    except ValueError as error:
                        st.error(str(error))
        else:
            st.info("No hay artistas para modificar.")

    with borrar:
        artistas = artistas_objeto()
        if artistas:
            id_artista = st.selectbox(
                "Artista a eliminar",
                [artista.id for artista in artistas],
                key="eliminar_artista",
                format_func=lambda valor: next(
                    artista.mostrar_ficha()
                    for artista in artistas
                    if artista.id == valor
                ),
            )
            st.warning(
                "No se puede eliminar un artista que tenga álbumes o conciertos asociados."
            )
            confirmar = st.checkbox("Confirmo que deseo eliminar al artista")
            if st.button("Eliminar artista", disabled=not confirmar):
                try:
                    eliminar_artista(id_artista)
                    st.success("Artista eliminado.")
                    st.rerun()
                except sqlite3.IntegrityError:
                    st.error(
                        "El artista tiene registros asociados. Eliminá primero sus "
                        "álbumes y conciertos."
                    )
        else:
            st.info("No hay artistas para eliminar.")


def pagina_albumes():
    st.title("Gestión de álbumes")
    listar, agregar, modificar, borrar = st.tabs(
        ["Listar y filtrar", "Agregar", "Modificar", "Eliminar"]
    )

    with listar:
        generos = [""] + valores_filtro_artistas("genero")
        genero = st.selectbox(
            "Filtrar por género del artista",
            generos,
            format_func=lambda valor: valor or "Todos",
        )
        mostrar_tabla(albumes_objeto(genero), "No hay álbumes para ese filtro.")

    with agregar:
        if artistas_objeto():
            with st.form("alta_album", clear_on_submit=True):
                titulo = st.text_input("Título")
                anio = st.number_input(
                    "Año de lanzamiento",
                    min_value=1,
                    max_value=date.today().year + 1,
                    value=date.today().year,
                )
                id_artista = seleccionar_artista("Artista", "artista_alta_album")
                if st.form_submit_button("Guardar álbum", type="primary"):
                    try:
                        identificador = agregar_album(titulo, anio, id_artista)
                        st.success(f"Álbum creado con ID {identificador}.")
                    except (ValueError, sqlite3.IntegrityError) as error:
                        st.error(str(error))
        else:
            st.info("Primero cargá un artista.")

    with modificar:
        albumes = albumes_objeto()
        if albumes:
            id_album = st.selectbox(
                "Álbum a modificar",
                [album.id for album in albumes],
                format_func=lambda valor: next(
                    album.mostrar_info() for album in albumes if album.id == valor
                ),
            )
            actual = obtener_album(id_album)
            with st.form("modificar_album"):
                titulo = st.text_input("Título", actual["titulo"])
                anio = st.number_input(
                    "Año",
                    min_value=1,
                    max_value=date.today().year + 1,
                    value=actual["anio_lanzamiento"],
                )
                id_artista = seleccionar_artista(
                    "Artista", "artista_modificar_album", actual["id_artista"]
                )
                if st.form_submit_button("Guardar cambios", type="primary"):
                    try:
                        actualizar_album(id_album, titulo, anio, id_artista)
                        st.success("Álbum actualizado correctamente.")
                    except (ValueError, sqlite3.IntegrityError) as error:
                        st.error(str(error))
        else:
            st.info("No hay álbumes para modificar.")

    with borrar:
        albumes = albumes_objeto()
        if albumes:
            id_album = st.selectbox(
                "Álbum a eliminar",
                [album.id for album in albumes],
                key="eliminar_album",
                format_func=lambda valor: next(
                    album.mostrar_info() for album in albumes if album.id == valor
                ),
            )
            confirmar = st.checkbox("Confirmo que deseo eliminar el álbum")
            if st.button("Eliminar álbum", disabled=not confirmar):
                eliminar_album(id_album)
                st.success("Álbum eliminado.")
                st.rerun()
        else:
            st.info("No hay álbumes para eliminar.")


def pagina_conciertos():
    st.title("Agenda de conciertos")
    listar, agregar, modificar, borrar = st.tabs(
        ["Listar y filtrar", "Agregar", "Modificar", "Eliminar"]
    )

    with listar:
        ciudades = [""] + obtener_ciudades()
        ciudad = st.selectbox(
            "Filtrar por ciudad",
            ciudades,
            format_func=lambda valor: valor or "Todas",
        )
        mostrar_tabla(
            conciertos_objeto(ciudad), "No hay conciertos para ese filtro."
        )

    with agregar:
        if artistas_objeto():
            with st.form("alta_concierto", clear_on_submit=True):
                nombre = st.text_input("Nombre del evento")
                fecha = st.date_input("Fecha", value=date.today())
                ciudad = st.text_input("Ciudad")
                id_artista = seleccionar_artista(
                    "Artista", "artista_alta_concierto"
                )
                if st.form_submit_button("Guardar concierto", type="primary"):
                    try:
                        identificador = agregar_concierto(
                            nombre, fecha, ciudad, id_artista
                        )
                        st.success(f"Concierto creado con ID {identificador}.")
                    except (ValueError, sqlite3.IntegrityError) as error:
                        st.error(str(error))
        else:
            st.info("Primero cargá un artista.")

    with modificar:
        conciertos = conciertos_objeto()
        if conciertos:
            id_concierto = st.selectbox(
                "Concierto a modificar",
                [concierto.id for concierto in conciertos],
                format_func=lambda valor: next(
                    concierto.mostrar_evento()
                    for concierto in conciertos
                    if concierto.id == valor
                ),
            )
            actual = obtener_concierto(id_concierto)
            fecha_actual = datetime.strptime(actual["fecha"], "%Y-%m-%d").date()
            with st.form("modificar_concierto"):
                nombre = st.text_input("Nombre del evento", actual["nombre_evento"])
                fecha = st.date_input("Fecha", value=fecha_actual)
                ciudad = st.text_input("Ciudad", actual["ciudad"])
                id_artista = seleccionar_artista(
                    "Artista",
                    "artista_modificar_concierto",
                    actual["id_artista"],
                )
                if st.form_submit_button("Guardar cambios", type="primary"):
                    try:
                        actualizar_concierto(
                            id_concierto, nombre, fecha, ciudad, id_artista
                        )
                        st.success("Concierto actualizado correctamente.")
                    except (ValueError, sqlite3.IntegrityError) as error:
                        st.error(str(error))
        else:
            st.info("No hay conciertos para modificar.")

    with borrar:
        conciertos = conciertos_objeto()
        if conciertos:
            id_concierto = st.selectbox(
                "Concierto a eliminar",
                [concierto.id for concierto in conciertos],
                key="eliminar_concierto",
                format_func=lambda valor: next(
                    concierto.mostrar_evento()
                    for concierto in conciertos
                    if concierto.id == valor
                ),
            )
            confirmar = st.checkbox("Confirmo que deseo eliminar el concierto")
            if st.button("Eliminar concierto", disabled=not confirmar):
                eliminar_concierto(id_concierto)
                st.success("Concierto eliminado.")
                st.rerun()
        else:
            st.info("No hay conciertos para eliminar.")


pagina = st.sidebar.radio(
    "Navegación", ["Inicio", "Artistas", "Álbumes", "Conciertos"]
)
if pagina == "Inicio":
    pagina_inicio()
elif pagina == "Artistas":
    pagina_artistas()
elif pagina == "Álbumes":
    pagina_albumes()
else:
    pagina_conciertos()
