import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import requests
from streamlit_lottie import st_lottie
from streamlit_option_menu import option_menu
from streamlit_extras.metric_cards import style_metric_cards

# Configuración inicial de la página
st.set_page_config(
    page_title="Análisis Futbolístico",
    page_icon="⚽",
    layout="wide"
)

# Custom CSS para mejorar la apariencia
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(to right, #1a1a1a, #2d2d2d);
        color: white;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 20px;
        padding: 10px 24px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
    }
    .metric-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 10px;
        padding: 20px;
        margin: 10px;
    }
    .glass-container {
        background: rgba(255,255,255,0.1);
        backdrop-filter: blur(10px);
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Función para cargar animaciones Lottie
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Función para cargar datos
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

# Función para convertir URLs a imágenes
def convertir_urls_a_imagenes(df):
    df_copy = df.copy()
    for col in df_copy.columns:
        if df_copy[col].astype(str).str.startswith('http').any():
            df_copy[col] = df_copy[col].apply(lambda url: f'<img src="{url}" width="50">' if isinstance(url, str) and url.startswith('http') else url)
    return df_copy

# Función para generar valores mensuales interpolados
def generar_valores_mensuales(valor_inicial, valor_final):
    fecha_inicio = datetime(2024, 1, 1)
    fecha_actual = datetime.now()
    meses = []
    valores = []
    
    fecha_actual = fecha_actual.replace(day=1)
    fecha = fecha_inicio
    while fecha <= fecha_actual:
        meses.append(fecha.strftime('%B %Y'))
        fecha += timedelta(days=32)
        fecha = fecha.replace(day=1)
    
    num_meses = len(meses)
    for i in range(num_meses):
        valor = valor_inicial + (valor_final - valor_inicial) * (i / (num_meses - 1))
        valores.append(valor)
    
    return meses, valores

# Cargar datos
data = load_data()
data["Valor de Mercado en 01/01/2024"] = data["Valor de Mercado en 01/01/2024"].apply(convertir_valor)
data["Valor de Mercado Actual"] = data["Valor de Mercado Actual"].apply(convertir_valor)

# Menú principal usando st.sidebar.radio
menu_principal = st.sidebar.radio(
    "Menú Principal",
    ["Introducción", "Objetivos", "Metodología", "Herramientas", "Resultados", "Conclusiones"]
)

if menu_principal == "Introducción":
    st.title("Introducción")
    
    st.markdown("""
        <div class="glass-container">
            <h3>La industria del fútbol ha evolucionado significativamente</h3>
            <p>Convirtiéndose en un mercado donde el valor de los jugadores es un indicador 
            crucial de su desempeño y potencial.</p>
        </div>
    """, unsafe_allow_html=True)
    
    lottie_url = "https://lottie.host/embed/3d48d4b9-51ad-4b7d-9d28-5e248cace11/Rz3QtSCq3.json"
    lottie_coding = load_lottieurl(lottie_url)
    if lottie_coding:
        st_lottie(lottie_coding, height=200, width=300)
    
    data_formateada = data.copy()
    data_formateada["Valor de Mercado en 01/01/2024"] = data_formateada["Valor de Mercado en 01/01/2024"].apply(lambda x: f"€{int(x):,}" if pd.notnull(x) else "N/A")
    data_formateada["Valor de Mercado Actual"] = data_formateada["Valor de Mercado Actual"].apply(lambda x: f"€{int(x):,}" if pd.notnull(x) else "N/A")

    data_con_imagenes = convertir_urls_a_imagenes(data_formateada)
    
    st.subheader("Datos de Jugadores")
    st.write("Tabla con imágenes de los jugadores y valores de mercado:")
    st.markdown(data_con_imagenes.to_html(escape=False), unsafe_allow_html=True)

elif menu_principal == "Objetivos":
    st.title("Objetivos del Proyecto")
    st.markdown("""
        <div class="glass-container">
            <h3>Objetivos Principales:</h3>
            <ul>
                <li>Analizar y visualizar el valor de mercado de los jugadores</li>
                <li>Evaluar el incremento porcentual del valor de mercado a lo largo del tiempo</li>
                <li>Identificar patrones y tendencias en la valoración de jugadores</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

elif menu_principal == "Metodología":
    # Aquí sigue la lógica para la sección de "Metodología" que ya tenías.
    pass

elif menu_principal == "Herramientas":
    # Aquí sigue la lógica para la sección de "Herramientas" que ya tenías.
    pass

elif menu_principal == "Resultados":
    # Aquí sigue la lógica para la sección de "Resultados" que ya tenías.
    pass

elif menu_principal == "Conclusiones":
    # Aquí sigue la lógica para la sección de "Conclusiones" que ya tenías.
    pass

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("""
    <div class="glass-container">
        <small>ANÁLISIS DE LAS ESTADÍSTICAS QUE TIENEN MAYOR CORRELACIÓN 
        CON EL VALOR DE MERCADO DE LOS JUGADORES DE FUTBOL EN ESPAÑA</small>
    </div>
""", unsafe_allow_html=True)

