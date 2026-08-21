# views/decisions.py
import streamlit as st
from utils.analysis_engine import get_top_products, get_city_revenue, get_monthly_trend

def show():
    st.header("💡 Panel de Decisiones Estratégicas")
    st.markdown("Traduciendo los datos en acciones concretas para DATASTORE S.A.C.")

    df = st.session_state.df
    if df is None:
        st.warning("Carga un archivo CSV primero.")
        return

    top_unidades, top_ingresos = get_top_products(df)
    top_ciudad = get_city_revenue(df).index[0] if len(get_city_revenue(df)) > 0 else "Lima"
    
    # --- DESEMPAQUETAMOS LOS 7 VALORES (la función ahora retorna 7) ---
    monthly, slope, pred_ingresos, pred_inferior, pred_superior, cambio_pct, mes_siguiente = get_monthly_trend(df)

    prod_mas_ingresos = top_ingresos.index[0] if len(top_ingresos) > 0 else "N/A"
    prod_mas_unidades = top_unidades.index[0] if len(top_unidades) > 0 else "N/A"
    prod_menos_ingresos = top_ingresos.index[-1] if len(top_ingresos) > 0 else "N/A"

    st.subheader("📋 Recomendaciones Automatizadas")

    # --- Decisión 1: Gestión de Stock ---
    st.markdown(f"""
    <div style="background-color:#f0f8ff; padding:15px; border-radius:10px; border-left:5px solid #1f77b4; margin:10px 0;">
        <b>📦 1. Gestión de Stock y Prioridad</b><br>
        <b>Dato:</b> <b>{prod_mas_ingresos}</b> genera mayores ingresos, mientras que <b>{prod_mas_unidades}</b> mueve más volumen.<br>
        <b>Decisión:</b> Establecer un stock de seguridad prioritario para {prod_mas_ingresos}. 
        Para {prod_mas_unidades}, negociar con proveedores para reducir costos unitarios aprovechando el alto volumen.
    </div>
    """, unsafe_allow_html=True)

    # --- Decisión 2: Estrategia Geográfica ---
    st.markdown(f"""
    <div style="background-color:#f0f8ff; padding:15px; border-radius:10px; border-left:5px solid #ff7f0e; margin:10px 0;">
        <b>📍 2. Estrategia Geográfica</b><br>
        <b>Dato:</b> <b>{top_ciudad}</b> concentra la mayor parte de los ingresos.<br>
        <b>Decisión:</b> Evaluar costos logísticos en {top_ciudad}. Considerar un centro de distribución regional 
        (ej. Arequipa) para reducir tiempos de entrega en el sur del país.
    </div>
    """, unsafe_allow_html=True)

    # --- Decisión 3: Predictiva (basada en la tendencia) ---
    if cambio_pct is not None and cambio_pct < -5:
        st.markdown(f"""
        <div style="background-color:#ffcccc; padding:15px; border-radius:10px; border-left:5px solid red; margin:10px 0;">
            <b>📉 3. Plan de Contingencia (Predicción)</b><br>
            <b>Dato:</b> La proyección indica una posible caída del <b>{cambio_pct:.1f}%</b> en el próximo mes ({mes_siguiente}).<br>
            <b>Decisión:</b> Activar promociones en productos de alto margen ({prod_mas_ingresos}) para estimular la demanda. 
            NO reducir compras sin antes validar si la caída es real o estacional.
        </div>
        """, unsafe_allow_html=True)
    elif cambio_pct is not None and cambio_pct > 5:
        st.markdown(f"""
        <div style="background-color:#ccffcc; padding:15px; border-radius:10px; border-left:5px solid green; margin:10px 0;">
            <b>📈 3. Aprovechar Crecimiento (Predicción)</b><br>
            <b>Dato:</b> La proyección indica un crecimiento del <b>{cambio_pct:.1f}%</b> para {mes_siguiente}.<br>
            <b>Decisión:</b> Asegurar abastecimiento y evaluar contratación de personal temporal para logística.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="background-color:#f0fdf4; padding:15px; border-radius:10px; border-left:5px solid #22c55e; margin:10px 0;">
            <b>➡️ 3. Estabilidad (Predicción)</b><br>
            <b>Dato:</b> La proyección indica estabilidad para {mes_siguiente} con un cambio del <b>{cambio_pct:+.1f}%</b>.<br>
            <b>Decisión:</b> Mantener las estrategias actuales y monitorear de cerca las variables de mercado.
        </div>
        """, unsafe_allow_html=True)

    # --- Decisión 4: Gestión de Catálogo ---
    st.markdown(f"""
    <div style="background-color:#f0f8ff; padding:15px; border-radius:10px; border-left:5px solid #d62728; margin:10px 0;">
        <b>🗑️ 4. Gestión de Catálogo</b><br>
        <b>Dato:</b> <b>{prod_menos_ingresos}</b> es el producto con menor ingresos.<br>
        <b>Decisión:</b> No retirar del catálogo sin verificar si se vende como complemento (ej. accesorios). 
        Si es aislado, considerar promoción de liquidación.
    </div>
    """, unsafe_allow_html=True)

    # --- Resumen ejecutivo de la proyección ---
    with st.expander("📊 Resumen de la proyección mensual"):
        if pred_ingresos is not None:
            st.markdown(f"""
            - **Mes proyectado:** {mes_siguiente}
            - **Ingreso esperado:** S/. {pred_ingresos:,.2f}
            - **Rango de confianza (95%):** S/. {pred_inferior:,.2f} — S/. {pred_superior:,.2f}
            - **Cambio vs último mes:** {cambio_pct:+.1f}%
            - **Pendiente de la tendencia:** {slope:+.2f} S/. por mes
            """)
        else:
            st.info("No hay suficientes datos mensuales para generar una proyección confiable.")

    st.caption("⚠️ Todas las decisiones están sujetas a la validación de costos e inventario, que no están disponibles en el CSV actual. Las proyecciones son estimaciones basadas en datos históricos y pueden variar.")