# utils/analysis_engine.py
import pandas as pd
import numpy as np
import streamlit as st

@st.cache_data
def get_all_aggregates(df):
    """Pre-calcula todos los agregados pesados una sola vez."""
    return {
        'top_unidades': df.groupby('PRODUCTO')['UNIDADES'].sum().sort_values(ascending=False),
        'top_ingresos': df.groupby('PRODUCTO')['INGRESOS'].sum().sort_values(ascending=False),
        'ingresos_categoria': df.groupby('CATEGORIA')['INGRESOS'].sum().sort_values(ascending=False),
        'ingresos_ciudad': df.groupby('CIUDAD')['INGRESOS'].sum().sort_values(ascending=False),
        'monthly': df.groupby(df['FECHA'].dt.to_period('M')).agg({'INGRESOS': 'sum', 'UNIDADES': 'sum'}).reset_index(),
        'prod_price_vol': df.groupby('PRODUCTO').agg({'UNIDADES': 'sum', 'PRECIO': 'mean'}).reset_index(),
    }

def get_kpis(df):
    """Calcula los indicadores clave."""
    total_ingresos = df['INGRESOS'].sum()
    registros = len(df)
    unidades = df['UNIDADES'].sum()
    ticket_prom = total_ingresos / registros if registros > 0 else 0
    return total_ingresos, registros, unidades, ticket_prom

def get_top_products(df):
    """Retorna productos top por unidades e ingresos."""
    top_unidades = df.groupby('PRODUCTO')['UNIDADES'].sum().sort_values(ascending=False)
    top_ingresos = df.groupby('PRODUCTO')['INGRESOS'].sum().sort_values(ascending=False)
    return top_unidades, top_ingresos

def get_pareto(df):
    """Calcula concentración de ingresos (Pareto)."""
    sorted_ingresos = df.groupby('PRODUCTO')['INGRESOS'].sum().sort_values(ascending=False)
    acum = sorted_ingresos.cumsum() / sorted_ingresos.sum() * 100
    top1 = acum.iloc[0] if len(acum) > 0 else 0
    top3 = acum.iloc[2] if len(acum) >= 3 else 0
    top5 = acum.iloc[4] if len(acum) >= 5 else 0
    return sorted_ingresos, acum, top1, top3, top5

def get_monthly_trend(df):
    monthly = df.groupby(df['FECHA'].dt.to_period('M'))['INGRESOS'].sum().reset_index()
    monthly['MES_NUM'] = range(len(monthly))
    monthly['MES_STR'] = monthly['FECHA'].astype(str)
    
    if len(monthly) > 2:
        x = monthly['MES_NUM'].values
        y = monthly['INGRESOS'].values
        slope, intercept = np.polyfit(x, y, 1)
        monthly['TENDENCIA'] = intercept + slope * x
        
        # Cálculo de Intervalo de Confianza (95%)
        residuos = y - monthly['TENDENCIA']
        std_error = np.std(residuos, ddof=1)
        z_score = 1.96  # 95% de confianza
        monthly['CI_SUPERIOR'] = monthly['TENDENCIA'] + (z_score * std_error)
        monthly['CI_INFERIOR'] = monthly['TENDENCIA'] - (z_score * std_error)
        
        # Proyección
        next_num = len(monthly)
        pred_ingresos = intercept + slope * next_num
        pred_superior = pred_ingresos + (z_score * std_error)
        pred_inferior = pred_ingresos - (z_score * std_error)
        
        ultimo_real = y[-1]
        cambio_pct = ((pred_ingresos - ultimo_real) / ultimo_real) * 100 if ultimo_real != 0 else 0
        
        mes_siguiente = pd.to_datetime(monthly['FECHA'].iloc[-1].start_time + pd.DateOffset(months=1)).strftime('%B %Y')
        
        return monthly, slope, pred_ingresos, pred_inferior, pred_superior, cambio_pct, mes_siguiente
    return monthly, 0, None, None, None, 0, None
    
def get_city_revenue(df):
    return df.groupby('CIUDAD')['INGRESOS'].sum().sort_values(ascending=False)

def get_category_revenue(df):
    return df.groupby('CATEGORIA')['INGRESOS'].sum().sort_values(ascending=False)

def get_product_price_volume(df):
    return df.groupby('PRODUCTO').agg({'UNIDADES': 'sum', 'PRECIO': 'mean'}).reset_index()