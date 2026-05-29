import streamlit as st
import pandas as pd

from database.artistas_db import *
from database.albumes_db import *
from database.conciertos_db import *

from database.conexion import crear_tablas

crear_tablas()

st.title("🎵 Live Music Pro")

menu = st.sidebar.selectbox(
    "Navegación",
    ["Inicio", "Artistas", "Álbumes", "Conciertos"]
)


if menu == "Inicio":

    st.header("Dashboard")

    total_artistas = len(obtener_artistas())
    total_albumes = len(obtener_albumes())
    total_conciertos = len(obtener_conciertos())

    col1, col2, col3 = st.columns(3)

    col1.metric("Artistas", total_artistas)
    col2.metric("Álbumes", total_albumes)
    col3.metric("Conciertos", total_conciertos)


elif menu == "Artistas":

    st.header("Gestión de Artistas")

    artistas = obtener_artistas()

    df = pd.DataFrame(
        artistas,
        columns=["ID", "Nombre", "Género", "País"]
    )

    st.dataframe(df)

    st.subheader("Agregar artista")

    nombre = st.text_input("Nombre")
    genero = st.text_input("Género")
    pais = st.text_input("País")

    if st.button("Guardar artista"):

        if nombre != "" and genero != "" and pais != "":

            agregar_artista(nombre, genero, pais)

            st.success("Artista agregado")

        else:
            st.error("Completar todos los campos")


elif menu == "Álbumes":

    st.header("Gestión de Álbumes")

    albumes = obtener_albumes()

    df = pd.DataFrame(
        albumes,
        columns=["ID", "Título", "Año", "Artista"]
    )

    st.dataframe(df)

    st.subheader("Agregar álbum")

    titulo = st.text_input("Título")

    anio = st.number_input(
        "Año",
        min_value=1900,
        max_value=2100,
        step=1
    )

    artistas = obtener_artistas()

    lista_artistas = {
        artista[1]: artista[0]
        for artista in artistas
    }

    artista_nombre = st.selectbox(
        "Artista",
        list(lista_artistas.keys())
    )

    if st.button("Guardar álbum"):

        id_artista = lista_artistas[artista_nombre]

        agregar_album(titulo, anio, id_artista)

        st.success("Álbum agregado")

elif menu == "Conciertos":

    st.header("Agenda de Conciertos")

    conciertos = obtener_conciertos()

    df = pd.DataFrame(
        conciertos,
        columns=["ID", "Evento", "Fecha", "Ciudad", "Artista"]
    )

    st.dataframe(df)

    st.subheader("Agregar concierto")

    nombre = st.text_input("Nombre del evento")

    fecha = st.date_input("Fecha")

    ciudad = st.text_input("Ciudad")

    artistas = obtener_artistas()

    lista_artistas = {
        artista[1]: artista[0]
        for artista in artistas
    }

    artista_nombre = st.selectbox(
        "Artista",
        list(lista_artistas.keys())
    )

    if st.button("Guardar concierto"):

        id_artista = lista_artistas[artista_nombre]

        agregar_concierto(
            nombre,
            str(fecha),
            ciudad,
            id_artista
        )

        st.success("Concierto agregado")