import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import requests
from streamlit_lottie import st_lottie
from streamlit_option_menu import option_menu
import json
from utils import load_lottieurl, convertir_valor
from components import (
    crear_grafico_evolucion,
    mostrar_metricas_jugador,
    crear_grafico_comparacion
)

# Configuración de la página
st.set_page_config(
    page_title="Análisis Futbolístico",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Función para convertir URLs en etiquetas HTML de imágenes
def convertir_urls_a_imagenes(df, columna_url, columna_nombre):
    df[columna_nombre] = df[columna_url].apply(
        lambda x: f'<img src="{x}" style="height:50px;"/>'
    )
    return df

# Cargar datos
@st.cache_data
def load_data():
    file_path = 'https://raw.githubusercontent.com/AndersonP444/PROYECTO-SIC-JAKDG/main/valores_mercado_actualizados%20(3).csv'
    df = pd.read_csv(file_path)
    df["Valor de Mercado en 01/01/2024"] = df["Valor de Mercado en 01/01/2024"].apply(convertir_valor)
    df["Valor de Mercado Actual"] = df["Valor de Mercado Actual"].apply(convertir_valor)
    df = convertir_urls_a_imagenes(df, "Jugador", "Imagen")
    return df

# Cargar datos
data = load_data()

# Menú principal usando option_menu
with st.sidebar:
    st.title("⚽ Análisis Futbolístico")
    menu_principal = option_menu(
        "Menú Principal",
        ["Dashboard", "Análisis Individual", "Comparativa", "Datos"],
        icons=['house', 'graph-up', 'arrow-left-right', 'table'],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "5!important", "background-color": "#1e3c72"},
            "icon": {"color": "orange", "font-size": "25px"}, 
            "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#4A4A4A"},
            "nav-link-selected": {"background-color": "#2a5298"},
        }
    )

# Contenido principal
if menu_principal == "Dashboard":
    st.title("Dashboard Futbolístico Interactivo")
    st.dataframe(
        data[["Imagen", "Nombre", "Valor de Mercado Actual"]],
        hide_index=True,
        use_container_width=True,
    )

elif menu_principal == "Análisis Individual":
    st.title("Análisis Individual de Jugadores")
    nombre_jugador = st.selectbox(
        "Selecciona un jugador:",
        data['Nombre'].unique(),
        index=0
    )
    jugador_data = data[data['Nombre'] == nombre_jugador]
    st.markdown(jugador_data[["Imagen", "Nombre"]].to_html(escape=False), unsafe_allow_html=True)

elif menu_principal == "Comparativa":
    st.title("Comparativa entre Jugadores")
    jugador1 = st.selectbox("Primer jugador:", data['Nombre'].unique(), index=0)
    jugador2 = st.selectbox("Segundo jugador:", data['Nombre'].unique(), index=1)
    comp_data = data[data['Nombre'].isin([jugador1, jugador2])]
    st.markdown(comp_data[["Imagen", "Nombre", "Valor de Mercado Actual"]].to_html(escape=False), unsafe_allow_html=True)

else:  # Datos
    st.title("Datos Completos")
    st.markdown(data[["Imagen", "Nombre", "Valor de Mercado Actual"]].to_html(escape=False), unsafe_allow_html=True)

# Footer
st.sidebar.markdown("---")
st.sidebar.info(
    "ANÁLISIS DE LAS ESTADÍSTICAS QUE TIENEN MAYOR CORRELACIÓN CON EL "
    "VALOR DE MERCADO DE LOS JUGADORES DE FUTBOL EN ESPAÑA"
)

