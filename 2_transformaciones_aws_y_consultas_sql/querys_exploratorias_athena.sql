/*******************************************************************************
  PROYECTO: Pipeline ETL - Análisis de Retail (Mercadona & Open Food Facts)
  HERRAMIENTA: Amazon Athena (Presto SQL Engine)
  BASE DE DATOS: db-productos-alimenticios
  
  DESCRIPCIÓN: 
  Estas consultas se realizaron durante la etapa de Análisis Exploratorio de Datos (EDA)
  en la capa "Raw" (datos en bruto) almacenada en AWS S3. Su objetivo es identificar 
  anomalías de calidad de datos, patrones de nulos y valores atípicos (outliers) 
  antes de diseñar y ejecutar el script definitivo de limpieza en AWS Glue.
*******************************************************************************/

-- =============================================================================
-- CONSULTA 1: Identificación de categorías críticas con alto volumen de nulos
-- Objetivo: Filtrar categorías donde más del 70% de los productos carecen de 
-- información calórica para evaluar su exclusión en el dataset final.
-- =============================================================================
SELECT 
    categoria,
    COUNT(CASE WHEN calorias_100g IS NULL THEN 1 END) AS nulos_calorias,
    COUNT(*) AS total_productos
FROM "db-productos-alimenticios"."raw"
GROUP BY categoria
HAVING (COUNT(CASE WHEN calorias_100g IS NULL THEN 1 END) * 100.0 / COUNT(*)) >= 70.0
ORDER BY total_productos DESC;


-- =============================================================================
-- CONSULTA 2: Detección de valores atípicos (Outliers) en aporte energético
-- Objetivo: Localizar registros con errores de origen en la API (valores > 900 kcal
-- por cada 100g no tienen coherencia biológica/nutricional) para su posterior depuración.
-- =============================================================================
SELECT 
    nombre,
    ean,
    calorias_100g
FROM "db-productos-alimenticios"."raw"
WHERE calorias_100g > 900
ORDER BY calorias_100g DESC;