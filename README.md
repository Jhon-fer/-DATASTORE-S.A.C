# 📊 DATASTORE S.A.C. — Sistema de Análisis de Ventas

> **Dashboard interactivo para el análisis, procesamiento y visualización de datos de ventas**

Aplicación web desarrollada con **Python** y **Streamlit**, orientada al procesamiento, análisis estadístico y visualización interactiva de datos de ventas de **DATASTORE S.A.C.**

El sistema permite transformar datos comerciales en información útil para facilitar el análisis y apoyar la toma de decisiones relacionadas con **productos, categorías, períodos de venta, inventario y rendimiento por sede**.

> 🔐 **Nota de privacidad:** Los datos reales de DATASTORE S.A.C. pueden contener información empresarial confidencial. Por motivos de privacidad, este README no expone nombres reales de productos, sedes, cantidades, montos u otros datos sensibles. Cuando es necesario representar un resultado específico, se utiliza `XXXX`.

## 📌 Descripción del proyecto

**DATASTORE S.A.C. — Sistema de Análisis de Ventas** es una aplicación web interactiva que permite explorar y analizar información relacionada con las ventas de una empresa.

El proyecto integra un flujo completo de procesamiento de datos:

**Carga de datos → Validación → Limpieza → Transformación → Análisis estadístico → Visualización interactiva → Interpretación → Conclusiones → Recomendaciones**

La aplicación busca convertir los datos disponibles en información comprensible para facilitar la identificación de tendencias, oportunidades y posibles puntos de mejora.

## 🎯 Objetivos

### Objetivo general

Desarrollar una aplicación web interactiva que permita analizar los datos de ventas de DATASTORE S.A.C., convirtiendo los registros comerciales en información útil para apoyar la toma de decisiones empresariales.

### Objetivos específicos

* Procesar y validar los datos de ventas.
* Detectar y tratar posibles inconsistencias.
* Limpiar y transformar la información antes del análisis.
* Calcular indicadores generales de desempeño comercial.
* Identificar productos con mayor y menor demanda.
* Determinar las categorías con mayor participación.
* Analizar la evolución de las ventas a través del tiempo.
* Comparar el rendimiento de las diferentes sedes.
* Crear visualizaciones interactivas.
* Facilitar la interpretación de los resultados.
* Generar conclusiones basadas en los datos.
* Proponer recomendaciones orientadas a mejorar la gestión comercial.

## 🛠️ Tecnologías utilizadas

| Tecnología   | Uso en el proyecto                                                 |
| ------------ | ------------------------------------------------------------------ |
| 🐍 Python    | Lenguaje principal de desarrollo                                   |
| 🎨 Streamlit | Creación de la aplicación web y dashboard                          |
| 🐼 Pandas    | Limpieza, transformación y análisis de datos                       |
| 🔢 NumPy     | Operaciones y cálculos numéricos                                   |
| 📊 Plotly    | Creación de gráficos interactivos                                  |
| 📗 OpenPyXL  | Procesamiento de archivos Excel cuando el proyecto utiliza `.xlsx` |

> **Nota:** OpenPyXL solo es necesario si la aplicación trabaja con archivos Excel (`.xlsx`). Si el proyecto utiliza únicamente archivos `.csv`, esta dependencia puede omitirse.

## 📂 Estructura del proyecto

**DATASTORE-S.A.C/**

* `app.py` — Archivo principal de la aplicación Streamlit.
* `data/` — Carpeta destinada a los datos utilizados por la aplicación.

  * `ventas.csv`
* `assets/` — Recursos visuales como logotipos e imágenes.

  * `logo.png`
* `README.md` — Documentación del proyecto.
* `requirements.txt` — Dependencias necesarias para ejecutar el proyecto.
* `.gitignore` — Archivos que Git debe ignorar.
* `LICENSE` — Licencia del proyecto.

> La estructura puede variar dependiendo de la versión final del proyecto.

## 🔄 Flujo de procesamiento de datos

**Datos de ventas**

↓

**Carga de datos**

↓

**Validación**

↓

**Limpieza**

↓

**Transformación**

↓

**Análisis estadístico**

↓

**Productos | Categorías | Sedes**

↓

**Análisis temporal**

↓

**Visualizaciones**

↓

**Interpretación**

↓

**Conclusiones**

↓

**Recomendaciones**

## 🧹 Procesamiento y limpieza de datos

Antes de realizar los análisis, los datos pasan por una etapa de revisión y preparación.

Entre las principales operaciones se encuentran:

* Identificación y revisión de columnas.
* Validación de tipos de datos.
* Detección de valores faltantes.
* Conversión de variables numéricas.
* Conversión y validación de fechas.
* Revisión de registros inválidos.
* Tratamiento de inconsistencias.
* Preparación de variables para el análisis.
* Cálculo de métricas necesarias para el dashboard.

Estas operaciones permiten mejorar la calidad de la información y reducir posibles errores durante el análisis.

## 📊 Indicadores principales

El dashboard presenta indicadores que permiten obtener una visión general del comportamiento comercial.

### 💰 Ventas totales

Monto acumulado correspondiente a las ventas registradas.

### 🧾 Número de transacciones

Cantidad de operaciones comerciales registradas.

### 📦 Unidades vendidas

Cantidad total de productos comercializados.

### 📈 Venta promedio

Promedio del valor de las ventas por transacción.

Estos indicadores permiten obtener una visión rápida del desempeño antes de realizar análisis más específicos.

## 🏆 Análisis de productos

La aplicación permite analizar el comportamiento de los productos comercializados.

### Producto con mayor demanda

Se identifica el producto que registra la mayor cantidad de unidades vendidas.

Este indicador puede utilizarse para:

* Planificar los niveles de inventario.
* Reducir el riesgo de quiebres de stock.
* Priorizar productos de alta rotación.
* Diseñar estrategias comerciales.
* Identificar oportunidades de crecimiento.

### Producto con menor demanda

También se identifican los productos con menor cantidad de unidades vendidas.

Esta información puede servir para:

* Evaluar promociones.
* Analizar estrategias de precios.
* Revisar la aceptación del producto.
* Diseñar campañas comerciales.
* Optimizar los niveles de inventario.

> 🔐 Los nombres y valores reales de los productos se mantienen confidenciales.

## 🏷️ Análisis por categoría

El sistema permite analizar la facturación y participación de las diferentes categorías de productos.

Este análisis permite identificar:

* Categorías con mayor aporte económico.
* Categorías con menor participación.
* Distribución porcentual de las ventas.
* Diferencias de rendimiento entre categorías.
* Posibles oportunidades comerciales.

Para facilitar la interpretación se utilizan visualizaciones como:

* Gráficos de barras.
* Gráficos circulares.
* Comparaciones porcentuales.

## 📅 Análisis temporal

El dashboard permite estudiar la evolución de las ventas según diferentes períodos.

Este análisis ayuda a identificar:

* Períodos con mayor facturación.
* Períodos con menor rendimiento.
* Variaciones en el comportamiento de las ventas.
* Posibles patrones de demanda.
* Tendencias comerciales.

La información puede utilizarse para:

* Planificar campañas comerciales.
* Preparar inventarios.
* Anticipar períodos de mayor demanda.
* Comparar períodos.
* Mejorar la planificación comercial.

## 🏢 Análisis por sede

La aplicación permite comparar el rendimiento comercial de las diferentes sedes de DATASTORE S.A.C.

Este análisis permite:

* Comparar la facturación entre sedes.
* Identificar sedes con mejor desempeño.
* Detectar diferencias comerciales.
* Analizar posibles estrategias de venta.
* Identificar oportunidades de mejora.

> 🔐 Los resultados específicos relacionados con las sedes se mantienen confidenciales.

## 📈 Visualizaciones

Las visualizaciones se desarrollan principalmente utilizando **Plotly**, permitiendo una interacción dinámica con los datos.

Entre los principales tipos de gráficos se encuentran:

* 📊 Gráficos de barras.
* 🥧 Gráficos circulares.
* 📈 Evolución temporal de las ventas.
* 📦 Comparación de productos.
* 🏷️ Distribución por categoría.
* 🏢 Comparación por sede.

El objetivo de las visualizaciones es facilitar la identificación de patrones, diferencias y tendencias.

## 🧠 Interpretación de resultados

El dashboard no se limita a mostrar valores estadísticos.

Los resultados se pueden interpretar mediante tres niveles:

### 📌 Resultado

Presenta el indicador o valor obtenido a partir de los datos.

### 🔎 Interpretación

Explica qué significa el resultado dentro del contexto comercial.

### 💡 Decisión propuesta

Plantea una posible acción empresarial basada en la información obtenida.

De esta manera:

**Datos → Información → Análisis → Interpretación → Posible decisión**

## ⚠️ Validación y manejo de errores

La aplicación contempla diferentes situaciones que pueden afectar el análisis.

### Datos inconsistentes

Los archivos pueden contener valores faltantes, formatos incorrectos o información que requiera transformación.

**Solución:** se aplican procesos de validación y limpieza mediante Pandas.

### Diferencias en los tipos de datos

Variables como fechas, cantidades y montos pueden ser interpretadas inicialmente como texto.

**Solución:** se realizan conversiones de tipos antes de ejecutar los cálculos.

### Datos insuficientes

Algunas visualizaciones requieren determinadas columnas y datos válidos.

**Solución:** se realizan validaciones antes de generar los gráficos y se muestran mensajes informativos cuando la información disponible no es suficiente.

### Visualización poco estructurada

Una presentación basada únicamente en texto puede dificultar la interpretación.

**Solución:** se organiza la información mediante indicadores, gráficos y componentes visuales de Streamlit.

## 💻 Requisitos

Para ejecutar correctamente el proyecto, se recomienda contar con los siguientes requisitos:

* **Python 3.10 o superior**
* **Git**
* **pip** (gestor de paquetes de Python)

### 📦 Instalación de las librerías

Las principales librerías utilizadas por el proyecto son **Streamlit, Pandas y Plotly**.

Para instalarlas, abrir una terminal dentro de la carpeta del proyecto y ejecutar:

`pip install streamlit pandas plotly`

También puedes utilizar:

`python -m pip install streamlit pandas plotly`

### 🔍 Verificar la instalación

Para comprobar que Python está instalado correctamente:

`python --version`

Para verificar la instalación de Streamlit:

`python -m streamlit --version`

Si los comandos anteriores muestran las versiones instaladas, el entorno está listo para ejecutar la aplicación.

### 🌐 Entorno virtual

También se recomienda utilizar un **entorno virtual** para mantener aisladas las dependencias del proyecto y evitar conflictos con otras aplicaciones de Python.

**Windows:**

`python -m venv venv`

Activar el entorno virtual:

`venv\Scripts\activate`

**Linux/macOS:**

`python3 -m venv venv`

Activar el entorno virtual:

`source venv/bin/activate`

Una vez activado el entorno virtual, instalar las librerías necesarias:

`python -m pip install streamlit pandas plotly`

Finalmente, la aplicación puede ejecutarse con:

`streamlit run app.py`


También se recomienda utilizar un entorno virtual para mantener aisladas las dependencias del proyecto.

## 📥 Instalación

### 1. Clonar el repositorio

`git clone https://github.com/Jhon-fer/-DATASTORE-S.A.C.git`

### 2. Ingresar al proyecto

`cd -DATASTORE-S.A.C`

### 3. Crear un entorno virtual

**Windows:**

`python -m venv venv`

**Linux/macOS:**

`python3 -m venv venv`

### 4. Activar el entorno virtual

**Windows:**

`venv\Scripts\activate`

**Linux/macOS:**

`source venv/bin/activate`

### 5. Instalar las dependencias

`pip install -r requirements.txt`

## ▶️ Ejecutar la aplicación

Una vez instaladas las dependencias, ejecutar:

`streamlit run app.py`

Streamlit iniciará el servidor local y mostrará una dirección similar a:

`http://localhost:8501`

Abrir la dirección indicada en el navegador para acceder al dashboard.

## 📁 Dataset

El proyecto utiliza un conjunto de datos de ventas para realizar los análisis.

Por defecto, puede utilizarse:

`data/ventas.csv`

Si la aplicación trabaja con Excel:

`data/ventas.xlsx`

La ruta, el nombre y el formato del archivo deben coincidir con la configuración implementada en `app.py`.

> 🔐 Los datos reales de la empresa no deben publicarse en repositorios públicos si contienen información confidencial.

## 🔐 Seguridad y privacidad

Nunca se deben incluir en un repositorio público:

* Contraseñas.
* Tokens de autenticación.
* Claves API.
* Credenciales.
* Archivos `.env`.
* Información personal sensible.
* Información financiera confidencial.
* Datos empresariales privados.

Se recomienda utilizar variables de entorno o mecanismos seguros de configuración para gestionar información sensible.

El archivo `.gitignore` debe configurarse correctamente para evitar subir accidentalmente archivos privados.

Ejemplo:

`venv/`

`.env`

`__pycache__/`

`*.pyc`

Si el dataset es confidencial, también puede añadirse:

`*.csv`

`*.xlsx`

## ⚡ Ejecución rápida

Después de clonar el repositorio:

`git clone https://github.com/Jhon-fer/-DATASTORE-S.A.C.git`

`cd -DATASTORE-S.A.C`

Crear el entorno virtual:

`python -m venv venv`

Activarlo en Windows:

`venv\Scripts\activate`

Activarlo en Linux/macOS:

`source venv/bin/activate`

Instalar las dependencias:

`pip install -r requirements.txt`

Ejecutar la aplicación:

`streamlit run app.py`

## 🏗️ Arquitectura del proyecto

**PYTHON**

↓

**Pandas | NumPy | Plotly**

↓

**Limpieza y transformación | Cálculos numéricos | Gráficos interactivos**

↓

**STREAMLIT**

↓

**DASHBOARD WEB**

↓

**Toma de decisiones**

## 📊 Resultado esperado

Al ejecutar la aplicación se obtiene un dashboard interactivo que permite consultar:

* Indicadores generales.
* Productos con mayor demanda.
* Productos con menor demanda.
* Distribución por categorías.
* Rendimiento por sede.
* Evolución temporal de las ventas.
* Gráficos estadísticos interactivos.
* Interpretación de resultados.
* Conclusiones.
* Recomendaciones.

El objetivo final es proporcionar una herramienta que facilite la exploración de datos y el análisis del desempeño comercial.

## 💡 Recomendaciones empresariales

Las recomendaciones generadas a partir del análisis pueden orientarse a diferentes áreas.

### 📦 Inventario

Mantener niveles adecuados de stock para productos de alta demanda y evaluar estrategias para productos de baja rotación.

### 🛒 Ventas

Fortalecer las categorías que presentan una mayor contribución a la facturación.

### 📢 Marketing

Evaluar promociones y estrategias comerciales para productos con menor demanda.

### 🏢 Sedes

Analizar las prácticas comerciales de las sedes con mejor rendimiento para identificar estrategias que puedan ser replicadas.

### 📅 Planificación

Utilizar el comportamiento histórico de las ventas para anticipar períodos de mayor demanda y mejorar la planificación de inventario y campañas.

## 🔮 Mejoras futuras

Entre las posibles mejoras del proyecto se encuentran:

* Implementar filtros avanzados.
* Incorporar nuevos indicadores KPI.
* Permitir la exportación de reportes a Excel.
* Permitir la generación de reportes PDF.
* Automatizar la actualización de los datos.
* Conectar la aplicación con una base de datos.
* Implementar autenticación de usuarios.
* Desplegar la aplicación en la nube.
* Incorporar modelos de análisis predictivo.
* Implementar predicción de demanda.
* Incorporar análisis de tendencias futuras.
* Mejorar la personalización visual del dashboard.

## 📄 Licencia

Este proyecto se distribuye con fines educativos y de análisis de datos.

La utilización, modificación o distribución del proyecto debe respetar las condiciones establecidas en el archivo `LICENSE`.

## 👥 Integrantes

**GRUPO N°3**

* HUENDISABEL ANGIELIZ TORRES LOPE
* JHON FERNANDO GOMEZ QUISPE
* LUCIA NATALY PUMA CHURA

## ⭐ Resumen

**DATASTORE S.A.C. — Sistema de Análisis de Ventas** integra procesamiento de datos, análisis estadístico y visualización interactiva en una aplicación desarrollada con **Python, Pandas, NumPy, Plotly y Streamlit**.

El proyecto busca facilitar el análisis de productos, categorías, períodos y sedes, proporcionando indicadores y visualizaciones que permitan comprender el comportamiento de las ventas y apoyar la toma de decisiones empresariales.

**DATASTORE S.A.C. — Sistema de Análisis de Ventas**

*Transformando datos en información para una mejor toma de decisiones.*
