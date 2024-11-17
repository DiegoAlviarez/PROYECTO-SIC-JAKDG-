import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import requests
from streamlit_lottie import st_lottie

# Configuración inicial de la página
st.set_page_config(
    page_title="Análisis Futbolístico",
    page_icon="⚽",
    layout="wide"
)

# Custom CSS para diseño y estilo
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
    }
    .stMetric {
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Función para cargar animaciones Lottie
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Cargar datos
@st.cache_data
def load_data():
    file_path = 'https://raw.githubusercontent.com/AndersonP444/PROYECTO-SIC-JAKDG/main/valores_mercado_actualizados%20(3).csv'
    return pd.read_csv(file_path)

# Función para convertir valores de mercado
def convertir_valor(valor):
    if isinstance(valor, str):
        if "mil €" in valor:
            return int(float(valor.replace(" mil €", "").replace(",", ".")) * 1_000)
        elif "mill. €" in valor:
            return int(float(valor.replace(" mill. €", "").replace(",", ".")) * 1_000_000)
    return None

# Función para convertir URLs a imágenes en cualquier columna
def convertir_urls_a_imagenes(df):
    df_copy = df.copy()
    for col in df_copy.columns:
        if df_copy[col].astype(str).str.startswith('http').any():
            df_copy[col] = df_copy[col].apply(lambda url: f'<img src="{url}" width="50">' if isinstance(url, str) and url.startswith('http') else url)
    return df_copy

# Cargar y preparar datos
data = load_data()
data["Valor de Mercado en 01/01/2024"] = data["Valor de Mercado en 01/01/2024"].apply(convertir_valor)
data["Valor de Mercado Actual"] = data["Valor de Mercado Actual"].apply(convertir_valor)
data_con_imagenes = convertir_urls_a_imagenes(data)

# Añadir animaciones Lottie
lottie_urls = {
    "introducción": "https://lottie.host/embed/3d48d4b9-51ad-4b7d-9d28-5e248cace11/Rz3QtSCq3.json",
    "metodología": "https://lottie.host/embed/91d83906-b6cd-4e23-8df3-8a9bc8f71fbb/x9JhDL5jsH.json",
    "objetivos": "https://lottie.host/embed/5e272377-38c8-49e8-b6e8-55c1b24d1472/WkTrfj8LQn.json",
    "resultados": "https://lottie.host/embed/a8b7ef7e-98a5-46c2-a774-82b4905f5987/xPS59skBVq.json",
    "conclusiones": "https://lottie.host/embed/b0121c87-8a0d-4c39-8053-322afeef3449/yN1pPQoORf.json"
}

# Sidebar con menú principal
st.sidebar.title("Menú Principal")
menu_principal = st.sidebar.radio(
    "Seleccione una sección:",
    ["Introducción", "Objetivos", "Metodología", "Resultados", "Conclusiones"]
)

# Contenido dinámico según el menú seleccionado
if menu_principal == "Introducción":
    st.title("Introducción")
    st.write("""
    La industria del fútbol ha evolucionado significativamente, convirtiéndose en un mercado 
    donde el valor de los jugadores es un indicador crucial de su desempeño y potencial.
    """)
    lottie_coding = load_lottieurl(lottie_urls["introducción"])
    if lottie_coding:
        st_lottie(lottie_coding, height=200, width=300)
    st.progress(100)

    with st.container():
        st.subheader("Datos de Jugadores")
        st.write("Tabla con imágenes de los jugadores y valores de mercado.")
        st.markdown(data_con_imagenes.to_html(escape=False), unsafe_allow_html=True)

elif menu_principal == "Objetivos":
    st.title("Objetivos del Proyecto")
    lottie_coding = load_lottieurl(lottie_urls["objetivos"])
    if lottie_coding:
        st_lottie(lottie_coding, height=200, width=300)
    st.info("Analizar y visualizar el valor de mercado de los jugadores en España.")

elif menu_principal == "Metodología":
    st.title("Metodología")
    lottie_coding = load_lottieurl(lottie_urls["metodología"])
    if lottie_coding:
        st_lottie(lottie_coding, height=200, width=300)
    st.success("Metodología cargada exitosamente.")

    visualizacion = st.selectbox(
        "Seleccione tipo de visualización:",
        ["Evolución Individual", "Comparación entre Jugadores", "Tendencias Generales"]
    )
    if visualizacion == "Evolución Individual":
        st.subheader("Evolución Individual del Valor de Mercado")
        nombre_jugador = st.selectbox("Selecciona un jugador:", data['Nombre'].unique())
        # Similar lógica a la del código base para visualización
        # ...

elif menu_principal == "Resultados":
    st.title("Resultados")
    lottie_coding = load_lottieurl(lottie_urls["resultados"])
    if lottie_coding:
        st_lottie(lottie_coding, height=200, width=300)
    st.success("Los resultados se presentan a continuación.")
    # Aquí podrías añadir gráficos específicos o métricas clave.

elif menu_principal == "Conclusiones":
    st.title("Conclusiones")
    lottie_coding = load_lottieurl(lottie_urls["conclusiones"])
    if lottie_coding:
        st_lottie(lottie_coding, height=200, width=300)
    st.info("""
    Este proyecto ha permitido identificar las tendencias principales en el valor de mercado
    de los jugadores, mostrando una correlación significativa con diversas estadísticas.
    """)

# Footer
st.sidebar.markdown("---")
st.sidebar.info("ANÁLISIS DE LAS ESTADÍSTICAS QUE TIENEN MAYOR CORRELACIÓN CON EL VALOR DE MERCADO DE LOS JUGADORES DE FUTBOL EN ESPAÑA")

