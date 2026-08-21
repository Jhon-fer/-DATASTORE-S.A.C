# utils/data_loader.py
import pandas as pd
import streamlit as st

@st.cache_data
def load_data_from_file(file):
    """Carga datos desde un archivo subido por el usuario."""
    try:
        df = pd.read_csv(file)
        return _normalize_and_clean(df)
    except Exception as e:
        st.error(f"Error al leer el archivo: {str(e)}")
        return None

@st.cache_data
def load_data(filepath='ventas.csv'):
    """Carga datos desde archivo local (fallback)."""
    try:
        df = pd.read_csv(filepath)
        return _normalize_and_clean(df)
    except FileNotFoundError:
        return None

def _normalize_and_clean(df):
    """Limpia y normaliza el DataFrame."""
    df.columns = df.columns.str.upper().str.strip()
    column_mapping = {
        'FECHA': 'FECHA', 'PRODUCTO': 'PRODUCTO', 'CATEGORIA': 'CATEGORIA',
        'CATEGORÍA': 'CATEGORIA', 'CANTIDAD': 'UNIDADES', 'PRECIO': 'PRECIO',
        'CIUDAD': 'CIUDAD'
    }
    for old, new in column_mapping.items():
        if old in df.columns and old != new:
            df.rename(columns={old: new}, inplace=True)
    
    required = ['FECHA', 'PRODUCTO', 'CATEGORIA', 'UNIDADES', 'PRECIO', 'CIUDAD']
    if not all(col in df.columns for col in required):
        raise ValueError("El archivo no contiene las columnas requeridas.")
    
    df['FECHA'] = pd.to_datetime(df['FECHA'], errors='coerce')
    df = df.dropna(subset=['FECHA'])
    df['UNIDADES'] = pd.to_numeric(df['UNIDADES'], errors='coerce')
    df['PRECIO'] = pd.to_numeric(df['PRECIO'], errors='coerce')
    df = df.dropna(subset=['UNIDADES', 'PRECIO'])
    df['INGRESOS'] = df['UNIDADES'] * df['PRECIO']
    return df