import requests
import pandas as pd
from datetime import datetime, timedelta

def load_lottieurl(url: str) -> dict:
    """Carga una animación Lottie desde una URL."""
    try:
        r = requests.get(url)
        return r.json() if r.status_code == 200 else None
    except:
        return None

def convertir_valor(valor: str) -> int:
    """Convierte valores de mercado de string a número."""
    if isinstance(valor, str):
        if "mil €" in valor:
            return int(float(valor.replace(" mil €", "").replace(",", ".")) * 1_000)
        elif "mill. €" in valor:
            return int(float(valor.replace(" mill. €", "").replace(",", ".")) * 1_000_000)
    return None

def generar_valores_mensuales(valor_inicial: float, valor_final: float) -> tuple:
    """Genera valores mensuales interpolados."""
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
    valores = [
        valor_inicial + (valor_final - valor_inicial) * (i / (num_meses - 1))
        for i in range(num_meses)
    ]
    
    return meses, valores

def format_large_number(number: float) -> str:
    """Formatea números grandes en formato legible."""
    if number >= 1_000_000:
        return f"€{number/1_000_000:.1f}M"
    elif number >= 1_000:
        return f"€{number/1_000:.1f}K"
    return f"€{number:.0f}"