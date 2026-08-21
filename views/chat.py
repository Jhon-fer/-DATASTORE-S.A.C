# views/chat.py
import streamlit as st
import pandas as pd

def show():
    st.header("🤖 Asistente Virtual de DATASTORE")
    st.markdown("Pregúntame sobre tus datos de ventas. Te daré respuestas basadas en el análisis.")

    df = st.session_state.df
    if df is None:
        st.warning("Carga un archivo CSV primero.")
        return

    # Inicializar historial del chat
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Mostrar historial
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Entrada del usuario
    prompt = st.chat_input("Escribe tu pregunta sobre los datos...")
    
    if prompt:
        # Agregar pregunta al historial
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # --- LÓGICA DE RESPUESTA (basada en palabras clave) ---
        respuesta = ""
        prompt_lower = prompt.lower()

        # 1. Preguntas sobre ingresos totales
        if "ingreso" in prompt_lower and ("total" in prompt_lower or "general" in prompt_lower):
            total = df['INGRESOS'].sum()
            respuesta = f"💰 Los ingresos totales son **S/. {total:,.2f}**."
        
        # 2. Producto más vendido
        elif "producto más vendido" in prompt_lower or "más vendido" in prompt_lower:
            top = df.groupby('PRODUCTO')['UNIDADES'].sum().idxmax()
            unidades = df.groupby('PRODUCTO')['UNIDADES'].sum().max()
            respuesta = f"📦 El producto más vendido en unidades es **{top}** con **{unidades:,.0f}** unidades."
        
        # 3. Producto con mayores ingresos
        elif "mayores ingresos" in prompt_lower or "estrella" in prompt_lower:
            top = df.groupby('PRODUCTO')['INGRESOS'].sum().idxmax()
            ingresos = df.groupby('PRODUCTO')['INGRESOS'].sum().max()
            respuesta = f"🏆 El producto que genera mayores ingresos es **{top}** con **S/. {ingresos:,.2f}**."
        
        # 4. Ciudad con mayores ventas
        elif "ciudad" in prompt_lower and ("más" in prompt_lower or "mayor" in prompt_lower):
            top = df.groupby('CIUDAD')['INGRESOS'].sum().idxmax()
            ingresos = df.groupby('CIUDAD')['INGRESOS'].sum().max()
            respuesta = f"🏙️ La ciudad con mayores ingresos es **{top}** con **S/. {ingresos:,.2f}**."
        
        # 5. Categoría líder
        elif "categoría" in prompt_lower and ("más" in prompt_lower or "mayor" in prompt_lower or "líder" in prompt_lower):
            top = df.groupby('CATEGORIA')['INGRESOS'].sum().idxmax()
            ingresos = df.groupby('CATEGORIA')['INGRESOS'].sum().max()
            respuesta = f"📂 La categoría líder es **{top}** con **S/. {ingresos:,.2f}**."
        
        # 6. Mes con mayores ventas
        elif "mes" in prompt_lower and ("mayor" in prompt_lower or "pico" in prompt_lower):
            monthly = df.groupby(df['FECHA'].dt.to_period('M'))['INGRESOS'].sum()
            top_mes = monthly.idxmax().strftime('%B %Y')
            ingresos = monthly.max()
            respuesta = f"📅 El mes con mayores ingresos es **{top_mes}** con **S/. {ingresos:,.2f}**."
        
        # 7. Producto menos vendido
        elif "menos vendido" in prompt_lower or "bajo" in prompt_lower:
            top = df.groupby('PRODUCTO')['UNIDADES'].sum().idxmin()
            unidades = df.groupby('PRODUCTO')['UNIDADES'].sum().min()
            respuesta = f"📉 El producto menos vendido en unidades es **{top}** con **{unidades:,.0f}** unidades."
        
        # 8. Resumen general
        elif "resumen" in prompt_lower or "general" in prompt_lower:
            total = df['INGRESOS'].sum()
            registros = len(df)
            top_prod = df.groupby('PRODUCTO')['INGRESOS'].sum().idxmax()
            top_ciudad = df.groupby('CIUDAD')['INGRESOS'].sum().idxmax()
            respuesta = f"""
            📊 **Resumen general:**
            - Total de ingresos: **S/. {total:,.2f}**
            - Registros analizados: **{registros:,}**
            - Producto estrella: **{top_prod}**
            - Ciudad líder: **{top_ciudad}**
            """
        
        # 9. Ticket promedio
        elif "ticket" in prompt_lower or "promedio" in prompt_lower:
            total = df['INGRESOS'].sum()
            registros = len(df)
            ticket = total / registros if registros > 0 else 0
            respuesta = f"🧾 El ticket promedio es **S/. {ticket:,.2f}**."
        
        # 10. Caída de agosto
        elif "agosto" in prompt_lower and ("caída" in prompt_lower or "bajo" in prompt_lower or "menos" in prompt_lower):
            meses = df['FECHA'].dt.month_name()
            ingresos_por_mes = df.groupby(meses)['INGRESOS'].sum()
            if 'August' in ingresos_por_mes.index or 'Agosto' in ingresos_por_mes.index:
                mes_agosto = 'August' if 'August' in ingresos_por_mes.index else 'Agosto'
                ing_agosto = ingresos_por_mes[mes_agosto]
                prom_sin_agosto = ingresos_por_mes[ingresos_por_mes.index != mes_agosto].mean()
                if prom_sin_agosto > 0:
                    caida = ((prom_sin_agosto - ing_agosto) / prom_sin_agosto) * 100
                    respuesta = f"⚠️ Agosto presenta una caída del **{caida:.1f}%** en comparación con el promedio mensual. Recomiendo validar la integridad de los datos de agosto."
                else:
                    respuesta = "No se detectó una caída significativa en agosto."
            else:
                respuesta = "No hay datos disponibles para agosto."
        
        # 11. Ayuda / Comandos disponibles
        elif "ayuda" in prompt_lower or "comandos" in prompt_lower or "qué puedes hacer" in prompt_lower:
            respuesta = """
            🤖 **Puedo ayudarte con estas preguntas:**
            - ¿Cuáles son los ingresos totales?
            - ¿Qué producto es el más vendido?
            - ¿Qué producto genera mayores ingresos?
            - ¿Qué ciudad tiene mayores ventas?
            - ¿Qué categoría es la líder?
            - ¿Cuál fue el mes con mayores ventas?
            - ¿Cuál es el producto menos vendido?
            - ¿Cómo va el ticket promedio?
            - ¿Qué pasó en agosto?
            - Resumen general de la empresa.
            """
        
        else:
            respuesta = "❓ No entendí tu pregunta. Puedes preguntarme sobre ingresos totales, producto más vendido, ciudad líder, categoría, mes pico, ticket promedio o pedirme un resumen general."

        # Mostrar respuesta
        with st.chat_message("assistant"):
            st.markdown(respuesta)
        st.session_state.chat_history.append({"role": "assistant", "content": respuesta})

        # Limpiar historial (opcional)
        if len(st.session_state.chat_history) > 20:
            st.session_state.chat_history = st.session_state.chat_history[-20:]