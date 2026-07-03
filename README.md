# Pipeline ETL de Retail: Extracción de APIs, AWS Cloud (Glue/PySpark) y Business Intelligence

## 🚀 Descripción del Proyecto
Este proyecto implementa un pipeline de datos de extremo a extremo (End-to-End) para extraer, procesar y analizar información nutricional y comercial de productos de consumo masivo (fuentes: API de Mercadona y API de Open Food Facts). El objetivo es consolidar un dataset limpio que permita identificar insights de negocio y detectar "productos engañosos" (alimentos ultraprocesados NOVA 4 camuflados bajo calificaciones Nutri-Score A/B).


## 🎯 Objetivo del Proyecto

El objetivo de este proyecto es construir un dataset real de productos de supermercado (en este caso, datos obtenidos de Mercadona y Open Food Facts) que incluya información nutricional y comercial.

A partir de este dataset, se busca realizar un análisis tanto económico como nutricional para extraer conclusiones útiles en la toma de decisiones de compra.

El propósito final es ayudar a los consumidores a identificar productos que ofrezcan un mejor equilibrio entre precio y calidad nutricional, considerando distintos escenarios:
- Cuando el presupuesto es un factor determinante
- Cuando el valor nutricional tiene mayor prioridad que el precio

Además, se desarrollan rankings de productos que sirven como referencia para facilitar la planificación de la compra.

Todo este análisis se materializa en un informe interactivo en Power BI, que permite filtrar productos por marca, categoría y características nutricionales, facilitando la exploración de los datos de forma dinámica.

## 🗺️ Arquitectura de Datos
Aquí se detalla el flujo de datos e integración tecnológica que usé durante la realización de este proyecto:

![Diagrama de Flujo ETL](./diagrama_de_flujo_ETL.png)

1. **Ingesta:** Extracción automatizada y enriquecimiento de datos de APIs mediante Python y Pandas, implementando lógica de tolerancia a fallos, reintentos y rate-limiting controlado. Durante la ejecución, el dataset se actualizó de forma incremental en un archivo **CSV** local. Posteriormente, dicho archivo se cargó en un bucket de **Amazon S3**, dentro de la carpeta **raw/**
2. **Análisis Exploratorio (EDA):** Consultas en **Amazon Athena** sobre los metadatos generados por **AWS Glue Crawler** para analizar la calidad del dato e identificar nulos y valores atípicos (*outliers*).
3. **Transformación y Limpieza (ETL):** Script robusto en **AWS Glue con PySpark** para el tipado de variables, filtrado de categorías fuera de alcance y normalización de estructuras complejas, almacenando el dataset optimizado en **Amazon S3** dentro de la carpeta **silver/** en formato columnar **Parquet**.
4. **Consumo y Dashboard:** Modelado, transformación final mediante Power Query (estándar decimal de España) y diseño del cuadro de mando interactivo en **Power BI**.



## 🛠️ Tecnologías utilizadas
Python, Pandas, AWS (S3, Glue, Athena), PySpark, Power BI

---

## 📁 Estructura del Repositorio

* `1_codigo_ingesta_apis/` -> Contiene el cuaderno de Jupyter (`.ipynb`) con el desarrollo de la extracción incremental y consumo de las APIs.
* `2_transformaciones_aws_y_consultas_sql/` -> Alberga el script de PySpark (`.py`) ejecutado en AWS Glue y las consultas de auditoría (`.sql`) utilizadas en Amazon Athena.
* `3_reporte_powerbi/` -> Contiene el informe analítico interactivo tanto en formato nativo (`.pbix`) como su exportación estática para lectura rápida (`.pdf`).
* `4_capturas/` -> Almacena de forma centralizada todas las imágenes del proyecto. Incluye un documento PDF con la bitácora resumida del paso a paso técnico.
* `5_data/` -> Almacena los datasets completos del proyecto divididos por capas de madurez (Arquitectura Medallion):
    * `raw/dataset_productos_en_bruto.csv` -> Datos originales extraídos directamente de las APIs con las anomalías identificadas.
    * `silver/productos_limpios.parquet` -> Dataset optimizado en formato columnar Parquet tras el procesamiento con PySpark.
* `diagrama_de_flujo_etl.png` -> Diagrama de la arquitectura y flujo de datos del pipeline ETL utilizado en el proyecto.

---

## 📊 Insights Destacados del Dashboard

### 1. Eficiencia Proteica y Comercial
Análisis del ratio óptimo de gramos de proteína por euro invertido entre múltiples categorías alimenticias para identificar las mejores opciones de compra.

📄 Este análisis se encuentra en la **página 1 del reporte de Power BI**:
[Ver reporte completo](./3_reporte_powerbi/Informe_Power_Bi.pdf)

### 2. Cruce entre Nutri-Score y clasificación NOVA
Análisis conjunto de las clasificaciones **Nutri-Score** y **NOVA** para identificar productos ultraprocesados que obtienen buenas calificaciones nutricionales.

📄 Este análisis se encuentra en la **página 3 del reporte de Power BI**:
[Ver reporte completo](./3_reporte_powerbi/Informe_Power_Bi.pdf)

> 💡 *Nota: En la carpeta `4_capturas/` se incluye un documento PDF resumido con las consultas ejecutadas en Amazon Athena, la resolución de anomalías detectadas en la consola de AWS y las reglas de negocio aplicadas.*

---

**Contacto:** Pablo Cesar Lira Cares | [LinkedIn](https://www.linkedin.com/in/pablo-lira-cares-2a4152368/)