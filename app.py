# app.py
import streamlit as st
from utils.data_loader import load_data, load_data_from_file
from utils.analysis_engine import get_kpis, get_top_products, get_city_revenue, get_monthly_trend

# --- CONFIGURACIÓN INICIAL ---
st.set_page_config(
    page_title="DATASTORE S.A.C. - Business Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CARGA DE CSS GLOBAL ---
def load_css():
    try:
        with open("assets/style.css", "r", encoding="utf-8") as f:
            css = f.read()
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("⚠️ Archivo style.css no encontrado. Usando estilos por defecto.")
load_css()

# --- INICIALIZACIÓN DE ESTADO ---
if 'df' not in st.session_state:
    st.session_state.df = None
    st.session_state.df_loaded = False
    st.session_state.drill_down_filter = {}
    st.session_state.authenticated = False
    st.session_state.chat_history = []  # Para el chatbot

# --- FUNCIÓN DE AUTENTICACIÓN ---
def login(username, password):
    # Credenciales predefinidas (simulando base de datos)
    valid_users = {
        "admin": "admin123",
        "gerente": "ventas2026",
        "analista": "bigdata"
    }
    if username in valid_users and valid_users[username] == password:
        st.session_state.authenticated = True
        st.session_state.username = username
        return True
    return False

def logout():
    st.session_state.authenticated = False
    st.session_state.username = None
    st.rerun()

# --- PANTALLA DE LOGIN ---
if not st.session_state.authenticated:
    st.title("🔐 DATASTORE S.A.C.")
    st.subheader("Acceso al Sistema de Business Intelligence")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login_form"):
            username = st.text_input("👤 Usuario", placeholder="admin, gerente o analista")
            password = st.text_input("🔑 Contraseña", type="password", placeholder="admin123, ventas2026 o bigdata")
            submitted = st.form_submit_button("Ingresar", use_container_width=True)
            
            if submitted:
                if login(username, password):
                    st.success(f"✅ Bienvenido {username}!")
                    st.rerun()
                else:
                    st.error("❌ Usuario o contraseña incorrectos.")
        
        st.caption("💡 Credenciales de prueba: admin/admin123, gerente/ventas2026, analista/bigdata")
    st.stop()

# --- SI ESTÁ AUTENTICADO, CONTINÚA ---

# --- HEADER PERSONALIZADO (con botón de logout) ---
st.markdown(f"""
<div class="custom-header">
    <div class="header-logo">
        <div style="background:#2563eb; width:40px; height:40px; border-radius:8px; display:flex; align-items:center; justify-content:center; color:white; font-weight:bold; font-size:20px;">D</div>
        <div>
            <h1>DATASTORE S.A.C.</h1>
            <div style="display:flex; gap:10px; margin-top:-5px;">
                <span style="font-size:0.7rem; color:#64748b;">Big Data Platform</span>
                <span style="background:#2563eb; color:white; font-size:0.6rem; padding:1px 10px; border-radius:20px;">v2.0</span>
            </div>
        </div>
    </div>
    <div class="header-user">
        <span class="badge">📡 Tiempo Real</span>
        <span style="display:flex; align-items:center; gap:8px;">
            <span style="font-weight:500; color:#0f172a;">{st.session_state.username}</span>
            <div style="background:#e2e8f0; width:32px; height:32px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-weight:bold; color:#475569; cursor:pointer;" onclick="location.reload();">{st.session_state.username[:2].upper()}</div>
        </span>
    </div>
</div>
""", unsafe_allow_html=True)

# --- BARRA LATERAL: CARGA + PERFIL + NAVEGACIÓN + CHATBOT ---
with st.sidebar:
    # Perfil del usuario
    st.markdown("""
    <div class="profile-container">
        <div class="profile-avatar">D</div>
        <div class="profile-name">DATASTORE S.A.C.</div>
        <div class="profile-role">Analytics & Big Data</div>
        <div style="font-size:0.7rem; color:#64748b; margin-top:5px;">Usuario: {}</div>
    </div>
    """.format(st.session_state.username), unsafe_allow_html=True)
    
    st.divider()
    
    # Carga de datos
    st.header("📂 Datos")
    uploaded_file = st.file_uploader(
        "Sube tu archivo ventas.csv",
        type=['csv'],
        help="Arrastra o selecciona el archivo CSV con los datos de ventas",
        label_visibility="collapsed"
    )
    
    if uploaded_file is not None:
        df = load_data_from_file(uploaded_file)
        if df is not None:
            st.session_state.df = df
            st.session_state.df_loaded = True
            st.success(f"✅ {len(df):,} registros cargados.")
    else:
        if not st.session_state.df_loaded:
            df = load_data()
            if df is not None:
                st.session_state.df = df
                st.session_state.df_loaded = True
                st.info(f"📂 Datos locales: {len(df):,} registros.")
            else:
                st.warning("⚠️ Sube un archivo CSV.")
                st.stop()
    
    st.divider()
    
    # Menú de navegación
    st.header("📋 Navegación")
    page = st.radio(
        "Ir a:",
        options=["🏠 Inicio", "📊 Análisis", "🔮 Predicciones", "📋 Datos", "💡 Decisiones"],
        index=0,
        label_visibility="collapsed"
    )
    
    st.divider()
    
    # --- CHATBOT INTEGRADO EN LA BARRA LATERAL ---
    with st.expander("🤖 Asistente Virtual (Chatbot)", expanded=False):
        st.caption("Pregúntame sobre tus datos de ventas.")
        
        # Mostrar historial del chat
        for msg in st.session_state.chat_history[-10:]:  # Últimos 10 mensajes
            if msg["role"] == "user":
                st.markdown(f"🧑 **Tú:** {msg['content']}")
            else:
                st.markdown(f"🤖 **Asistente:** {msg['content']}")
        
        # Input del usuario
        user_input = st.text_input("Escribe tu pregunta:", key="chat_input", placeholder="Ej: ¿Cuál es el producto más vendido?")
        if user_input:
            # Agregar mensaje del usuario al historial
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            
            # Generar respuesta (usando datos si están disponibles)
            response = generate_chat_response(user_input, st.session_state.df)
            st.session_state.chat_history.append({"role": "assistant", "content": response})
            st.rerun()
    
    st.divider()
    st.caption("📌 Filtros globales aplicados en todas las vistas.")
    
    # Botón de logout
    if st.button("🚪 Cerrar Sesión", use_container_width=True):
        logout()

# --- VERIFICACIÓN DE DATOS ---
if st.session_state.df is None:
    st.warning("Por favor, sube el archivo ventas.csv en la barra lateral.")
    st.stop()

# --- ROUTER DE PÁGINAS ---
from views import home, analytics, predictions, data_view, decisions

if page == "🏠 Inicio":
    home.show()
elif page == "📊 Análisis":
    analytics.show()
elif page == "🔮 Predicciones":
    predictions.show()
elif page == "📋 Datos":
    data_view.show()
elif page == "💡 Decisiones":
    decisions.show()

# --- FOOTER GLOBAL ---
st.markdown("""
<div class="custom-footer">
    <div>
        © 2026 DATASTORE S.A.C. — Todos los derechos reservados.
    </div>
    <div class="footer-techs">
        <span>⚡ Streamlit</span>
        <span>🐼 Pandas</span>
        <span>📈 Plotly</span>
        <span>⚙️ Apache Spark (Conceptual)</span>
    </div>
</div>
""", unsafe_allow_html=True)

# --- FUNCIÓN DEL CHATBOT (basado en datos) ---
def generate_chat_response(question, df):
    """Genera respuestas a preguntas comunes sobre los datos."""
    if df is None:
        return "⚠️ No hay datos cargados. Sube un archivo CSV primero."
    
    question_lower = question.lower()
    
    # --- PREGUNTAS FRECUENTES ---
    # 1. Producto más vendido (unidades)
    if any(word in question_lower for word in ["más vendido", "producto top", "mayor unidades", "producto estrella", "cuál producto vende más"]):
        top_unidades = df.groupby('PRODUCTO')['UNIDADES'].sum().sort_values(ascending=False)
        if len(top_unidades) > 0:
            top = top_unidades.index[0]
            cant = top_unidades.iloc[0]
            return f"🏆 El producto con más unidades vendidas es **{top}** con **{cant:,.0f}** unidades."
        return "No hay datos suficientes."
    
    # 2. Producto con mayores ingresos
    if any(word in question_lower for word in ["mayor ingreso", "más dinero", "genera más ingresos", "más factura"]):
        top_ingresos = df.groupby('PRODUCTO')['INGRESOS'].sum().sort_values(ascending=False)
        if len(top_ingresos) > 0:
            top = top_ingresos.index[0]
            ing = top_ingresos.iloc[0]
            return f"💰 El producto que genera más ingresos es **{top}** con **S/. {ing:,.2f}**."
        return "No hay datos suficientes."
    
    # 3. Ciudad con mayores ingresos
    if any(word in question_lower for word in ["ciudad", "lugar", "sede", "ubicación", "dónde"]):
        top_ciudad = df.groupby('CIUDAD')['INGRESOS'].sum().sort_values(ascending=False)
        if len(top_ciudad) > 0:
            ciudad = top_ciudad.index[0]
            ing = top_ciudad.iloc[0]
            return f"📍 La ciudad que genera más ingresos es **{ciudad}** con **S/. {ing:,.2f}**."
        return "No hay datos suficientes."
    
    # 4. Categoría con mayores ingresos
    if any(word in question_lower for word in ["categoría", "tipo", "familia"]):
        top_cat = df.groupby('CATEGORIA')['INGRESOS'].sum().sort_values(ascending=False)
        if len(top_cat) > 0:
            cat = top_cat.index[0]
            ing = top_cat.iloc[0]
            return f"📂 La categoría que más ingresos genera es **{cat}** con **S/. {ing:,.2f}**."
        return "No hay datos suficientes."
    
    # 5. Mes con mayores ingresos
    if any(word in question_lower for word in ["mes", "fecha", "cuándo", "periodo"]):
        monthly = df.groupby(df['FECHA'].dt.to_period('M'))['INGRESOS'].sum().sort_values(ascending=False)
        if len(monthly) > 0:
            mes = monthly.index[0]
            ing = monthly.iloc[0]
            return f"📅 El mes con mayores ingresos es **{mes}** con **S/. {ing:,.2f}**."
        return "No hay datos suficientes."
    
    # 6. Ventas totales
    if any(word in question_lower for word in ["total", "suma", "general", "todo"]):
        total = df['INGRESOS'].sum()
        return f"💰 El total de ingresos generados es **S/. {total:,.2f}**."
    
    # 7. Ticket promedio
    if any(word in question_lower for word in ["ticket", "promedio", "media", "promedio de venta"]):
        total = df['INGRESOS'].sum()
        registros = len(df)
        if registros > 0:
            ticket = total / registros
            return f"🧾 El ticket promedio es de **S/. {ticket:,.2f}** por transacción."
        return "No hay datos suficientes."
    
    # 8. Volumen de unidades
    if any(word in question_lower for word in ["unidades", "volumen", "cantidad", "cuántos"]):
        unidades = df['UNIDADES'].sum()
        return f"📦 Se han vendido un total de **{unidades:,.0f}** unidades."
    
    # 9. Preguntas sobre tendencias (caída de agosto)
    if any(word in question_lower for word in ["agosto", "bajó", "cayó", "disminuyó"]):
        meses = df['FECHA'].dt.month_name()
        ingresos_mes = df.groupby(meses)['INGRESOS'].sum()
        if 'August' in ingresos_mes.index or 'Agosto' in ingresos_mes.index:
            mes_agosto = 'August' if 'August' in ingresos_mes.index else 'Agosto'
            ing_ago = ingresos_mes[mes_agosto]
            prom = ingresos_mes[ingresos_mes.index != mes_agosto].mean()
            if prom > 0:
                caida = ((prom - ing_ago) / prom) * 100
                return f"📉 En agosto los ingresos fueron de S/. {ing_ago:,.2f}, un **{caida:.1f}%** menor que el promedio mensual (S/. {prom:,.2f}). Podría deberse a datos incompletos."
        return "No se encontraron datos de agosto o no hay suficiente información."
    
    # 10. Respuesta por defecto
    return "🤔 No entendí tu pregunta. Puedo responder sobre: productos más vendidos, ingresos por ciudad/categoría, meses, totales, ticket promedio, unidades y caída de agosto. ¿Qué te gustaría saber?"