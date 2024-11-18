import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import requests
from streamlit_lottie import st_lottie
from streamlit_option_menu import option_menu
import hydralit_components as hc
from streamlit_card import card
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

# Menú principal mejorado
with st.sidebar:
    menu_principal = option_menu(
        "Menú Principal",
        ["Introducción", "Objetivos", "Metodología", "Herramientas", "Resultados", "Conclusiones"],
        icons=['house', 'target', 'gear', 'tools', 'graph-up', 'check-circle'],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "5!important", "background-color": "#262730"},
            "icon": {"color": "orange", "font-size": "25px"},
            "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px"},
            "nav-link-selected": {"background-color": "#0083B8"},
        }
    )

if menu_principal == "Introducción":
    st.title("Introducción")
    
    with st.container():
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
    
    with st.container():
        st.markdown('<div class="glass-container">', unsafe_allow_html=True)
        st.subheader("Datos de Jugadores")
        st.write("Tabla con imágenes de los jugadores y valores de mercado.")
        st.markdown(data_con_imagenes.to_html(escape=False), unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

elif menu_principal == "Metodología":
    st.title("Metodología")
    
    with st.container():
        st.markdown('<div class="glass-container">', unsafe_allow_html=True)
        visualizacion = st.selectbox(
            "Seleccione tipo de visualización:",
            ["Evolución Individual", "Comparación entre Jugadores", "Tendencias Generales"]
        )
        
        if visualizacion == "Evolución Individual":
            st.subheader("Evolución Individual del Valor de Mercado")
            nombre_jugador = st.selectbox("Selecciona un jugador:", data['Nombre'].unique())
            
            jugador = data[data['Nombre'] == nombre_jugador]
            if not jugador.empty:
                valor_inicial = jugador['Valor de Mercado en 01/01/2024'].iloc[0]
                valor_final = jugador['Valor de Mercado Actual'].iloc[0]
                
                meses, valores = generar_valores_mensuales(valor_inicial, valor_final)
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=meses,
                    y=valores,
                    mode='lines+markers',
                    name=nombre_jugador,
                    line=dict(width=3),
                    marker=dict(size=10)
                ))
                
                fig.update_layout(
                    title=f'Evolución Mensual del Valor de Mercado de {nombre_jugador}',
                    xaxis_title='Mes',
                    yaxis_title='Valor de Mercado (€)',
                    hovermode='x unified',
                    showlegend=True,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white')
                )
                st.plotly_chart(fig)
                
                df_mensual = pd.DataFrame({
                    'Mes': meses,
                    'Valor de Mercado (€)': [f"€{int(v):,}" for v in valores]
                })
                st.write("Valores mensuales:")
                st.dataframe(df_mensual)
        
        elif visualizacion == "Comparación entre Jugadores":
            st.subheader("Comparación entre Jugadores")
            col1, col2 = st.columns(2)
            with col1:
                jugador1 = st.selectbox("Primer jugador:", data['Nombre'].unique())
            with col2:
                jugador2 = st.selectbox("Segundo jugador:", data['Nombre'].unique())
            
            if jugador1 and jugador2:
                fig = go.Figure()
                
                for jugador in [jugador1, jugador2]:
                    datos_jugador = data[data['Nombre'] == jugador]
                    valor_inicial = datos_jugador['Valor de Mercado en 01/01/2024'].iloc[0]
                    valor_final = datos_jugador['Valor de Mercado Actual'].iloc[0]
                    meses, valores = generar_valores_mensuales(valor_inicial, valor_final)
                    
                    fig.add_trace(go.Scatter(
                        x=meses,
                        y=valores,
                        mode='lines+markers',
                        name=jugador,
                        line=dict(width=3),
                        marker=dict(size=10)
                    ))
                
                fig.update_layout(
                    title='Comparación de Valores de Mercado',
                    xaxis_title='Mes',
                    yaxis_title='Valor de Mercado (€)',
                    hovermode='x unified',
                    showlegend=True,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white')
                )
                st.plotly_chart(fig)

        st.markdown('</div>', unsafe_allow_html=True)
elif menu_principal == "Objetivos":
    st.title("Objetivos")

    with st.container():
        st.markdown("""
        <div class="glass-container">
            <h3>Objetivo General</h3>
            <p>Analizar los valores de mercado de los jugadores y su evolución en el tiempo, 
            para ofrecer insights relevantes para clubes, agentes y fanáticos del fútbol.</p>
            <h3>Objetivos Específicos</h3>
            <ul>
                <li>Visualizar la evolución del valor de mercado de jugadores individuales.</li>
                <li>Comparar el rendimiento económico entre diferentes jugadores.</li>
                <li>Identificar tendencias generales en los valores del mercado futbolístico.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

elif menu_principal == "Herramientas":
    st.title("Herramientas")

    with st.container():
        st.markdown("""
        <div class="glass-container">
            <h3>Herramientas Utilizadas</h3>
            <ul>
                <li><strong>Python</strong>: Lenguaje de programación principal.</li>
                <li><strong>Streamlit</strong>: Framework para la creación de aplicaciones web interactivas.</li>
                <li><strong>Pandas</strong>: Para la manipulación y análisis de datos.</li>
                <li><strong>Plotly</strong>: Para la visualización gráfica avanzada.</li>
                <li><strong>Requests</strong>: Para la obtención de datos externos.</li>
                <li><strong>Lottie Animations</strong>: Para mejorar la experiencia visual de la aplicación.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

elif menu_principal == "Resultados":
    st.title("Resultados")

    with st.container():
        st.markdown("""
        <div class="glass-container">
            <h3>Principales Hallazgos</h3>
            <p>El análisis de los valores de mercado ha permitido identificar fluctuaciones
            significativas en base al rendimiento de los jugadores y eventos globales que afectan la industria.</p>
            <ul>
                <li>Jugadores jóvenes tienden a incrementar su valor con mayor rapidez.</li>
                <li>El rendimiento en torneos importantes impacta directamente en el valor de mercado.</li>
                <li>Factores externos como lesiones o transferencias afectan considerablemente las evaluaciones.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

elif menu_principal == "Conclusiones":
    st.title("Conclusiones")

    with st.container():
        st.markdown("""
        <div class="glass-container">
            <h3>Resumen de Conclusiones</h3>
            <p>La evaluación del valor de mercado en el fútbol es una herramienta clave 
            para la toma de decisiones estratégicas en la industria deportiva.</p>
            <ul>
                <li>El análisis de datos históricos y actuales permite realizar proyecciones más precisas.</li>
                <li>Las visualizaciones interactivas facilitan la comunicación de insights.</li>
                <li>La tecnología es fundamental para optimizar el análisis de grandes volúmenes de datos.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("""
    <hr>
    <footer style="text-align: center; color: white;">
        <p>Desarrollado por el equipo de análisis ⚽ | 2024</p>
    </footer>
""", unsafe_allow_html=True)

