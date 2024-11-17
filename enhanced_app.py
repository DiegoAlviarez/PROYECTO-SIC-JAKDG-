
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

# Custom CSS
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

# Cargar datos
@st.cache_data
def load_data():
    file_path = 'https://raw.githubusercontent.com/AndersonP444/PROYECTO-SIC-JAKDG/main/valores_mercado_actualizados%20(3).csv'
    df = pd.read_csv(file_path)
    df["Valor de Mercado en 01/01/2024"] = df["Valor de Mercado en 01/01/2024"].apply(convertir_valor)
    df["Valor de Mercado Actual"] = df["Valor de Mercado Actual"].apply(convertir_valor)
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
    
    # Animación Lottie
    lottie_url = "https://lottie.host/3d48d4b9-51ad-4b7d-9d28-5e248cace11/Rz3QtSCq3.json"
    lottie_coding = load_lottieurl(lottie_url)
    if lottie_coding:
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            st_lottie(lottie_coding, height=200)
    
    # Estadísticas generales con efectos visuales mejorados
    st.subheader("📈 Estadísticas Generales")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        valor_total_inicial = data["Valor de Mercado en 01/01/2024"].sum()
        st.metric("Valor Total Inicial", f"€{valor_total_inicial:,.0f}")
    
    with col2:
        valor_total_actual = data["Valor de Mercado Actual"].sum()
        cambio_total = valor_total_actual - valor_total_inicial
        st.metric("Valor Total Actual", f"€{valor_total_actual:,.0f}", 
                 delta=f"€{cambio_total:,.0f}")
    
    with col3:
        cambio_porcentual = ((valor_total_actual - valor_total_inicial) / valor_total_inicial) * 100
        st.metric("Cambio Porcentual", f"{cambio_porcentual:.1f}%")

    # Top 5 jugadores por valor actual
    st.subheader("🏆 Top 5 Jugadores por Valor Actual")
    top_5 = data.nlargest(5, "Valor de Mercado Actual")
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=top_5["Nombre"],
        y=top_5["Valor de Mercado Actual"],
        marker_color='#FFA500',
        text=[f"€{x:,.0f}" for x in top_5["Valor de Mercado Actual"]],
        textposition='auto',
    ))
    fig.update_layout(
        template='plotly_dark',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        yaxis_title="Valor de Mercado (€)",
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)

elif menu_principal == "Análisis Individual":
    st.title("Análisis Individual de Jugadores")
    
    # Selector de jugador con búsqueda y filtro
    nombre_jugador = st.selectbox(
        "Selecciona un jugador:",
        data['Nombre'].unique(),
        index=0
    )
    
    if nombre_jugador:
        jugador_data = data[data['Nombre'] == nombre_jugador]
        
        # Mostrar métricas del jugador
        mostrar_metricas_jugador(jugador_data)
        
        # Gráfico de evolución
        fig = crear_grafico_evolucion(
            nombre_jugador,
            jugador_data['Valor de Mercado en 01/01/2024'].iloc[0],
            jugador_data['Valor de Mercado Actual'].iloc[0]
        )
        st.plotly_chart(fig, use_container_width=True)

elif menu_principal == "Comparativa":
    st.title("Comparativa entre Jugadores")
    
    col1, col2 = st.columns(2)
    with col1:
        jugador1 = st.selectbox("Primer jugador:", data['Nombre'].unique(), index=0)
    with col2:
        jugador2 = st.selectbox("Segundo jugador:", 
                               data[data['Nombre'] != jugador1]['Nombre'].unique(),
                               index=0)
    
    if jugador1 and jugador2:
        fig = crear_grafico_comparacion(data, [jugador1, jugador2])
        st.plotly_chart(fig, use_container_width=True)
        
        # Tabla comparativa
        st.subheader("Comparación Detallada")
        comp_data = data[data['Nombre'].isin([jugador1, jugador2])]
        st.dataframe(
            comp_data,
            column_config={
                "Valor de Mercado en 01/01/2024": st.column_config.NumberColumn(
                    "Valor Inicial",
                    format="€%.0f"
                ),
                "Valor de Mercado Actual": st.column_config.NumberColumn(
                    "Valor Actual",
                    format="€%.0f"
                )
            },
            hide_index=True
        )

else:  # Datos
    st.title("Datos Completos")
    
    # Filtros mejorados
    col1, col2 = st.columns(2)
    with col1:
        min_valor = st.number_input(
            "Valor mínimo (€)",
            min_value=0,
            max_value=int(data["Valor de Mercado Actual"].max()),
            value=0
        )
    with col2:
        max_valor = st.number_input(
            "Valor máximo (€)",
            min_value=0,
            max_value=int(data["Valor de Mercado Actual"].max()),
            value=int(data["Valor de Mercado Actual"].max())
        )
    
    # Búsqueda por nombre
    search = st.text_input("🔍 Buscar por nombre:", "")
    
    # Filtrar datos
    filtered_data = data[
        (data["Valor de Mercado Actual"] >= min_valor) &
        (data["Valor de Mercado Actual"] <= max_valor) &
        (data["Nombre"].str.contains(search, case=False))
    ]
    
    # Mostrar datos filtrados
    st.dataframe(
        filtered_data,
        column_config={
            "Valor de Mercado en 01/01/2024": st.column_config.NumberColumn(
                "Valor Inicial",
                format="€%.0f"
            ),
            "Valor de Mercado Actual": st.column_config.NumberColumn(
                "Valor Actual",
                format="€%.0f"
            )
        },
        hide_index=True
    )

# Footer
st.sidebar.markdown("---")
st.sidebar.info(
    "ANÁLISIS DE LAS ESTADÍSTICAS QUE TIENEN MAYOR CORRELACIÓN CON EL "
    "VALOR DE MERCADO DE LOS JUGADORES DE FUTBOL EN ESPAÑA"
)

# Función para añadir estilo personalizado
def agregar_estilo_css():
    css = """
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background-color: #f4f4f4;
        }
        h1, h2, h3, h4, h5 {
            color: #333;
        }
        .stButton button {
            background-color: #007bff;
            color: white;
            border-radius: 5px;
        }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# Llamar a la función de estilo
agregar_estilo_css()

# Animaciones adicionales
st.markdown("## 🎉 Efectos Visuales")
lottie_url_loader = "https://assets2.lottiefiles.com/packages/lf20_kkflmtur.json"
lottie_animation = load_lottieurl(lottie_url_loader)
if lottie_animation:
    st_lottie(lottie_animation, height=300, width=500, key="animation1")

# Barra de progreso dinámica
if st.button("Cargar progreso"):
    with st.spinner("Cargando datos..."):
        for i in range(101):
            st.progress(i)
    st.success("¡Datos cargados con éxito!")

# Notificaciones dinámicas
st.sidebar.markdown("## 🚨 Notificaciones")
st.sidebar.success("¡Nueva actualización de datos disponible!")

