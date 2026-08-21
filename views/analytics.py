# views/analytics.py
import streamlit as st
from utils.analysis_engine import (
    get_all_aggregates,
    get_pareto,
    get_monthly_trend,
)
from utils.visualizations import create_graphs

def show():
    st.header("📊 Análisis Gráfico Completo")
    st.markdown("Los siguientes 8 gráficos han sido seleccionados para responder preguntas clave del negocio.")

    df = st.session_state.df
    if df is None:
        st.warning("Carga un archivo CSV primero.")
        return

    # --- OBTENER DATOS AGREGADOS ---
    aggregates = get_all_aggregates(df)
    top_unidades = aggregates['top_unidades']
    top_ingresos = aggregates['top_ingresos']
    ingresos_categoria = aggregates['ingresos_categoria']
    ingresos_ciudad = aggregates['ingresos_ciudad']
    monthly = aggregates['monthly']
    prod_price_vol = aggregates['prod_price_vol']

    sorted_ingresos, acum, _, _, _ = get_pareto(df)

    # Desempaquetar correctamente los 7 valores de get_monthly_trend
    monthly_trend, slope, pred_ingresos, pred_inferior, pred_superior, cambio_pct, mes_siguiente = get_monthly_trend(df)

    if monthly_trend is not None and not monthly_trend.empty:
        monthly_for_graph = monthly_trend
    else:
        monthly_for_graph = monthly.copy()
        monthly_for_graph['MES_STR'] = monthly_for_graph['FECHA'].astype(str)

    # --- GENERAR GRÁFICOS ---
    graphs = create_graphs(
        df=df,
        top_unidades=top_unidades,
        top_ingresos=top_ingresos,
        ingresos_categoria=ingresos_categoria,
        ingresos_ciudad=ingresos_ciudad,
        monthly=monthly_for_graph,
        sorted_ingresos=sorted_ingresos,
        acum=acum,
        prod_price_vol=prod_price_vol
    )

    # --- MOSTRAR EN CUADRÍCULA DE 2 COLUMNAS CON TOOLTIPS ---
    cols = st.columns(2)
    
    with cols[0]:
        st.plotly_chart(graphs['fig1'], use_container_width=True, key="fig1")
        st.caption("📌 *Muestra qué productos tienen mayor salida (volumen). Útil para planificar compras.*")
        
        st.plotly_chart(graphs['fig3'], use_container_width=True, key="fig3")
        st.caption("📌 *Relaciona cuánto se vende (volumen) con cuánto dinero genera (ingresos). Los puntos arriba a la derecha son los más valiosos.*")
        
        st.plotly_chart(graphs['fig5'], use_container_width=True, key="fig5")
        st.caption("📌 *Compara el rendimiento por ciudad. Identifica mercados clave para expandir o consolidar.*")
        
        st.plotly_chart(graphs['fig7'], use_container_width=True, key="fig7")
        st.caption("📌 *Curva de Pareto: muestra que unos pocos productos concentran la mayor parte del dinero. Si la curva es muy empinada, la empresa depende de pocos productos.*")
    
    with cols[1]:
        st.plotly_chart(graphs['fig2'], use_container_width=True, key="fig2")
        st.caption("📌 *Muestra qué productos generan más dinero (ingresos). No siempre coincide con el más vendido en unidades.*")
        
        st.plotly_chart(graphs['fig4'], use_container_width=True, key="fig4")
        st.caption("📌 *Distribución de ingresos por categoría. Útil para saber qué categorías dominan y cuáles necesitan impulso.*")
        
        st.plotly_chart(graphs['fig6'], use_container_width=True, key="fig6")
        st.caption("📌 *Evolución mensual de ingresos. Permite detectar tendencias, estacionalidad o caídas (ej. agosto).*")
        
        st.plotly_chart(graphs['fig8'], use_container_width=True, key="fig8")
        st.caption("📌 *Relación entre precio promedio y volumen vendido. Ayuda a definir estrategias de precios: productos de alto volumen/bajo precio vs. bajo volumen/alto precio.*")

    # --- INTERPRETACIÓN GENERAL ---
    with st.expander("📖 ¿Qué nos dicen estos gráficos? (Guía rápida)"):
        st.markdown("""
        - **Gráfico 1 y 2**: Si el top 10 de unidades no coincide con el top 10 de ingresos, significa que hay productos que venden mucho pero generan poco dinero, y viceversa.
        - **Gráfico 3**: Los productos en la esquina superior derecha son los que más aportan (alto volumen y alto ingreso).
        - **Gráfico 4**: Si una categoría domina (>40%), la empresa depende mucho de ella. Diversificar podría ser una estrategia.
        - **Gráfico 5**: Ciudades con bajos ingresos pero alto costo logístico podrían no ser rentables.
        - **Gráfico 6**: Si ves una caída fuerte (ej. agosto), investiga si es real o un problema de datos.
        - **Gráfico 7**: Si el Top 3 concentra más del 60% de los ingresos, la empresa tiene alto riesgo de concentración.
        - **Gráfico 8**: Productos con alto volumen y bajo precio son ideales para captar mercado; los de bajo volumen y alto precio son para nichos especializados.
        """)

    st.caption("💡 Haz clic en cualquier gráfico para ver detalles. Los filtros globales afectan a todos.")