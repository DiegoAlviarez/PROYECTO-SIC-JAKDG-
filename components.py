import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from utils import format_large_number, generar_valores_mensuales

def crear_grafico_evolucion(nombre_jugador: str, valor_inicial: float, valor_final: float) -> go.Figure:
    """Crea un gráfico de evolución para un jugador."""
    meses, valores = generar_valores_mensuales(valor_inicial, valor_final)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=meses,
        y=valores,
        mode='lines+markers',
        name=nombre_jugador,
        line=dict(width=3, color='#FFA500'),
        marker=dict(size=10, symbol='diamond'),
        hovertemplate='%{y:,.0f}€<extra></extra>'
    ))
    
    fig.update_layout(
        title={
            'text': f'Evolución del Valor de Mercado: {nombre_jugador}',
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis_title='Mes',
        yaxis_title='Valor de Mercado (€)',
        hovermode='x unified',
        showlegend=True,
        template='plotly_dark',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

def mostrar_metricas_jugador(jugador_data):
    """Muestra métricas relevantes de un jugador."""
    cols = st.columns(3)
    
    with cols[0]:
        valor_inicial = jugador_data['Valor de Mercado en 01/01/2024'].iloc[0]
        st.metric(
            "Valor Inicial",
            format_large_number(valor_inicial),
            delta=None
        )
    
    with cols[1]:
        valor_actual = jugador_data['Valor de Mercado Actual'].iloc[0]
        cambio = valor_actual - valor_inicial
        st.metric(
            "Valor Actual",
            format_large_number(valor_actual),
            format_large_number(cambio)
        )
    
    with cols[2]:
        cambio_porcentual = ((valor_actual - valor_inicial) / valor_inicial) * 100
        st.metric(
            "Cambio Porcentual",
            f"{cambio_porcentual:.1f}%",
            None
        )

def crear_grafico_comparacion(data, jugadores):
    """Crea un gráfico de comparación entre jugadores."""
    fig = go.Figure()
    
    colors = ['#FFA500', '#4A90E2']
    for jugador, color in zip(jugadores, colors):
        datos_jugador = data[data['Nombre'] == jugador]
        valor_inicial = datos_jugador['Valor de Mercado en 01/01/2024'].iloc[0]
        valor_final = datos_jugador['Valor de Mercado Actual'].iloc[0]
        
        meses, valores = generar_valores_mensuales(valor_inicial, valor_final)
        
        fig.add_trace(go.Scatter(
            x=meses,
            y=valores,
            mode='lines+markers',
            name=jugador,
            line=dict(width=3, color=color),
            marker=dict(size=8),
            hovertemplate='%{y:,.0f}€<extra></extra>'
        ))
    
    fig.update_layout(
        title='Comparación de Evolución del Valor de Mercado',
        xaxis_title='Mes',
        yaxis_title='Valor de Mercado (€)',
        hovermode='x unified',
        showlegend=True,
        template='plotly_dark',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig