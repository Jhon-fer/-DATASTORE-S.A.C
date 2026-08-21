# views/home.py
import streamlit as st
import pandas as pd
from utils.analysis_engine import get_kpis, get_top_products, get_category_revenue, get_city_revenue

def show():
    st.header("🏠 Panel de Control Ejecutivo")
    
    df = st.session_state.df
    if df is None:
        st.warning("Carga un archivo CSV primero.")
        return

    # --- CÁLCULOS RÁPIDOS ---
    total_ingresos, registros, unidades, ticket_prom = get_kpis(df)
    top_unidades, top_ingresos = get_top_products(df)
    top_categoria = get_category_revenue(df).index[0] if len(get_category_revenue(df)) > 0 else "N/A"
    top_ciudad = get_city_revenue(df).index[0] if len(get_city_revenue(df)) > 0 else "N/A"
    
    # Mes con mayores ingresos
    ingresos_mensuales = df.groupby(df['FECHA'].dt.to_period('M'))['INGRESOS'].sum()
    mes_top = ingresos_mensuales.idxmax().strftime('%B %Y') if not ingresos_mensuales.empty else "N/A"
    
    prod_mas_ingresos = top_ingresos.index[0] if len(top_ingresos) > 0 else "N/A"
    prod_mas_unidades = top_unidades.index[0] if len(top_unidades) > 0 else "N/A"

    # --- RESUMEN EJECUTIVO (En lenguaje natural) ---
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%); padding: 20px; border-radius: 12px; border-left: 6px solid #2563eb; margin-bottom: 25px;">
        <h4 style="margin:0 0 8px 0; color: #0f172a;">📌 Resumen Ejecutivo</h4>
        <p style="margin:0; color: #334155; font-size: 1.05rem; line-height: 1.6;">
            DATASTORE ha generado <b>S/. {total_ingresos:,.2f}</b> en el período analizado. 
            El motor de ingresos es la categoría <b>{top_categoria}</b>, destacando la ciudad de <b>{top_ciudad}</b>. 
            El mes con mayor actividad fue <b>{mes_top}</b>.
            <br><br>
            <span style="color:#475569;">💡 <b>Ojo:</b> Revisa la pestaña de <b>Predicciones</b> para ver hacia dónde se dirigen las ventas.</span>
        </p>
    </div>
    """, unsafe_allow_html=True)

    # --- KPIS CON TOOLTIPS ---
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "💰 Ingresos Totales",
            f"S/. {total_ingresos:,.2f}",
            help="Suma total de todo el dinero generado por todas las ventas (Cantidad × Precio)."
        )
    with col2:
        st.metric(
            "📦 Unidades Vendidas",
            f"{unidades:,}",
            help="Cantidad total de productos físicos que han salido del almacén."
        )
    with col3:
        st.metric(
            "🧾 Ticket Promedio",
            f"S/. {ticket_prom:,.2f}",
            help="Promedio de gasto por cada registro de venta. Se calcula como Ingresos Totales / Número de registros."
        )
    with col4:
        st.metric(
            "🏆 Producto Estrella",
            prod_mas_ingresos,
            help="Producto que genera la mayor cantidad de dinero, aunque no sea el que más unidades vende."
        )

    # Segunda fila de KPIs
    col5, col6, col7, col8 = st.columns(4)
    
    with col5:
        st.metric(
            "📈 Producto más vendido (unidades)",
            prod_mas_unidades,
            help="Producto con mayor cantidad de unidades vendidas (volumen)."
        )
    with col6:
        st.metric(
            "🏙️ Ciudad líder",
            top_ciudad,
            help="Ciudad que genera mayores ingresos."
        )
    with col7:
        st.metric(
            "📂 Categoría líder",
            top_categoria,
            help="Categoría que genera mayores ingresos."
        )
    with col8:
        st.metric(
            "📅 Mes pico",
            mes_top,
            help="Mes con mayores ingresos registrados."
        )

    st.divider()

    # --- ALERTAS AUTOMÁTICAS ---
    st.subheader("🔔 Alertas de Gestión")
    
    # Verificar caída de agosto
    meses = df['FECHA'].dt.month_name()
    ingresos_por_mes = df.groupby(meses)['INGRESOS'].sum()
    if 'August' in ingresos_por_mes.index or 'Agosto' in ingresos_por_mes.index:
        mes_agosto = 'August' if 'August' in ingresos_por_mes.index else 'Agosto'
        ing_agosto = ingresos_por_mes[mes_agosto]
        prom_sin_agosto = ingresos_por_mes[ingresos_por_mes.index != mes_agosto].mean()
        if prom_sin_agosto > 0:
            caida = ((prom_sin_agosto - ing_agosto) / prom_sin_agosto) * 100
            if caida > 10:
                st.error(f"""
                ⚠️ **Caída Crítica en Agosto**  
                Las ventas cayeron un **{caida:.1f}%** en comparación con el promedio mensual.  
                📌 **Recomendación:** Revisa la integridad de los datos de agosto con el área de TI.
                """)

    # Verificar conflicto Volumen vs Ingresos
    if len(top_unidades) > 0 and len(top_ingresos) > 0:
        if top_unidades.index[0] != top_ingresos.index[0]:
            st.warning(f"""
            ⚠️ **Estrategias en conflicto**  
            **{top_unidades.index[0]}** vende más unidades, pero **{top_ingresos.index[0]}** genera más ingresos.  
            📌 **Recomendación:** Define prioridades de stock según el objetivo (¿volumen o valor?).
            """)
        else:
            st.success(f"""
            ✅ **Alineado**  
            **{top_ingresos.index[0]}** lidera tanto en volumen como en ingresos.
            """)

    # --- BOTÓN DE EXPORTAR REPORTE ---
    st.divider()
    if st.button("📄 Generar Reporte Ejecutivo (Resumen)", use_container_width=True):
        report_text = f"""
        === REPORTE EJECUTIVO DATASTORE S.A.C. ===
        Fecha: {pd.Timestamp.now().strftime('%d/%m/%Y %H:%M')}

        1. INGRESOS TOTALES: S/. {total_ingresos:,.2f}
        2. PRODUCTO ESTRELLA (ingresos): {prod_mas_ingresos}
        3. PRODUCTO MÁS VENDIDO (unidades): {prod_mas_unidades}
        4. CIUDAD PRINCIPAL: {top_ciudad}
        5. CATEGORÍA REINA: {top_categoria}
        6. MES PICO: {mes_top}
        7. TICKET PROMEDIO: S/. {ticket_prom:,.2f}

        NOTA: Este reporte es automático. Para un análisis detallado, revisar los gráficos interactivos.
        """
        st.download_button(
            label="⬇️ Descargar Resumen en TXT",
            data=report_text,
            file_name="reporte_ejecutivo_datastore.txt",
            mime="text/plain"
        )

    st.caption("📌 Navega por las pestañas superiores para ver gráficos, predicciones y decisiones.")