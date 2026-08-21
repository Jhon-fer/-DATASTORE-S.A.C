# 📊 DATASTORE S.A.C. — Sistema de Análisis de Ventas

> **Dashboard interactivo para el análisis, procesamiento y visualización de datos de ventas con IA integrada**

Aplicación web desarrollada con **Python** y **Streamlit**, orientada al procesamiento, análisis estadístico y visualización interactiva de datos de ventas de **DATASTORE S.A.C.**

El sistema permite transformar datos comerciales en información útil para facilitar el análisis y apoyar la toma de decisiones relacionadas con **productos, categorías, períodos de venta, inventario y rendimiento por sede**, incorporando además un **asistente virtual con IA** para consultas en lenguaje natural.

---

## 📌 Descripción del proyecto

**DATASTORE S.A.C. — Sistema de Análisis de Ventas** es una aplicación web interactiva que permite explorar y analizar información relacionada con las ventas de una empresa.

El proyecto integra un flujo completo de procesamiento de datos:

**Carga de datos → Validación → Limpieza → Transformación → Análisis estadístico → Visualización interactiva → Interpretación → Conclusiones → Recomendaciones**

La aplicación busca convertir los datos disponibles en información comprensible para facilitar la identificación de tendencias, oportunidades y posibles puntos de mejora.

### 🆕 Novedades de la versión final

- **Sistema de autenticación** con 3 roles de usuario (admin, gerente, analista)
- **Asistente virtual con IA** que responde preguntas en lenguaje natural sobre los datos
- **CSS profesional** con header, footer, perfil de usuario y diseño corporativo
- **Predicciones con intervalo de confianza** del 95% usando regresión lineal
- **Estructura modular** con vistas separadas y lógica de negocio en `utils/`
- **Drill-down interactivo** en gráficos (clics para filtrar)
- **Panel de decisiones automatizadas** basadas en los datos

---

## 🎯 Objetivos

### Objetivo general

Desarrollar una aplicación web interactiva que permita analizar los datos de ventas de DATASTORE S.A.C., convirtiendo los registros comerciales en información útil para apoyar la toma de decisiones empresariales.

### Objetivos específicos

- Procesar y validar los datos de ventas.
- Detectar y tratar posibles inconsistencias.
- Limpiar y transformar la información antes del análisis.
- Calcular indicadores generales de desempeño comercial.
- Identificar productos con mayor y menor demanda.
- Determinar las categorías con mayor participación.
- Analizar la evolución de las ventas a través del tiempo.
- Comparar el rendimiento de las diferentes sedes.
- Crear visualizaciones interactivas.
- Facilitar la interpretación de los resultados.
- Generar conclusiones basadas en los datos.
- Proponer recomendaciones orientadas a mejorar la gestión comercial.
- **Implementar un asistente virtual con IA para consultas en lenguaje natural.**
- **Incorporar predicciones con intervalos de confianza.**

---

## 🛠️ Tecnologías utilizadas

| Tecnología | Uso en el proyecto |
|------------|-------------------|
| 🐍 Python | Lenguaje principal de desarrollo |
| 🎨 Streamlit | Creación de la aplicación web y dashboard |
| 🐼 Pandas | Limpieza, transformación y análisis de datos |
| 🔢 NumPy | Operaciones y cálculos numéricos |
| 📊 Plotly | Creación de gráficos interactivos |
| 🤖 Google Gemini API / Ollama | Asistente virtual con IA (opcional) |
| 📗 OpenPyXL | Procesamiento de archivos Excel (opcional) |

---

## 📂 Estructura del proyecto
C: "TU USUARIO"
│   .gitignore
│   app.py
│   README.md
│   requirements.txt
│   
├───assets
│       style.css
│       
├───utils
│   │   analysis_engine.py
│   │   data_loader.py
│   │   visualizations.py
│   │   __init__.py
│   │   
│   └───__pycache__
│           analysis_engine.cpython-314.pyc
│           data_loader.cpython-314.pyc
│           visualizations.cpython-314.pyc
│           __init__.cpython-314.pyc
│           
└───views
    │   analytics.py
    │   chat.py
    │   data_view.py
    │   decisions.py
    │   home.py
    │   predictions.py
    │   __init__.py
    │   
    └───__pycache__
            analytics.cpython-314.pyc
            data_view.cpython-314.pyc
            decisions.cpython-314.pyc
            home.cpython-314.pyc
            predictions.cpython-314.pyc
            __init__.cpython-314.pyc
