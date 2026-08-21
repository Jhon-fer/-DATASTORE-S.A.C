import streamlit as st
import pandas as pd
import re
import unicodedata
import plotly.express as px

# ==========================================================
# CONFIGURACIÓN
# ==========================================================

st.set_page_config(
    page_title="DATASTORE S.A.C.",
    page_icon="📊",
    layout="wide"
)

st.title("📊 DATASTORE S.A.C.")
st.subheader("Sistema de análisis de ventas")

st.write(
    "Carga, validación, procesamiento y análisis estadístico "
    "de los datos de ventas."
)


# ==========================================================
# NORMALIZAR NOMBRE DE COLUMNA
# ==========================================================

def normalizar_nombre(nombre):

    nombre = str(nombre)

    nombre = nombre.replace("\ufeff", "")

    nombre = unicodedata.normalize(
        "NFKD",
        nombre
    ).encode(
        "ascii",
        "ignore"
    ).decode(
        "utf-8"
    )

    nombre = nombre.lower()

    nombre = re.sub(
        r"[^a-z0-9]+",
        "_",
        nombre
    )

    nombre = nombre.strip("_")

    return nombre


# ==========================================================
# HACER COLUMNAS ÚNICAS
# ==========================================================

def hacer_columnas_unicas(columnas):

    nuevas = []

    contador = {}

    for columna in columnas:

        if columna not in contador:

            contador[columna] = 0

            nuevas.append(
                columna
            )

        else:

            contador[columna] += 1

            nuevas.append(
                f"{columna}_{contador[columna]}"
            )

    return nuevas


# ==========================================================
# BUSCAR COLUMNA
# ==========================================================

def buscar_columna(columnas, posibles):

    columnas = list(columnas)

    posibles_normalizados = [
        normalizar_nombre(x)
        for x in posibles
    ]

    # ------------------------------------------------------
    # COINCIDENCIA EXACTA
    # ------------------------------------------------------

    for posible in posibles_normalizados:

        if posible in columnas:

            return posible

    # ------------------------------------------------------
    # COINCIDENCIA PARCIAL
    # ------------------------------------------------------

    for columna in columnas:

        for posible in posibles_normalizados:

            if (
                posible in columna
                or columna in posible
            ):

                return columna

    return None


# ==========================================================
# CONVERTIR NÚMEROS DE FORMA ROBUSTA
# ==========================================================

def convertir_numero(serie):

    def convertir(valor):

        if pd.isna(valor):

            return None

        texto = str(valor).strip()

        if texto == "":

            return None

        # Quitar moneda, letras y espacios
        texto = re.sub(
            r"[^\d,.\-]",
            "",
            texto
        )

        if texto == "":

            return None

        # --------------------------------------------------
        # 1.234,56
        # --------------------------------------------------

        if "," in texto and "." in texto:

            if texto.rfind(",") > texto.rfind("."):

                texto = texto.replace(
                    ".",
                    ""
                )

                texto = texto.replace(
                    ",",
                    "."
                )

            else:

                texto = texto.replace(
                    ",",
                    ""
                )

        # --------------------------------------------------
        # 1234,56
        # --------------------------------------------------

        elif "," in texto:

            partes = texto.split(",")

            if (
                len(partes) == 2
                and len(partes[1]) <= 2
            ):

                texto = (
                    partes[0]
                    + "."
                    + partes[1]
                )

            else:

                texto = texto.replace(
                    ",",
                    ""
                )

        # --------------------------------------------------
        # 1234.56
        # --------------------------------------------------

        elif "." in texto:

            partes = texto.split(".")

            if len(partes) > 2:

                texto = "".join(partes)

        try:

            return float(texto)

        except:

            return None

    return serie.apply(convertir)


# ==========================================================
# 1. CARGA DE DATOS
# ==========================================================

st.header("1. Carga de datos")

archivo = st.file_uploader(
    "Seleccione un archivo CSV de ventas",
    type=["csv"]
)

if archivo is None:

    st.info(
        "👆 Seleccione un archivo CSV para comenzar."
    )

    st.stop()


# ==========================================================
# 2. LEER CSV
# ==========================================================

try:

    df = pd.read_csv(
        archivo,
        sep=None,
        engine="python",
        encoding="utf-8-sig"
    )

except UnicodeDecodeError:

    try:

        archivo.seek(0)

        df = pd.read_csv(
            archivo,
            sep=None,
            engine="python",
            encoding="latin-1"
        )

    except Exception as e:

        st.error(
            "❌ No se pudo leer el archivo."
        )

        st.error(str(e))

        st.stop()

except Exception as e:

    st.error(
        "❌ No se pudo leer el archivo."
    )

    st.error(str(e))

    st.stop()


# ==========================================================
# VALIDAR ARCHIVO
# ==========================================================

if df.empty:

    st.error(
        "❌ El archivo CSV está vacío."
    )

    st.stop()


# ==========================================================
# NORMALIZAR COLUMNAS
# ==========================================================

df.columns = [
    normalizar_nombre(columna)
    for columna in df.columns
]


# ==========================================================
# EVITAR COLUMNAS DUPLICADAS
# ==========================================================

df.columns = hacer_columnas_unicas(
    df.columns
)


# ==========================================================
# CONFIRMACIÓN
# ==========================================================

st.success(
    "✅ Archivo cargado y leído correctamente."
)

st.info(
    f"📄 Archivo seleccionado: **{archivo.name}**"
)


# ==========================================================
# 2. INFORMACIÓN DEL ARCHIVO
# ==========================================================

st.header(
    "2. Información del archivo"
)

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Registros",
        f"{len(df):,}"
    )

with col2:

    st.metric(
        "Columnas",
        len(df.columns)
    )

with col3:

    st.metric(
        "Celdas",
        f"{df.size:,}"
    )


st.subheader(
    "Columnas detectadas"
)

st.code(
    ", ".join(df.columns)
)


# ==========================================================
# 3. REGISTROS
# ==========================================================

st.header(
    "3. Registros cargados"
)

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)


# ==========================================================
# 4. VALIDACIÓN
# ==========================================================

st.header(
    "4. Validación de información"
)

valores_vacios = df.isnull().sum()

total_vacios = int(
    valores_vacios.sum()
)

duplicados = int(
    df.duplicated().sum()
)


v1, v2 = st.columns(2)


with v1:

    if total_vacios == 0:

        st.success(
            "✅ No existen valores vacíos."
        )

    else:

        st.warning(
            f"⚠️ Se encontraron "
            f"{total_vacios:,} valores vacíos."
        )


with v2:

    if duplicados == 0:

        st.success(
            "✅ No existen registros duplicados."
        )

    else:

        st.warning(
            f"⚠️ Se encontraron "
            f"{duplicados:,} registros duplicados."
        )


# ==========================================================
# VALORES VACÍOS
# ==========================================================

st.subheader(
    "Valores vacíos por columna"
)

validacion = pd.DataFrame({

    "Columna": df.columns,

    "Valores vacíos": valores_vacios.values

})

st.dataframe(
    validacion,
    use_container_width=True,
    hide_index=True
)


# ==========================================================
# TIPOS DE DATOS
# ==========================================================

st.subheader(
    "Tipos de datos"
)

tipos = pd.DataFrame({

    "Columna": df.columns,

    "Tipo de dato": [
        str(tipo)
        for tipo in df.dtypes
    ]

})

st.dataframe(
    tipos,
    use_container_width=True,
    hide_index=True
)


# ==========================================================
# 5. PROCESAMIENTO
# ==========================================================

st.header(
    "5. Procesamiento de datos"
)

df_procesado = (
    df
    .copy()
    .drop_duplicates()
    .dropna(how="all")
)


registros_iniciales = len(df)

registros_finales = len(
    df_procesado
)

registros_eliminados = (
    registros_iniciales
    -
    registros_finales
)


st.subheader(
    "Resultado del procesamiento"
)

p1, p2, p3 = st.columns(3)


with p1:

    st.metric(
        "Registros iniciales",
        f"{registros_iniciales:,}"
    )


with p2:

    st.metric(
        "Registros procesados",
        f"{registros_finales:,}"
    )


with p3:

    st.metric(
        "Registros eliminados",
        f"{registros_eliminados:,}"
    )


if registros_eliminados == 0:

    st.success(
        "✅ No fue necesario eliminar registros."
    )

else:

    st.warning(
        f"⚠️ Se eliminaron "
        f"{registros_eliminados:,} registros."
    )


st.subheader(
    "Datos procesados"
)

st.dataframe(
    df_procesado,
    use_container_width=True,
    hide_index=True
)


# ==========================================================
# 6. PROCESAMIENTO ESTADÍSTICO
# ==========================================================

st.header(
    "6. Procesamiento estadístico"
)

st.write(
    "A partir de los datos procesados se calcularán "
    "los principales indicadores de ventas."
)


# ==========================================================
# IDENTIFICAR COLUMNAS
# ==========================================================

columnas = list(
    df_procesado.columns
)


# ==========================================================
# FECHA
# ==========================================================

col_fecha = buscar_columna(
    columnas,
    [
        "fecha",
        "fecha_venta",
        "fecha_de_venta",
        "date",
        "sale_date",
        "fecha_transaccion",
        "fecha_compra"
    ]
)


# ==========================================================
# PRODUCTO
# ==========================================================

col_producto = buscar_columna(
    columnas,
    [
        "producto",
        "nombre_producto",
        "product",
        "producto_vendido",
        "articulo",
        "articulo_vendido",
        "item"
    ]
)


# ==========================================================
# CATEGORÍA
# ==========================================================

col_categoria = buscar_columna(
    columnas,
    [
        "categoria",
        "tipo_producto",
        "tipo_de_producto",
        "category",
        "rubro",
        "familia",
        "linea_producto"
    ]
)


# ==========================================================
# CANTIDAD
# ==========================================================

col_cantidad = buscar_columna(
    columnas,
    [
        "cantidad",
        "cantidad_vendida",
        "unidades",
        "unidades_vendidas",
        "uds",
        "ud",
        "unidad",
        "units",
        "qty",
        "quantity",
        "cantidad_productos",
        "numero_unidades",
        "cantidad_comprada"
    ]
)


# ==========================================================
# PRECIO
# ==========================================================

col_precio = buscar_columna(
    columnas,
    [
        "precio_unitario",
        "unit_price",
        "precio",
        "price",
        "valor_unitario",
        "valor_de_unitario"
    ]
)


# ==========================================================
# VENTA
# ==========================================================

col_venta = buscar_columna(
    columnas,
    [
        "venta_total",
        "total_venta",
        "total_ventas",
        "importe",
        "monto_total",
        "precio_total",
        "valor_venta",
        "valor_total",
        "venta",
        "ventas",
        "monto",
        "total"
    ]
)


# ==========================================================
# SEDE / CIUDAD
# ==========================================================

col_sede = buscar_columna(
    columnas,
    [
        "sede",
        "ciudad",
        "city",
        "sucursal",
        "sucursal_venta",
        "local",
        "tienda",
        "ubicacion",
        "establecimiento"
    ]
)


# ==========================================================
# MOSTRAR DETECCIÓN
# ==========================================================

st.subheader(
    "Columnas utilizadas para el análisis"
)

columnas_detectadas = pd.DataFrame({

    "Dato": [
        "Fecha",
        "Producto",
        "Categoría",
        "Cantidad",
        "Precio unitario",
        "Venta",
        "Sede / Ciudad"
    ],

    "Columna encontrada": [
        col_fecha or "No encontrada",
        col_producto or "No encontrada",
        col_categoria or "No encontrada",
        col_cantidad or "No encontrada",
        col_precio or "No encontrada",
        col_venta or "No encontrada",
        col_sede or "No encontrada"
    ]

})

st.dataframe(
    columnas_detectadas,
    use_container_width=True,
    hide_index=True
)


# ==========================================================
# VALIDAR DATOS FUNDAMENTALES
# ==========================================================

columnas_faltantes = []


if col_producto is None:

    columnas_faltantes.append(
        "Producto"
    )


if col_cantidad is None:

    columnas_faltantes.append(
        "Cantidad"
    )


if (
    col_venta is None
    and col_precio is None
):

    columnas_faltantes.append(
        "Venta o Precio unitario"
    )


if columnas_faltantes:

    st.error(
        "❌ El archivo no contiene los datos "
        "mínimos necesarios para realizar "
        "el análisis de ventas."
    )

    st.write(
        "### Datos faltantes:"
    )

    for elemento in columnas_faltantes:

        st.write(
            f"- {elemento}"
        )

    st.write(
        "### Columnas disponibles:"
    )

    st.code(
        ", ".join(
            columnas
        )
    )

    st.stop()


# ==========================================================
# 7. PREPARACIÓN DE DATOS
# ==========================================================

st.header(
    "7. Preparación de datos para el análisis"
)


df_analisis = df_procesado.copy()


# ==========================================================
# CONVERTIR CANTIDAD
# ==========================================================

df_analisis[col_cantidad] = (
    convertir_numero(
        df_analisis[col_cantidad]
    )
)


# ==========================================================
# CONSTRUIR VENTA
#
# IMPORTANTE:
#
# Si tenemos cantidad + precio unitario,
# SIEMPRE calculamos venta = cantidad × precio.
#
# Esto soluciona el problema del segundo CSV.
# ==========================================================

if col_precio is not None:

    df_analisis[col_precio] = (
        convertir_numero(
            df_analisis[col_precio]
        )
    )


# ----------------------------------------------------------
# SI TENEMOS PRECIO Y CANTIDAD
# ----------------------------------------------------------

if (
    col_precio is not None
    and col_cantidad is not None
):

    df_analisis["venta_calculada"] = (
        df_analisis[col_cantidad]
        *
        df_analisis[col_precio]
    )

    col_venta_analisis = "venta_calculada"

    st.success(
        "✅ Venta calculada correctamente "
        "como Cantidad × Precio unitario."
    )


# ----------------------------------------------------------
# SI NO TENEMOS PRECIO, USAR VENTA EXISTENTE
# ----------------------------------------------------------

elif col_venta is not None:

    df_analisis[col_venta] = (
        convertir_numero(
            df_analisis[col_venta]
        )
    )

    col_venta_analisis = col_venta

    st.success(
        "✅ Se utilizará la columna de venta "
        "existente en el archivo."
    )


else:

    st.error(
        "❌ No fue posible obtener el valor de venta."
    )

    st.stop()


# ==========================================================
# CONVERTIR FECHA
# ==========================================================

if col_fecha is not None:

    df_analisis[col_fecha] = pd.to_datetime(
        df_analisis[col_fecha],
        errors="coerce"
    )


# ==========================================================
# VERIFICACIÓN DE DATOS
# ==========================================================

st.subheader(
    "Verificación de datos para el análisis"
)


verificacion = pd.DataFrame({

    "Dato": [
        "Producto",
        "Cantidad",
        "Precio unitario",
        "Venta"
    ],

    "Columna": [
        col_producto,
        col_cantidad,
        col_precio or "No aplica",
        col_venta_analisis
    ],

    "Valores totales": [
        len(df_analisis),
        len(df_analisis),
        len(df_analisis)
        if col_precio is not None
        else 0,
        len(df_analisis)
    ],

    "Valores válidos": [
        df_analisis[col_producto].notna().sum(),
        df_analisis[col_cantidad].notna().sum(),
        (
            df_analisis[col_precio].notna().sum()
            if col_precio is not None
            else 0
        ),
        df_analisis[
            col_venta_analisis
        ].notna().sum()
    ]

})


st.dataframe(
    verificacion,
    use_container_width=True,
    hide_index=True
)


# ==========================================================
# MOSTRAR DATOS PREPARADOS
# ==========================================================

with st.expander(
    "🔎 Ver datos preparados para el análisis"
):

    columnas_mostrar = []

    # Función para evitar duplicados
    def agregar_columna_si_no_existe(
        lista,
        columna
    ):

        if (
            columna is not None
            and columna not in lista
            and columna in df_analisis.columns
        ):

            lista.append(
                columna
            )


    agregar_columna_si_no_existe(
        columnas_mostrar,
        col_producto
    )

    agregar_columna_si_no_existe(
        columnas_mostrar,
        col_cantidad
    )

    agregar_columna_si_no_existe(
        columnas_mostrar,
        col_precio
    )

    agregar_columna_si_no_existe(
        columnas_mostrar,
        col_venta_analisis
    )

    agregar_columna_si_no_existe(
        columnas_mostrar,
        col_categoria
    )

    agregar_columna_si_no_existe(
        columnas_mostrar,
        col_fecha
    )

    agregar_columna_si_no_existe(
        columnas_mostrar,
        col_sede
    )

    # ------------------------------------------------------
    # IMPORTANTE:
    # Se crea una copia con nombres únicos para Streamlit.
    # ------------------------------------------------------

    datos_mostrar = (
        df_analisis[
            columnas_mostrar
        ]
        .copy()
    )

    datos_mostrar.columns = (
        hacer_columnas_unicas(
            datos_mostrar.columns
        )
    )

    st.dataframe(
        datos_mostrar,
        use_container_width=True,
        hide_index=True
    )


# ==========================================================
# VALIDAR PRODUCTO
# ==========================================================

producto_invalidos = int(
    df_analisis[
        col_producto
    ]
    .isna()
    .sum()
)


# ==========================================================
# VALIDAR CANTIDAD
# ==========================================================

cantidad_invalidas = int(
    df_analisis[
        col_cantidad
    ]
    .isna()
    .sum()
)


# ==========================================================
# VALIDAR VENTA
# ==========================================================

venta_invalidas = int(
    df_analisis[
        col_venta_analisis
    ]
    .isna()
    .sum()
)


# ==========================================================
# FILTRAR REGISTROS VÁLIDOS
# ==========================================================

filas_antes_analisis = len(
    df_analisis
)


df_analisis = (
    df_analisis
    .dropna(
        subset=[
            col_producto,
            col_cantidad,
            col_venta_analisis
        ]
    )
    .copy()
)


filas_despues_analisis = len(
    df_analisis
)


filas_no_validas = (
    filas_antes_analisis
    -
    filas_despues_analisis
)


# ==========================================================
# RESULTADO DEL FILTRADO
# ==========================================================

if filas_no_validas > 0:

    st.warning(
        f"⚠️ Se excluyeron "
        f"{filas_no_validas:,} registros "
        "que no tenían información válida "
        "para calcular los indicadores."
    )

else:

    st.success(
        "✅ Todos los registros contienen "
        "la información necesaria para el análisis."
    )


# ==========================================================
# VERIFICAR QUE EXISTAN REGISTROS
# ==========================================================

if df_analisis.empty:

    st.error(
        "❌ No existen registros válidos "
        "para realizar el análisis estadístico."
    )

    st.subheader(
        "Diagnóstico"
    )

    st.write(
        f"- Productos inválidos: {producto_invalidos}"
    )

    st.write(
        f"- Cantidades inválidas: {cantidad_invalidas}"
    )

    st.write(
        f"- Ventas inválidas: {venta_invalidas}"
    )

    st.stop()


# ==========================================================
# 8. RESULTADOS ESTADÍSTICOS
# ==========================================================

st.header(
    "8. Resultados estadísticos"
)


# ==========================================================
# TOTAL VENTAS
# ==========================================================

total_ventas = (
    df_analisis[
        col_venta_analisis
    ]
    .sum()
)


# ==========================================================
# TRANSACCIONES
# ==========================================================

numero_transacciones = len(
    df_analisis
)


# ==========================================================
# CANTIDAD PRODUCTOS
# ==========================================================

cantidad_productos = (
    df_analisis[
        col_cantidad
    ]
    .sum()
)


# ==========================================================
# PROMEDIO
# ==========================================================

if numero_transacciones > 0:

    promedio_venta = (
        total_ventas
        /
        numero_transacciones
    )

else:

    promedio_venta = 0


# ==========================================================
# PRODUCTOS
# ==========================================================

ventas_por_producto = (

    df_analisis
    .groupby(
        col_producto
    )[col_cantidad]
    .sum()
    .sort_values(
        ascending=False
    )

)


if not ventas_por_producto.empty:

    producto_mas_vendido = (
        ventas_por_producto.index[0]
    )

    cantidad_producto_mas_vendido = (
        ventas_por_producto.iloc[0]
    )

    producto_menos_vendido = (
        ventas_por_producto.index[-1]
    )

    cantidad_producto_menos_vendido = (
        ventas_por_producto.iloc[-1]
    )

else:

    producto_mas_vendido = "N/A"

    cantidad_producto_mas_vendido = 0

    producto_menos_vendido = "N/A"

    cantidad_producto_menos_vendido = 0


# ==========================================================
# CATEGORÍA
# ==========================================================

if col_categoria is not None:

    ventas_por_categoria = (

        df_analisis
        .groupby(
            col_categoria
        )[col_venta_analisis]
        .sum()
        .sort_values(
            ascending=False
        )

    )

    if not ventas_por_categoria.empty:

        categoria_mayor_venta = (
            ventas_por_categoria.index[0]
        )

        monto_categoria_mayor = (
            ventas_por_categoria.iloc[0]
        )

    else:

        categoria_mayor_venta = (
            "No disponible"
        )

        monto_categoria_mayor = 0

else:

    categoria_mayor_venta = (
        "No disponible"
    )

    monto_categoria_mayor = 0


# ==========================================================
# MES
# ==========================================================

if col_fecha is not None:

    # Número del mes
    df_analisis["mes_numero"] = (
        df_analisis[col_fecha].dt.month
    )

    # Nombres de meses en español
    meses_espanol = {
        1: "Enero",
        2: "Febrero",
        3: "Marzo",
        4: "Abril",
        5: "Mayo",
        6: "Junio",
        7: "Julio",
        8: "Agosto",
        9: "Septiembre",
        10: "Octubre",
        11: "Noviembre",
        12: "Diciembre"
    }

    df_analisis["mes_nombre"] = (
        df_analisis["mes_numero"]
        .map(meses_espanol)
    )

    ventas_por_mes = (

        df_analisis
        .dropna(
            subset=[
                "mes_numero",
                "mes_nombre"
            ]
        )
        .groupby(
            [
                "mes_numero",
                "mes_nombre"
            ]
        )[col_venta_analisis]
        .sum()
        .reset_index()
        .sort_values(
            col_venta_analisis,
            ascending=False
        )

    )

    if not ventas_por_mes.empty:

        mes_mayor_venta = (
            ventas_por_mes
            .iloc[0]["mes_nombre"]
        )

        monto_mes_mayor = (
            ventas_por_mes
            .iloc[0][col_venta_analisis]
        )

    else:

        mes_mayor_venta = "No disponible"

        monto_mes_mayor = 0

else:

    mes_mayor_venta = "No disponible"

    monto_mes_mayor = 0

# ==========================================================
# SEDE
# ==========================================================

if col_sede is not None:

    ventas_por_sede = (

        df_analisis
        .groupby(
            col_sede
        )[col_venta_analisis]
        .sum()
        .sort_values(
            ascending=False
        )

    )

    if not ventas_por_sede.empty:

        sede_mayor_venta = (
            ventas_por_sede.index[0]
        )

        monto_sede_mayor = (
            ventas_por_sede.iloc[0]
        )

    else:

        sede_mayor_venta = (
            "No disponible"
        )

        monto_sede_mayor = 0

else:

    sede_mayor_venta = (
        "No disponible"
    )

    monto_sede_mayor = 0


# ==========================================================
# 9. KPI
# ==========================================================

st.header(
    "9. Indicadores principales"
)


kpi1, kpi2, kpi3 = st.columns(3)


with kpi1:

    st.metric(
        "💰 Total de ventas",
        f"S/ {total_ventas:,.2f}"
    )


with kpi2:

    st.metric(
        "🧾 Número de transacciones",
        f"{numero_transacciones:,}"
    )


with kpi3:

    st.metric(
        "📦 Productos vendidos",
        f"{cantidad_productos:,.0f}"
    )


kpi4, kpi5, kpi6 = st.columns(3)


with kpi4:

    st.metric(
        "📊 Promedio de venta",
        f"S/ {promedio_venta:,.2f}"
    )


with kpi5:

    st.metric(
        "🏆 Producto más vendido",
        str(producto_mas_vendido)
    )


with kpi6:

    st.metric(
        "📉 Producto menos vendido",
        str(producto_menos_vendido)
    )


kpi7, kpi8, kpi9 = st.columns(3)


with kpi7:

    st.metric(
        "🏷️ Categoría con mayor venta",
        str(categoria_mayor_venta)
    )


with kpi8:

    st.metric(
        "📅 Mes con mayor venta",
        str(mes_mayor_venta)
    )


with kpi9:

    st.metric(
        "🏢 Sede con mayor venta",
        str(sede_mayor_venta)
    )


# ==========================================================
# 10. RESUMEN
# ==========================================================

st.header(
    "10. Resumen estadístico"
)


resumen = pd.DataFrame({

    "Indicador": [

        "Total de ventas",

        "Número de transacciones",

        "Cantidad total de productos vendidos",

        "Promedio de venta",

        "Producto más vendido",

        "Producto menos vendido",

        "Categoría con mayor venta",

        "Mes con mayor venta",

        "Sede con mayor venta"

    ],

    "Resultado": [

        f"S/ {total_ventas:,.2f}",

        f"{numero_transacciones:,}",

        f"{cantidad_productos:,.0f}",

        f"S/ {promedio_venta:,.2f}",

        (
            f"{producto_mas_vendido} "
            f"({cantidad_producto_mas_vendido:,.0f} unidades)"
        ),

        (
            f"{producto_menos_vendido} "
            f"({cantidad_producto_menos_vendido:,.0f} unidades)"
        ),

        (
            f"{categoria_mayor_venta} "
            f"(S/ {monto_categoria_mayor:,.2f})"
            if categoria_mayor_venta != "No disponible"
            else "No disponible"
        ),

        (
            f"{mes_mayor_venta} "
            f"(S/ {monto_mes_mayor:,.2f})"
            if mes_mayor_venta != "No disponible"
            else "No disponible"
        ),

        (
            f"{sede_mayor_venta} "
            f"(S/ {monto_sede_mayor:,.2f})"
            if sede_mayor_venta != "No disponible"
            else "No disponible"
        )

    ]

})


st.dataframe(
    resumen,
    use_container_width=True,
    hide_index=True
)


# ==========================================================
# FINAL
# ==========================================================

st.success(
    "🎉 Análisis de ventas completado correctamente."
)

# ==========================================================
# 11. GRÁFICOS ESTADÍSTICOS
# ==========================================================

st.header(
    "11. Gráficos estadísticos"
)

st.write(
    "Los siguientes gráficos se generan automáticamente "
    "a partir de los datos procesados y permiten analizar "
    "el comportamiento de las ventas desde diferentes "
    "perspectivas empresariales."
)


# ==========================================================
# CONFIGURACIÓN DE COLORES
# ==========================================================

color_principal = "#1f77b4"
color_secundario = "#2ca02c"
color_rojo = "#d62728"
color_naranja = "#ff7f0e"
color_morado = "#9467bd"


# ==========================================================
# GRÁFICO 1
# VENTAS POR MES
# ==========================================================

st.subheader(
    "📅 1. Ventas por mes"
)

st.caption(
    "Permite identificar los meses que generan "
    "mayor y menor facturación."
)


if col_fecha is not None:

    ventas_mes_grafico = (

        df_analisis
        .dropna(
            subset=[
                col_fecha,
                col_venta_analisis
            ]
        )
        .copy()

    )

    if not ventas_mes_grafico.empty:

        ventas_mes_grafico["mes_numero"] = (
            ventas_mes_grafico[col_fecha]
            .dt.month
        )

        ventas_mes_grafico["mes_nombre"] = (
            ventas_mes_grafico["mes_numero"]
            .map(meses_espanol)
        )

        ventas_mes_grafico = (

            ventas_mes_grafico
            .groupby(
                [
                    "mes_numero",
                    "mes_nombre"
                ]
            )[col_venta_analisis]
            .sum()
            .reset_index()
            .sort_values(
                "mes_numero"
            )

        )

        if not ventas_mes_grafico.empty:

            datos_grafico = (
                ventas_mes_grafico
                .set_index("mes_nombre")[
                    col_venta_analisis
                ]
            )

            st.bar_chart(
                datos_grafico,
                color=color_principal
            )

            mes_mayor = (
                ventas_mes_grafico
                .sort_values(
                    col_venta_analisis,
                    ascending=False
                )
                .iloc[0]
            )

            mes_menor = (
                ventas_mes_grafico
                .sort_values(
                    col_venta_analisis,
                    ascending=True
                )
                .iloc[0]
            )

            st.info(
                f"📊 **Análisis:** El mes con mayor "
                f"facturación fue **{mes_mayor['mes_nombre']}**, "
                f"con ventas de **S/ "
                f"{mes_mayor[col_venta_analisis]:,.2f}**. "
                f"El mes con menor facturación fue "
                f"**{mes_menor['mes_nombre']}**, con "
                f"**S/ {mes_menor[col_venta_analisis]:,.2f}**."
            )

    else:

        st.info(
            "No existen datos suficientes para mostrar "
            "las ventas por mes."
        )

else:

    st.info(
        "El archivo no contiene una columna de fecha."
    )


# ==========================================================
# GRÁFICO 2
# VENTAS POR CATEGORÍA
# ==========================================================

st.subheader(
    "🏷️ 2. Ventas por categoría"
)

st.caption(
    "Permite determinar qué categorías generan "
    "mayores ingresos para la empresa."
)


if col_categoria is not None:

    ventas_categoria_grafico = (

        df_analisis
        .groupby(
            col_categoria
        )[col_venta_analisis]
        .sum()
        .sort_values(
            ascending=False
        )

    )

    if not ventas_categoria_grafico.empty:

        st.bar_chart(
            ventas_categoria_grafico,
            color=color_secundario
        )

        categoria_mayor = (
            ventas_categoria_grafico
            .index[0]
        )

        monto_categoria = (
            ventas_categoria_grafico
            .iloc[0]
        )

        porcentaje_categoria = (
            monto_categoria
            /
            total_ventas
            *
            100
            if total_ventas > 0
            else 0
        )

        st.info(
            f"📊 **Análisis:** La categoría con mayor "
            f"facturación es **{categoria_mayor}**, "
            f"con **S/ {monto_categoria:,.2f}**, "
            f"equivalente al **{porcentaje_categoria:.1f}%** "
            f"del total de ventas."
        )

    else:

        st.info(
            "No existen datos suficientes para mostrar "
            "las ventas por categoría."
        )

else:

    st.info(
        "El archivo no contiene una columna de categoría."
    )


# ==========================================================
# GRÁFICO 3
# PRODUCTOS MÁS VENDIDOS
# ==========================================================

st.subheader(
    "🏆 3. Productos más vendidos"
)

st.caption(
    "Muestra los 10 productos con mayor cantidad "
    "de unidades vendidas."
)


productos_mas_vendidos = (

    df_analisis
    .groupby(
        col_producto
    )[col_cantidad]
    .sum()
    .sort_values(
        ascending=False
    )
    .head(10)

)


if not productos_mas_vendidos.empty:

    st.bar_chart(
        productos_mas_vendidos,
        color=color_principal
    )

    producto_top = (
        productos_mas_vendidos
        .index[0]
    )

    unidades_top = (
        productos_mas_vendidos
        .iloc[0]
    )

    st.info(
        f"📊 **Análisis:** El producto con mayor "
        f"cantidad de unidades vendidas es "
        f"**{producto_top}**, con "
        f"**{unidades_top:,.0f} unidades**."
    )

else:

    st.info(
        "No existen datos suficientes para mostrar "
        "los productos más vendidos."
    )


# ==========================================================
# GRÁFICO 4
# PRODUCTOS MENOS VENDIDOS
# ==========================================================

st.subheader(
    "📉 4. Productos menos vendidos"
)

st.caption(
    "Permite identificar productos con baja rotación "
    "que podrían requerir estrategias comerciales."
)


productos_menos_vendidos = (

    df_analisis
    .groupby(
        col_producto
    )[col_cantidad]
    .sum()
    .sort_values(
        ascending=True
    )
    .head(10)

)


if not productos_menos_vendidos.empty:

    st.bar_chart(
        productos_menos_vendidos,
        color=color_rojo
    )

    producto_bajo = (
        productos_menos_vendidos
        .index[0]
    )

    unidades_bajo = (
        productos_menos_vendidos
        .iloc[0]
    )

    st.info(
        f"📊 **Análisis:** El producto con menor "
        f"cantidad de unidades vendidas es "
        f"**{producto_bajo}**, con "
        f"**{unidades_bajo:,.0f} unidades**. "
        f"Estos productos pueden ser evaluados para "
        f"promociones o estrategias de rotación."
    )

else:

    st.info(
        "No existen datos suficientes para mostrar "
        "los productos menos vendidos."
    )


# ==========================================================
# GRÁFICO 5
# VENTAS POR SEDE / CIUDAD
# ==========================================================

st.subheader(
    "🏢 5. Ventas por sede o ciudad"
)

st.caption(
    "Permite identificar qué ubicación genera "
    "mayores ingresos."
)


if col_sede is not None:

    ventas_sede_grafico = (

        df_analisis
        .groupby(
            col_sede
        )[col_venta_analisis]
        .sum()
        .sort_values(
            ascending=False
        )

    )

    if not ventas_sede_grafico.empty:

        st.bar_chart(
            ventas_sede_grafico,
            color=color_naranja
        )

        sede_top = (
            ventas_sede_grafico
            .index[0]
        )

        monto_sede_top = (
            ventas_sede_grafico
            .iloc[0]
        )

        st.info(
            f"📊 **Análisis:** La sede con mayor "
            f"facturación es **{sede_top}**, "
            f"con **S/ {monto_sede_top:,.2f}**."
        )

    else:

        st.info(
            "No existen datos suficientes para mostrar "
            "las ventas por sede."
        )

else:

    st.info(
        "El archivo no contiene una columna de sede "
        "o ciudad."
    )


# ==========================================================
# GRÁFICO 6
# EVOLUCIÓN DE LAS VENTAS
# ==========================================================

st.subheader(
    "📈 6. Evolución de las ventas"
)

st.caption(
    "Permite observar cómo cambian las ventas "
    "a lo largo del tiempo."
)


if col_fecha is not None:

    evolucion_ventas = (

        df_analisis
        .dropna(
            subset=[
                col_fecha,
                col_venta_analisis
            ]
        )
        .groupby(
            col_fecha
        )[col_venta_analisis]
        .sum()
        .sort_index()

    )

    if not evolucion_ventas.empty:

        st.line_chart(
            evolucion_ventas,
            color=color_principal
        )

        venta_maxima_dia = (
            evolucion_ventas.max()
        )

        fecha_maxima = (
            evolucion_ventas.idxmax()
        )

        st.info(
            f"📊 **Análisis:** El mayor nivel de ventas "
            f"registrado en una fecha fue de "
            f"**S/ {venta_maxima_dia:,.2f}**, "
            f"correspondiente al **{fecha_maxima.strftime('%d/%m/%Y')}**."
        )

    else:

        st.info(
            "No existen datos suficientes para mostrar "
            "la evolución de las ventas."
        )

else:

    st.info(
        "El archivo no contiene una columna de fecha."
    )


# ==========================================================
# GRÁFICO 7
# CANTIDAD DE PRODUCTOS POR CATEGORÍA
# ==========================================================

st.subheader(
    "📦 7. Cantidad de productos vendidos por categoría"
)

st.caption(
    "Permite comparar el volumen de unidades vendidas "
    "entre las diferentes categorías."
)


if col_categoria is not None:

    cantidad_categoria_grafico = (

        df_analisis
        .groupby(
            col_categoria
        )[col_cantidad]
        .sum()
        .sort_values(
            ascending=False
        )

    )

    if not cantidad_categoria_grafico.empty:

        st.bar_chart(
            cantidad_categoria_grafico,
            color=color_morado
        )

        categoria_unidades = (
            cantidad_categoria_grafico
            .index[0]
        )

        unidades_categoria = (
            cantidad_categoria_grafico
            .iloc[0]
        )

        st.info(
            f"📊 **Análisis:** La categoría con mayor "
            f"cantidad de unidades vendidas es "
            f"**{categoria_unidades}**, con "
            f"**{unidades_categoria:,.0f} unidades**."
        )

    else:

        st.info(
            "No existen datos suficientes para mostrar "
            "la cantidad de productos por categoría."
        )

else:

    st.info(
        "El archivo no contiene una columna de categoría."
    )


# ==========================================================
# GRÁFICO 8
# COMPARACIÓN DE VENTAS ENTRE SEDES
# ==========================================================

st.subheader(
    "⚖️ 8. Comparación de ventas entre sedes"
)

st.caption(
    "Permite comparar directamente el rendimiento "
    "comercial de las diferentes sedes."
)


if col_sede is not None:

    comparacion_sedes = (

        df_analisis
        .groupby(
            col_sede
        )[col_venta_analisis]
        .sum()
        .sort_values(
            ascending=False
        )

    )

    if not comparacion_sedes.empty:

        st.bar_chart(
            comparacion_sedes,
            color=color_secundario
        )

        sede_mayor = (
            comparacion_sedes
            .index[0]
        )

        sede_menor = (
            comparacion_sedes
            .index[-1]
        )

        diferencia_sedes = (
            comparacion_sedes.iloc[0]
            -
            comparacion_sedes.iloc[-1]
        )

        st.info(
            f"📊 **Análisis:** La sede con mayor "
            f"facturación es **{sede_mayor}**, mientras "
            f"que la de menor facturación es "
            f"**{sede_menor}**. "
            f"La diferencia entre ambas es de "
            f"**S/ {diferencia_sedes:,.2f}**."
        )

    else:

        st.info(
            "No existen datos suficientes para comparar "
            "las sedes."
        )

else:

    st.info(
        "El archivo no contiene una columna de sede "
        "o ciudad."
    )


# ==========================================================
# CONCLUSIÓN DE LOS GRÁFICOS
# ==========================================================

st.subheader(
    "📋 Conclusión del análisis gráfico"
)

st.write(
    "Los gráficos anteriores se construyen directamente "
    "con los registros válidos del archivo cargado. "
    "De esta manera, los resultados cambian "
    "automáticamente cuando se utiliza otro conjunto "
    "de datos."
)

st.success(
    "✅ Se generaron los 8 gráficos estadísticos "
    "utilizando los datos procesados."
)

# ==========================================================
# 11. ANÁLISIS E INTERPRETACIÓN DE LOS DATOS
# ==========================================================

st.header(
    "11. Análisis e interpretación de los datos"
)

st.write(
    "En esta sección se interpretan los resultados obtenidos "
    "y se plantean posibles decisiones empresariales basadas "
    "en la información analizada."
)


# ==========================================================
# ANÁLISIS 1
# PRODUCTO QUE DEBERÍA RECIBIR MAYOR STOCK
# ==========================================================

st.subheader(
    "📦 1. ¿Qué producto debería recibir mayor stock?"
)

if not ventas_por_producto.empty:

    porcentaje_producto_top = (
        cantidad_producto_mas_vendido
        /
        cantidad_productos
        *
        100
        if cantidad_productos > 0
        else 0
    )

    st.markdown("### Resultado")

    st.write(
        f"El producto **{producto_mas_vendido}** "
        f"representa el **{porcentaje_producto_top:.1f}%** "
        f"de las unidades vendidas, con "
        f"**{cantidad_producto_mas_vendido:,.0f} unidades**."
    )

    st.markdown("### Interpretación")

    st.write(
        f"El producto **{producto_mas_vendido}** presenta "
        f"la mayor demanda dentro de los productos analizados."
    )

    st.markdown("### Decisión propuesta")

    st.write(
        f"Se recomienda incrementar o asegurar el stock de "
        f"**{producto_mas_vendido}**, evitando quiebres de inventario "
        f"y evaluando estrategias comerciales para mantener "
        f"su nivel de ventas."
    )


# ==========================================================
# ANÁLISIS 2
# CATEGORÍA CON MAYORES INGRESOS
# ==========================================================

st.subheader(
    "🏷️ 2. ¿Qué categoría genera mayores ingresos?"
)

if col_categoria is not None and not ventas_por_categoria.empty:

    porcentaje_categoria_top = (
        monto_categoria_mayor
        /
        total_ventas
        *
        100
        if total_ventas > 0
        else 0
    )

    st.markdown("### Resultado")

    st.write(
        f"La categoría **{categoria_mayor_venta}** "
        f"generó **S/ {monto_categoria_mayor:,.2f}**, "
        f"representando el **{porcentaje_categoria_top:.1f}%** "
        f"de las ventas totales."
    )

    st.markdown("### Interpretación")

    st.write(
        f"La categoría **{categoria_mayor_venta}** "
        f"es la que genera mayores ingresos para la empresa."
    )

    st.markdown("### Decisión propuesta")

    st.write(
        f"Se recomienda evaluar una mayor inversión comercial "
        f"en la categoría **{categoria_mayor_venta}**, "
        f"manteniendo disponibilidad de sus productos "
        f"y analizando oportunidades de crecimiento."
    )

else:

    st.info(
        "No es posible realizar este análisis porque "
        "el archivo no contiene una categoría válida."
    )


# ==========================================================
# ANÁLISIS 3
# PERÍODO CON MAYORES VENTAS
# ==========================================================

st.subheader(
    "📅 3. ¿En qué período se producen mayores ventas?"
)

if col_fecha is not None and not ventas_por_mes.empty:

    st.markdown("### Resultado")

    st.write(
        f"El período con mayores ventas fue **{mes_mayor_venta}**, "
        f"con una facturación de **S/ {monto_mes_mayor:,.2f}**."
    )

    st.markdown("### Interpretación")

    st.write(
        f"Durante **{mes_mayor_venta}** se alcanzó el mayor "
        f"nivel de facturación entre los períodos disponibles."
    )

    st.markdown("### Decisión propuesta")

    st.write(
        f"Se recomienda analizar las condiciones comerciales "
        f"de **{mes_mayor_venta}** y replicar, cuando sea posible, "
        f"las estrategias que contribuyeron al incremento de las ventas."
    )

else:

    st.info(
        "No es posible analizar los períodos porque "
        "el archivo no contiene una fecha válida."
    )


# ==========================================================
# ANÁLISIS 4
# PRODUCTO CON MENOR DEMANDA
# ==========================================================

st.subheader(
    "📉 4. ¿Qué producto presenta menor demanda?"
)

if not ventas_por_producto.empty:

    porcentaje_producto_bajo = (
        cantidad_producto_menos_vendido
        /
        cantidad_productos
        *
        100
        if cantidad_productos > 0
        else 0
    )

    st.markdown("### Resultado")

    st.write(
        f"El producto **{producto_menos_vendido}** "
        f"presenta la menor cantidad de unidades vendidas, "
        f"con **{cantidad_producto_menos_vendido:,.0f} unidades**."
    )

    st.markdown("### Interpretación")

    st.write(
        f"El producto **{producto_menos_vendido}** "
        f"presenta una demanda inferior al resto de los productos analizados."
    )

    st.markdown("### Decisión propuesta")

    st.write(
        f"Se recomienda evaluar estrategias promocionales para "
        f"**{producto_menos_vendido}**, revisar su precio y analizar "
        f"si existe una baja demanda que justifique reducir su stock."
    )


# ==========================================================
# ANÁLISIS 5
# SEDE CON MEJOR RENDIMIENTO
# ==========================================================

st.subheader(
    "🏢 5. ¿Qué sede tiene mejor rendimiento?"
)

if col_sede is not None and not ventas_por_sede.empty:

    porcentaje_sede_top = (
        monto_sede_mayor
        /
        total_ventas
        *
        100
        if total_ventas > 0
        else 0
    )

    st.markdown("### Resultado")

    st.write(
        f"La sede **{sede_mayor_venta}** registra la mayor "
        f"facturación, con **S/ {monto_sede_mayor:,.2f}**, "
        f"equivalente al **{porcentaje_sede_top:.1f}%** "
        f"de las ventas totales."
    )

    st.markdown("### Interpretación")

    st.write(
        f"La sede **{sede_mayor_venta}** presenta el mejor "
        f"rendimiento comercial según el volumen de ventas."
    )

    st.markdown("### Decisión propuesta")

    st.write(
        f"Se recomienda analizar las estrategias utilizadas "
        f"por la sede **{sede_mayor_venta}** y evaluar cuáles "
        f"pueden ser aplicadas en las demás sedes."
    )

else:

    st.info(
        "No es posible realizar este análisis porque "
        "el archivo no contiene una sede o ciudad válida."
    )


# ==========================================================
# ANÁLISIS 6
# CATEGORÍA QUE DEBERÍA RECIBIR MAYOR INVERSIÓN
# ==========================================================

st.subheader(
    "💰 6. ¿Qué categoría debería recibir mayor inversión?"
)

if col_categoria is not None and not ventas_por_categoria.empty:

    st.markdown("### Resultado")

    st.write(
        f"La categoría **{categoria_mayor_venta}** "
        f"presenta la mayor facturación con "
        f"**S/ {monto_categoria_mayor:,.2f}**."
    )

    st.markdown("### Interpretación")

    st.write(
        f"La categoría **{categoria_mayor_venta}** "
        f"demuestra un mayor aporte económico al negocio."
    )

    st.markdown("### Decisión propuesta")

    st.write(
        f"Se recomienda evaluar una mayor inversión en "
        f"**{categoria_mayor_venta}**, especialmente en "
        f"inventario, marketing y disponibilidad de productos."
    )


# ==========================================================
# ANÁLISIS 7
# PRODUCTO QUE PODRÍA REQUERIR PROMOCIÓN
# ==========================================================

st.subheader(
    "🎯 7. ¿Qué producto podría requerir una estrategia de promoción?"
)

if not ventas_por_producto.empty:

    st.markdown("### Resultado")

    st.write(
        f"El producto identificado con menor demanda es "
        f"**{producto_menos_vendido}**, con "
        f"**{cantidad_producto_menos_vendido:,.0f} unidades vendidas**."
    )

    st.markdown("### Interpretación")

    st.write(
        f"La baja cantidad de unidades vendidas puede indicar "
        f"una menor aceptación o rotación del producto."
    )

    st.markdown("### Decisión propuesta")

    st.write(
        f"Se recomienda evaluar promociones, descuentos, "
        f"combos o campañas de marketing para aumentar la "
        f"rotación de **{producto_menos_vendido}**."
    )


# ==========================================================
# ANÁLISIS 8
# DECISIÓN EMPRESARIAL GENERAL
# ==========================================================

st.subheader(
    "📊 8. ¿Qué decisión podría tomar la empresa utilizando esta información?"
)

st.markdown("### Resultado")

st.write(
    f"El análisis permitió identificar que **{producto_mas_vendido}** "
    f"es el producto con mayor demanda, **{categoria_mayor_venta}** "
    f"es la categoría con mayores ingresos y **{sede_mayor_venta}** "
    f"es la sede con mayor facturación."
)

st.markdown("### Interpretación")

st.write(
    "Los resultados permiten identificar dónde se concentra "
    "la demanda y cuáles son las áreas con mejor desempeño "
    "comercial."
)

st.markdown("### Decisión propuesta")

st.write(
    "La empresa puede utilizar esta información para mejorar "
    "la planificación del inventario, orientar las inversiones "
    "comerciales, diseñar promociones y fortalecer las sedes "
    "o categorías con mejores resultados."
)

# ==========================================================
# 12. CONCLUSIONES
# ==========================================================

st.header(
    "12. Conclusiones"
)

st.write(
    "A partir del procesamiento, validación y análisis "
    "estadístico de los datos de ventas, se presentan los "
    "principales resultados y conclusiones obtenidos."
)


# ==========================================================
# RESUMEN EJECUTIVO
# ==========================================================

st.subheader(
    "📊 Resumen ejecutivo"
)

con1, con2, con3, con4 = st.columns(4)

with con1:

    st.metric(
        "💰 Ventas totales",
        f"S/ {total_ventas:,.2f}"
    )

with con2:

    st.metric(
        "🧾 Transacciones",
        f"{numero_transacciones:,}"
    )

with con3:

    st.metric(
        "📦 Unidades vendidas",
        f"{cantidad_productos:,.0f}"
    )

with con4:

    st.metric(
        "📊 Venta promedio",
        f"S/ {promedio_venta:,.2f}"
    )


# ==========================================================
# PRINCIPALES RESULTADOS
# ==========================================================

st.subheader(
    "🏆 Principales resultados"
)

resultados_conclusion = pd.DataFrame({

    "Indicador": [
        "Producto con mayor demanda",
        "Producto con menor demanda",
        "Categoría con mayores ingresos",
        "Mes con mayor facturación",
        "Sede con mayor facturación"
    ],

    "Resultado": [
        str(producto_mas_vendido),
        str(producto_menos_vendido),
        str(categoria_mayor_venta),
        str(mes_mayor_venta),
        str(sede_mayor_venta)
    ],

    "Valor": [
        f"{cantidad_producto_mas_vendido:,.0f} unidades",
        f"{cantidad_producto_menos_vendido:,.0f} unidades",
        f"S/ {monto_categoria_mayor:,.2f}",
        f"S/ {monto_mes_mayor:,.2f}",
        f"S/ {monto_sede_mayor:,.2f}"
    ]

})

st.dataframe(
    resultados_conclusion,
    use_container_width=True,
    hide_index=True
)


# ==========================================================
# GRÁFICOS DE CONCLUSIÓN
# ==========================================================

st.subheader(
    "📈 Distribución de los resultados"
)


# ==========================================================
# COLUMNAS PARA GRÁFICOS
# ==========================================================

graf1, graf2 = st.columns(2)


# ==========================================================
# GRÁFICO CIRCULAR - CATEGORÍAS
# ==========================================================

with graf1:

    st.markdown(
        "### 🏷️ Participación de ventas por categoría"
    )

    if (
        col_categoria is not None
        and not ventas_por_categoria.empty
    ):

        datos_categoria = (
            ventas_por_categoria
            .reset_index()
        )

        datos_categoria.columns = [
            "Categoria",
            "Ventas"
        ]

        fig_categoria = px.pie(
            datos_categoria,
            names="Categoria",
            values="Ventas",
            hole=0.35,
            title="Distribución de ventas"
        )

        fig_categoria.update_traces(
            textposition="inside",
            textinfo="percent+label"
        )

        fig_categoria.update_layout(
            showlegend=True,
            height=450
        )

        st.plotly_chart(
            fig_categoria,
            use_container_width=True
        )

    else:

        st.info(
            "No existen datos suficientes para mostrar "
            "la distribución por categoría."
        )


# ==========================================================
# GRÁFICO CIRCULAR - SEDES
# ==========================================================

with graf2:

    st.markdown(
        "### 🏢 Participación de ventas por sede"
    )

    if (
        col_sede is not None
        and not ventas_por_sede.empty
    ):

        datos_sede = (
            ventas_por_sede
            .reset_index()
        )

        datos_sede.columns = [
            "Sede",
            "Ventas"
        ]

        fig_sede = px.pie(
            datos_sede,
            names="Sede",
            values="Ventas",
            hole=0.35,
            title="Distribución de ventas"
        )

        fig_sede.update_traces(
            textposition="inside",
            textinfo="percent+label"
        )

        fig_sede.update_layout(
            showlegend=True,
            height=450
        )

        st.plotly_chart(
            fig_sede,
            use_container_width=True
        )

    else:

        st.info(
            "No existen datos suficientes para mostrar "
            "la distribución por sede."
        )


# ==========================================================
# COMPARACIÓN PRODUCTOS
# ==========================================================

st.subheader(
    "📦 Comparación de productos"
)

col_producto1, col_producto2 = st.columns(2)


# ==========================================================
# PRODUCTOS MÁS VENDIDOS
# ==========================================================

with col_producto1:

    st.markdown(
        "### 🏆 Productos con mayor demanda"
    )

    if not productos_mas_vendidos.empty:

        fig_top_productos = px.bar(
            x=productos_mas_vendidos.values,
            y=productos_mas_vendidos.index,
            orientation="h",
            labels={
                "x": "Unidades vendidas",
                "y": "Producto"
            },
            title="Top 10 productos"
        )

        fig_top_productos.update_layout(
            height=500
        )

        st.plotly_chart(
            fig_top_productos,
            use_container_width=True
        )


# ==========================================================
# PRODUCTOS MENOS VENDIDOS
# ==========================================================

with col_producto2:

    st.markdown(
        "### 📉 Productos con menor demanda"
    )

    if not productos_menos_vendidos.empty:

        fig_bajos_productos = px.bar(
            x=productos_menos_vendidos.values,
            y=productos_menos_vendidos.index,
            orientation="h",
            labels={
                "x": "Unidades vendidas",
                "y": "Producto"
            },
            title="Productos con menor rotación"
        )

        fig_bajos_productos.update_layout(
            height=500
        )

        st.plotly_chart(
            fig_bajos_productos,
            use_container_width=True
        )


# ==========================================================
# CONCLUSIONES PRINCIPALES
# ==========================================================

st.subheader(
    "📋 Conclusiones principales"
)


conclusion1, conclusion2 = st.columns(2)


with conclusion1:

    st.info(
        f"📦 **Inventario:** "
        f"**{producto_mas_vendido}** es el producto "
        f"con mayor demanda, por lo que debería "
        f"mantenerse una disponibilidad adecuada."
    )

    st.info(
        f"🏷️ **Categoría:** "
        f"**{categoria_mayor_venta}** genera los mayores "
        f"ingresos con **S/ {monto_categoria_mayor:,.2f}**."
    )

    st.info(
        f"📅 **Período:** "
        f"**{mes_mayor_venta}** fue el período con "
        f"mayor facturación, alcanzando "
        f"**S/ {monto_mes_mayor:,.2f}**."
    )


with conclusion2:

    st.warning(
        f"📉 **Producto de baja rotación:** "
        f"**{producto_menos_vendido}** presenta la menor "
        f"cantidad de unidades vendidas."
    )

    st.success(
        f"🏢 **Sede:** "
        f"**{sede_mayor_venta}** presenta el mayor "
        f"nivel de facturación con "
        f"**S/ {monto_sede_mayor:,.2f}**."
    )

    st.success(
        "💡 **Decisión empresarial:** "
        "Los resultados pueden utilizarse para mejorar "
        "la planificación del inventario, orientar "
        "inversiones y diseñar estrategias comerciales."
    )


# ==========================================================
# RECOMENDACIONES
# ==========================================================

st.subheader(
    "💡 Recomendaciones finales"
)

recomendaciones = pd.DataFrame({

    "Prioridad": [
        "Alta",
        "Alta",
        "Media",
        "Media",
        "Media"
    ],

    "Área": [
        "Inventario",
        "Ventas",
        "Marketing",
        "Sedes",
        "Planificación"
    ],

    "Recomendación": [
        f"Asegurar stock de {producto_mas_vendido}.",
        f"Fortalecer la categoría {categoria_mayor_venta}.",
        f"Evaluar promociones para {producto_menos_vendido}.",
        f"Analizar las estrategias de {sede_mayor_venta}.",
        f"Estudiar el comportamiento de {mes_mayor_venta}."
    ]

})

st.dataframe(
    recomendaciones,
    use_container_width=True,
    hide_index=True
)


# ==========================================================
# CIERRE
# ==========================================================

st.subheader(
    "🎯 Conclusión final"
)

st.write(
    f"El análisis de **{numero_transacciones:,} transacciones** "
    f"permitió identificar los principales factores que "
    f"determinan el comportamiento de las ventas de la empresa."
)

st.write(
    f"Con ventas totales de **S/ {total_ventas:,.2f}**, "
    f"el sistema permitió identificar a "
    f"**{producto_mas_vendido}** como el producto de mayor "
    f"demanda, a **{categoria_mayor_venta}** como la categoría "
    f"de mayor aporte económico y a **{sede_mayor_venta}** "
    f"como la sede con mejor facturación."
)

st.success(
    "🎉 Análisis de ventas finalizado correctamente. "
    "La información obtenida puede utilizarse como apoyo "
    "para la toma de decisiones empresariales."
)
