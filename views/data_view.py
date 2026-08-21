# views/data_view.py
import streamlit as st

def show():
    st.header("📋 Exploración de Datos")
    st.markdown("Visualiza y exporta los datos brutos o filtrados.")

    df = st.session_state.df
    if df is None:
        st.warning("Carga un archivo CSV primero.")
        return

    # Filtros específicos de la vista de datos (opcional)
    with st.expander("🔍 Filtros Rápidos para Datos", expanded=False):
        ciudad_filter = st.multiselect("Ciudad", options=df['CIUDAD'].unique(), default=df['CIUDAD'].unique())
        cat_filter = st.multiselect("Categoría", options=df['CATEGORIA'].unique(), default=df['CATEGORIA'].unique())
        if ciudad_filter and cat_filter:
            df = df[df['CIUDAD'].isin(ciudad_filter) & df['CATEGORIA'].isin(cat_filter)]

    st.dataframe(df, use_container_width=True, height=500)

    # Exportación
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⬇️ Descargar datos filtrados (CSV)",
        data=csv,
        file_name='ventas_filtradas.csv',
        mime='text/csv'
    )