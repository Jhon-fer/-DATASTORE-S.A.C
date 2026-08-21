# utils/visualizations.py
import plotly.express as px
import plotly.graph_objects as go

def create_graphs(df, top_unidades, top_ingresos, ingresos_categoria, ingresos_ciudad, monthly, sorted_ingresos, acum, prod_price_vol):
    """Retorna un diccionario con las 8 figuras de Plotly."""
    
    # Gráfico 1: Top 10 Unidades
    fig1 = px.bar(top_unidades.head(10), orientation='h', title="1. Top 10 en Unidades",
                  labels={'value': 'Unidades', 'PRODUCTO': ''}, color=top_unidades.head(10).values,
                  color_continuous_scale='Blues')
    fig1.update_layout(coloraxis_showscale=False, height=400)

    # Gráfico 2: Top 10 Ingresos
    fig2 = px.bar(top_ingresos.head(10), orientation='h', title="2. Top 10 en Ingresos (S/.)",
                  labels={'value': 'Ingresos', 'PRODUCTO': ''}, color=top_ingresos.head(10).values,
                  color_continuous_scale='Greens')
    fig2.update_layout(coloraxis_showscale=False, height=400)

    # Gráfico 3: Scatter Volumen vs Ingresos
    prod_agg = df.groupby('PRODUCTO').agg({'UNIDADES': 'sum', 'INGRESOS': 'sum'}).reset_index()
    fig3 = px.scatter(prod_agg, x='UNIDADES', y='INGRESOS', hover_name='PRODUCTO',
                      title="3. Relación Volumen vs Ingresos",
                      labels={'UNIDADES': 'Unidades', 'INGRESOS': 'Ingresos (S/.)'})

    # Gráfico 4: Ingresos por Categoría (Pie)
    fig4 = px.pie(values=ingresos_categoria.values, names=ingresos_categoria.index,
                  title="4. Distribución por Categoría", hole=0.3)

    # Gráfico 5: Ingresos por Ciudad (Barras)
    fig5 = px.bar(ingresos_ciudad, title="5. Ingresos por Ciudad",
                  labels={'value': 'Ingresos', 'CIUDAD': ''}, color=ingresos_ciudad.values,
                  color_continuous_scale='Oranges')
    fig5.update_layout(coloraxis_showscale=False)

    # Gráfico 6: Evolución Mensual
    fig6 = px.line(monthly, x='MES_STR', y='INGRESOS', markers=True,
                   title="6. Evolución Mensual de Ingresos",
                   labels={'MES_STR': 'Mes', 'INGRESOS': 'Ingresos (S/.)'})

    # Gráfico 7: Pareto (Concentración)
    fig7 = go.Figure()
    fig7.add_trace(go.Bar(x=sorted_ingresos.index, y=sorted_ingresos.values, name="Ingresos", marker_color='steelblue'))
    fig7.add_trace(go.Scatter(x=sorted_ingresos.index, y=acum, name="% Acumulado", yaxis="y2", mode='lines+markers', marker_color='red'))
    fig7.update_layout(title="7. Concentración de Ingresos (Pareto)", xaxis_title="Producto",
                       yaxis_title="Ingresos", yaxis2=dict(title="% Acumulado", overlaying="y", side="right", range=[0, 100]))

    # Gráfico 8: Precio vs Volumen
    fig8 = px.scatter(prod_price_vol, x='UNIDADES', y='PRECIO', hover_name='PRODUCTO',
                      title="8. Precio Promedio vs Volumen Vendido",
                      labels={'UNIDADES': 'Unidades', 'PRECIO': 'Precio Promedio (S/.)'})

    return {
        'fig1': fig1, 'fig2': fig2, 'fig3': fig3, 'fig4': fig4,
        'fig5': fig5, 'fig6': fig6, 'fig7': fig7, 'fig8': fig8
    }