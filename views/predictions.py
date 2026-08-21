# views/predictions.py
import streamlit as st
import plotly.graph_objects as go
from utils.analysis_engine import get_monthly_trend

def show():
    st.header("🔮 Predicciones y Tendencias (Big Data)")
    st.markdown("Utilizando regresión lineal sobre los datos históricos, proyectamos el comportamiento futuro con un **95% de confianza**.")

    df = st.session_state.df
    if df is None:
        st.warning("Carga un archivo CSV primero.")
        return

    # Obtener todos los valores de la tendencia (incluyendo intervalos)
    monthly, slope, pred_ingresos, pred_inferior, pred_superior, cambio_pct, mes_siguiente = get_monthly_trend(df)

    if monthly is not None and len(monthly) > 1:
        st.subheader("📈 Proyección para el próximo mes")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("📅 Mes Proyectado", mes_siguiente)
            if pred_ingresos is not None:
                st.metric("💰 Ingresos Proyectados", f"S/. {pred_ingresos:,.2f}", 
                          delta=f"{cambio_pct:+.1f}% vs último mes")
                st.caption(f"📊 Rango estimado (95% confianza): S/. {pred_inferior:,.2f} — S/. {pred_superior:,.2f}")
        with col2:
            if cambio_pct is not None and cambio_pct > 5:
                st.success("✅ **Tendencia alcista.** Buen momento para invertir en stock y promociones.")
            elif cambio_pct is not None and cambio_pct < -5:
                st.error("⚠️ **Tendencia bajista.** Revisar estrategias de marketing y considerar promociones.")
            else:
                st.info("➡️ **Tendencia estable.** Mantener estrategias actuales y monitorear de cerca.")

        # --- GRÁFICO DE EVOLUCIÓN CON BANDA DE CONFIANZA ---
        fig = go.Figure()

        # Datos históricos
        fig.add_trace(go.Scatter(
            x=monthly['MES_STR'], 
            y=monthly['INGRESOS'], 
            mode='lines+markers', 
            name='Histórico', 
            line=dict(color='blue', width=2),
            marker=dict(size=8)
        ))

        # Línea de tendencia
        fig.add_trace(go.Scatter(
            x=monthly['MES_STR'], 
            y=monthly['TENDENCIA'], 
            mode='lines', 
            name='Tendencia Lineal', 
            line=dict(color='red', dash='dash', width=2)
        ))

        # Banda de confianza (95%) - Relleno entre superior e inferior
        fig.add_trace(go.Scatter(
            x=monthly['MES_STR'], 
            y=monthly['CI_SUPERIOR'],
            mode='lines', 
            name='Límite Superior (95%)', 
            line=dict(color='rgba(0,255,0,0)', width=0)
        ))
        fig.add_trace(go.Scatter(
            x=monthly['MES_STR'], 
            y=monthly['CI_INFERIOR'],
            mode='lines', 
            name='Intervalo de Confianza (95%)', 
            line=dict(color='rgba(0,255,0,0)', width=0),
            fill='tonexty',
            fillcolor='rgba(0, 255, 0, 0.15)'  # Verde claro transparente
        ))

        # Proyección (punto estrella)
        if pred_ingresos is not None and mes_siguiente:
            fig.add_trace(go.Scatter(
                x=[mes_siguiente], 
                y=[pred_ingresos], 
                mode='markers', 
                name='Proyección', 
                marker=dict(color='green', size=18, symbol='star', line=dict(width=2, color='darkgreen'))
            ))
            # Mostrar también los límites superior e inferior de la proyección
            fig.add_trace(go.Scatter(
                x=[mes_siguiente], 
                y=[pred_superior], 
                mode='markers', 
                name='Límite Superior Proyectado', 
                marker=dict(color='rgba(0,255,0,0.5)', size=10, symbol='triangle-up')
            ))
            fig.add_trace(go.Scatter(
                x=[mes_siguiente], 
                y=[pred_inferior], 
                mode='markers', 
                name='Límite Inferior Proyectado', 
                marker=dict(color='rgba(255,165,0,0.5)', size=10, symbol='triangle-down')
            ))

        fig.update_layout(
            title="Evolución de Ingresos y Proyección con Intervalo de Confianza (95%)",
            xaxis_title="Mes",
            yaxis_title="Ingresos (S/.)",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            height=500,
            hovermode="x unified"
        )

        st.plotly_chart(fig, use_container_width=True)

        # Interpretación adicional
        with st.expander("📖 ¿Cómo interpretar este gráfico?"):
            st.markdown("""
            - **Línea azul**: Ingresos reales mes a mes.
            - **Línea roja discontinua**: Tendencia general (creciente o decreciente).
            - **Banda verde**: Intervalo de confianza del 95%. Cuanto más ancha sea, mayor incertidumbre.
            - **Estrella verde**: Proyección puntual para el próximo mes.
            - **Triángulos**: Límites superior e inferior de la proyección.
            
            **Regla práctica**: Si la banda es estrecha y la tendencia es clara, la predicción es confiable. Si la banda es ancha, los datos son muy volátiles y se debe ser cauteloso.
            """)

        # Mostrar pendiente
        st.caption(f"📐 **Pendiente de la tendencia**: {slope:+.2f} S/. por mes. {'Crecimiento' if slope > 0 else 'Decrecimiento'} gradual.")

    else:
        st.info("Se necesitan al menos **3 meses de datos históricos** para calcular la tendencia con intervalo de confianza.")